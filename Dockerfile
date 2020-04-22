FROM python:3.6-slim
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN apt-get install libgtk2.0-dev -y
RUN apt install -y tesseract-ocr
WORKDIR /deploy/
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/google-research/tf-slim
COPY ./nets/ /deploy/nets/

COPY ./utils/bbox/ /deploy/utils/bbox/
COPY ./utils/dataset/ /deploy/utils/dataset/
COPY ./utils/prepare/ /deploy/utils/prepare/
COPY ./utils/rpn_msr/ /deploy/utils/rpn_msr/
COPY ./utils/text_connector/ /deploy/utils/text_connector/

COPY ./checkpoints_mlt/ /deploy/checkpoints_mlt/
COPY ./extract_text.py /deploy/
COPY ./server.py /deploy/
COPY ./main/ /deploy/main/
RUN python /deploy/utils/bbox/setup.py build_ext 
RUN python /deploy/utils/bbox/setup.py install
RUN ls -la /deploy/build/*
RUN mv /deploy/build/*/*.so /deploy/utils/bbox/

# RUN chmod +X /deploy/utils/bbox/make.sh
# RUN sh /deploy/utils/bbox/make.sh
EXPOSE 8080
ENTRYPOINT ["python", "server.py"]