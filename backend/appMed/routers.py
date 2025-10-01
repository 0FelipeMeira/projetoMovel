from rest_framework import routers
from .viewsets import RegistroViewSet, RegistroMedViewSet

router = routers.DefaultRouter()
router.register(r'registro', RegistroViewSet, basename='registro')
router.register(r'registro-med', RegistroMedViewSet, basename='registro-med')

urlpatterns = router.urls