from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

# Create your views here.
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.select_related('booking__client__user')
    serializer_class = PaymentSerializer
    
    @action(detail=True, methods=['post'], url_path='confirm-payment')
    def confirm_payment(self, request, pk=None):
        payment = self.get_object()
        payment.status = Payment.Status.PAID
        payment.paid_at = timezone.now()
        payment.transaction_id = request.data.get('transaction_id', '')
        payment.save()
        return Response({'status': 'payment confirmed'})