from django.urls import path
from .views import PaymentAPIView

urlpatterns = [
    path('pay', PaymentAPIView.as_view(), name='process_payment'),
    path('list', PaymentAPIView.as_view(), name='payment_list'),
]