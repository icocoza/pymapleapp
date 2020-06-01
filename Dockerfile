FROM centos:7

RUN yum update -y
RUN yum -y install yum-utils
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install gcc gcc-c++ mysql python36u python36u-devel python36u-pip convmv
RUN easy_install-3.6 pip
RUN pip3 -V
RUN pip3 install --upgrade setuptools
RUN pip install --upgrade pip

RUN pip3 install \
    kafka \
    kafka-python \
    mysql-connector-python==8.0.5 \
    requests \
    numpy \
    pandas \
    confluent-kafka \
    python-dateutil \
    pytz \
    SQLAlchemy \
    pymysql \
    flask_restplus \
    confluent_kafka \
    flask \
    sqlalchemy \
    redis \
    apscheduler \
    Crypto \
    pybase62 \
    beautifulsoup4 \
    tqdm \
    pillow \
    pycrypto \
    enum34

RUN localedef -f UTF-8 -i ko_KR ko_KR.utf8
RUN export LANG=ko_KR.utf8
RUN export LC_ALL=ko_KR.utf8
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN export LANG="ko_KR.UTF-8"
RUN convmv -f euc-kr -t ko_KR.UTF-8 --notest *

VOLUME /iot
WORKDIR /iot

COPY . /iot
ENTRYPOINT ["./start_inference.sh"]
CMD [""]
