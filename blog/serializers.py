from rest_framework import serializers
from .models import Article, Tag, Comment
from users.serializers import ArticleAuthorSerializer

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'

class ArticleSerialize(serializers.ModelSerializer):
	full_short_link = serializers.CharField()
	hits = serializers.IntegerField(source='hits.count', read_only=True)
	like = serializers.IntegerField(source='like.count', read_only=True)
	saves = serializers.IntegerField(source='saves.count', read_only=True)
	readtime = serializers.IntegerField(read_only=True)
	tags = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
	author = ArticleAuthorSerializer()
	class Meta:
		model = Article
		exclude = ('short_link', )

class ArticleCreateSerializer(serializers.ModelSerializer):
	tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), slug_field='name', many=True, required=False)
	class Meta:
		model = Article
		fields = ('title', 'content', 'status', 'image', 'tags', 'slug')
		read_only_fields = ('slug',)
	
	def create(self, validated_data):
		validated_data['author'] = self.context['request'].user
		return super(ArticleCreateSerializer, self).create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
	author = ArticleAuthorSerializer(read_only=True)
	children = serializers.SerializerMethodField()
	class Meta:
		model = Comment
		fields = ('id', 'content', 'author', 'article', 'parent', 'children', 'created')
		read_only_fields = ('id', 'author', 'article', 'children', 'created')
	
	def get_children(self, obj):
		return CommentSerializer(obj.children.all(), many=True).data