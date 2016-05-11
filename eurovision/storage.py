# -*- coding: utf-8 -*
from abc import ABCMeta, abstractmethod
import csv


class DoesNotExist(Exception):
    pass


class ABCStorageMixin(metaclass=ABCMeta):

    __metaclass__ = ABCMeta

    @abstractmethod
    def persist(self, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def persist_multiple(self, objects):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_object(self, key, value):
        raise NotImplementedError()

    @abstractmethod
    def retrieve_objects(self, **kwargs):
        raise NotImplementedError()
        
    @abstractmethod
    def wipe(self):
        raise NotImplementedError()


class PureMemoryStorage(ABCStorageMixin):

    storage_name = 'Pure Memory Storage'
    
    def __init__(self):
        self._storage = []

    def persist(self, **kwargs):
        self._storage.append(kwargs)
        
    def persist_multiple(self, objects):
        for obj in objects:
            self._storage.append(obj)
        
    def retrieve_object(self, key, value):
        for obj in self._storage:
            if obj.get(key) == value:
                return obj
        
        raise DoesNotExist(
            "Couldn't find {obj_storage} matching {key} {value}".format(
                obj_storage=self.storage_name,
                key=key,
                value=value
            )
        )

    def retrieve_objects(self, **kwargs):
        if not kwargs:
            return self._storage

        objects = []
        for key, value in kwargs.items():
            for obj in self._storage:
                if obj.get(key) == value:
                    objects.append(obj)

        return objects
        
    def wipe(self):
        self._storage = []
        
        
class CSVStorage(PureMemoryStorage):

    storage_name = 'CSV Storage'

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        if self._storage:
            with open(self.file_name, 'w') as file_object:
                header = self._storage[0].keys()
                dict_writer = csv.DictWriter(file_object, header)
                dict_writer.writeheader()
                for obj in self._storage:
                    dict_writer.writerow(obj)
        
    def wipe(self):
        self._storage = []
