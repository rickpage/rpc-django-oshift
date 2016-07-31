from django.test import TestCase
from django.test.client import Client

class StaticFilesTestCase(TestCase):
    '''
     django.test.client doesn't find static files on dev server
    '''
    test_url = "static/js.js"
    
    def setUp(self):
        self.client = Client();
        
    def TODO_test_static_file_get(self):
        '''
        TODO: Check against a running sever
        '''
        pass