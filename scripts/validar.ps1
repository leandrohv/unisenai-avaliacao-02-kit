$ErrorActionPreference = 'Stop'
$port = if ($env:APP_PORT) { $env:APP_PORT } else {
  $config = Get-Content .env | Where-Object { $_ -match '^APP_PORT=' } | Select-Object -First 1
  if ($config) { ($config -split '=',2)[1] } else { '8080' }
}
Write-Host '[1/4] Configuração do Compose'
docker compose config --quiet
if ($LASTEXITCODE -ne 0) { throw 'Compose inválido' }
Write-Host '[2/4] Serviços'
docker compose ps
Write-Host '[3/4] Saúde do backend'
Invoke-RestMethod "http://127.0.0.1:$port/api/health" | ConvertTo-Json
Write-Host '[4/4] Cadastro e listagem'
$body = @{titulo='Validação automatizada da aula 13'} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:$port/api/tasks" -Method Post -ContentType 'application/json' -Body $body | ConvertTo-Json
Invoke-RestMethod "http://127.0.0.1:$port/api/tasks" | ConvertTo-Json
