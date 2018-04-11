A simple app for pulling pages from Business Catalyst intoa Django project
-------------

Requirements
-------------
python requests library

You'll also need server to server auth with BC to obtain the authentication and refresh tokens which you need to use in headers, site ID, secure URL etc.

These can also be obtained from BC admin but the token is valid for maximum of 4 hours, which is enough to pull the data out.



