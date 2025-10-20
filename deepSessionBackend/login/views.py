import datetime
import random

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTP, User
from .serializers import SendOTPSerializer
from .serializers import VerifyOTPSerializer


class SendOTPView(APIView):
    def post(self, request):
        print("reached here in send otp view")
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user, _ = User.objects.get_or_create(email=email)

        # Generate OTP
        code = str(random.randint(100000, 999999))
        expires_at = timezone.now() + datetime.timedelta(minutes=10)

        OTP.objects.create(user=user, code=code, expires_at=expires_at)

        try:
            send_mail(
                subject="ddhyaan app OTP",
                message=f"Your OTP is {code}. It expires in 10 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                # from_email="saikumar01.g@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp']

        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(user=user, code=otp_code, is_used=False).last()
        except User.DoesNotExist:
            return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

        if otp and otp.is_valid():
            otp.is_used = True
            otp.save()
            user.last_login = timezone.now()
            user.save()

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            # Set the user in request for subsequent views
            request.user = user  # This sets the user context for the request

            return Response({
                'message': 'OTP verified successfully',
                'user': {'user_id': str(user.user_id), 'email': user.email},
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)


class HealthCheckView(APIView):
    def get(self, request):
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
