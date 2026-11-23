---
id: L-001
type: note
status: supported
trust: ai-inferred
confidence: 0.6
author: agent-role:scout
created: 2026-11-10
tags: [literature, spatial-cv]
---

# L-001: заметка Scout'а — обзор spatial-CV

Обобщение robertsspatiotemporal для нашего кейса:

- Случайное разбиение при автокорреляции > 0.5 на лаге размера блока → оптимистичный R² (подтверждено у нас: F-019).
- Рекомендация обзора: блоки по физическому расстоянию, а не по индексу сцены — совпадает с D-014.
- Буферная CV точнее leave-block-out при n < 20k; у нас n = 12 480 → кандидат для финальной оценки (см. D-014 альтернатива 3).

Статус: ai-inferred, до применения в методологии нужен human-review.
