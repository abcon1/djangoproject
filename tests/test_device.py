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

    def test_add_device(self):
        pers = models.Device(name='My new device')
        pers.save()

        fresh_pers = models.Device.objects().first()
        self.assertEqual(fresh_pers.name, 'My new device')
    
    def test_get_devices_on_empty(self):
        pass
    
    def test_get_devices_with_some_devices(self):
        pass
    
    def test_post_invalid_argument(self):
        pass
    
    def test_put_new_name(self):
        pass

    def test_put_already_existing_name(self):
        pass
    
    def test_put_with_not_existing_device_id(self):
        pass

    def test_delete_existing_device(self):
        pass
    
    def test_delete_not_existing_device(self):
        pass