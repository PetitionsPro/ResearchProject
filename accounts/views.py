from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(access)
            }, status=status.HTTP_201_CREATED)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                "user": {
                    "id":user.id,
                    "email":user.email,
                    "full_name":user.full_name
                },
                "refresh": str(refresh),
                "access": str(access)
            }, status=status.HTTP_200_OK)  
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
