import re
def check_html_content(content,min=10,max=100):
    '''
    检查为html格式的内容数量是否符合要求
    '''
    if type(content)!=str:
        return False,"wrong type"
    format=r"<(.*?)>(.*?)</(.*?)>"
    pattern=re.compile(format)
    results=pattern.findall(content)
    total_len=0

    #验证标签是否一一对应，并且统计字符
    if len(results)==0:
        return False,"wrong html"
    for result in results:
        if result[0]!=result[2]:
            return False,"wrong html"
        total_len+=len(result[1])
    if total_len<min:
        return False,"too short"
    if total_len>max:
        return False,"too long"
    return True,"ok"
