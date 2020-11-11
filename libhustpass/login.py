import libhustpass.sbDes as sbDes
import libhustpass.captcha as captcha
import requests
import re
import random

def toWideChar(data):
    data_bytes = bytes(data, encoding="utf-8")
    ret = []
    for i in data_bytes:
        ret.extend([0, i])
    while len(ret) % 8 != 0:
        ret.append(0)
    return ret

def Enc(data, first_key, second_key, third_key):
    data_bytes = toWideChar(data)
    key1_bytes = toWideChar(first_key)
    key2_bytes = toWideChar(second_key)
    key3_bytes = toWideChar(third_key)
    ret_ = []

    i = 0
    while i < len(data_bytes):
        tmp = data_bytes[i : i + 8]
        x = 0
        y = 0
        z = 0
        while x < len(key1_bytes):
            enc1_ = sbDes.des(key1_bytes[x : x + 8], sbDes.ECB)
            tmp = list(enc1_.encrypt(tmp))
            x += 8
        while y < len(key2_bytes):
            enc2_ = sbDes.des(key2_bytes[y : y + 8], sbDes.ECB)
            tmp = list(enc2_.encrypt(tmp))
            y += 8
        while z < len(key3_bytes):
            enc3_ = sbDes.des(key3_bytes[z : z + 8], sbDes.ECB)
            tmp = list(enc3_.encrypt(tmp))
            z += 8
        ret_.extend(tmp)
        i += 8

    ret = ""
    for i in ret_:
        ret += "%02X" % i

    return ret


def login(username, password, url):
    r = requests.session()
    login_html = r.get(url)
    captcha_content = r.get("https://pass.hust.edu.cn/cas/code?"+str(random.random()), stream=True)
    captcha_content.raw.decode_content = True
    nonce = re.search(
        '<input type="hidden" id="lt" name="lt" value="(.*)" />', login_html.text
    ).group(1)
    action = re.search(
        '<form id="loginForm" action="(.*)" method="post">', login_html.text
    ).group(1)
    post_params = {
        "code": captcha.deCaptcha(captcha_content.raw),
        "rsa": Enc(username + password + nonce, "1", "2", "3"),
        "ul": len(username),
        "pl": len(password),
        "lt": nonce,
        "execution": "e1s1",
        "_eventId": "submit",
    }
    redirect_html = r.post(
        "https://pass.hust.edu.cn" + action, data=post_params, allow_redirects=False
    )
    try:
        return redirect_html.headers["Location"]
    except:
        raise Exception("login failed")
