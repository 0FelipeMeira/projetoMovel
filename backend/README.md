# DoseCerta API (Backend Django)

API REST para o aplicativo DoseCerta (controle de horários de medicamentos para idosos e responsáveis), construída com Django e Django REST Framework.

## Visão Geral

- Cadastro de responsáveis (pais/filhos) e perfis de idosos.
- Cadastro de medicamentos com horários fixos e período de uso.
- Agenda do dia por idoso (com base nos horários fixos cadastrados).
- Registro de tomada (confirmação de uso do medicamento), gerando histórico.
- Painel administrativo para gestão e inspeção via Django Admin.

## Stack e Requisitos

- `Python 3.10+`
- `Django 5.2.6`
- `Django REST Framework 3.16.1`
- Banco: `SQLite` (desenvolvimento)

Instalação de dependências:

```
cd backend
python -m pip install -r requirements.txt
```

## Como Rodar Localmente

1) Aplicar migrações

```
python manage.py makemigrations appMed
python manage.py migrate
```

2) (Opcional) Criar superusuário admin

```
python manage.py createsuperuser
```

Observação: já foi criado um admin padrão para testes:
- usuário: `admin`
- email: `admin@gmail.com`
- senha: `admin2025`

3) Iniciar o servidor

```
python manage.py runserver
```

URLs úteis:

- Home (HTML): `http://127.0.0.1:8000/`
- Healthcheck (JSON): `http://127.0.0.1:8000/healthz` (retorna 200 com DB ok; 503 se DB falhar)
- API Root: `http://127.0.0.1:8000/api/v1/`
- Admin: `http://127.0.0.1:8000/admin/`

## Modelos de Dados (Resumo)

- `Registro`: responsável (nome, email, senha com hash)
- `Idoso`: vinculado a um `Registro` responsável
- `Medicamento`: vinculado a um `Idoso` (nome, dosagem, data_inicio, data_termino opcional, frequencia_tipo, dias_semana, ativo)
- `Horario`: horário fixo (`time`) relacionado a `Medicamento`
- `Tomada`: histórico de tomada (horario_previsto, tomado, data_hora_tomada, observacao)

## Endpoints

Base: `http://127.0.0.1:8000/api/v1/`

### Registros (responsáveis)

- `GET /registros/` — lista
- `POST /registros/` — cria
- `GET /registros/{id}/` — detalhe
- `PUT/PATCH /registros/{id}/` — atualiza
- `DELETE /registros/{id}/` — remove

Exemplo de criação:

```
POST /api/v1/registros/
{
  "nome": "Fulano",
  "email": "fulano@example.com",
  "senha": "senha123",
  "confirmar_senha": "senha123"
}
```

### Idosos

- `GET /idosos/` — lista (filtro opcional `?responsavel={id}`)
- `POST /idosos/` — cria
- `GET /idosos/{id}/` — detalhe
- `PUT/PATCH /idosos/{id}/` — atualiza
- `DELETE /idosos/{id}/` — remove
- `GET /idosos/{id}/agenda?data=YYYY-MM-DD` — agenda do dia (com horários fixos)

Exemplo de criação:

```
POST /api/v1/idosos/
{ "responsavel": 1, "nome": "Dona Maria", "data_nascimento": "1940-07-01" }
```

Exemplo de agenda:

```
GET /api/v1/idosos/1/agenda?data=2025-01-10
```

Resposta (exemplo):

```
[
  {
    "medicamento_id": 3,
    "medicamento": "Losartana",
    "dosagem": "50 mg",
    "horario_previsto": "2025-01-10T08:00:00-03:00",
    "tomado": false,
    "tomada_id": null
  }
]
```

### Medicamentos

