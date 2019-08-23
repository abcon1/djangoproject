import unittest
from mongoengine import connect, disconnect
from system_service.database import models

from system_service.app import app

class TestDevice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        models.Device.objects().delete()
        models.User.objects().delete()
        disconnect()

    def test_add_user_with_valid_argument(self):
        pers = models.User(username='newuser', password='mynewpassword', devices=[])
        pers.save()

        fresh_pers = models.User.objects().first()
        self.assertEqual(fresh_pers.username, 'newuser')
    
    def test_add_user_with_invalid_argument(self):
        pass
    
    def test_add_device_to_user_with_existing_device_id(self):
        pass
    
    def test_add_device_to_user_with_not_existing_device_id(self):
        pass
    
    def test_add_device_to_more_than_three_users(self):
        pass