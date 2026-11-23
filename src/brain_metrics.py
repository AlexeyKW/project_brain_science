#!/usr/bin/env python
"""brain_metrics.py — метрики здоровья мозга (§11) для бейджей README.

  python src/brain_metrics.py --brain .brain [--json] [--write-badges README.md]

Считает из файлов (источник истины), ничего не выдумывает.
"""
import argparse, datetime as dt, json, re, sys
from pathlib import Path

import yaml

FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)
TOKEN_EST = 1.35  # слов->токенов, грубая оценка для кириллицы


def load_cards(brain):
    cards = []
    for path in sorted((brain / "WARM").rglob("*")):
        if path.suffix not in (".md", ".yaml", ".yml"):
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".md":
            m = FRONTMATTER.match(text)
            if not m:
                continue
            docs = list(yaml.safe_load_all(m.group(1)))
        else:
            docs = list(yaml.safe_load_all(text))
        try:
            d = {}
            for doc in docs:
                if isinstance(doc, dict):
                    d.update(doc)
        except yaml.YAMLError:
            continue
        if isinstance(d, dict) and "id" in d:
            cards.append(d)
    return cards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brain", default=".brain")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    brain = Path(args.brain)
    cards = load_cards(brain)
    today = dt.date.today()

    # time-to-context: объём HOT-слоя
    hot_words = sum(len((brain / "HOT" / f).read_text(encoding="utf-8").split())
                    for f in ("INDEX.md", "HANDOFF.md", "CONSTRAINTS.md"))
    hot_tokens = round(hot_words * TOKEN_EST)

    claims = [c for c in cards if c.get("type") == "claim" and c.get("status") != "retracted"]
    ladder = ["ai-inferred", "machine-verified", "human-verified", "published"]
    repro = sum(1 for c in claims
                if ladder.index(c.get("trust", "ai-inferred")) >= ladder.index("machine-verified"))
    orphans = [c["id"] for c in claims
               if c.get("status") != "retracted" and not (c.get("evidence") or {}).get("runs")]
    stale = [c["id"] for c in cards
             if c.get("valid_until") and dt.date.fromisoformat(str(c["valid_until"])) < today]

    fails_text = (brain / "WARM" / "FAILURES.md").read_text(encoding="utf-8")
    dead_h = [c for c in cards if c.get("type") == "hypothesis" and c.get("status") in ("retracted", "contested")]
    neg_cov = sum(1 for h in dead_h if str(h["id"]) in fails_text)
    decisions = len([c for c in cards if c.get("type") == "decision"])

    metrics = {
        "time_to_context_tokens": hot_tokens,
        "reproducibility_rate": round(repro / max(len(claims), 1), 2),
        "orphan_claims": len(orphans),
        "staleness_fraction": round(len(stale) / max(len(cards), 1), 2),
        "negative_result_coverage": (neg_cov / len(dead_h)) if dead_h else 1.0,
        "decisions_recorded": decisions,
        "claims_total": len(claims), "cards_total": len(cards),
    }
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
