from Qinghuiyue.venus.models import Court
def set_court_next_week():
    courts=Court.objects()
    for court in courts:
        court.set_schedule()
def start_draw():
    courts=Court.objects()
    for court in courts:
        court.draw()
