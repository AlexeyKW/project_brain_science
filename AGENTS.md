<!-- СГЕНЕРИРОВАНО src/render_adapters.py ИЗ .brain/ — правки руками откатываются CI (X-08) -->

# AGENTS.md — адаптер Research Brain

# INDEX.md — карта памяти (HOT, грузится всегда)

Только «где что лежит», без содержания. Адресная подгрузка: `.brain/WARM/<раздел>/<ID>.md|yaml`.

## Статус проекта

- Фаза: основные результаты собраны; рукопись в черновике.
- Активный прогон: **E-023** (блочная spatial-CV, Sentinel LST + OSM).
- Открытая гипотеза: **H-001** (предрегистрирована до данных).
- Ключевое утверждение рукописи: **C-007** (`machine-verified`).
- Предупреждение: **F-019** — все метрики до E-021 недействительны (утечка CV).

## Где что лежит (WARM)

| Путь | Что | Читать когда |
|---|---|---|
| `WARM/MAP.md` | граф пайплайна: данные → препроцессинг → модель → фигура | нужен контекст модулей |
| `WARM/GLOSSARY.md` | термины, CRS, единицы, кодировки | любой анализ |
| `WARM/HYPOTHESES/H-001.md` | предрегистрация основной гипотезы | цитирование гипотезы |
| `WARM/DECISIONS/D-014-spatial-cv.md` | почему блочная CV, а не случайная K-fold | методология |
| `WARM/EXPERIMENTS/E-023.yaml` | ключевой прогон: seed, хеши, метрики | любое число из проекта |
| `WARM/CLAIMS/C-007.md` | главный claim (NDVI → LST) | раздел Results |
| `WARM/CLAIMS/C-004..C-006.md` | retracted (см. F-019) | не использовать |
| `WARM/FAILURES.md` | реестр отрицательных результатов (F-019…) | перед новым экспериментом |
| `WARM/LITERATURE/` | refs.bib, notes/, verified.yaml | любая ссылка |
| `WARM/DATA/` | datasets.yaml, DATACARDS/, LICENSES.md, ETHICS.md | перед работой с данными |
| `WARM/METHODS/` | protocols/, preregistration/ | воспроизведение |

## ID-система

`C-NNN` claim · `H-NNN` hypothesis · `D-NNN` decision (ADR) · `E-NNN` experiment · `F-NNN` failure · `DS-NNN` dataset.
Одна сущность = один файл с постоянным ID → почти нет merge-конфликтов.

## COLD

`sessions/` — сырые логи сессий (union-merge); `archive/` — закрытые ветки;
`.index/` — sqlite + эмбеддинги (gitignored, пересобирается из файлов, никогда не источник истины).

## Схемы и роли

- `.brain/schema/*.json` — JSON Schema для каждого типа карточки (claim, hypothesis, experiment, decision, failure, dataset).
- `.brain/agents/*.yaml` — роли Scout / Data steward / Analyst / Critic / Scribe: промпты и write-scope.
- `.brain/hooks/` — session-end, pre-commit.


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
