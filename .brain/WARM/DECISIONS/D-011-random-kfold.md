---
id: D-011
type: decision
status: superseded
trust: ai-inferred
confidence: 0.5
author: agent:claude-sonnet-4.6@2026-10-28
created: 2026-10-28
valid_until: 2027-10-28
superseded_by: D-014
tags: [validation, superseded, leakage]
---

# D-011 [SUPERSEDED]: «Валидация — случайная K-fold CV»

## История

Первоначальный выбор схемы валидации (2026-10-28), до оценки пространственной автокорреляции LST.

## Почему superseded

F-019 (2026-11-14): утечка через соседние пиксели → все метрики случайной CV недействительны.
Заменено решением D-014 (блочная spatial-CV, human-verified).

## Урок

Схему валидации выбирать ДО первых метрик и проверять расстояние train/test
(полураспад автокорреляции) — чек-лист Critic'а, пункт 1.
