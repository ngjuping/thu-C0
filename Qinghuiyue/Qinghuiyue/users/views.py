from Qinghuiyue.users.models import *
from Qinghuiyue.models.models import Stat
from django.http import HttpResponse, JsonResponse
import json

#@require('post')
def signup(request):
    '''

    :param request:
    :return:

    目前可以根据注册人数自动增加id,但是还没有做重复的检查，工会id不能重复
    '''
    params = json.loads(request.body)
    stat=Stat.objects(name="size_of_collection")[0]

    user = User.create(password=params['pwd'],user_id=stat.data['user']+1,name=params['name'],api_id=params['user_id'])
    stat.data['user']+=1
    stat.save()
    return JsonResponse({"message":"ok","user_id":user.user_id})


#@require('post')
def login(request):
    print(request.body)
    params = json.loads(request.body)

    #print(params)
    user = User.objects(api_id=params['user_id']).first()

    if user and user.authenticate(params['pwd']):
        request.session['user_id']=user.id
        return JsonResponse({"message":"ok","user_info":{'user_id': user.api_id,'name':user.name}})
    else:
        return JsonResponse({"message": "用户名或密码错误！"},status=400)




#@require('post')

def logout(request):
    #print(request.session['user_id'])
    request.session.delete()
    return JsonResponse({"message":"ok","content":"logout success"})
