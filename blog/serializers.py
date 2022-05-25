from rest_framework import serializers
from .models import Article, Tag, Comment
from users.serializers import AuthorSerializer

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'

class ArticleSerialize(serializers.ModelSerializer):
	full_short_link = serializers.CharField()
	hits = serializers.IntegerField(source='hits.count', read_only=True)
	tags = TagSerializer(many=True)
	author = AuthorSerializer()
	formatted_date = serializers.JSONField()
	class Meta:
		model = Article
		exclude = ('short_link', 'published')

class ArticleCreateSerializer(serializers.ModelSerializer):
	tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), slug_field='name', many=True, required=False)
	class Meta:
		model = Article
		fields = ('title', 'content', 'status', 'image', 'tags')
	
	def create(self, validated_data):
		validated_data['author'] = self.context['request'].user
		return super(ArticleCreateSerializer, self).create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
	author = AuthorSerializer(read_only=True)
	class Meta:
		model = Comment
		fields = ('id', 'content', 'author', 'article', 'parent', 'children', 'created', 'formatted_date')
		read_only_fields = ('id', 'author', 'article', 'children')
	def get_fields(self, *args, **kwargs):
		fields = super(CommentSerializer, self).get_fields(*args, **kwargs)
		fields['children'] = CommentSerializer(many=True, read_only=True)
		return fields