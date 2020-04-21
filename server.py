from flask import Flask, json, request
import numpy
import cv2
from main import demo
from PIL import Image
import extract_text
api = Flask(__name__)

@api.route('/detect', methods=['GET'])
def get_pages():
  return json.dumps({'Success':'S3 pages'})

@api.route('/detect', methods=['POST'])
def post_pages(): 
    
    img = cv2.imdecode(numpy.frombuffer(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    bb = demo.main(img[:, :, ::-1])
    im_pil = Image.fromarray(img)
    text = extract_text.extract(im_pil, bb)
    return json.dumps({'Success':text})

if __name__ == '__main__':
  api.run(host='0.0.0.0', port=8080)