from rest_framework import serializers
from .models import Article, Category, Tag

class ArticleSerialize(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = '__all__'
	publish_date = serializers.DateField(source='date', read_only=True)



class CategorySerialize(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'name', 'articles')


class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'