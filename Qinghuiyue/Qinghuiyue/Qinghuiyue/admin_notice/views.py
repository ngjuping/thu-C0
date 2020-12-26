from Qinghuiyue.users.models import *
from Qinghuiyue.venues.models import *
from Qinghuiyue.models.models import *
from Qinghuiyue.models.models import Stat
from django.http import HttpResponse, JsonResponse
import json
import datetime
from dateutil.parser import parse
from pytz import tzinfo
from pytz import utc
from Qinghuiyue import settings
from Qinghuiyue.checkers.content_len_checker import *
from Qinghuiyue.utils import require

@require('post',privilege=1)
def create_notice(request):
    notice_id = Stat.add_object("notification")
    params = json.loads(request.body)

    try:
        title = params['title']
        assert check_content_len(title,min=3,max=10) == (True,"ok")
    except:
        return JsonResponse({"error": "requires correct title"}, status=401)
    try:
        content = params['content']
        assert check_content_len(content,min=3,max=100) == (True,"ok")
    except:
        return JsonResponse({"error": "requires correct content"}, status=401)

    notice = Notification(
          title = title,
          content = content,
          notice_id = notice_id,
          time = datetime.datetime.now()
          ).save()

    return JsonResponse({"message": "ok", "notice_id": notice_id})

@require('post',privilege=1)
def delete_notice(request):
    params = json.loads(request.body)
    try:
        notice_id = params['notice_id']
        assert Notification.objects(notice_id=notice_id).first() != None
        Notification.objects(notice_id=notice_id).delete()
    except:
        return JsonResponse({"message": "requires correct notice id"}, status=401)

    return JsonResponse({"message": "ok"})

@require('post',privilege=1)
def update_notice(request):
    params = json.loads(request.body)
    try:
        notice_id = params['notice_id']
        notice = Notification.objects(notice_id=int(notice_id)).first()  # the court found with id in database
    except:
        return JsonResponse({"message": "notice id error"}, status=401)

    try:
        title = params['title']
        assert check_content_len(title,min=3,max=10) == (True,"ok")
    except:
        return JsonResponse({"message": "requires correct title"}, status=401)
    try:
        content = params['content']
        assert check_content_len(content,min=3,max=100) == (True,"ok")
    except:
        return JsonResponse({"message": "requires correct content"}, status=401)

    Notification.objects(notice_id=notice_id).update_one(set__title=title)
    Notification.objects(notice_id=notice_id).update_one(set__content=content)
    Notification.objects(notice_id=notice_id).update_one(set__time=datetime.datetime.now())

    return JsonResponse({"message": "ok"})

@require('get',privilege=1)
def get_notice(request):
    try:
        page = int(request.GET.get('page'))
        size = int(request.GET.get('size'))
        assert page > 0
        assert size > 0
    except:
        return JsonResponse({"message": "requires correct page and size"}, status=401)

    notice = Notification.objects().order_by("-time")  # all notices in db
    total = len(notice)
    begin = size * (page - 1)   # included
    end = size * page           # not included
    notices = [{"id":iter['notice_id'], "title":iter['title'], "content":iter['content']} for iter in notice[begin:end]]

    return JsonResponse({"message": "ok", "total":total, "notices": notices})