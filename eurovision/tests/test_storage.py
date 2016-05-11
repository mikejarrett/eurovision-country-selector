# -*- coding: utf-8 -*-
import os

from unittest2 import TestCase

from ..storage import PureMemoryStorage, DoesNotExist, CSVStorage

class StorageTestInterface:

    def test_persist(self):
        self.assertEqual(len(self.storage._storage), 1)
        self.storage.persist(name='Eugene')
        self.assertEqual(len(self.storage._storage), 2)
        
    def test_persist_multiple(self):
        self.assertEqual(len(self.storage._storage), 1)
        olivia = {'name': 'Olivia'}
        amanda = {'name': 'Amanda'}
        donna = {'name': 'Donna'}
        self.storage.persist_multiple(
            [
                olivia,
                amanda,
                donna,
            ]
        )
        self.assertEqual(len(self.storage._storage), 4)
        
    def test_retrieve_object(self):
        obj = self.storage.retrieve_object('name', 'Mike')
        self.assertDictEqual(obj, self.obj)
        
    def test_retrieve_object_that_does_not_exist(self):
        with self.assertRaises(DoesNotExist):
            self.storage.retrieve_object('name', 'Steve')
            
    def test_retrieve_objects(self):
        objects = self.storage.retrieve_objects(name='Mike')
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0], self.obj)
        
    def test_retrieve_objects_empty_list(self):
        objects = self.storage.retrieve_objects(bar='foo')
        self.assertEqual(objects, [])
        
    def test_retrieve_objects_with_multiple_objects_returned(self):
        obj = {'name': 'Olivia'}
        self.storage.persist(**obj)
        objects = self.storage.retrieve_objects()
        self.assertEqual(len(objects), 2)
        self.assertIn(obj, objects)
        self.assertIn(self.obj, objects)


class TestPureMemoryStorage(StorageTestInterface, TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storage = PureMemoryStorage()

    def setUp(self):
        self.obj = {'name': 'Mike', 'foo': 'bar'}
        self.storage._storage.append(self.obj)
        
    def tearDown(self):
        self.storage.wipe()


class TestCSVStorage(StorageTestInterface, TestCase):

    @classmethod
    def setUpClass(cls):
        cls.storage = CSVStorage('SHOULD_NOT_CREATE').__enter__()

    def setUp(self):
        self.obj = {'name': 'Mike', 'foo': 'bar'}
        self.storage._storage.append(self.obj)
        
    def tearDown(self):
        self.storage.wipe()
        
    def test_csvstorage__exit__(self):
        filename = 'created.csv'
        with CSVStorage(filename) as storage:
            storage._storage.append(self.obj)
        self.assertTrue(os.path.isfile(filename))
        os.remove(filename)
        self.assertFalse(os.path.isfile(filename))
