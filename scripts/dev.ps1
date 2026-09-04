param(
  [ValidateSet("up", "down", "logs", "test", "pull")]
  [string]$Action = "up"
)

$ComposeFile = Join-Path $PSScriptRoot "..\infra\docker-compose.yml"

switch ($Action) {
  "up" { docker compose -f $ComposeFile up -d --build }
  "down" { docker compose -f $ComposeFile down }
  "logs" { docker compose -f $ComposeFile logs -f api worker web }
  "pull" { docker compose -f $ComposeFile pull postgres redis keycloak flower miniflux }
  "test" {
    docker compose -f $ComposeFile --profile test run --rm test
  }
}
