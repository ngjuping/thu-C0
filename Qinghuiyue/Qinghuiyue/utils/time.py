import datetime
def str2datetime(str):
    date=datetime.datetime.strptime(str,"%Y-%m-%dT%H:%M:%S")
    return date