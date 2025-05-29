from rest_framework.routers import DefaultRouter
from .views import FeeCategoryViewSet, PaymentMethodViewSet, PaymentViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r'fee-categories', FeeCategoryViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = router.urls
