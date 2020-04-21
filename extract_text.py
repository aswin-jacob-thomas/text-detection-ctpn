from PIL import Image, ImageOps
# import cv2
# import numpy as np 
import pytesseract

def extract(img, bbox_list):
    custom_oem_psm_config = r'--psm 6'
    data = []
    for bbox in bbox_list:
        img_copy = img.copy()
        img_copy = img_copy.crop(bbox)

        # new_im = ImageOps.expand(img_copy, border=5, fill=(255,255,255))
        new_im = img_copy

        # new_im.show()
        a = pytesseract.image_to_string(new_im, config=custom_oem_psm_config)
        data.append(a)
    
    return data

if __name__ == "__main__":
    bbox_list = bbox_list = [(79,26,238,46),(0,393,105,414),(255,348,300,366),(97,60,220,81),(26,352,97,371),(255,193,300,208),(264,369,308,387),(44,435,238,451),(8,92,88,113),(35,9,264,29),(8,190,79,205),(141,134,202,151),(255,288,300,305),(26,374,61,391),(0,130,70,149),(247,211,300,228),(17,208,123,226),(8,308,300,328),(255,249,300,266),(255,136,317,154),(17,228,158,246),(17,269,114,286),(105,45,194,62),(88,150,229,169),(211,391,308,411),(247,230,300,246),(247,268,300,284),(26,290,132,308),(17,250,105,265),]

    img = Image.open('1145-receipt.jpg')
    print(extract(img, bbox_list))