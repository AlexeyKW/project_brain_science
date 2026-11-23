---
id: DS-002
type: dataset
status: active
trust: machine-verified
author: agent-role:data-steward
created: 2026-11-03
valid_until: 2027-06-01
tags: [osm, kazan, geodata, odbL]
---

# DS-002: OpenStreetMap extract, Казань, дамп 2024-06-15

## Источник и версия

- Источник: Geofabrik extract (Central Federal District → г. Казань), **датафиксация дампа 2024-06-15**.
- Датафиксация критична: OSM — живой источник; значения атрибутов «плавают» между дампами.
- Слои: buildings (polygons), landuse, roads, water. Использовано: buildings + landuse.

## Лицензия

ODbL-1.0. Производные БД — share-alike; **атрибуция обязательна** (см. LICENSES.md).
Публикация производных слоёв в RO-Crate/Zenodo допустима с указанием ODbL.

## Хранение и хеш

- DVC: `data/raw/osm_kazan_20240615.dvc`, hash `dvc:osm_kazan_20240615`.
- Производные: `built_fraction` по кварталам — в `data/processed/` (тоже DVC).

## Известные дефекты

1. Полнота зданий неоднородна по районам → контроль застройки недооценивает окраины
   (Critic, 2026-11-18; см. MAP §дефекты).
2. Паркинги и гаражи иногда размечены как building → фильтр `building !~ /garage|shed/` в align.py.

## Использование

- Аналитическая единица «квартал» (OSM-полигоны, n = 12 480 — см. E-023).
- При смене дампа: новый dvc_hash, контроль стабильности built_fraction (допуск 5%), запись в FAILURES при отклонении.
