import os
import jwt
from datetime import timedelta
from django.conf import settings
from django.db import connection
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from .models import Registro
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def healthcheck(request):
    status_http = 200
    db_ok = True
    error_msg = None
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception as exc:
        db_ok = False
        error_msg = str(exc)
        status_http = 503

    payload = {
        "name": "DoseCerta API",
        "status": "ok" if db_ok else "error",
        "version": getattr(settings, "APP_VERSION", "dev"),
        "commit": os.environ.get("GIT_COMMIT", "dev"),
        "time": timezone.now().isoformat(),
        "db": {"ok": db_ok},
        "links": {
            "api_root": "/api/v1/",
            "admin": "/admin/",
        },
    }
    if error_msg:
        payload["error"] = error_msg

    return JsonResponse(payload, status=status_http)


@csrf_exempt
@require_POST
def auth_login(request):
    try:
        import json
        body = json.loads(request.body.decode('utf-8')) if request.body else {}
    except Exception:
        return JsonResponse({'detail': 'JSON inválido.'}, status=400)

    email = body.get('email')
    senha = body.get('senha')
    if not email or not senha:
        return JsonResponse({'detail': 'email e senha são obrigatórios.'}, status=400)

    try:
        registro = Registro.objects.get(email=email)
    except Registro.DoesNotExist:
        return JsonResponse({'detail': 'Credenciais inválidas.'}, status=401)

    if not check_password(senha, registro.senha):
        return JsonResponse({'detail': 'Credenciais inválidas.'}, status=401)

    issued_at = now()
    exp = issued_at + timedelta(hours=12)
    payload = {
        'sub': registro.id,
        'email': registro.email,
        'iat': int(issued_at.timestamp()),
        'exp': int(exp.timestamp()),
        'iss': 'DoseCerta'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return JsonResponse({
        'access': token,
        'token_type': 'bearer',
        'expires_in': int((exp - issued_at).total_seconds()),
        'user': {
            'id': registro.id,
            'nome': registro.nome,
            'email': registro.email,
        }
    })


def home(request):
    html = """
    <!doctype html>
    <html lang="pt-br">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>DoseCerta API</title>
        <style>
          body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; margin: 40px; color: #222; }
          .card { max-width: 720px; padding: 24px; border: 1px solid #eee; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,.04); }
          h1 { margin-top: 0; }
          a { color: #7100b3; text-decoration: none; }
          a:hover { text-decoration: underline; }
          .links { display: grid; gap: 8px; margin-top: 16px; }
          code { background: #f6f6f6; padding: 2px 6px; border-radius: 6px; }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>🚑 DoseCerta API</h1>
          <p>Backend em Django para controle de horários de medicamentos.</p>
          <div class="links">
            <div>• <a href="/api/v1/">API Root</a></div>
            <div>• <a href="/admin/">Admin</a></div>
            <div>• <a href="/healthz">Healthcheck JSON</a></div>
          </div>
          <p style="margin-top:16px;color:#666">Veja também <code>/backend/README.md</code> para documentação completa.</p>
        </div>
      </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html; charset=utf-8")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def auth_me(request):
    user = getattr(request, 'user', None)
    registro = getattr(user, 'registro', None)
    if not registro:
        return Response({'detail': 'Não autenticado.'}, status=401)
    return Response({
        'id': registro.id,
        'nome': registro.nome,
        'email': registro.email,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def auth_refresh(request):
    user = getattr(request, 'user', None)
    registro = getattr(user, 'registro', None)
    if not registro:
        return Response({'detail': 'Não autenticado.'}, status=401)

    issued_at = now()
    exp = issued_at + timedelta(hours=12)
    payload = {
        'sub': registro.id,
        'email': registro.email,
        'iat': int(issued_at.timestamp()),
        'exp': int(exp.timestamp()),
        'iss': 'DoseCerta'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return Response({
        'access': token,
        'token_type': 'bearer',
        'expires_in': int((exp - issued_at).total_seconds()),
    })
