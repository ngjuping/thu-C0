# 清会约API设计



| URL                              | 类型 | 参数                                 | 返回值                                                       | 解释                        |
| -------------------------------- | ---- | ------------------------------------ | ------------------------------------------------------------ | --------------------------- |
| /api/login                       | POST | JSON格式，id(str),pwd(str)           | JSON格式，正确{"message":"ok", user_id:<user_id>}，错误返回{"message":"<details>"} | 登陆                        |
| /api/signup                      | POST | JSON格式，id(str),pwd(str),name(str) | JSON格式，正确{"message":"ok", user_id:<user_id>}，错误返回{"message":"<details>"}, details 包括错误的地方 | 注册                        |
| /login                           | GET  |                                      | HTML页                                                       | 登录页                      |
| /signup                          | GET  |                                      | HTML页                                                       | 注册页                      |
| /api/main/notice                 | GET  |                                      | JSON格式，{"message":"ok",<br/>"notice": 前三个通知(标题，内容)} | 获取最新三个主页通知        |
| /main                            | GET  |                                      | HTML页                                                       | 主页                        |
| /api/main/venues?id=X            | GET  | 场馆id                               | JSON格式，{“message":"ok",<br/>"venue_info":{<br/>"notice":[通知1 (标题，内容) ,通知2]},<br/>"name":<name>,<br/>"description":<description>,<br/>"img":"url",<br/>"review":最新反馈 (内容，打星，相对时间) )}<br/>} | 获取场馆详情，url query格式 |
| /api/booking?id=X &day=Y&month=Z | GET  | 场馆id, 日期                         | JSON格式，{“message":"ok", <br/>"venue_name":<venue_name>,<br/>courts":[场地1 (名字，类型，[给定日期1st时间段的状态 (具体时间段，状态号)，2nd时间段的状态])，场地2，... ]<br/>} | 获取场馆下所有场地信息      |
| /booking                         | GET  |                                      | HTML页                                                       | 预定页                      |
|                                  |      |                                      |                                                              |                             |

*Error codes