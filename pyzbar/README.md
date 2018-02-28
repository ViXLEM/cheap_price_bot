Pyzbar is my craft version for deploy to heroku
[official version: https://pypi.python.org/pypi/pyzbar/]

Before deploing this app you must add Zbar buildpack:
[https://github.com/sheck/heroku-buildpack-zbar]

After that need set virtual env var ZBAR_LIB:
[heroku config:set ZBAR_LIB=vendor/lib/libzbar.so]

In this app was taken and cut pyzbar package:
[https://github.com/NaturalHistoryMuseum/pyzbar/]