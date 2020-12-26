import re
from Qinghuiyue.checkers.content_len_checker import check_content_len


def check_signup(content):
    api_id = content.get('api_id')

    if type(api_id) != str or len(re.match(r'[0-9]*', api_id).group()) != 10:
        return False, "api_id"
    name = content.get('name')
    ok, _ = check_content_len(name, 2, 10)
    if not ok:
        return False, 'name'
    pwd = content.get('pwd')
    if type(pwd) != str or len(pwd) > 20 or len(pwd) < 6:
        return False, 'pwd'
    if re.search(r'[0-9]', pwd) is None or re.search(r'[a-zA-Z]', pwd) is None:
        return False, 'pwd'

    return True, "ok"
