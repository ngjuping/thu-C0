import json
from django.http import HttpResponse, JsonResponse
from Qinghuiyue.feedback.models import Feedback
from Qinghuiyue.venues.models import *
from Qinghuiyue.models.models import *
from Qinghuiyue.utils import require

@require('get')
def get_venues_info(request):
    '''
    获取场馆信息
    :return:
    '''
    venue_id = request.GET['id']
    venue = Venue.objects(venue_id=venue_id).first()
    if venue == None:
        return JsonResponse({"message":"require correct venue id"},status=401)
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

@require('get')
def get_courts_info(request):
   '''
    获取某个场馆下所有场地的信息
    :return:
    '''
   try:
      venue_id = int(request.GET['id'])
      venue = Venue.objects(venue_id=venue_id).first()
      assert venue != None
      courts_id = venue.courts
   except:
      return JsonResponse({"message":"venue id required"}, status=400)

   courts = [Court.objects(id=i)[0] for i in courts_id]
   #print(courts)

   court_json = [{"id": i.court_id, "type": i.enum_id,"name":i.name,
               "status":[{"start":j['start'],"end":j['end'],"code":j['code']} for j in i.Status]
               } for i in courts]


   try:
      year = request.GET['year']
      for i in range(len(court_json)):
        times_filtered = [item for item in court_json[i]['status'] if str(item['start'].year) == str(year)]
        court_json[i]['status'] = times_filtered
   except:
      year = 0

   try:
      month = request.GET['month']
      for i in range(len(court_json)):
        times_filtered = [item for item in court_json[i]['status'] if str(item['start'].month) == str(month)]
        court_json[i]['status'] = times_filtered
   except:
      month = 0

   try:
      day = request.GET['day']
      for i in range(len(court_json)):
        times_filtered = [item for item in court_json[i]['status'] if str(item['start'].day) == str(day)]
        court_json[i]['status'] = times_filtered
   except:

      day = 0

   for i in range(len(court_json)):
        times_filtered = [item for item in court_json[i]['status'] if item['code'] > 0]
        court_json[i]['status'] = times_filtered

   return JsonResponse({
      "message": "ok",
      "requestedDate":[int(day),int(month),int(year)],
      "venue_name": venue.name,
      "courts": court_json
   })


@require('get')
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