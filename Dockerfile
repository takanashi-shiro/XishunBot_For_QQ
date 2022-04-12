FROM python:3.8
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt update
RUN apt install ffmpeg -y
COPY . .
RUN pip install nb-cli nonebot-adapter-cqhttp -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install paho-mqtt requests lxml BeautifulSoup4 mysql-connector-python -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD python3 main.py