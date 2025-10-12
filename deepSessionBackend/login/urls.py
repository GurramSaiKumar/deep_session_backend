from django.urls import path
from .views import SendOTPView, VerifyOTPView, HealthCheckView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('health/', HealthCheckView.as_view(), name='health_check'),
]
