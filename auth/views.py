from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.auth.serializers import ChangePasswordSerializer, UpdateUserSerializer
from core.user.models import User


class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
