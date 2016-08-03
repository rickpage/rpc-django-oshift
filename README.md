RPCodes Django quickstart for Openshift

Work in progress. 

Intended to ease the creation of a new Django project, especially for REST API projects with user accounts. 
Based off of openshift/django-example

Combines common elements that I often use in Django projects:

+contrib.auth.Users
++Registration
++SessionAuth
++Rate Limiting

+Django Rest Framework
++Browsable API and JSON view
++Token Auth
++Django-filters

+Logging
++Logging the time it takes for a view to render (middleware)

+More...

