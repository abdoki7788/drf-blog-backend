from rest_framework import serializers
from .models import Article, Tag
from django.utils.text import slugify

class ArticleSerialize(serializers.ModelSerializer):
	hits = serializers.IntegerField(source='hits.count', read_only=True)
	class Meta:
		model = Article
		fields = '__all__'

class ArticleCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ('title', 'content', 'status')
	
	def create(self, validated_data):
		validated_data['slug'] = slugify(validated_data['title'], allow_unicode=True)
		validated_data['author'] = self.context['request'].user
		obj = Article.objects.create(**validated_data)
		obj.save()
		return obj

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'