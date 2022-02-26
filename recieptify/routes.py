from rest_framework.routers import DefaultRouter

from apps.core.views import AuthViewSet, ReceiptViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='api-auth')
router.register(r'receipt', ReceiptViewSet, basename='api-receipt')
