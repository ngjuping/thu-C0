def check_content_len(content,min=3,max=10):
    if type(content)!=str:
        return False,"wrong type"
    if len(content)<min:
        return False,"too short"
    if len(content)>max:
        return False,"too long"


    return True,"ok"