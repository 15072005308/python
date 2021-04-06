import json
import requests

# 1.获取access_token
#  请求方式 GET

class WxTools():
    def __init__(self,app_id,app_secret):
        self.app_id=app_id
        self.app_secret=app_secret


    def get_access_token(self):

        url=f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}'

        resp=requests.get(url).json()

        access_token=resp.get('access_token')

        return access_token

# 2.利用access_token发送微信的通知
#  http请求方式:
#  POST https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=ACCESS_TOKEN

    def send_wx_customer_msg(self,opend_id,msg='有人闯入了你的家'):

        url=f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={self.get_access_token()}'

        req_data={
            "touser":opend_id,
            "msgtype":"text",
            "text":
            {
                 "content":msg
            }
        }

        # 数据转换为 utf-8 编码
        # 通过 post 发送请求
        requests.post(url,data=json.dumps(req_data,ensure_ascii=False).encode('utf-8'))



if __name__ == '__main__':
    # 获取access_token
    app_id = 'wxea488ba870c85999'
    app_secret = '673f4c25703cd2a0dca15c39a323b775'

    # access_token=get_access_token(app_id,app_secret)
    #
    # # 发送请求
    # send_wx_customer_msg(access_token,'oimIq5vOv176R_VjfUvz4hn2SqtI','我是小偷，我闯入了你的家！')

    wx_tools=WxTools(app_id,app_secret)
    wx_tools.send_wx_customer_msg('oimIq5vOv176R_VjfUvz4hn2SqtI')