- `GET /medicamentos/` — lista (filtro opcional `?idoso={id}`)
- `POST /medicamentos/` — cria (aceita `horarios` aninhados)
- `GET /medicamentos/{id}/` — detalhe
- `PUT/PATCH /medicamentos/{id}/` — atualiza (pode substituir `horarios`)
- `DELETE /medicamentos/{id}/` — remove
- `POST /medicamentos/{id}/registrar-tomada` — registra/atualiza tomada para um horário previsto

Exemplo de criação com horários:

```
POST /api/v1/medicamentos/
{
  "idoso": 1,
  "nome": "Losartana",
  "dosagem": "50 mg",
  "data_inicio": "2025-01-01",
  "frequencia_tipo": "horarios_fixos",
  "dias_semana": "SEG,TER,QUA,QUI,SEX,SAB,DOM",
  "horarios": [{"hora": "08:00"}, {"hora": "20:00"}]
}
```

Registrar tomada:

```
POST /api/v1/medicamentos/1/registrar-tomada
{
  "horario_previsto": "2025-01-10T08:00:00-03:00",
  "tomado": true,
  "observacao": "Tomado com água"
}
```

### Tomadas

- `GET /tomadas/` — lista (filtros `?idoso={id}`, `?medicamento={id}`)
- `POST /tomadas/` — cria
- `GET /tomadas/{id}/` — detalhe
- `PUT/PATCH /tomadas/{id}/` — atualiza
- `DELETE /tomadas/{id}/` — remove

## Exemplos Rápidos (cURL)

Criar responsável:

```
curl -X POST http://127.0.0.1:8000/api/v1/registros/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"Fulano","email":"fulano@example.com","senha":"senha123","confirmar_senha":"senha123"}'
```

Criar idoso:

```
curl -X POST http://127.0.0.1:8000/api/v1/idosos/ \
  -H "Content-Type: application/json" \
  -d '{"responsavel":1,"nome":"Dona Maria","data_nascimento":"1940-07-01"}'
```

Criar medicamento com horários:

```
curl -X POST http://127.0.0.1:8000/api/v1/medicamentos/ \
  -H "Content-Type: application/json" \
  -d '{"idoso":1,"nome":"Losartana","dosagem":"50 mg","data_inicio":"2025-01-01","frequencia_tipo":"horarios_fixos","dias_semana":"SEG,TER,QUA,QUI,SEX,SAB,DOM","horarios":[{"hora":"08:00"},{"hora":"20:00"}]}'
```

Agenda do dia do idoso:

```
curl http://127.0.0.1:8000/api/v1/idosos/1/agenda?data=2025-01-10
```

Registrar tomada:

```
curl -X POST http://127.0.0.1:8000/api/v1/medicamentos/1/registrar-tomada \
  -H "Content-Type: application/json" \
  -d '{"horario_previsto":"2025-01-10T08:00:00-03:00","tomado":true,"observacao":"Tomado com água"}'
```

## Autenticação e Segurança

- As senhas do `Registro` são armazenadas com hash.
- Não há autenticação JWT ou sessão configurada na API pública neste momento. Caso necessário, recomenda-se integrar `djangorestframework-simplejwt` e permissões por escopo (responsável ↔ idoso).

## Postman/Insomnia

- Coleção Postman disponível em `backend/postman_collection.json` com variáveis e exemplos prontos.
- Importe a coleção e ajuste a variável `base_url` se necessário.

## CORS

Para uso com um frontend em outro host/porta, considere adicionar `django-cors-headers`.

## Estrutura de Pastas (backend)

```
backend/
├── MedTime/           # projeto Django
├── appMed/            # app com modelos, serializers, viewsets e rotas
├── db.sqlite3         # banco de dev
├── manage.py
├── requirements.txt
└── README.md          # este arquivo
```

## Roadmap Sugerido

- Autenticação JWT e permissões por responsável/idoso.
- Geração de agenda para `intervalo_horas` (além de horários fixos).
- Endpoint de “doses perdidas” e webhooks/Push para responsáveis.
- Registro de device tokens e orquestração de notificações.
