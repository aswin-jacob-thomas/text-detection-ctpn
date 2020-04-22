from PIL import Image, ImageOps
import numpy as np 
import pytesseract
# from cv2 import cv2

# from skimage import io
# from skimage import filters
import re
# from matplotlib import pyplot as plt

def is_current_digit(value):
    
    if len(value) == 0:
        return False
    
    regex_for_possible_value = r'^\s*\$?\s*[\d|\s]+[\.\,]\s*\d*[\.|\,]?\s*$'#r'\d+[\.|\,]\d+[\.|\,]?'
    if re.match(regex_for_possible_value, value):
        return True
    else:
        return False

def get_item_value(split_data):
    possible_value = split_data[-1]
    if len(possible_value) == 0:
        return (None, None)
    regex_for_possible_value = r'^\s*.*\s*[\d|\s]+[\.\,]\s*\d\d[\.|\,]?[^\d]*$'#r'\d+[\.|\,]\d+[\.|\,]?'
    
    print("I go ", possible_value)
    if re.match(regex_for_possible_value, possible_value):
        # item = str([' '.join(split_data[k]) for k in range(len(split_data)-1)])
        item = ''
        for k in range(len(split_data)-1):
            item += split_data[k] +' '
        item = item.strip()
        regex_for_item = re.compile(r'[^a-zA-Z0-9\s%().,]')
        item = regex_for_item.sub('', item)
        regex_for_value = re.compile(r'[^0-9]')
        value = regex_for_value.sub('', possible_value)
        # value = possible_value.replace(' ','').replace(',','').replace('.','')
        l = len(value)-2
        value = value[:l] + '.'+ value[l:]
        print("Item is ", item)
        print("Value is ", value)
        if len(item) != 0 and len(value)>=3:
            return (item, value)
        else: 
            return (None, None)
    else:
        return (None, None)

def extract(img, bbox_list):
    # img = np.array(img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
    #                                       cv2.THRESH_BINARY, 11, 2)
    # cv2.imshow('thresholding ', img)
    # cv2.waitKey(0)
    # img = Image.fromarray(img)

    possible_total = '' #need to send this together with the items
    custom_oem_psm_config = r'--psm 6'
    data = []
    paired = get_item_amount(bbox_list)

    for bbox_pairs in paired:
        bbox_pairs = sorted(bbox_pairs, key=lambda x: x[0])
        new_pair = [] 
       
        for bbox in bbox_pairs:
            img_copy = img.copy()
            img_copy = img_copy.crop(bbox)

            new_im = ImageOps.expand(img_copy, border=(2,3), fill=(255,255,255))

            a = pytesseract.image_to_string(new_im, config=custom_oem_psm_config)
            new_pair.append(a)
        data.append(new_pair)
    # print("Before all the madness ", data)
    for i in range(1, len(data)):
        d = data[i]
        if len(d) == 1 and is_current_digit(d[0]):
            data[i-1].append(data[i][0])

    # print("data = ", data)
    return_result = []
    for d in data:

        if len(d) == 1:
            split_data = d[0].split()
            # print("hello split data: ", split_data)
            if len(split_data) == 0:
                continue
        elif len(d) == 3:
            split_data = d
        else:
            print("Now i have ", d)
            item = d[0]
            value = d[1]
            split_data = d

        (item, value) = get_item_value(split_data)
        if item is not None and 'tota' in item.lower() and 'sub' not in item.lower():
            possible_total = value
        elif item is not None:
                return_result.append([item,value])

    return possible_total, return_result

def get_item_amount(bbox_list):
    groups = {}
    paired_bbox_list = []
    bbox_list = np.array(bbox_list)
    heights = bbox_list[:,1]
    indices = np.argsort(heights)
    bbox_list = bbox_list[indices]

    j = 0
    groups[j] = 0
    paired_bbox_list.append([bbox_list[0]])

    for i in range(1, bbox_list.shape[0]):
        first_box = bbox_list[i-1]
        second_box = bbox_list[i]

        if abs(first_box[1] - second_box[1]) <= 10:
            groups[i] = groups[i-1]
            paired_bbox_list[groups[i]].append(second_box)
        else:
            j += 1
            groups[i] = j
            paired_bbox_list.append([second_box])
    
    return paired_bbox_list
    

if __name__ == "__main__":
    bbox_list = bbox_list = [[79,26,238,46],[0,393,105,414],[255,348,300,366],[97,60,220,81],[26,352,97,371],[255,193,300,208],[264,369,308,387],[44,435,238,451],[8,92,88,113],[35,9,264,29],[8,190,79,205],[141,134,202,151],[255,288,300,305],[26,374,61,391],[0,130,70,149],[247,211,300,228],[17,208,123,226],[8,308,300,328],[255,249,300,266],[255,136,317,154],[17,228,158,246],[17,269,114,286],[105,45,194,62],[88,150,229,169],[211,391,308,411],[247,230,300,246],[247,268,300,284],[26,290,132,308],[17,250,105,265]]
    img = Image.open('1145-receipt.jpg')

    print(extract(img, bbox_list))
