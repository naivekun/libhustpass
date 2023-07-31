# libhustpass

![Python package](https://github.com/naivekun/libhustpass/workflows/Python%20package/badge.svg?branch=master)


now the `pass.hust.edu.cn` changed the encryption method from DES to RSA again.

## Installation

```
python setup.py install
```

## Usage

```python
from libhustpass import login

ticket = login("username","password","https://one.hust.edu.cn/dcp/")

# now copy ticket to browser is ok
# or open a new session in script

import requests
r = requests.session()
ret = r.get(ticket)

# do whatever you want

print(ret.text)

```

## Implementation

`jsencryption.js` uses normal RSA to encrypt.

so I use package **pycryptodome** to implement the RSA encryption.

```python
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

def encrypt(password, public_key):
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()
```


## changelog

#### 20201111

Rebuild shit mountain && add tests

accuracy is 995/1000

#### 20200501 support captcha

`pass.hust.edu.cn` force user input captcha since 20200501

`captcha.py` uses library [Tesseract](https://tesseract-ocr.github.io/) to auto-fuck captcha

Install Tesseract first !

#### 20230723

`pass.hust.edu.cn` use RSA to encrypt frontend input nows, libhustpass now support it.


## License

WTFPL
