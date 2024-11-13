FROM python:3.10-slim
MAINTAINER "pd"

WORKDIR app
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple  \
    && pip --no-cache-dir install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple