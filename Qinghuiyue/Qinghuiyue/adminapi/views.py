from Qinghuiyue.users.models import *
from Qinghuiyue.venus.models import *
from Qinghuiyue.models.models import Stat
from django.http import HttpResponse, JsonResponse
import json
import datetime
from dateutil.parser import parse
from pytz import tzinfo
from pytz import utc
from Qinghuiyue import settings



def modify_court(request):

    params = json.loads(request.body)
    courts = params['court'] # court_id

    for court in courts:     # In POST params
        try:
            this_court = Court.objects(court_id=court['id']).first()  # the court found with id in database
        except:
            return JsonResponse({"message":"court id error"}, status=401)

        this_court.enum_id = court['type']
        for status in court['status']:  # iterate status in each court in POST params
            flag = False                # have matching starttime and endtime
            for i,status_db in enumerate(this_court.Status): # look for the matching status in database
                if(parse(status['start']) == status_db['start'].replace(tzinfo=utc)
                and parse(status['end']) == status_db['end'].replace(tzinfo=utc)):
                    this_court.Status[i]['code'] = status['code']
                    Court.objects(court_id=court['id']).update_one(set__Status=this_court.Status)
                    flag = True
            if not flag:
                return JsonResponse({"error": "start time or end time not matched"}, status=401)

    return JsonResponse({
        "message": "ok"
    })

def modify_venue(request):
    try:
        venue_id = request.POST.get('venue_id')  # type(venue_id) is str
        this_venue = Venue.objects(venue_id=int(venue_id)).first()  # the court found with id in database
    except:
        return JsonResponse({"message": "venue id error"}, status=401)
    try:
        name = request.POST.get('name')
        Venue.objects(venue_id=venue_id).update_one(set__name=name)
    except:
        pass
    try:
        description = request.POST.get('description')
        Venue.objects(venue_id=venue_id).update_one(set__intro=description)
    except:
        pass
    try:
        img = request.FILES.get('img')
        #print(type(img))
        print(img.size)
        if img.size < 128 or img.size > 2048**2:
            return JsonResponse({"error": "image size invalid"}, status=401)
        Venue.objects(venue_id=venue_id).update_one(set__image=img.name)
        try:
            with open(settings.STATIC_URL + img.name, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
        except:
            return JsonResponse({"error": "save image failed"}, status=500)

    except:
        pass
    return JsonResponse({
        "message": "ok"
    })


