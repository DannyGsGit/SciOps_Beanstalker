## Build
After thorough testing, it appears that the EB environment fails when loading Python packages using C. Because of the way C and modwsgi access the Python interpreter, we need to make some changes to the environment configuration.

http://stackoverflow.com/questions/27570326/elastic-beanstalk-scipy-fails-silently/28565858

https://emptysqua.re/blog/python-c-extensions-and-mod-wsgi/

http://modwsgi.readthedocs.io/en/develop/user-guides/application-issues.html#python-simplified-gil-state-api

https://dev.mikamai.com/2016/11/08/flask-and-python-saml-on-amazon-elastic-beanstalk/

WSGI (Web Server Gateway Interface) is part of the EB Python configuration. It does not play nicely with Python libraries that access C.

To remediate, try adding a .config file to /.ebextensions containing:
```
files:
  "/etc/httpd/conf.d/wsgi_custom.conf":
    mode: "000644"
    owner: root
    group: root
    content: |
      WSGIApplicationGroup %{GLOBAL}
```

Success!!! This remediates issues using the Numpy package.
