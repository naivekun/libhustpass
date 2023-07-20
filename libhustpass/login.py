import libhustpass.sbDes as sbDes
import libhustpass.captcha as captcha
import requests
import re
import random
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

def encrypt(password, public_key):
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()


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
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    login_html = r.get(url, headers=headers)
    captcha_content = r.get("https://pass.hust.edu.cn/cas/code?"+str(random.random()), stream=True,headers=headers)
    captcha_content.raw.decode_content = True
    nonce = re.search(
        '<input type="hidden" id="lt" name="lt" value="(.*)" />', login_html.text
    ).group(1)
    action = re.search(
        '<form id="loginForm" action="(.*)" method="post">', login_html.text
    ).group(1)
    response = requests.post("http://pass.hust.edu.cn/cas/rsa",headers=headers)
    data = response.json()
    public_key = data['publicKey']
    public_key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
    username_enc = encrypt(username, public_key)
    password_enc = encrypt(password, public_key)
    post_params = {
        "code": captcha.deCaptcha(captcha_content.raw),
        # "rsa": Enc(username + password + nonce, "1", "2", "3"),
        "ul": username_enc,
        "pl": password_enc,
        "lt": nonce,
        "execution": "e2s1",
        "_eventId": "submit",
    }
    redirect_html = r.post(
        "https://pass.hust.edu.cn" + action, data=post_params, allow_redirects=False,headers=headers
    )
    try:
        return redirect_html.headers["Location"]
    except:
        raise Exception("login failed")
