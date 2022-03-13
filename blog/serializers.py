from rest_framework import serializers
from .models import Article, Tag, Comment
from users.serializers import AuthorSerializer
from django.utils.text import slugify

class ArticleSerialize(serializers.ModelSerializer):
	full_short_link = serializers.CharField()
	hits = serializers.IntegerField(source='hits.count', read_only=True)
	author = AuthorSerializer()
	class Meta:
		model = Article
		fields = '__all__'

class ArticleCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ('title', 'content', 'status')
	
	def create(self, validated_data):
		validated_data['author'] = self.context['request'].user
		obj = Article.objects.create(**validated_data)
		obj.save()
		return obj

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
	author = AuthorSerializer(read_only=True)
	class Meta:
		model = Comment
		fields = ('id', 'content', 'author')
		read_only_fields = ('id', 'author', 'article')