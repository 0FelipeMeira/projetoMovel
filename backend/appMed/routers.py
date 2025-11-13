from rest_framework import routers
from .viewsets import (
    RegistroViewSet,
    IdosoViewSet,
    MedicamentoViewSet,
    TomadaViewSet,
)

router = routers.DefaultRouter()
router.register(r'registros', RegistroViewSet, basename='registros')
router.register(r'idosos', IdosoViewSet, basename='idosos')
router.register(r'medicamentos', MedicamentoViewSet, basename='medicamentos')
router.register(r'tomadas', TomadaViewSet, basename='tomadas')

urlpatterns = router.urls
