from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import FeeCategory, PaymentMethod, Payment, Invoice
from .permissions import IsFinanceAdminOrReadOnly
from rest_framework import viewsets
from .serializers import FeeCategorySerializer, PaymentMethodSerializer, PaymentSerializer, InvoiceSerializer

class IsFinanceAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read-only for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # Write permissions only for finance/admin users
        return request.user.is_staff or request.user.has_perm('finance.manage_payments')

class FeeCategoryViewSet(viewsets.ModelViewSet):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsFinanceAdminOrReadOnly]

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated, IsFinanceAdminOrReadOnly]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsFinanceAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['student__id', 'fee_category__id', 'payment_method__id', 'paid_on']
    search_fields = ['transaction_reference', 'student__user__username']
    ordering_fields = ['paid_on', 'amount_paid']

    def get_queryset(self):
        user = self.request.user
        # Admin/finance can see all payments
        if user.is_staff or user.has_perm('finance.view_all_payments'):
            return self.queryset
        # Students/parents see only their payments
        return self.queryset.filter(student__user=user)

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsFinanceAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student__id', 'fee_category__id', 'is_paid', 'due_date']
    ordering_fields = ['due_date', 'generated_on']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.has_perm('finance.view_all_invoices'):
            return self.queryset
        return self.queryset.filter(student__user=user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user.student_profile)
        
        
