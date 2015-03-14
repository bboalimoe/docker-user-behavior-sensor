FROM texastribune/supervisor
MAINTAINER tech@texastribune.org

RUN apt-get -yq install nginx
# There's a known harmless warning generated here:
# See https://github.com/benoitc/gunicorn/issues/788

RUN pip install gunicorn==19.1.1
RUN pip install Django



# 1.every service should add the dependency to the requirements.txt

RUN mkdir /scipy
WORKDIR /app

# TOOD: move this to ancestor image?


RUN mkdir /app/run
RUN mkdir /app/djangoapp
#add the project to the /app/
ADD djangoapp/ /app/djangoapp
WORKDIR /app/djangoapp



#dependency install
#RUN pip install -r requirements.txt

# scipy install
#WORKDIR /scipy
#RUN apt-get install python python-dev atlas3-base-dev gcc g77 g++
#RUN git clone https://github.com/scipy/scipy.git
#RUN cd scipy
#RUN git clean -xdf
#RUN python setup.py install



ADD gunicorn_conf.py /app/
ADD gunicorn.supervisor.conf /etc/supervisor/conf.d/

ADD nginx.conf /app/
ADD nginx.supervisor.conf /etc/supervisor/conf.d/


VOLUME ["/app/logs"]
EXPOSE 9011
