from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView , GenericAPIView

from .serializers import ReadUserSerializer, WriteUserSerializer, \
    CustomAuthTokenSerializer, UsersEmailSerializer
from .permissions import IsSuperAdmin, IsOwner
from .models import User
from .exceptions import PrivilegeException
import pdb


class UsersView(ListCreateAPIView):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsSuperAdmin()]
        else:
            return []

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadUserSerializer
        else:
            return WriteUserSerializer


class UserSpecificView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ReadUserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin|IsOwner]
    http_method_names = ["patch", "delete", "get"]

    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        self.check_object_permissions(self.request, user)
        user.delete(request)
        return Response(None, 200)

    def patch(self, request, pk):
        obj = User.objects.get(id=pk)
        self.check_object_permissions(self.request, obj)
        instance = self.get_object()
        if instance.role == "admin":
            if not request.user == instance:
                raise PrivilegeException("You must be the owner to change details of a admin user")
        partial_serializer = WriteUserSerializer(
            instance, data=request.data, partial=True, context={'request': request}
        )
        partial_serializer.is_valid(raise_exception=True)
        partial_serializer.save()
        return Response(data=partial_serializer.data, status=202)



class LoginView(GenericAPIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        token_serializer = CustomAuthTokenSerializer(data=request.data)

        token_serializer.is_valid(raise_exception=True)
        user = token_serializer.validated_data['user']
        _ = Token.objects.filter(user=user)
        if _:
            _.delete()
        token = Token.objects.create(user=user)
        serialized_user = ReadUserSerializer(user)
        content = {
            'token': token.key,
            'user': serialized_user.data
        }
        return Response(content)


class LogoutView(APIView):

    def delete(self, request):
        token = request.headers['Authorization'].split(" ")[1]
        _ = Token.objects.get(key=token).delete()
        return Response("Logged out successfully")


class GetUsersEmailView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        users_email = User.objects.all().values_list('email', flat=True)
        return Response(users_email, 200)
