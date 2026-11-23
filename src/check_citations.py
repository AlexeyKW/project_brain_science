#!/usr/bin/env python
"""check_citations.py — CI check 4: цитаты.

  - DOI/URL в LITERATURE/verified.yaml корректны по формату и резолвятся (HEAD-запрос, best-effort);
  - рукопись (paper/) не содержит [UNVERIFIED] и citekeys из списка unverified.
"""
import argparse, re, sys, urllib.request

COMMENT = re.compile(r"<!--.*?-->", re.S)
from pathlib import Path

import yaml

DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")


def check_doi(doi):
    req = urllib.request.Request(f"https://doi.org/{doi}", method="HEAD",
                                 headers={"User-Agent": "brain-ci/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return 200 <= r.status < 400
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brain", default=".brain")
    ap.add_argument("--offline", action="store_true", help="не ходить в сеть (только формат)")
    args = ap.parse_args()
    brain = Path(args.brain)
    verified = yaml.safe_load((brain / "WARM" / "LITERATURE" / "verified.yaml")
                              .read_text(encoding="utf-8"))
    errors = []
    for rec in verified.get("verified", []):
        if rec.get("doi") and not DOI_RE.match(rec["doi"]):
            errors.append(f"DOI формат: {rec.get('citekey')} -> {rec['doi']}")
        if not args.offline and rec.get("doi") and not check_doi(rec["doi"]):
            errors.append(f"DOI не резолвится: {rec.get('citekey')} -> {rec['doi']}")
    banned = {r["citekey"] for r in verified.get("unverified", [])}
    for md in Path("paper").rglob("*.md"):
        text = COMMENT.sub("", md.read_text(encoding="utf-8"))  # комментарии не рендерятся
        if "[UNVERIFIED]" in text:
            errors.append(f"{md}: содержит [UNVERIFIED] — сборка рукописи блокируется")
        for key in banned:
            if f"{{{key}}}" in text or f"@{key}" in text:
                errors.append(f"{md}: неразрешённый citekey {key}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    print("citations: OK")


if __name__ == "__main__":
    main()
