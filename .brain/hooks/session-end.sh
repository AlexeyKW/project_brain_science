#!/usr/bin/env bash
# session-end hook: фиксация diff памяти перед закрытием сессии (§6).
# Запуск: клиент агента при завершении сессии. Не блокирует выход, но предупреждает.
set -u
BRAIN=".brain"
STAMP="$(date +%Y-%m-%dT%H-%M)"
BRANCH="brain/session-${STAMP}"

echo "[brain] session-end: формирую diff памяти в ветке ${BRANCH}"

git checkout -b "${BRANCH}" 2>/dev/null || git checkout "${BRANCH}"

# 1. Сырой лог → COLD
mkdir -p "${BRAIN}/COLD/sessions"
cp "${SESSION_LOG:-/dev/null}" "${BRAIN}/COLD/sessions/${STAMP}.md" 2>/dev/null || true

# 2. Напоминание агенту (проверка человеком)
cat <<'EOF' > /tmp/brain_session_checklist.txt
[brain] Обязательно перед коммитом:
  - HANDOFF.md обновлён (сделано / блокеры / 3 шага / что не пробовать / вопросы к человеку)
  - новые/изменённые карточки проходят make validate
  - отрицательные результаты записаны в WARM/FAILURES.md (X-05)
  - нет чисел без run_id (X-01), ссылок без верификации (X-02)
EOF
cat /tmp/brain_session_checklist.txt

# 3. Коммит diff памяти
git add "${BRAIN}/HOT" "${BRAIN}/WARM" "${BRAIN}/COLD/sessions" 2>/dev/null || true
git commit -m "brain: session diff ${STAMP}" --no-verify >/dev/null 2>&1 || true
git push -u origin "${BRANCH}" >/dev/null 2>&1 || true

echo "[brain] открой PR из ${BRANCH}; CI запустит проверки схемы, графа и свежести."
