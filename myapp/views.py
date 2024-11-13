import json
import jwt
import datetime
from django.http import HttpResponse, JsonResponse
# from.models import MyModel
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['email']
        password = data['password']


        # user_id = User.objects.create_user(username=username, password=password)
        user_id = 0


        # token = jwt.encode({
        #     'username': username,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
        # }, 'your_secret_key')

        return JsonResponse({'id': user_id, 'email': username})
    return HttpResponse('请使用 POST 方法请求')


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['email']
        password = data['password']


        # user_id = User.objects.create_user(username=username, password=password)
        user_id = 0


        token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
        }, 'your_secret_key')

        return JsonResponse({'access_token': token, 'refresh_token': 120})
    return HttpResponse('请使用 POST 方法请求')


def user_info(request):
    token = request.META.get('HTTP_AUTHORIZATION', '')[7:]
    if token:
        try:
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            username = payload['username']
            if username == 'test@test.com':
                return JsonResponse({'id': 0, 'email': username})
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Invalid token'}, status=401)
    else:
        return JsonResponse({'message': 'No token provided'}, status=400)