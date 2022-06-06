from rest_framework import serializers
from .models import Article


class ArticleSerializerForAuthor(serializers.ModelSerializer):
	full_short_link = serializers.CharField()
	hits = serializers.IntegerField(source='hits.count', read_only=True)
	like = serializers.IntegerField(source='like.count', read_only=True)
	saves = serializers.IntegerField(source='saves.count', read_only=True)
	tags = serializers.StringRelatedField(many=True)

	class Meta:
		model = Article
		exclude = ('short_link', 'author')