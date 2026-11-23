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
