# -*- coding: utf-8 -*
from abc import ABCMeta, abstractmethod
import csv

from six import with_metaclass


class DoesNotExist(Exception):
    pass


class ABCStorageMixin(with_metaclass(ABCMeta)):

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
        """ Persist a single dictionary object to storage. """
        self._storage.append(kwargs)

    def persist_multiple(self, objects):
        """ Persist multiple dictionary objects to storage. """
        for obj in objects:
            self._storage.append(obj)

    def retrieve_object(self, key, value):
        """ Retrieve a single object.

        Loop through objects in ``self._storage`` and look for a
        ``key`` in the dict that matches the ``value`` passed in.

        If there are multiple objects that match the ``key`` / ``value``
        return the first one.

        Args:
            key (str): The key we use to obtain a value to check.
            value (str): The value we compare the retrieved value against.

        Returns:
            dict: Representing and object.

        Raises:
             DoesNotExist: If not objects are found.
        """
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
        """ Retrieve all objects that match the passed in key-value pair.

        If no "query" args are passed in return everything in ``self._storage``.

        Returns:
            list: Of dictionary objects.
        """
        if not kwargs:
            return self._storage

        objects = []
        for key, value in kwargs.items():
            for obj in self._storage:
                if obj.get(key) == value:
                    objects.append(obj)

        return objects

    def wipe(self):
        """ Clear storage. Should only be used in testing. """
        self._storage = []


class CSVStorage(PureMemoryStorage):

    storage_name = 'CSV Storage'

    def __init__(self, file_name):
        super(CSVStorage, self).__init__()
        self.file_name = file_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ Write objects in storage to ``self.file_name``. """
        if self._storage:
            with open(self.file_name, 'w') as file_object:
                header = self._storage[0].keys()
                dict_writer = csv.DictWriter(file_object, header)
                dict_writer.writeheader()
                for obj in self._storage:
                    dict_writer.writerow(obj)
