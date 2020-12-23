from Qinghuiyue.venus.models import Court
from datetime import datetime
def set_court_next_week():
    print("执行设置场地 ",datetime.now())
    courts=Court.objects()
    for court in courts:
        court.set_future_court(1)
def start_draw():
    print("执行抽签 ",datetime.now())
    courts=Court.objects()
    for court in courts:
        court.draw()

