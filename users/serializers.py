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
		fields = ('id', 'username', 'get_full_name', 'profile')

class CustomUserSerializer(UserSerializer):
	socials = SocialsSerializer()
	followers = FollowerOrFollowingSerializer(many=True)
	followings = FollowerOrFollowingSerializer(many=True)
	saved_articles = ArticleSerializerForAuthor(many=True)
	class Meta(UserSerializer.Meta):
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'get_full_name', 'profile', 'followers', 'followings', 'about', 'socials', 'saved_articles')



class AuthorSerializer(CustomUserSerializer):
	class Meta(CustomUserSerializer.Meta):
		fields = ('id', 'username', 'email', 'get_full_name', 'profile', 'followers', 'followings', 'about', 'socials')

class ArticleAuthorSerializer(AuthorSerializer):
	class Meta(AuthorSerializer.Meta):
		fields = ('id', 'username', 'get_full_name', 'profile', 'about', 'socials')


class CommentAuthorSerializer(AuthorSerializer):
	class Meta(AuthorSerializer.Meta):
		fields = ('id', 'username', 'get_full_name', 'profile')