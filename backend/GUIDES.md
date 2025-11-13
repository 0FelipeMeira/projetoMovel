# Guias de Operação e Teste — DoseCerta API

Este documento complementa o README com instruções práticas para monitoramento, testes e operação local.

## 1) Healthcheck e Monitoramento

- Home (HTML): `http://127.0.0.1:8000/`
  - Página simples com links para API, Admin e Healthcheck.
- Healthcheck (JSON): `http://127.0.0.1:8000/healthz`
  - Resposta esperada (HTTP 200 quando DB ok, 503 se DB falhar):
    ```json
    {
      "name": "DoseCerta API",
      "status": "ok",
      "version": "0.1.0",
      "commit": "dev",
      "time": "2025-01-10T12:34:56-03:00",
      "db": {"ok": true},
      "links": {"api_root": "/api/v1/", "admin": "/admin/"}
    }
    ```
  - Teste rápido (curl):
    ```bash
    curl -i http://127.0.0.1:8000/healthz
    ```

Observações:
- O campo `commit` pode ser definido via variável de ambiente `GIT_COMMIT` no momento do deploy. Localmente, fica como `dev`.
- Em caso de erro de banco de dados, o endpoint retorna HTTP 503 e inclui a mensagem de erro no campo `error`.

## 2) Acesso ao Admin e Usuário Padrão

- Admin: `http://127.0.0.1:8000/admin/`
- Credenciais padrão criadas para testes:
  - usuário: `admin`
  - email: `admin@gmail.com`
  - senha: `admin2025`

Para criar outro superusuário:
```bash
python manage.py createsuperuser
```

## 3) Testes Rápidos de API (cURL)

Criar responsável:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/registros/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Fulano","email":"fulano@example.com","senha":"senha123","confirmar_senha":"senha123"}'
```

Criar idoso:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/idosos/ \
  -H "Content-Type: application/json" \
  -d '{"responsavel":1,"nome":"Dona Maria","data_nascimento":"1940-07-01"}'
```

Criar medicamento com horários:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/medicamentos/ \
  -H "Content-Type: application/json" \
  -d '{"idoso":1,"nome":"Losartana","dosagem":"50 mg","data_inicio":"2025-01-01","frequencia_tipo":"horarios_fixos","dias_semana":"SEG,TER,QUA,QUI,SEX,SAB,DOM","horarios":[{"hora":"08:00"},{"hora":"20:00"}]}'
```

Agenda do dia do idoso:
```bash
curl http://127.0.0.1:8000/api/v1/idosos/1/agenda?data=2025-01-10
```

Registrar tomada:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/medicamentos/1/registrar-tomada \
  -H "Content-Type: application/json" \
  -d '{"horario_previsto":"2025-01-10T08:00:00-03:00","tomado":true,"observacao":"Tomado com água"}'
```

## 4) Dicas de Integração com Frontend

- Base URL de API: `http://127.0.0.1:8000/api/v1/`
- Para apps rodando em outra origem (porta/domínio), considere `django-cors-headers`.
- Endpoints relevantes:
  - Cadastro/Login (responsável): por enquanto só cadastro em `/registros/` (senha com hash). Podemos integrar JWT.
  - Gestão: `/idosos/`, `/medicamentos/` (com horários), `/tomadas/`.
  - Agenda do dia para UI: `GET /idosos/{id}/agenda?data=YYYY-MM-DD`.

## 5) Roadmap Operacional (sugestão)

- Adicionar JWT (`djangorestframework-simplejwt`) e permissões por escopo (responsável ↔ idoso).
- Estender healthcheck para serviços externos e métricas de latência.
- Expor versão/commit via pipeline de CI/CD (variáveis de ambiente).

## 6) Coleção Postman

- Arquivo: `backend/postman_collection.json`.
- Contém requests para healthcheck, API root, criação de responsável, idoso, medicamento com horários, agenda do dia, registrar tomada e histórico.
- Após importar, ajuste a variável `base_url` se necessário.
- Adicionar endpoint de "doses perdidas" e fila de notificações (push).
- Registrar device tokens no backend para push notifications.
