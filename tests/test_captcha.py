import pytest, os
from libhustpass import deCaptcha
import logging

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_deCaptcha():
    with open(os.path.join(THIS_DIR, "result.txt")) as f:
        ansList = f.read().split("\n")

    accu = 0.0
    passedCase = 0
    for i in range(1000):
        logging.debug(i)
        ans = ansList[i][5:]
        ret = deCaptcha(os.path.join(THIS_DIR, "cases" + os.sep + f"{i}.gif"))
        if ret == ans:
            passedCase += 1
        else:
            print(f"case #{i} failed: expect {ans} but got {ret}")
        accu = passedCase/(i+1)
        print(f"running test #{i}, accuracy={accu}")
        
    assert accu > 0.99