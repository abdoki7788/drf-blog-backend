import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from djoser.views import UserViewSet

# Create your views here.

class CustomUserViewSet(UserViewSet):
	@action(methods=['get'], detail=True)
	def follow(self, request, id):
		to_follow_user = self.get_object()
		follower_user = request.user
		to_follow_user.followers.add(follower_user)
		return Response('followed successfuly')

class UserActivationView(APIView):
	def get(self, request, uid, token):
		protocol = 'https://' if request.is_secure() else 'http://'
		web_url = protocol + request.get_host()
		post_url = web_url + "/api/auth/users/activation/"
		print(post_url)
		post_data = {'uid': uid, 'token': token}
		result = requests.post(post_url, data = post_data)
		return Response(data=result.content, status=result.status_code)