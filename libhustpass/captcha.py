from PIL import Image, GifImagePlugin, ImageFilter, ImageOps
from pytesseract import image_to_string

# def deCaptcha(imageContent, maxConfirmDepoint = 10):
    # with Image.open(imageContent) as imageObject:
    #     imageObject.seek(1)
    #     grayImage = imageObject.convert("L")
    # binarizedImage = grayImage.point(lambda i: i == 255 and 255)
    # depointedImage = binarizedImage.filter(ImageFilter.MedianFilter(3))
    # code = image_to_string(depointedImage, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')[0:4]
    # return code
def depoint(img):
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > 245:#上
                count = count + 1
            if pixdata[x,y+1] > 245:#下
                count = count + 1
            if pixdata[x-1,y] > 245:#左
                count = count + 1
            if pixdata[x+1,y] > 245:#右
                count = count + 1
            if pixdata[x-1,y-1] > 245:#左上
                count = count + 1
            if pixdata[x-1,y+1] > 245:#左下
                count = count + 1
            if pixdata[x+1,y-1] > 245:#右上
                count = count + 1
            if pixdata[x+1,y+1] > 245:#右下
                count = count + 1
            if count > 5:
                pixdata[x,y] = 255
    return img

def deCaptcha(imageContent, maxConfirmDepoint = 10):
    with Image.open(imageContent) as imageObject:
        imageObject.seek(1)
        grayImage = ImageOps.expand(imageObject.convert("L"), border=5, fill='white')
    binarizedImage = grayImage.point(lambda i: i == 255 and 255)
    depointedImage = depoint(binarizedImage)
    ret = "0000"
    while maxConfirmDepoint > 0:
        # remove median filter to improve accurcy from 0.984 to 0.994

        depointedImage = depoint(depointedImage)
        # depointedImage = depointedImage.filter(ImageFilter.MedianFilter(3))
        code1 = image_to_string(depointedImage, config='--psm 10 --oem 3 -c tessedit_char_whitelist=Oo0123456789')
        depointedImage = depoint(depointedImage)
        # depointedImage = depointedImage.filter(ImageFilter.MedianFilter(3))
        code2 = image_to_string(depointedImage, config='--psm 10 --oem 3 -c tessedit_char_whitelist=Oo0123456789')
        depointedImage = depoint(depointedImage)
        # depointedImage = depointedImage.filter(ImageFilter.MedianFilter(3))
        code3 = image_to_string(depointedImage, config='--psm 10 --oem 3 -c tessedit_char_whitelist=Oo0123456789')
        
        if code1 == code2 or code1 == code3:
            ret = code1
            break
        if code2 == code3:
            ret = code2
            break
        maxConfirmDepoint -= 1
    return "".join([x.replace("o", "0").replace("O", "0") for x in ret if x not in ["\n", "\x0c"]])
