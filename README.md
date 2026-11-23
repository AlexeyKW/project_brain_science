# Research Brain: Urban Heat Islands × Green Zones (Kazan)

Скелет репозитория **Research Brain** — лабораторного журнала как код для научного проекта.
Единица памяти — не решение, а пара «утверждение + доказательство» (claim → evidence).

Тема сквозного примера: связь NDVI (зелёные зоны, Sentinel-2) и LST (ландшафтная температура,
Sentinel-3 SLSTR) в Казани. Данные: Sentinel LST + OpenStreetMap (датафиксированные дампы).

## Метрики здоровья мозга

![time-to-context](https://img.shields.io/badge/time--to--context-2.7k%20tokens-green)
![reproducibility-rate](https://img.shields.io/badge/reproducibility%20rate-67%25-yellow)
![orphan-claims](https://img.shields.io/badge/orphan%20claims-0-green)
![staleness](https://img.shields.io/badge/staleness-4%25-green)
![negative-result-coverage](https://img.shields.io/badge/negative--result%20coverage-100%25-green)
![decision-coverage](https://img.shields.io/badge/decision%20coverage-80%25-green)

См. §11 спецификации: эти бейджи — критерий готовности проекта к подаче статьи.

## Быстрый старт для агента

1. Прочитай `.brain/HOT/INDEX.md` → `.brain/HOT/HANDOFF.md` → `.brain/HOT/CONSTRAINTS.md` (~2.5k токенов).
2. Дальше — только адресная подгрузка карточек по ID (`.brain/WARM/**`), никакого «прочитай всю папку».
3. Источник истины — `.brain/`, а не чат и не `AGENTS.md` (генерируемый адаптер).

## Быстрый старт для человека

```bash
make validate     # валидация front-matter всех карточек по JSON Schema
make reproduce E-023   # smoke-перезапуск ключевого эксперимента на подвыборке
make metrics      # пересчёт метрик здоровья мозга для бейджей README
```

## Структура

```
.brain/            # источник истины: HOT / WARM / COLD, schema, agents, hooks
data/              # DVC / git-annex, в git только указатели (.dvc)
src/               # код воспроизведения (make reproduce)
notebooks/ results/ paper/
.github/workflows/brain-ci.yml   # иммунная система памяти
```

Полное описание формата — в `.brain/brain.yaml` и спецификации проекта.

## Лестница доверия

`ai-inferred` → `machine-verified` (CI) → `human-verified` (подписанный коммит) → `published` (DOI).
Агент **не может** повысить уровень доверия собственной записи. `ai-inferred`-числа блокируют сборку рукописи.
