#!/usr/bin/env python
"""render_adapters.py — регенерация AGENTS.md / CLAUDE.md / .cursor/rules из .brain.

Адаптеры НЕ редактируются руками (X-08, CI check 7): источник шаблонов — этот скрипт
+ HOT-слой. Запуск: make adapters.
"""
import argparse
from pathlib import Path

HEADER = "<!-- СГЕНЕРИРОВАНО src/render_adapters.py ИЗ .brain/ — правки руками откатываются CI (X-08) -->\n\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brain", default=".brain")
    args = ap.parse_args()
    brain = Path(args.brain)
    index = (brain / "HOT" / "INDEX.md").read_text(encoding="utf-8")
    constraints = (brain / "HOT" / "CONSTRAINTS.md").read_text(encoding="utf-8")

    Path("AGENTS.md").write_text(
        HEADER + "# AGENTS.md — адаптер Research Brain\n\n" + index + "\n\n" + constraints,
        encoding="utf-8")
    Path("CLAUDE.md").write_text(
        HEADER + "# CLAUDE.md — адаптер Research Brain\n\n"
        "Старт: HOT-слой (INDEX → HANDOFF → CONSTRAINTS), затем адресная подгрузка карточек.\n\n"
        + constraints,
        encoding="utf-8")
    cursor = Path(".cursor/rules")
    cursor.mkdir(parents=True, exist_ok=True)
    (cursor / "brain.mdc").write_text(
        HEADER + "---\ndescription: Research Brain\nalwaysApply: true\n---\n\n"
        "Старт: .brain/HOT/{INDEX,HANDOFF,CONSTRAINTS}.md. Только адресная подгрузка карточек.\n\n"
        + constraints,
        encoding="utf-8")
    print("адаптеры пересобраны: AGENTS.md, CLAUDE.md, .cursor/rules/brain.mdc")


if __name__ == "__main__":
    main()
