from djoser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import Socials
from blog.ArticleSerializerForAuthor import ArticleSerializerForAuthor
User = get_user_model()

class SocialsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Socials
		fields = ['telegram', 'linkedin', 'instagram', 'github', 'website'] 

class FollowerOrFollowingSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'profile')

class CustomUserSerializer(UserSerializer):
	socials = SocialsSerializer()
	followers = FollowerOrFollowingSerializer(many=True)
	followings = FollowerOrFollowingSerializer(many=True)
	class Meta(UserSerializer.Meta):
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'get_full_name', 'profile', 'followers', 'followings', 'about', 'socials')



class AuthorSerializer(CustomUserSerializer):
	saved_articles = ArticleSerializerForAuthor(many=True)
	class Meta(CustomUserSerializer.Meta):
		fields = ('username', 'email', 'get_full_name', 'profile', 'followers', 'followings', 'about', 'socials', 'saved_articles')

class ArticleAuthorSerializer(AuthorSerializer):
	class Meta(AuthorSerializer.Meta):
		fields = ('username', 'get_full_name', 'profile', 'about', 'socials')


class CommentAuthorSerializer(AuthorSerializer):
	class Meta(AuthorSerializer.Meta):
		fields = ('username', 'get_full_name', 'profile')