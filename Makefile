# Research Brain — Makefile
# Источник истины: .brain/brain.yaml. Этот файл — генерируемый адаптер.

PYTHON ?= python
BRAIN  ?= .brain
E_ID   ?= E-023

.PHONY: boot validate reproduce metrics clean adapters

## boot: что читает агент в начале сессии (HOT-слой, ~2.5k токенов)
boot:
	@cat $(BRAIN)/HOT/INDEX.md
	@cat $(BRAIN)/HOT/HANDOFF.md
	@cat $(BRAIN)/HOT/CONSTRAINTS.md

## validate: front-matter всех карточек против JSON Schema + целостность графа
validate:
	$(PYTHON) src/validate_brain.py --brain $(BRAIN)

## reproduce: smoke-перезапуск эксперимента на подвыборке + сверка метрик с допуском.
## Использование: make reproduce E-023
reproduce:
	$(PYTHON) src/reproduce.py --experiment $(E_ID) --smoke --tolerance 0.02

## metrics: пересчёт метрик здоровья мозга (бейджи README)
metrics:
	$(PYTHON) src/brain_metrics.py --brain $(BRAIN)

## adapters: регенерация AGENTS.md / CLAUDE.md / .cursor/rules из .brain
adapters:
	$(PYTHON) src/render_adapters.py --brain $(BRAIN)

clean:
	rm -rf $(BRAIN)/COLD/.index results/smoke/*
