# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 13:18:58 2018

@author: Lenovo
"""

# -*- coding: utf-8 -*-

import requests
import urllib
import random
from datetime import datetime
import sys
print(sys.getdefaultencoding())

# python2 和 python3的兼容代码
try:
    # python2 中
    import cookielib

    print(f"user cookielib in python2.")
except:
    # python3 中
    import http.cookiejar as cookielib

    print(f"user cookielib in python3.")

# session代表某一次连接
huihuSession = requests.session()
# 因为原始的session.cookies 没有save()方法，所以需要用到cookielib中的方法LWPCookieJar，这个类实例化的cookie对象，就可以直接调用save方法。
huihuSession.cookies = cookielib.LWPCookieJar(filename="huihuCookies.txt")

userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
header = {
    # "origin": "https://passport.huihu.cn",
    "Referer": "http://portal.zts.com.cn/cas/login?service=http%3A%2F%2Fportal.zts.com.cn%3A80%2Fportal_back%2Fapp%2Fuser%2Fv1%2FuserLogin",
    'User-Agent': userAgent,
}


def huihuLogin(account, password):
    #
    print("开始模拟登录蜂巢")

    postUrl = "http://portal.zts.com.cn/cas/login?service=http%3A%2F%2Fportal.zts.com.cn%3A80%2Fportal_back%2Fapp%2Fuser%2Fv1%2FuserLogin"
    postData = {
        "username": account,
        "password": password,
    }

    # 使用session直接post请求
    responseRes = huihuSession.post(postUrl, data=postData, headers=header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    # responseRes = requests.post(postUrl, data = postData, headers = header)
    # 无论是否登录成功，状态码一般都是 statusCode = 200
    print(f"statusCode = {responseRes.status_code}")
    # print(f"text = {responseRes.text}")
    print(responseRes.text.encode('gbk').decode('gbk'))
    huihuSession.cookies.save()


def isLoginStatus():
    # 通过访问个人中心页面的返回状态码来判断是否为登录状态

    routeUrl = "http://portal.zts.com.cn/portal_web/portal/home"

    # 下面有两个关键点
    # 第一个是header，如果不设置，会返回500的错误
    # 第二个是allow_redirects，如果不设置，session访问时，服务器返回302，
    # 然后session会自动重定向到登录页面，获取到登录页面之后，变成200的状态码
    # allow_redirects = False  就是不允许重定向
    try:
        responseRes = huihuSession.get(routeUrl, headers=header, allow_redirects=False)
        result = responseRes.text


    except Exception as e:
        print('登陆失败，失败原因：' + e)


if __name__ == "__main__":
    # 从返回结果来看，有登录成功
    huihuLogin("zhubh", "zbh123")
    isLogin1 = isLoginStatus()
    print(f"is login huihu = {isLogin1}")
