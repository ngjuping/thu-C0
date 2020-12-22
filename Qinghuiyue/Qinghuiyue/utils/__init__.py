from functools import wraps
import json
from django.http import HttpResponse,JsonResponse
def require(method,online=False,privilege=0,check_id=False):
    '''
    检测请求方式是否符合要求。online表示是否要求用户在线（登陆状态）
    privilege要求用户为管理员
    check_id会检查request传来的user_id是否和session中一致,
    要求check_id或pricilege自动要求online
    '''
    if check_id or privilege:
        online=True
    def decorator(func):
        @wraps(func)
        def wrapper(request,*args,**kwargs):
            if request.method.upper()!=method.upper():
                return HttpResponse(status=400)
            if online:
                user_id=request.session.get('user_id')
                if not user_id:
                    return JsonResponse({"message":"请登陆之后再进行操作！"},status=403)
                if check_id and user_id!=json.loads(request.body)['user_id']:
                    return JsonResponse({"message":"用户验证错误，请尝试重新登陆"},status=403)

            if privilege:
                user_privilege=request.session.get('privilege')
                if not user_privilege:
                    return JsonResponse({"message":"您无管理员权限"},status=403)

            return func(request,*args,**kwargs)

        return wrapper
    return decorator
