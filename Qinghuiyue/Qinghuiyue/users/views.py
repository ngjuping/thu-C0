import json
from django.http import HttpResponse, JsonResponse
from Qinghuiyue.users.models import *
from Qinghuiyue.models.models import Stat
from Qinghuiyue.utils import require
from Qinghuiyue.checkers.signup_checker import check_signup


@require('post')
def signup(request):
    '''

    :param request:
    :return:

    目前可以根据注册人数自动增加id,但是还没有做重复的检查，工会id不能重复
    '''
    params = json.loads(request.body)
    ok,message=check_signup(params)
    if not ok:
        return JsonResponse({"message":message+"字段错误"},status=400)
    user=User.objects(api_id=params['api_id']).first()
    if user:
        return JsonResponse({"message": "该工号已经注册过啦！请进入登陆界面", "user_id": user.user_id},status=403)

    user = User.create(password=params['pwd'], user_id=Stat.add_object("user"), name=params['name'],
                       api_id=params['api_id'],privilege=0)
    return JsonResponse({"message": "ok", "user_id": user.user_id})


@require('post')
def login(request):
    params = json.loads(request.body)
    user = User.objects(api_id=params['api_id']).first()

    if user and user.authenticate(params['pwd']):
        request.session['user_id'] = user.user_id
        request.session['privilege']=user.privilege
        return JsonResponse(
            {"message": "ok", "user_info": {'user_id': user.user_id, 'name': user.name, 'privilege': user.privilege}})
    else:
        return JsonResponse({"message": "用户名或密码错误！"}, status=403)


@require('post')
def logout(request):
    request.session.delete()
    return JsonResponse({"message": "ok", "content": "logout success"})


@require('get')
def get_name_by_id(request):
    '''
    通过用户名获取id
    '''
    users_raw = User.objects(name__contains=request.GET['user_name'])
    users=[{
        "user_id":user.user_id,
        "api_id":user.api_id
    } for user in users_raw]
    return JsonResponse({"message":"ok","users":users})