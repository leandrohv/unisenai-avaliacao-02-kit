# UniSENAI | Aula 13 - Docker Compose multicontêineres

Projeto didático **frontend (Nginx + HTML/JS) → backend (Flask) → banco (PostgreSQL)**. Cada componente é um serviço. O navegador usa `/api/` no Nginx; o Nginx encaminha ao backend por DNS interno `backend:8000`; o backend acessa o banco pelo serviço `db:5432`. O banco usa volume nomeado para persistência.

## Pré-requisitos

- Docker Engine + plugin Compose v2 funcionando; internet para baixar imagens na primeira execução.
- Porta local **8080** disponível; aproximadamente 2 GB de RAM livres (estimativa conservadora para o laboratório).
- Terminal PowerShell (Windows) ou Bash/sh (Linux/macOS). No Windows, Docker Desktop com backend Linux.

## Etapa 1: preparar o projeto

Linux/macOS:

```sh
cp .env.example .env
docker compose version
docker compose config --quiet
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
docker compose version
docker compose config --quiet
```

A senha em `.env.example` é **exclusivamente didática**. Não publique `.env` em repositórios e não use essa senha em ambiente real. Para a aula, edite `APP_PORT` se 8080 já estiver em uso.

## Etapa 2: subir os serviços

```sh
docker compose up -d --build
docker compose ps
docker compose logs --tail=40
```

Acesse **http://127.0.0.1:8080** (ou porta definida em `.env`). Crie uma tarefa e recarregue a página. Aguarde a saúde dos serviços indicar `healthy` caso necessário.

## Etapa 3: compreender o fluxo

1. Browser GET `/` → Nginx entrega HTML/CSS/JS.
2. Browser GET `/api/tasks` → Nginx faz proxy para `http://backend:8000`.
3. Backend executa SQL parametrizado no PostgreSQL, pela rede `data_net`.
4. POST `/api/tasks` grava em volume gerenciado `pgdata` (com o banco).

O navegador **não** consegue resolver `backend` nem `db` diretamente: esses nomes são DNS de redes Docker internas. O frontend só precisa conhecer `backend`, não o banco.

## Etapa 4: validar pela API

Linux/macOS:

```sh
curl -i http://127.0.0.1:8080/api/health
curl -i http://127.0.0.1:8080/api/tasks
curl -i -X POST http://127.0.0.1:8080/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"titulo":"Minha primeira tarefa"}'
```

Windows PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8080/api/health
Invoke-RestMethod http://127.0.0.1:8080/api/tasks
Invoke-RestMethod -Uri http://127.0.0.1:8080/api/tasks -Method Post -ContentType 'application/json' -Body '{"titulo":"Minha primeira tarefa"}'
```

Também é possível executar `sh scripts/validar.sh` ou `./scripts/validar.ps1` dentro da pasta raiz (respectivamente).

## Etapa 5: persistência

```sh
docker compose down
docker compose up -d
docker compose ps
```

Reabra a página: **a tarefa anterior deve permanecer**. A razão é o volume `pgdata`, mantido pelo Docker.

**Atenção**: `docker compose down -v` remove os volumes associados à aplicação. Neste laboratório, apaga os dados persistidos. Use somente se quiser restaurar o banco ao estado vazio.

## Etapa 6: simular e diagnosticar falhas

```sh
docker compose stop db
docker compose ps
docker compose logs --tail=40 backend
```

Recarregue a página: a API deve falhar ao consultar o banco. A saúde do backend fica degradada quando os healthchecks detectam a falha; o frontend pode continuar ativo e encaminhar erros HTTP da API. Recupere:

```sh
docker compose start db
docker compose ps
docker compose logs --tail=40 db
```

Aguarde o banco atingir `healthy` e recarregue a página. O Compose **não garante** recuperação automática das aplicações em cascata apenas por `depends_on`: a API deve implementar tolerância e reconexão.

## Diagnóstico rápido

| Sintoma | Verificação | Correção provável |
|---|---|---|
| Porta 8080 em uso | `docker compose ps` e logs | Altere `APP_PORT` em `.env` |
| `backend unhealthy` | `docker compose logs backend db` | Verifique saúde do banco e `DATABASE_URL` |
| Resposta 502 | `docker compose logs frontend backend` | Proxy ou backend indisponível |
| Banco vazio após recriar | `docker volume ls` | Verifique se rodou `down -v` |
| Acesso a `db:5432` no host falha | `docker compose config` | Comportamento esperado: porta não publicada |
| Mudança na API não aparece | `docker compose up -d --build` | Rebuild da imagem do backend |

## Desafio (20 minutos)

1. Explique por que apenas o serviço **frontend** tem `ports`, enquanto o backend usa `expose` e o banco não publica porta.
2. Mostre que os dados persistem após `docker compose down` / `up -d`.
3. Identifique um risco de segurança e uma melhoria de confiabilidade.
4. **Opcional:** implemente rota DELETE `/api/tasks/<id>` com SQL parametrizado e botão para exclusão no frontend.

**Entregáveis do aluno:** screenshot do `docker compose ps`; navegador com tarefa criada; evidência de persistência; resposta aos itens 1 e 3.

## Uso responsável

Este laboratório é para máquina local, sem autenticação, HTTPS, rate limiting, migrações versionadas ou backup de produção. Não exponha o serviço em rede pública. O Compose é excelente para desenvolvimento, teste e host único controlado, mas não é automaticamente alta disponibilidade/orquestração distribuída.

## Referências

- Material da disciplina: *Aula_Docker_Basico_ao_Avancado.pdf* (arquivo fornecido pelo docente).
- Docker Docs: https://docs.docker.com/compose/how-tos/startup-order/
- Docker Docs: https://docs.docker.com/compose/how-tos/networking/
- Docker Docs: https://docs.docker.com/compose/gettingstarted/
