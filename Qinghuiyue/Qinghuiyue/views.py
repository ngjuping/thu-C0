from django.http import HttpResponse, JsonResponse

from Qinghuiyue.models import *
from Qinghuiyue.models.models import *
from Qinghuiyue.models.models import Stat
import json
from django.core import serializers


def get_notices(request):
	'''
    首页获取前三个通知
    :return:
    '''
	try:
		notices_raw = Notification.objects().order_by("-time")[:3]  # 排序且只取前三个
		notices = []
		for notice in notices_raw:
			notices.append({"title": notice.title, "content": notice.content, "time": notice.time})
		return JsonResponse({
			"message": "ok",
			"notices": notices
		})
	except Exception:
		return HttpResponse(status=400)

