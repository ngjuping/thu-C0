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


def create_course(request):
    course_id = 1
    while True:
        if Course.objects(course_id=course_id).first() != None:
            course_id += 1
        else:
            break
    params = json.loads(request.body)

    try:
        name = params['name']
        assert len(name) > 0
    except:
        return JsonResponse({"error": "requires correct course name"}, status=401)
    try:
        price = params['price']
        assert len(price) > 0
    except:
        return JsonResponse({"error": "requires correct price"}, status=401)

    course = Course(
          course_id = course_id,
          name = name,
          price = price,
          ).save()

    return JsonResponse({"message": "ok", "course_id": course_id})



def update_course(request):
    params = json.loads(request.body)

    try:
        course_id= params['course_id']
        course = Course.objects(course_id=course_id).first()
        assert course != None
    except:
        return JsonResponse({"error": "requires correct course id"}, status=401)

    try:
        name = params['name']
        try:
            assert len(name) > 0
        except:
            return JsonResponse({"error": "requires correct course name"}, status=401)
        Course.objects(course_id=course_id).update_one(set__name=name)
    except:
        pass

    try:
        price = params['price']
        try:
            assert len(price) > 0
        except:
            return JsonResponse({"error": "requires correct price"}, status=401)
        Course.objects(course_id=course_id).update_one(set__price=price)
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
        return JsonResponse({"error": "requires correct course id"}, status=401)

    return JsonResponse({
        "message": "ok"
    })



