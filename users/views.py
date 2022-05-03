import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin
from djoser.views import UserViewSet
from .serializers import AuthorSerializer, CustomUserSerializer
from blog.permissions import EveryOne
from .models import CustomUser as User
from djoser import email

# Create your views here.

class ActivationEmail(email.ActivationEmail):
    template_name = 'email/activations.html'

class CustomUserViewSet(UserViewSet):
	@action(methods=['get'], detail=True, permission_classes=[EveryOne])
	def followings(self, request, id):
		obj = self.get_object()
		res = CustomUserSerializer(obj.followings.all(), many=True)
		return Response(res.data)

	@action(methods=['get'], detail=True, permission_classes=[EveryOne])
	def followers(self, request, id):
		obj = self.get_object()
		res = CustomUserSerializer(obj.followers.all(), many=True)
		return Response(res.data)

	@action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
	def follow(self, request, id):
		to_follow_user = self.get_object()
		follower_user = request.user
		to_follow_user.followers.add(follower_user)
		return self.followers(request=request, id=id)
	
	@action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
	def unfollow(self, request, id):
		to_unfollow_user = self.get_object()
		unfollower_user = request.user
		to_unfollow_user.followers.remove(unfollower_user)
		return self.followers(request=request, id=id)


class UserActivationView(APIView):
	def get(self, request, uid, token):
		protocol = 'https://' if request.is_secure() else 'http://'
		web_url = protocol + request.get_host()
		post_url = web_url + "/api/auth/users/activation/"
		print(post_url)
		post_data = {'uid': uid, 'token': token}
		result = requests.post(post_url, data = post_data)
		return Response(data=result.content, status=result.status_code)





class AuthorView(RetrieveAPIView):
	queryset = User.objects.filter(is_active=True)
	serializer_class = AuthorSerializer
	lookup_field = 'username'