RPCodes Django quickstart for Openshift

Work in progress.

Intended to ease the creation of a new Django project, especially for REST API projects with user accounts.
Based off of openshift/django-example but adds significant features.
See requirements.txt for dependencies.

Combines common elements that I often use in Django projects:

+ contrib.auth.Users
++Registration
++SessionAuth

+ Django Rest Framework
++ Browsable API view in Debug only
++ Token Auth

In the works:
+ Auth:
++Rate Limiting (via django rest if easiest)
++Permissions, Groups (not yet, for now use createsuperuser for admin accounts)
++Messaging system - demonstrates use of Groups

+ User Management features
++Django-filters

+Logging
++Logging the time it takes for a view to render (middleware)
++Some form of Auditting for *at least the) User model

+More...

Note to self

Working on:
User registration standard, including password reset
