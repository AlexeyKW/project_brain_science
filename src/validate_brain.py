#!/usr/bin/env python
"""validate_brain.py — проверка карточек Research Brain (CI check 1: схема, check 2: граф).

Проверяет:
  1. front-matter каждой карточки .brain/WARM/** валиден по JSON Schema (.brain/schema/);
  2. ID уникальны, совпадают с именем файла;
  3. целостность графа: claim -> runs -> experiment -> hypothesis -> dataset;
  4. X-09: агент не может присвоить human-verified / published сам;
  5. свежесть: valid_until < сегодня -> предупреждение (--stale-fail EXIT=1 при превышении доли).

Usage:
  python src/validate_brain.py --brain .brain [--fast] [--stale-fail FRAC]
"""
import argparse, datetime as dt, json, re, sys
from pathlib import Path

import yaml

try:
    import jsonschema
    from referencing import Registry, Resource
except ImportError:  # минимальный режим без jsonschema: только граф
    jsonschema = None

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)
CARD_ID = re.compile(r"^(C|H|D|E|F|DS|L|M)-[0-9]{3}$")

TYPES_WITHOUT_SCHEMA = {"note"}


def load_cards(brain: Path):
    """Карточки: md/yaml файлы в WARM с front-matter (для .yaml — весь файл)."""
    cards, errors = [], []
    for path in sorted((brain / "WARM").rglob("*")):
        if path.suffix not in (".md", ".yaml", ".yml"):
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".md":
            m = FRONTMATTER.match(text)
            if not m:
                continue  # обычные md (MAP, GLOSSARY...) — не карточки
            docs = list(yaml.safe_load_all(m.group(1)))
        else:
            docs = list(yaml.safe_load_all(text))
        try:
            # front-matter +, возможно, тело карточки — сливаем в один dict
            data = {}
            for d in docs:
                if isinstance(d, dict):
                    data.update(d)
        except yaml.YAMLError as e:
            errors.append(f"{path}: YAML parse error: {e}")
            continue
        if not isinstance(data, dict) or "id" not in data:
            continue
        cards.append({"path": path, "data": data})
    return cards, errors


def schema_registry(brain: Path):
    base = "https://brain.example/schema/"
    resources = {}
    for f in (brain / "schema").glob("*.schema.json"):
        resources[base + f.name] = Resource.from_contents(json.loads(f.read_text(encoding="utf-8")))
    return Registry().with_resources([(uri, res) for uri, res in resources.items()])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brain", default=".brain")
    ap.add_argument("--fast", action="store_true", help="только схемы, без графа")
    ap.add_argument("--stale-fail", type=float, default=None,
                    help="exit 1, если доля карточек с истёкшим valid_until > FRAC")
    args = ap.parse_args()
    brain = Path(args.brain)

    cards, errors = load_cards(brain)
    warnings, today = [], dt.date.today()

    # --- 1. Схемы ---
    registry = schema_registry(brain) if jsonschema else None
    for c in cards:
        d, path = c["data"], c["path"]
        if d.get("type") in TYPES_WITHOUT_SCHEMA:
            continue
        if jsonschema is None:
            break
        schema_name = f"{d.get('type')}.schema.json"
        schema_uri = f"https://brain.example/schema/{schema_name}"
        if not (brain / "schema" / schema_name).exists():
            errors.append(f"{path}: нет схемы {schema_name} для type={d.get('type')}")
            continue
        try:
            jsonschema.Draft202012Validator(
                {"$ref": schema_uri}, registry=registry
            ).validate(d)
        except jsonschema.ValidationError as e:
            errors.append(f"{path}: schema: {e.message} (поле {'/'.join(map(str, e.path))})")

    # --- 2. Уникальность ID и имена файлов ---
    seen = {}
    for c in cards:
        cid, path = str(c["data"].get("id")), c["path"]
        if not CARD_ID.match(cid):
            errors.append(f"{path}: ID '{cid}' не по шаблону X-NNN")
        if cid in seen:
            errors.append(f"{cid}: дубликат ID ({seen[cid]} и {path})")
        seen[cid] = path
        if path.stem != cid and not path.stem.startswith(cid.split("-")[0]):
            warnings.append(f"{path}: имя файла '{path.stem}' != id '{cid}'")

    # --- 3. Целостность графа ---
    if not args.fast:
        by_id = {str(c["data"].get("id")): c for c in cards}
        # datasets.yaml: реестр DS-*
        ds_yaml = brain / "WARM" / "DATA" / "datasets.yaml"
        ds_ids = set()
        if ds_yaml.exists():
            reg = yaml.safe_load(ds_yaml.read_text(encoding="utf-8")) or {}
            ds_ids = {d["id"] for d in reg.get("datasets", [])}
        for c in cards:
            d, path = c["data"], c["path"]
            cid, ctype = str(d.get("id")), d.get("type")
            for link_key in ("supersedes",):
                for tgt in ([d.get(link_key)] if isinstance(d.get(link_key), str) else (d.get(link_key) or [])):
                    if tgt and str(tgt) not in by_id:
                        errors.append(f"{path}: {link_key} -> несуществующая карточка {tgt}")
            if d.get("superseded_by") and str(d["superseded_by"]) not in by_id:
                errors.append(f"{path}: superseded_by -> несуществующая карточка {d['superseded_by']}")
            if ctype == "claim" and d.get("status") != "retracted":
                ev = d.get("evidence") or {}
                for r in ev.get("runs", []):
                    t = by_id.get(str(r))
                    if not t:
                        errors.append(f"{path}: evidence.runs -> нет прогона {r}")
                    elif t["data"].get("type") != "experiment":
                        errors.append(f"{path}: {r} — не experiment")
            if ctype == "experiment":
                h = d.get("hypothesis")
                if h and str(h) not in by_id:
                    errors.append(f"{path}: hypothesis -> нет гипотезы {h}")
                for inp in (d.get("data") or {}).get("inputs", []):
                    if inp.get("id") and inp["id"] not in ds_ids:
                        errors.append(f"{path}: data.inputs -> нет датасета {inp['id']} в datasets.yaml")
            # X-09: агент не присваивает human-verified/published сам
            author = str(d.get("author", ""))
            if author.startswith(("agent:", "agent-role:")) and d.get("trust") in ("human-verified", "published"):
                errors.append(f"{path}: X-09: агент '{author}' присвоил trust={d['trust']} своей записи")

    # --- 4. Свежесть ---
    expired = [str(c["data"].get("id")) for c in cards
               if c["data"].get("valid_until")
               and dt.date.fromisoformat(str(c["data"]["valid_until"])) < today]
    for e in expired:
        warnings.append(f"STALE: {e} valid_until истёк")

    stale_frac = len(expired) / max(len(cards), 1)
    report = {
        "cards": len(cards), "errors": len(errors), "warnings": len(warnings),
        "stale": expired, "stale_fraction": round(stale_frac, 4),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)

    if args.stale_fail is not None and stale_frac > args.stale_fail:
        errors.append(f"доля stale-карточек {stale_frac:.2%} > порога {args.stale_fail:.2%}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
