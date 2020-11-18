from Qinghuiyue.venus.models import *
from Qinghuiyue.models.models import *
from django.http import HttpResponse, JsonResponse
import json


def get_venues_info(request):
	'''
    获取场馆信息
    :return:
    '''
	venue_id = request.GET['id']
	venue = Venue.objects(venue_id=venue_id).first()
	courts = venue.courts
	notices_id = venue.notices
	feedbacks = Feedback.objects(court__in=courts).order_by("-time")
	if len(feedbacks):
		feedback = feedbacks[0]
		review = {
			"content": feedback.content,
			"stars": feedback.stars,
			"time": feedback.time
		}
	else:
		review = {}

	notices_raw = Notification.objects(id__in=notices_id).order_by("-time")[:3]
	notices = []
	for notice in notices_raw:
		notices.append({"title": notice.title, "content": notice.content, "time": notice.time})
	return JsonResponse({
		"message": "ok",
		"venue_info": {
			"name": venue.name,
			"intro": venue.intro,
			"img": venue.image,
			"review": review,
			"notices": notices
		}
	})


def get_courts_info(request):
   '''
    获取某个场馆下所有场地的信息
    :return:
    '''
   venue_id = request.GET['id']
   venue = Venue.objects(venue_id=venue_id).first()
   courts_id = venue.courts
   courts = [Court.objects(_id=i)[0] for i in courts_id]
   court_json = [{"name": i.name, "enum_id": i.enum_id,
               "times":[j for j in i.Status]
               } for i in courts]

   return JsonResponse({
      "message": "ok",
      "venue_name": venue.name,
      "courts": court_json
   })