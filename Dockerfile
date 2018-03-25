FROM httpd:latest

# set varibles
ENV root_app /cmdb
ENV root_apache /usr/local/apache2
ENV django_settings cmdb.prd-settings

# system setup
RUN apt-get update
RUN apt-get install -y python3-pip libapache2-mod-wsgi-py3
RUN pip3 install -U pip 

# copy django app
ADD . ${root_app}
WORKDIR ${root_app}

# install requirements 
RUN pip3 install -r requirements.txt

# configure apache
COPY ./extra/httpd.conf ${root_apache}/conf/httpd.conf
RUN echo "Include ${root_app}/extra/httpd-vhosts.conf" >> ${root_apache}/conf/httpd.conf

# deploy django app
RUN python3 manage.py collectstatic --noinput --settings "${django_settings}"
RUN python3 manage.py migrate --settings "${django_settings}"

# expose http service
EXPOSE 8080/tcp
