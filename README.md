2019年09月06日19:19:07
### install devel

#### centos 7
```
yum install python36.x86_64 python36-pip.noarch python36-devel
yum install gcc libffi-devel  openssl-devel mysql-devel
```

#### python3.6
```
yum install python36.x86_64 python36-pip.noarch python36-devel
yum install gcc libffi-devel  openssl-devel mysql-devel
```

#### django2.2
```
pip 3.6 install django==2.2
```

#### other 
```
pip3.6 install  Markdown  mysqlclient django-pure-pagination markdown django-celery  celery-with-redis  redis==2.10.6 flower gunicorn
```
#### django start
```
python3.6 manage.py runserver 0.0.0.0:8000
or
gunicorn reboot.wsgi:application  -b 0.0.0.0:8000
```
#### celery start 
```
cd $WORKHOME
celery -A reboot worker -l info
celery -A reboot beat -l info
celery -A reboot flower --address=0.0.0.0 --port=5555
```

#2019年09月16日18:41:23
```
pip3.6 install pillow
```


