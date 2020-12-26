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

def create_course(request):
    course_id = Stat.add_object("course")
    params = json.loads(request.body)

    try:
        name = params['name']
        assert check_content_len(name,min=3,max=10) == (True,"ok")
    except:
        return JsonResponse({"message": "requires correct course name"}, status=401)
    try:
        price = params['price']
        assert len(price) > 0
    except:
        return JsonResponse({"message": "requires correct price"}, status=401)
    try:
        tel = params['tel']
        assert check_content_len(tel,min=3,max=20) == (True,"ok")
    except:
        return JsonResponse({"message": "requires correct telephone"}, status=401)
    try:
        intro = params['intro']
        assert check_content_len(intro,min=3,max=100) == (True,"ok")
    except:
        return JsonResponse({"message": "requires correct introduction"}, status=401)

    course = Course(
          course_id = course_id,
          name = name,
          price = price,
          tel = tel,
          intro = intro
          ).save()

    return JsonResponse({"message": "ok", "course_id": course_id})



def update_course(request):
    params = json.loads(request.body)

    try:
        course_id= params['course_id']
        course = Course.objects(course_id=course_id).first()
        assert course != None
    except:
        return JsonResponse({"message": "requires correct course id"}, status=401)

    try:
        name = params['name']
        if name != None:
            try:
                assert check_content_len(name,min=3,max=10) == (True,"ok")
            except:
                return JsonResponse({"message": "requires correct course name"}, status=401)
            Course.objects(course_id=course_id).update_one(set__name=name)
    except:
        pass

    try:
        price = params['price']
        if price != None:
            try:
                assert len(price) > 0
            except:
                return JsonResponse({"message": "requires correct price"}, status=401)
            Course.objects(course_id=course_id).update_one(set__price=price)
    except:
        pass

    try:
        intro = params['intro']
        if intro != None:
            try:
                assert check_content_len(intro,min=3,max=100) == (True,"ok")
            except:
                return JsonResponse({"message": "requires correct introduction"}, status=401)
            Course.objects(course_id=course_id).update_one(set__intro=intro)
    except:
        pass

    try:
        tel = params['tel']
        if tel != None:
            try:
                assert check_content_len(tel,min=3,max=20) == (True,"ok")
            except:
                return JsonResponse({"message": "requires correct telephone"}, status=401)
            Course.objects(course_id=course_id).update_one(set__tel=tel)
    except:
        pass

    return JsonResponse({
        "message": "ok"
    })

def delete_course(request):
    params = json.loads(request.body)

    try:
        course_id= params['course_id']
        assert Course.objects(course_id=course_id).first() != None
        Course.objects(course_id=course_id).delete()
    except:
        return JsonResponse({"message": "requires correct course id"}, status=401)

    return JsonResponse({
        "message": "ok"
    })


def get_course(request):
    try:
        page = int(request.GET.get('page'))
        size = int(request.GET.get('size'))
        assert page > 0
        assert size > 0
    except:
        return JsonResponse({"message": "requires correct page and size"}, status=401)

    course = Course.objects().all()  # all courses in db
    total = len(course)
    begin = size * (page - 1)   # included
    end = size * page           # not included
    courses = [{"id":iter['course_id'], "name":iter['name'], "price":iter['price'],"intro":iter['intro'],"tel":iter['tel']}
                for iter in course[begin:end]]

    return JsonResponse({"message": "ok", "total":total, "courses": courses})


