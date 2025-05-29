from rest_framework import serializers
from .models import FeeCategory, PaymentMethod, Payment, Invoice

class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = ['id', 'name', 'description', 'amount']

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name']

class PaymentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    fee_category = FeeCategorySerializer(read_only=True)
    fee_category_id = serializers.PrimaryKeyRelatedField(queryset=FeeCategory.objects.all(), source='fee_category', write_only=True)
    payment_method = PaymentMethodSerializer(read_only=True)
    payment_method_id = serializers.PrimaryKeyRelatedField(queryset=PaymentMethod.objects.all(), source='payment_method', write_only=True)
    recorded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'student', 'fee_category', 'fee_category_id', 'amount_paid',
            'payment_method', 'payment_method_id', 'transaction_reference',
            'paid_on', 'recorded_by'
        ]
        read_only_fields = ['paid_on', 'recorded_by', 'student']

    def create(self, validated_data):
        user = self.context['request'].user
        student = validated_data.get('student') or user.student_profile  # adapt based on your user-student relationship
        validated_data['recorded_by'] = user
        validated_data['student'] = student
        return super().create(validated_data)

class InvoiceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    fee_category = FeeCategorySerializer(read_only=True)
    fee_category_id = serializers.PrimaryKeyRelatedField(queryset=FeeCategory.objects.all(), source='fee_category', write_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'student', 'fee_category', 'fee_category_id', 'amount_due', 'due_date', 'is_paid', 'generated_on']
        read_only_fields = ['is_paid', 'generated_on', 'student']
