from Qinghuiyue.users.models import *
from Qinghuiyue.venus.models import *
from Qinghuiyue.models.models import Stat
from Qinghuiyue.reservation.models import *
from django.http import HttpResponse, JsonResponse
import json
import datetime
from dateutil.parser import parse
from pytz import tzinfo
from pytz import utc
from Qinghuiyue import settings
import pandas as pd
import zipfile
import os

def create_venue(request):
    venue_id = 1
    while True:
        if Venue.objects(venue_id=venue_id).first() != None:
            venue_id += 1
        else:
            break
    try:
        name = request.POST.get('name')
        assert type(name) == str
    except:
        return JsonResponse({"error": "require venue name"}, status=401)
    try:
        description = request.POST.get('description')
        assert type(name) == str
    except:
        return JsonResponse({"error": "require venue description"}, status=401)
    try:
        img = request.FILES.get('img')
        assert img.name.endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))
        if img.size < 128 or img.size > 2048 ** 2:
            return JsonResponse({"error": "image size invalid"}, status=401)

        try:
            img_format = img.name.split('.')[-1]
            img_name = 'venue_' + str(venue_id) + '_img.' + img_format
            Venue.objects(venue_id=venue_id).update_one(set__image='static/venue/' + img_name)
            if not os.path.exists('static/venue/'):
                os.mkdir('static/venue')
            with open('static/venue/' + img_name, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
        except:
            return JsonResponse({"error": "save image failed"}, status=500)

    except:
        return JsonResponse({"error": "image format illegal"}, status=401)

    Venue(name=name,
        intro=description,
        courts=[],
        image='static/venue/' + img_name,
        venue_id=venue_id,
        notices=[]).save()

    return JsonResponse({
        "message": "ok",
        "venue_id": venue_id
    })

def create_court(request):

    params = json.loads(request.body)
    court_id = 1
    while True:
        if Court.objects(court_id=court_id).first() != None:
            court_id += 1
        else:
            break
    try:
        venue_id = params['venue_id']
        this_venue = Venue.objects(venue_id=int(venue_id)).first()  # the venue found with id in database
        courts_ls = this_venue.courts
    except:
        return JsonResponse({"message": "venue id error"}, status=401)
    try:
        name = params['name']
    except:
        return JsonResponse({"message": "requires court name"}, status=401)
    try:
        price = params['price']
        assert price>0
    except:
        return JsonResponse({"message": "requires a integer price"}, status=401)
    try:
        type = params['type']
        # assert type(type) == int
        assert 0 <= type <= 5     # 需要改
    except:
        return JsonResponse({"message": "venue sport type error"}, status=401)
    try:
        param_status = params['status'] # from parameters
        all_status = []
        for status in param_status:  # iterate status in each court in POST params
            new_status = {
                "start":parse(status['start']),
                "end":parse(status['end']),
                "code":status['code']
            }
            all_status.append(new_status)
    except:
        return JsonResponse({"message": "status error"}, status=401)

    new_court = Court(name=name,
          enum_id = type,
          venue = this_venue.id,
          rent_queue = [],
          draw_list = [],
          rent_for_long = [],
          Status = all_status,
          status = '开放',
          court_id = court_id,
          price = price
          ).save()

    courts_ls.append(new_court.id)
    Venue.objects(venue_id=venue_id).update_one(set__courts=courts_ls)
    return JsonResponse({"message": "ok"})

def update_court(request):

    params = json.loads(request.body)
    courts = params['court'] # court_id

    for court in courts:     # In POST params
        try:
            this_court = Court.objects(court_id=court['id']).first()  # the court found with id in database
        except:
            return JsonResponse({"message":"court id error"}, status=401)

        try:
            this_court.enum_id = court['type']
        except:
            pass
        try:
            this_court.price = court['price']
        except:
            pass
        for status in court['status']:  # iterate status in each court in POST params
            flag = False                # have matching starttime and endtime
            for i,status_db in enumerate(this_court.Status): # look for the matching status in database
                if(parse(status['start']) == status_db['start'].replace(tzinfo=utc)
                and parse(status['end']) == status_db['end'].replace(tzinfo=utc)):
                    this_court.Status[i]['code'] = status['code']
                    Court.objects(court_id=court['id']).update_one(set__Status=this_court.Status)
                    flag = True
            if not flag:
                return JsonResponse({"message": "start time or end time not matched"}, status=401)

    return JsonResponse({
        "message": "ok"
    })

def update_venue(request):
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
        #print(img.size)
        if img.size < 128 or img.size > 2048**2:
            return JsonResponse({"message": "image size invalid"}, status=401)
        
        img_format = img.name.split('.')[1]
        img_name = 'venue_' + str(venue_id) + '_img.' + img_format
        Venue.objects(venue_id=venue_id).update_one(set__image='static/venue/' + img_name)
        try:
            with open('static/venue/'  + img_name, 'wb+') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
        except:
            return JsonResponse({"message": "save image failed"}, status=500)

    except:
        pass
    return JsonResponse({
        "message": "ok"
    })

def delete_venue(request):

    params = json.loads(request.body)
    try:
        venue_id = params['venue_id']
        this_venue = Venue.objects(venue_id=venue_id).first()
        assert this_venue != None
    except:
        return JsonResponse({
            "message": "venue id error"
        }, status=401)

    for court in this_venue.courts:
        this_court = Court.objects(id=court).first()
        if this_court != None:
            Court.objects(id=court).delete()

    Venue.objects(venue_id=venue_id).delete()

    return JsonResponse({
        "message": "ok"
    })


def delete_court(request):

    params = json.loads(request.body)
    try:
        court_id = params['court_id']
        this_court = Court.objects(court_id=court_id).first()
        assert this_court != None
    except:
        return JsonResponse({
            "message": "court id error"
        }, status=401)
    try:
        this_venue = Venue.objects(id=this_court.venue).first()
        this_venue.courts.remove(this_court.id)
        this_venue.save()
    except:
        pass

    Court.objects(court_id=court_id).delete()
    return JsonResponse({
        "message": "ok"
    })

def list_court(request):
    courts = Court.objects().all()
    total = len(courts)
    courts_ret = []

    try:
        page = int(request.GET['page'])
        size = int(request.GET['size'])
    except:
        return JsonResponse({
            "message": "require page and size"
        })
    begin = size * (page - 1)   # included
    end = size * page           # not included
    courts = courts[begin:end]

    for court in courts:
        court_ret = {
            "id":court.court_id,
            "name":court.name,
            "type":court.enum_id,
            "venue":Venue.objects(id=court.venue).first().name
        }
        courts_ret.append(court_ret)
    return JsonResponse({
        "message": "ok",
        "total": total,
        "courts": courts_ret
    })

def make_schedule(request):
    '''
    学期场地预定，接受
    {
    price: 15,
    court_id:1,
    matrix:[
    [1,2,3,1,2,2,3],
    [1,2,3,1,2,2,3],
    ...
    ]#大小7*15，15代表十五个时间段，7-8,8-9...21-22
    }
    '''
    if request.session.get('privilege')!=1:
        return JsonResponse({"message":"你没有权限"},status=401)
    params=json.loads(request.body)
    court=Court.objects(court_id=params['court_id']).first()
    if not court:
        return JsonResponse({"message":"该场地不存在"},status=501)
    court.price=params['price']
    court.matrix=params['matrix']
    court.save()
    court.set_schedule()
    return JsonResponse({"message":"ok"})

def generate_csv(request):

    path = "static/reservation"
    if not os.path.exists(path):
        os.mkdir(path)

    # find next monday
    today = datetime.date.today()
    #today -= datetime.timedelta(days = 1) * 26 # set 11.26 for test

    while today.weekday() != 0: # stand for Monday
        today += datetime.timedelta(days = 1)
    next_monday = today
    date = next_monday
    # print(date)
    file_list = [] # all files generated this time

    venues = Venue.objects().all()

    for venue in venues:
        date = next_monday
        for _ in range(7): # loop for days in next week
            df = pd.DataFrame(columns = ['venue', 'court','date','7:00-8:00','8:00-9:00','9:00-10:00','10:00-11:00',
                                     '11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00','15:00-16:00','16:00-17:00',
                                     '17:00-18:00','18:00-19:00','19:00-20:00','20:00-21:00'])
            # set courts (line)
            courts = []

            for court__id in venue.courts:
                court = Court.objects(id=court__id).first()
                courts.append(court)
            for court in courts:
                df.loc[court.id]=[venue.name, court.name, str(date) ,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0]

            # add reservations
            reservations = Reservation.objects().all()
            for reserv in reservations:
                if (reserv.details['start'].month == date.month and
                    reserv.details['start'].day == date.day and
                    Court.objects(id=reserv.details['court']).first() in courts):
                    # check the status of the reservation:
                    if reserv.status == 1:
                        status = '[未付款]'
                    elif reserv.status == 2:
                        status = ''
                    else:
                        continue
                    court = Court.objects(id=reserv.details['court']).first()

                    # make the time form in the charm header
                    str_time = str(reserv.details['start'].hour) + ':00-' + str(reserv.details['end'].hour) + ':00'
                    user = User.objects(user_id=reserv.details['user_id']).first()

                    # set the string to fill in this pos of the chart
                    str_in_blank = ''
                    str_in_blank += user.name
                    str_in_blank += status
                    df.loc[court.id,str_time]=str_in_blank

            # print('-----------' + venue.name + '------------' + str(date) + '------------')
            # print(df)
            file_name = 'static/reservation/' + venue.name + '_' + str(date) +'data.csv'
            try:
                df.to_csv(file_name,encoding='utf_8_sig',index=False)
            except:
                return JsonResponse({"message":"save image error, save path not exists"}, status=500)
            file_list.append(file_name)

            date += datetime.timedelta(days = 1)

    zip_path = 'static/reservation/' + str(next_monday) + '.zip'
    zip_file = zipfile.ZipFile(zip_path,'w')
    for file in file_list:
        zip_file.write(file)
    zip_file.close()

    return JsonResponse({"message":"ok", "path": zip_path})