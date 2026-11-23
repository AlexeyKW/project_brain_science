---
id: M-001
type: note
status: supported
trust: human-verified
author: alexey
reviewed_by: alexey
created: 2026-11-06
tags: [spatial-cv, protocol, methodology]
---

# M-001: Протокол блочной spatial-CV (D-014)

Реализация: `src/models/spatial_cv.py`. Прогоны: E-021 … E-024.

1. **Блоки.** Координаты кварталов (центроиды, EPSG:3576) → k-means, k = 40 кластеров → 5 блоков
   (равномерный размер ±10%). Привязка блоков к seed = 42 фиксируется артефактом `results/blocks_E-0XX.json`.
2. **Правило расстояния.** Минимальное расстояние между train и test внутри фолда ≥ 1.8 км
   (полураспад вариограммы LST). Проверка — ассерт в коде, отказ при нарушении (защита от F-019).
3. **Оценка.** OLS с HC3-ошибками; β и ДИ — бутстрэп по блокам, B = 1000, seed = 42.
4. **Отчёт.** Метрики в `results/metrics/E-0XX.metrics.json`; сверка smoke-прогоном (допуск 0.02) — `make reproduce`.
5. **Multiplicity.** Каждая серия из > 1 сравнения — запись `E-0XX.multiplicity.yaml` (X-04).

Изменения протокола — только через ADR (supersedes). Текущая версия: 3 (2026-11-14, после F-019).
