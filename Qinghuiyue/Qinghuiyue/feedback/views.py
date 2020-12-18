from django.http import HttpResponse, JsonResponse
from Qinghuiyue.feedback.models import Feedback
from Qinghuiyue.users.models import User
from Qinghuiyue.venus.models import Court
import json
import datetime
def create_feedback(request):
    '''
    创建反馈，接受的是form-data
    目前图片处理尚未完成
    :param request:
    :return:
    '''
    params=request.POST
    img=request.FILES.get('img')

    ok,feedback_id=Feedback.create_feedback({"user_id":int(params['user_id']),
                                             "stars":int(params['stars']),"content":params["content"],"img":img,
                                             "reservation_id":int(params['reservation_id'])})

    if ok:
        return JsonResponse({"message":"ok","feedback_id":feedback_id})
    else:
        return JsonResponse({"message":feedback_id},status=500)

def get_all_feedback(request):
    '''
    获取所有反馈
    :param request:
    :return:
    '''
    page=int(request.GET['page'])
    size=int(request.GET['size'])

    feedbacks_all=Feedback.objects().order_by("-time")
    total=len(feedbacks_all)
    if page*size>total:
        feedbacks_page=feedbacks_all
    else:
        feedbacks_page=feedbacks_all[(page-1)*size:page*size]

    feedbacks=[
        {
            "feedback_id":feedback.feedback_id,
            "content":feedback.content,
            "publish_date":feedback.time,
            "court_id":Court.objects(id=feedback.court)[0].court_id,
            "img":feedback.img,
            "reply":feedback.reply,
            "solved":feedback.solved,
            "stars":feedback.stars,
            "user_id": feedback.user_id
        }for feedback in feedbacks_page
    ]
    return JsonResponse({"message":"ok","total":total,"feedbacks":feedbacks})
def get_user_feedbacks(request):
    '''
    获取单个用户的反馈
    :param request:
    :return:
    '''
    page=int(request.GET['page'])
    size=int(request.GET['size'])

    user_id=int(request.GET['user_id'])
    user=User.objects(user_id=user_id).first()
    feedbacks_all=Feedback.objects(id__in=user.feedback).order_by("-time")
    total = len(feedbacks_all)
    if page * size > total:
        feedbacks_page = feedbacks_all
    else:
        feedbacks_page = feedbacks_all[(page - 1) * size:page * size]
    feedbacks=[
        {
            "feedback_id":feedback.feedback_id,
            "content":feedback.content,
            "publish_date":feedback.time,
            "court_id":Court.objects(id=feedback.court)[0].court_id,
            "img":feedback.img,
            "reply":feedback.reply,
            "solved":feedback.solved,
            "stars":feedback.stars,
            "user_id":feedback.user_id
        }for feedback in feedbacks_page
    ]
    return JsonResponse({"message": "ok", "total": total, "feedbacks": feedbacks})

def update_feedback(request):
    #目前上传新的图片会更改图片的名字，但是原来的图片没有删除。删除反馈的图片时候也没有删除
    try:
        params = request.POST
        feedback=Feedback.objects(feedback_id=int(params['feedback_id'])).first()
        feedback.content=params['content']
        feedback.stars=int(params['stars'])
        img=request.FILES.get("img")
        if img:
            img_name="static/feedback/"+ str(feedback.feedback_id) + params['img'].name
            feedback.img = img_name
            feedback.save()
            with open(img_name, 'wb+') as img_file:
                for chunk in img:
                    img_file.write(chunk)
        feedback.time=datetime.datetime.now()
        feedback.save()
        return JsonResponse({"message":"ok"})
    except Exception:
        return JsonResponse({"message": "服务器内部错误"}, status=500)

def delete_feedback(request):
    params=json.loads(request.body)
    feedback=Feedback.objects(feedback_id=params['feedback_id']).first()
    user=User.objects(user_id=feedback.user_id).first()
    user.feedback.remove(feedback.id)
    user.save()
    feedback.delete()
    return JsonResponse({"message":"ok"})

def reply_feedback(request):
    '''
    管理员回复
    :param request:
    :return:
    '''
    params=json.loads(request.body)
    feedback=Feedback.objects(feedback_id=params['feedback_id']).first()
    feedback.reply=params['reply']
    feedback.solved=params['solved']
    feedback.save()

    return JsonResponse({"message":"ok"})
