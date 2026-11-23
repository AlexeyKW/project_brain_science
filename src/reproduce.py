#!/usr/bin/env python
"""reproduce.py — smoke-перезапуск эксперимента (CI check 3: воспроизводимость).

  make reproduce E-023
      = python src/reproduce.py --experiment E-023 --smoke --tolerance 0.02

Детерминированный smoke-прогон на синтетической подвыборке (seed из карточки),
сверка beta_NDVI и R²_oob с expected в EXPERIMENTS/E-*.yaml в пределах допуска.
"""
import argparse, json, sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from models.spatial_cv import synthetic_grid, run_blocked_cv, min_train_test_distance


def load_experiment(brain: Path, eid: str):
    path = brain / "WARM" / "EXPERIMENTS" / f"{eid}.yaml"
    if not path.exists():
        sys.exit(f"ERROR: нет карточки {path}")
    data = {}
    for d in yaml.safe_load_all(path.read_text(encoding="utf-8")):
        if isinstance(d, dict):
            data.update(d)   # front-matter + тело карточки
    return data, path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--experiment", required=True)
    ap.add_argument("--brain", default=".brain")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--tolerance", type=float, default=0.02)
    args = ap.parse_args()
    brain = Path(args.brain)

    exp, path = load_experiment(brain, args.experiment)
    seed = int(exp["environment"]["seed"])
    design = exp.get("design", {})
    blocks = int(design.get("cv", {}).get("blocks", 5))
    n = int(design.get("n", 1000))
    smoke = exp.get("smoke", {})
    subset = float(smoke.get("subset", 0.05)) if args.smoke else 1.0
    tolerance = float(smoke.get("tolerance", args.tolerance))
    expected = smoke.get("expected", {})

    grid = synthetic_grid(int(n * subset), seed=seed)
    metrics = run_blocked_cv(grid, blocks=blocks)

    # Защита от утечки (M-001, правило расстояния)
    dmin = min_train_test_distance(grid, blocks=blocks)
    if dmin < 1.8 / (1 / subset ** 0.5):  # масштабированный порог для подвыборки
        print(f"WARNING: min train/test distance = {dmin:.0f} м — проверьте блоки")

    report = {"experiment": args.experiment, "seed": seed, "smoke": args.smoke,
              "subset": subset, "metrics": metrics, "expected": expected,
              "tolerance": tolerance, "checks": {}}
    ok = True
    for key, exp_val in expected.items():
        got = metrics.get(key)
        passed = got is not None and abs(got - float(exp_val)) <= tolerance
        report["checks"][key] = {"expected": exp_val, "got": got, "passed": passed}
        ok &= passed

    out = Path("results/metrics")
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{args.experiment}.smoke.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
