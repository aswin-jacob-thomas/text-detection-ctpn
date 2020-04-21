from flask import Flask, json, request
import numpy
import cv2
from main import demo
api = Flask(__name__)

@api.route('/detect', methods=['GET'])
def get_pages():
  return json.dumps({'Success':'S3 pages'})

@api.route('/detect', methods=['POST'])
def post_pages(): 
    
    img = cv2.imdecode(numpy.frombuffer(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)[:, :, ::-1]
    bb = demo.main(img)
    print(bb)
    return json.dumps({'Success':'gotcha'})

if __name__ == '__main__':
  api.run(host='0.0.0.0', port=8080)