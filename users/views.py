import requests
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class UserActivationView(APIView):
	def get(self, request, uid, token):
		protocol = 'https://' if request.is_secure() else 'http://'
		web_url = protocol + request.get_host()
		post_url = web_url + "/api/auth/users/activation/"
		print(post_url)
		post_data = {'uid': uid, 'token': token}
		result = requests.post(post_url, data = post_data)
		return Response(data=result.content, status=result.status_code)