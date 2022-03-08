from rest_framework import serializers
from .models import Article, Tag

class ArticleSerialize(serializers.ModelSerializer):
	hits = serializers.IntegerField(source='hits.count', read_only=True)
	class Meta:
		model = Article
		fields = '__all__'



class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'