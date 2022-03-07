from rest_framework import serializers
from .models import Article, Category, Tag

class ArticleSerialize(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = '__all__'



class CategorySerialize(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'