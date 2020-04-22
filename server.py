from flask import Flask, json, request
import numpy
import cv2
from main import demo
from PIL import Image
import extract_text
from flask import Flask
from flask_cors import CORS

api = Flask(__name__)
CORS(api)

@api.route('/detect', methods=['GET'])
def get_pages():
  return json.dumps({'Success':'S3 pages'})

@api.route('/detect', methods=['POST'])
def post_pages(): 
    
    img = cv2.imdecode(numpy.frombuffer(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    bb = demo.main(img[:, :, ::-1])
    im_pil = Image.fromarray(img)
    total, text = extract_text.extract(im_pil, bb)
    return json.dumps({'status':'SUCCESS','total':total, 'items':text})

if __name__ == '__main__':
  api.run(host='0.0.0.0', port=8080, debug=True)