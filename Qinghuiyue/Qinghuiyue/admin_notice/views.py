from Qinghuiyue.users.models import *
from Qinghuiyue.venus.models import *
from Qinghuiyue.models.models import *
from Qinghuiyue.models.models import Stat
from django.http import HttpResponse, JsonResponse
import json
import datetime
from dateutil.parser import parse
from pytz import tzinfo
from pytz import utc
from Qinghuiyue import settings


def create_notice(request):
    notice_id = 1
    while True:
        if Notification.objects(notice_id=notice_id).first() != None:
            notice_id += 1
        else:
            break
    params = json.loads(request.body)

    try:
        title = params['title']
        assert len(title) > 0
    except:
        return JsonResponse({"error": "requires correct title"}, status=401)
    try:
        content = params['content']
        assert len(content) > 0
    except:
        return JsonResponse({"error": "requires correct content"}, status=401)

    notice = Notification(
          title = title,
          content = content,
          notice_id = notice_id,
          time = datetime.datetime.now()
          ).save()

    return JsonResponse({"message": "ok", "notice_id": notice_id})

def delete_notice(request):
    params = json.loads(request.body)
    try:
        notice_id = params['notice_id']
        assert Notification.objects(notice_id=notice_id).first() != None
        Notification.objects(notice_id=notice_id).delete()
    except:
        return JsonResponse({"error": "requires correct notice id"}, status=401)

    return JsonResponse({"message": "ok"})

def update_notice(request):
    params = json.loads(request.body)
    try:
        notice_id = params['notice_id']
        notice = Notification.objects(notice_id=int(notice_id)).first()  # the court found with id in database
    except:
        return JsonResponse({"error": "notice id error"}, status=401)

    try:
        title = params['title']
        assert len(title) > 0
    except:
        return JsonResponse({"error": "requires correct title"}, status=401)
    try:
        content = params['content']
        assert len(content) > 0
    except:
        return JsonResponse({"error": "requires correct content"}, status=401)

    Notification.objects(notice_id=notice_id).update_one(set__title=title)
    Notification.objects(notice_id=notice_id).update_one(set__content=content)
    Notification.objects(notice_id=notice_id).update_one(set__time=datetime.datetime.now())

    return JsonResponse({"message": "ok"})