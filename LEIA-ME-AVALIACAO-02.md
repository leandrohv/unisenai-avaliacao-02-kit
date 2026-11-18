# Avaliação 02 - Kit inicial do estudante

Este kit é uma **cópia didática do laboratório da Aula 13**, fornecido como ponto de partida para a Avaliação 02. A solução exigida **não** está implementada: a avaliação descreve as alterações a realizar.

## O que foi alterado no kit de partida
- Projeto Docker isolado: `name: unisenai-av02-${AV02_ID:-aluno}`.
- `.env.example` tem `AV02_ID=aluno` e porta inicial `8080`. Os alunos devem definir seu identificador e a porta solicitada.
- Os três serviços, a API `/api/health`, rede e banco vêm do laboratório original.

## Início (após ler a avaliação)
Linux/macOS: `cp .env.example .env`

Windows PowerShell: `Copy-Item .env.example .env`

Abra a pasta no editor, cumpra as etapas da Avaliação 02 e registre as evidências em `relatorio_evidencias.md`. **Não entregue `.env`**, dumps, credenciais reais ou dados pessoais desnecessários.

## Uso seguro
Somente ambiente local e dados fictícios. Evite `docker compose down -v` e `docker system prune` no ambiente de prova. O banco não publica a porta 5432 no host.
