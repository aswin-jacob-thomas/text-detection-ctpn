from PIL import Image, ImageOps
import numpy as np 
import pytesseract

def extract(img, bbox_list):
    custom_oem_psm_config = r'--psm 6'
    data = []
    paired = get_item_amount(bbox_list)
    
    for bbox_pairs in paired:
        bbox_pairs = sorted(bbox_pairs, key=lambda x: x[0])
        new_pair = [] 
        if len(bbox_pairs) != 2:
            continue
        for bbox in bbox_pairs:
            img_copy = img.copy()
            img_copy = img_copy.crop(bbox)

            # new_im = ImageOps.expand(img_copy, border=5, fill=(255,255,255))
            new_im = img_copy

            # new_im.show()
            a = pytesseract.image_to_string(new_im, config=custom_oem_psm_config)
            new_pair.append(a)
        data.append(new_pair)
    
    # for d in data:
    #     if len(d) == 1:
    #     elif len(d) == 2:
    #         possible_value = d[1]
    #         item = d[0]
    #         try:
    #             possible_value = float(possible_value)
    #         except:

    return data

def get_item_amount(bbox_list):
    groups = {}
    paired_bbox_list = []
    bbox_list = np.array(bbox_list)
    heights = bbox_list[:,1]
    indices = np.argsort(heights)
    bbox_list = bbox_list[indices]
    # print(bbox_list.shape)
    # print(bbox_list)
    j = 0
    groups[j] = 0
    paired_bbox_list.append([bbox_list[0]])

    for i in range(1, bbox_list.shape[0]):
        first_box = bbox_list[i-1]
        second_box = bbox_list[i]

        if abs(first_box[1] - second_box[1]) <= 5:
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