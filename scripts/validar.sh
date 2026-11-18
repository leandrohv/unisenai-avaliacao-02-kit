#!/usr/bin/env sh
set -eu
PORT="${APP_PORT:-$(sed -n 's/^APP_PORT=//p' .env | head -n 1)}"
PORT="${PORT:-8080}"
echo '[1/4] Configuração do Compose'; docker compose config --quiet
echo '[2/4] Serviços'; docker compose ps
echo '[3/4] Saúde do backend'; curl -fsS "http://127.0.0.1:${PORT}/api/health"; echo
echo '[4/4] Cadastro e listagem';
curl -fsS -X POST "http://127.0.0.1:${PORT}/api/tasks" \
  -H 'Content-Type: application/json' -d '{"titulo":"Validação automatizada da aula 13"}'
echo; curl -fsS "http://127.0.0.1:${PORT}/api/tasks"; echo
