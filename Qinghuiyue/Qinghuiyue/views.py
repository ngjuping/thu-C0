from django.http import HttpResponse, JsonResponse

from Qinghuiyue.models import *
from Qinghuiyue.models.models import User


#@require('post')
def signup(request):
    params = request.params
    user = User.create(**{
        'password': params['password']
    })
    return JsonResponse({'id': user.id})


#@require('post')
def login(request):
    params = request.params
    user = User.objects.first()
    if user and user.authenticate(params['password']):
        request.session['user_id'] = user.id
        return JsonResponse(user.todict())
    return HttpResponse(status=400)


#@require('post')
def logout(request):
    request.session.delete()
    return JsonResponse({})
