from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserSerializer(UserSerializer):
	class Meta(UserSerializer.Meta):
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'get_full_name', 'profile')