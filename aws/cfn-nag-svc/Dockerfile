FROM ubuntu:16.04

RUN apt update; \
    apt -y dist-upgrade; \
    apt -y install ruby python-pip nginx nginx

RUN gem install cfn-nag; \
    pip install -U "pip<10.0"; \
    pip install -U uwsgi; \
    pip install -U flask; \
    mkdir /sock; \
    chmod 777 /sock; \
    usermod -s /bin/bash www-data

COPY nginx.conf /etc/nginx/nginx.conf
COPY app /app
COPY run_cfn_nag_app.sh /run_cfn_nag_app.sh

EXPOSE 80
CMD ["/run_cfn_nag_app.sh"]
