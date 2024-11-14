import json
import jwt
import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
from .models import User


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['email']
        password = data['password']

        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'user exist'}, status=401)

        user = User(username=username, password=password)
        user.save()

        return JsonResponse({'id': user.id, 'email': username})

    return HttpResponse('请使用 POST 方法请求')


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['email']
        password = data['password']

        user = User.objects.filter(username=username, password=password)
        if user:
            token = jwt.encode({
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
            }, 'your_secret_key')

            return JsonResponse({'access_token': token, 'refresh_token': 120})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)

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