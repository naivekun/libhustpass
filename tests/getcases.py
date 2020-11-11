import requests
import random

url = "https://pass.hust.edu.cn/cas/code?"

for i in range(1):
    with open(f"cases/{i}.gif", "wb") as f:
        print(f"downloading case #{i}")
        f.write(requests.get(url+str(random.random())).content)