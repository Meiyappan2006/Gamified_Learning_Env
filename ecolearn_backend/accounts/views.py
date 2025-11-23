from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.decorators import api_view  # for api_root

# Register API (only Students & Universities allowed)
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        if request.data.get('role') == 'ADMIN':
            return Response({"error": "Admins cannot register here."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)


# Login API (Students, Universities, Admins)
class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })


# Optional: Base API view for /api/accounts/
@api_view(['GET'])
def api_root(request):
    return Response({
        "register": "/api/accounts/register/",
        "login": "/api/accounts/login/"
    })
