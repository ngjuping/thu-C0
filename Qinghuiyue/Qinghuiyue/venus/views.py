from Qinghuiyue.feedback.models import Feedback
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
            "publish_date": feedback.time
        }
    else:
        review = {}

    notices_raw = Notification.objects(id__in=notices_id).order_by("-time")[:3]
    notices = []
    for notice in notices_raw:
        notices.append(
            {"title": notice.title, "content": notice.content, "time": notice.time})
    return JsonResponse({
        "message": "ok",
        "venue_info": {
            "id":venue.venue_id,
            "name": venue.name,
            "description": venue.intro,
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
   try:
      venue_id = request.GET['id']
      venue = Venue.objects(venue_id=venue_id).first()
      courts_id = venue.courts
   except:
      return JsonResponse({"message":"venue id required"}, status=400)

   courts = [Court.objects(_id=i)[0] for i in courts_id]
   #print(courts)
   court_json = [{"id": i.court_id, "type": i.enum_id,"price": i.price,
               "status":[j for j in i.Status]
               } for i in courts]

   try:
      year = request.GET['year']
      times_filtered = [item for item in court_json[0]['status'] if str(item['start'].year) == str(year)]
      court_json[0]['status'] = times_filtered
   except:
      pass

   try:
      month = request.GET['month']
      times_filtered = [item for item in court_json[0]['status'] if str(item['start'].month) == str(month)]
      court_json[0]['status'] = times_filtered
   except:
      pass

   try:
      day = request.GET['day']
      times_filtered = [item for item in court_json[0]['status'] if str(item['start'].day) == str(day)]
      court_json[0]['status'] = times_filtered
   except:
      pass


   return JsonResponse({
      "message": "ok",
      "venue_name": venue.name,
      "courts": court_json
   })


def get_venues_list(request):
    '''
        获取所有场馆的列表
        :param request:
        :return:
        '''
    venues = Venue.objects()
    venues_list = [{
        "id": venue.venue_id,
        "name": venue.name
    }
        for venue in venues]
    return JsonResponse({"message": "ok","venues":venues_list})
