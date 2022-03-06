from rest_framework import serializers
from .models import Article, Category

class ArticleSerialize(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = '__all__'



class CategorySerialize(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'name', 'articles')