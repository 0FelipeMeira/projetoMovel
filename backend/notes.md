superuser
admin
admin@gmail.com
admin2025

API v1 (base: /api/v1/)

1) Cadastro de responsável
POST /registros/
{
  "nome": "Fulano",
  "email": "fulano@email.com",
  "senha": "minha_senha_segura",
  "confirmar_senha": "minha_senha_segura"
}

2) Idosos
- POST /idosos/
  { "responsavel": 1, "nome": "Dona Maria", "data_nascimento": "1940-07-01" }
- GET /idosos/?responsavel=1
- GET /idosos/{id}/agenda?data=2025-01-10

3) Medicamentos
- POST /medicamentos/
{
  "idoso": 1,
  "nome": "Losartana",
  "dosagem": "50 mg",
  "data_inicio": "2025-01-01",
  "frequencia_tipo": "horarios_fixos",
  "dias_semana": "SEG,TER,QUA,QUI,SEX,SAB,DOM",
  "horarios": [{"hora": "08:00"}, {"hora": "20:00"}]
}
- GET /medicamentos/?idoso=1

4) Registrar tomada
- POST /medicamentos/{medicamento_id}/registrar-tomada
{
  "horario_previsto": "2025-01-10T08:00:00-03:00",
  "tomado": true,
  "observacao": "Tomado com água"
}

5) Histórico de tomadas
- GET /tomadas/?idoso=1
