from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import Socials

User = get_user_model()

class SocialsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Socials
		fields = ['telegram', 'linkedin', 'instagram', 'github', 'website'] 

class CustomUserSerializer(UserSerializer):
	socials = SocialsSerializer()
	class Meta(UserSerializer.Meta):
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'get_full_name', 'profile', 'followers', 'followings', 'about', 'socials')



class AuthorSerializer(CustomUserSerializer):
	class Meta(CustomUserSerializer.Meta):
		fields = ('username', 'email', 'get_full_name', 'profile', 'followers', 'followings', 'about', 'socials')

class ArticleAuthorSerializer(AuthorSerializer):
	class Meta(AuthorSerializer.Meta):
		fields = ('username', 'get_full_name', 'profile', 'about', 'socials')


class CommentAuthorSerializer(AuthorSerializer):
	class Meta(AuthorSerializer.Meta):
		fields = ('username', 'get_full_name', 'profile')