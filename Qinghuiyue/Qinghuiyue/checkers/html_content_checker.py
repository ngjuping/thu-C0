import re
def check_html_content(content,min=10,max=100):
    '''
    检查为html格式的内容数量是否符合要求
    '''
    if type(content)!=str:
        return False,"wrong type"
    format=r"<.*?>"
    pattern=re.compile(format)
    results=re.sub(pattern,"",content)
    total_len=len(results)

    if total_len<min:
        return False,"too short"
    if total_len>max:
        return False,"too long"
    return True,"ok"
