# Avaliação 02 - Relatório de evidências

Estudante: _________________________________
Turma: __________________  Data: ___/___/2026
Identificador AV02_ID: ___________   Porta utilizada: ___________

## E01 - Preparação / configuração válida
- Comandos executados:
- Saída relevante (retire qualquer senha real):
- Evidência anexada: E01_....png

## E02 - Configuração segura do Compose
- Alterações no compose.yaml e .env.example:
- Como conferi que backend e db não publicam portas no host:
- Evidência anexada:

## E03 - Liveness, readiness e healthcheck
- Respostas HTTP normais observadas:
- Arquivos alterados:
- Evidência anexada:

## E04 - Integração
- Título único da tarefa: AV02-<seu-ID>-integracao
- POST: código HTTP e trecho da resposta:
- GET ou tela da tarefa:
- Caminho da requisição browser > ... > banco:

## E05 - Persistência
- ID/título antes do down:
- Comandos utilizados, sem -v:
- Evidência do mesmo registro após up:

## E06 - Falha controlada e recuperação
- Com db parado: /api/live = ___ e /api/ready = ___
- Qual log ou sinal investiguei:
- Após o start do db: /api/ready = ___
- Evidência anexada:

## E07 - Justificativa técnica
1. Por que somente o frontend publica uma porta no host?
Resposta:

2. Por que .env não deve ser tratado como cofre de segredos?
Resposta:

3. depends_on: service_healthy resolve indisponibilidade posterior do banco?
Resposta:

4. Volume nomeado é o mesmo que backup externo? Justifique.
Resposta:

## Checklist final
- [ ] compose.yaml final
- [ ] backend/app.py final
- [ ] .env.example com valores estritamente fictícios
- [ ] relatorio_evidencias.md preenchido
- [ ] Evidências E01-E06
- [ ] Sem .env nem dados sensíveis
