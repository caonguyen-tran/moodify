from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework import viewsets, mixins, generics, status
from .models import User

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'update_password':
            return ChangePasswordSerializer
        return UserSerializer

    @action(methods=['patch'], detail=False, url_path='update-password', url_name='update-password')
    def update_password(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)