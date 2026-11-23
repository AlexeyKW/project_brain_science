<!-- СГЕНЕРИРОВАНО src/render_adapters.py ИЗ .brain/ — правки руками откатываются CI (X-08) -->

# CLAUDE.md — адаптер Research Brain

Старт: HOT-слой (INDEX → HANDOFF → CONSTRAINTS), затем адресная подгрузка карточек.

# CONSTRAINTS.md — жёсткие правила проекта (HOT)

Каждое правило имеет `owner`, `date`, `valid_until`; устаревшие автоматически попадают в отчёт CI.
Нарушение агентом = PR не мержится. Источник: §5 спецификации.

---

- id: X-01
  rule: "Ни одного числа в тексте без run_id. Нет прогона — нет числа."
  owner: alexey
  date: 2026-11-01
  valid_until: 2027-06-01

- id: X-02
  rule: "Ни одной ссылки без разрешённого DOI/URL; проверка в CI через LITERATURE/verified.yaml. Иначе — тег [UNVERIFIED]."
  owner: alexey
  date: 2026-11-01
  valid_until: 2027-06-01

- id: X-03
  rule: "Гипотезу нельзя менять после просмотра данных без amendment в H-*.md (обоснование + дата). Старая версия остаётся в Git."
  owner: alexey
  date: 2026-11-01
  valid_until: 2027-06-01

- id: X-04
  rule: "Каждая серия проверок пишется в multiplicity-лог (поправка на множественность, метод коррекции)."
  owner: alexey
  date: 2026-11-01
  valid_until: 2027-06-01

- id: X-05
  rule: "Отрицательный результат записывается всегда, до закрытия сессии (FAILURES.md)."
  owner: alexey
  date: 2026-11-01
  valid_until: 2027-06-01

- id: X-06
  rule: "CRS для площадей — equal-area; для веб-карт — EPSG:3857. Не смешивать."
  owner: alexey
  date: 2026-11-01
  valid_until: 2027-06-01

- id: X-07
  rule: "Запрещено грузить сырые персональные данные в облачные модели; embargo до 2027-03."
  owner: alexey
  date: 2026-11-01
  valid_until: 2027-03-01

- id: X-08
  rule: "Источник истины — .brain/, не чат и не AGENTS.md (генерируемый адаптер)."
  owner: alexey
  date: 2026-11-01
  valid_until: 2027-06-01

- id: X-09
  rule: "Агент не может повысить уровень доверия (trust) собственной записи — только CI или человек."
  owner: alexey
  date: 2026-11-05
  valid_until: 2027-06-01

- id: X-10
  rule: "Одна сущность = один файл с постоянным ID; append-only журналы (FAILURES, sessions) не редактируются задним числом."
  owner: alexey
  date: 2026-11-05
  valid_until: 2027-06-01
