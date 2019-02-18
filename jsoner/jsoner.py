# -*- coding: utf-8 -*-

import abc
import json
import typing as T
from collections import UserDict
from functools import partial
from datetime import datetime
from importlib import import_module

import pytz

from .errors import JsonEncodingError
# from .registry import encoding_registry
# from .registry import decoding_registry
#
#
# class JsonSerializable(abc.ABC):
#     @classmethod
#     def __subclasshook__(cls, other_cls: type):
#         is_in_default_encoding = (
#             bool(decoding_registry.get(other_cls)) and
#             bool(encoding_registry.get(other_cls))
#         )
#
#         return is_in_default_encoding
#
#
# class JsonDictSerializable(JsonSerializable):
#     @abc.abstractmethod
#     def to_dict(self):
#         raise NotImplementedError
#
#     @classmethod
#     @abc.abstractmethod
#     def from_dict(cls, data_dict: dict):
#         raise NotImplementedError
#
#     @classmethod
#     def __subclasshook__(cls, other_cls: type):
#         is_dict_convertible = hasattr(other_cls, 'to_dict') and hasattr(other_cls, 'from_dict')
#         return is_dict_convertible
#
#
# class JsonStrSerializable(JsonSerializable):
#     @abc.abstractmethod
#     def to_json(self):
#         raise NotImplementedError
#
#     @classmethod
#     @abc.abstractmethod
#     def from_json(cls, json_str: str):
#         raise NotImplementedError
#
#     @classmethod
#     def __subclasshook__(cls, other_cls: type):
#         is_str_convertible = hasattr(other_cls, 'to_json') and hasattr(other_cls, 'from_json')
#         return is_str_convertible


# def is_serializable(obj: T.Union[type, object]) -> bool:
#
#     json_serializable = isinstance(obj, JsonStrSerializable)
#     is_dict_convertible = isinstance(obj, JsonDictSerializable)
#     is_in_default_encoding = isinstance(obj, JsonSerializable)
#
#     serializable = json_serializable or is_dict_convertible or is_in_default_encoding
#
#     if not serializable:
#         try:
#             json_serializable = issubclass(obj, JsonStrSerializable)
#             is_dict_convertible = issubclass(obj, JsonDictSerializable)
#             is_in_default_encoding = issubclass(obj, JsonSerializable)
#
#             serializable = json_serializable or is_dict_convertible or is_in_default_encoding
#         except TypeError:
#             pass
#     return serializable


# class Registry:
#     registry = {}
#
#     def __init__(self, register_type: type):
#         if register_type in self.registry:
#             msg = "`{}` was already registered!".format(register_type)
#             raise KeyError(msg)
#
#         self.register_type = register_type
#
#     def __call__(self, callable_obj: callable) -> callable:
#         self.registry[self.register_type] = callable_obj
#
#         return callable_obj
#
#     @classmethod
#     def get(cls, obj_or_type: T.Union[object, type]) -> callable:
#         """
#         Returns the registered function for the given object or type
#         :param obj_or_type:
#         :return:
#         """
#         if obj_or_type is None:
#             return None
#         try:
#             return cls.registry[obj_or_type]
#         except KeyError:
#             pass
#
#         obj_type = obj_or_type.__class__
#
#         try:
#             return cls.registry[obj_type]
#         except KeyError:
#             pass
#
#         for default_obj_type in cls.registry:
#             if issubclass(obj_type, default_obj_type):
#                 return cls.registry[default_obj_type]
#         else:
#             return None
#
#
# class decoding_registry(Registry):
#     registry = {}
#
#
# class encoding_registry(Registry):
#     registry = {}
#
#
# def _get_obj_type(obj_type: str, module: str = None):
#     """
#     Given an object type and a module, this function returns
#     the corresponding class.
#
#     *obj_type* can also be of form *module.type*. In this case the module
#     argument can be empty.
#
#     :param obj_type:
#     :param module:
#     :return:
#     """
#     try:
#         if module is not None:
#             obj_module = import_module(module)
#             obj_type = obj_type.rpartition('.')[2]
#
#             obj_type = getattr(obj_module, obj_type)
#
#         else:
#             obj_module, _, obj_type = obj_type.rpartition('.')
#             if obj_module:
#                 obj_module = import_module(obj_module)
#                 obj_type = getattr(obj_module, obj_type)
#             else:
#                 msg = 'obj_type has no module information!. Please provide a module!'
#                 raise ValueError(msg)
#
#         return obj_type
#     except (ImportError, AttributeError):
#         return None


######################################################################
# Here you can specify encoding and decoding functions for different
# types, which are not json serializable by default.
#
# The encoding function receives a object of the specified type and
# should return an json serializable object.
#
# The decoding function will receive this object and the object type
# and can construct an object again out of the data.
#
# This will also be applied for subclasses of the given type.
# So you must pay attention that your classes are substitutable.
#
# Be aware that those functions will only be applied, if the object
# has no `to_json`, `from_json` or `to_dict`, `from_dict` method pair.
######################################################################

#
# @encoding_registry(datetime)
# def datetime_to_dict(dt: datetime):
#     """
#     Converts a datetime object to a dictionary, by saving the timestamp and the
#     timezone.
#
#     :param dt:
#     :return:
#     """
#     tz = dt.tzinfo
#     if tz is not None:
#         tz = str(tz)
#
#     dt_dict = {
#         'epoch': dt.timestamp(),
#         'tz': tz
#     }
#     return dt_dict
#
#
# @decoding_registry(datetime)
# def dict_to_datetime(dt_dict: dict, *args, **kwargs):
#     """
#     Creates a datetime object from a dictionary.
#
#     Usage::
#         >>> dt_dict = {'epoch': 1539785575.303671,
#         ...            'tz': 'UTC'}
#
#         >>> dt = dict_to_datetime(dt_dict)
#         >>> dt
#         datetime.datetime(2018, 10, 17, 14, 12, 55, 303671, tzinfo=<UTC>)
#
#     :param dt_dict:
#     :return:
#     """
#
#     timestamp = dt_dict.get('epoch') or dt_dict.get('timestamp')
#     tz = dt_dict.get('tz')
#
#     if tz:
#         tz = pytz.timezone(tz)
#     else:
#         tz = None
#     dt = datetime.fromtimestamp(timestamp, tz=tz)
#
#     return dt
#
#
# @decoding_registry(UserDict)
# def decode_user_dict(json_data: dict, obj_type: type) -> UserDict:
#     """
#     Decodes an json serialized UserDict.
#     :param json_data:
#     :param obj_type:
#     :return:
#     """
#
#     if hasattr(obj_type, 'from_dict'):
#         obj = obj_type.from_dict(json_data)
#     else:
#         obj = obj_type(**json_data)
#     return obj
#
#
# @encoding_registry(UserDict)
# def encode_user_dict(user_dict: UserDict):
#     if hasattr(user_dict, 'to_dict'):
#         return user_dict.to_dict()
#     else:
#         return dict(user_dict)
#
#
# class JsonEncoder(json.JSONEncoder):
#     """
#     JsonEncoder will decode datetime objects and all objects,
#     which implement either `to_dict` and `from_dict` or `to_json` and `from_json`.
#
#     If you want to implement to_json, you can use the  json encoder.
#     This way, all objects which implement one of those methods will also be
#     serialized and you don't have to consider them.
#     """
#     def default(self, obj, *args, **kwargs):
#         """
#
#         :param obj:
#         :return:
#         """
#
#         if is_serializable(obj):
#             obj_dict = {
#                 '__obj_module__': obj.__class__.__module__,
#                 '__type__': obj.__class__.__qualname__,
#                 '__json_data__': None
#             }
#
#             if isinstance(obj, JsonStrSerializable):
#                 json_str = obj.to_json()
#                 if not isinstance(json_str, str):
#                     msg = '`to_json` from {} did not return a valid json string!'.format(obj)
#                     raise JsonEncodingError(msg)
#
#                 obj_dict['__json_data__'] = json_str
#                 return obj_dict
#
#             elif isinstance(obj, JsonDictSerializable):
#                 obj_dict['__json_data__'] = obj.to_dict()
#                 return obj_dict
#
#             else:
#                 encoder_func = encoding_registry.get(obj)
#
#                 assert encoder_func is not None
#
#                 obj_dict['__json_data__'] = encoder_func(obj)
#                 return obj_dict
#
#         else:
#             return super().default(obj, *args, **kwargs)
#
#
# def json_hook(primitive: T.Any) -> T.Any:
#     """
#     This function will restore a object which was encoded by using the
#     JsonEncoder.
#     :param primitive:
#     :return:
#     """
#
#     if isinstance(primitive, dict):
#         module = primitive.get('__obj_module__')
#         obj_type = primitive.get('__type__')
#         json_data = primitive.get('__json_data__')
#
#         if module or obj_type:
#             obj_type = _get_obj_type(obj_type, module)
#         else:
#             return primitive
#
#         if is_serializable(obj_type):
#
#             if issubclass(obj_type, JsonStrSerializable):
#                 return obj_type.from_json(json_data)
#
#             elif issubclass(obj_type, JsonDictSerializable):
#                 # obj_dict = json.loads(json_data)
#                 return obj_type.from_dict(json_data)
#
#             else:
#                 decoding_func = decoding_registry.get(obj_type)
#
#                 obj = decoding_func(json_data, obj_type)
#
#                 return obj
#
#     # else also for inner block:
#     return primitive
#
#
# # # Encoding function
# # def dumps(obj):
# #     """
# #     Dumps objects into a json format. Usually classes cannot be dumped, however
# #     the JsonEncoder looks for either `to_json` and `from_json` or `to_dict`
# #     and `from dict` and uses those methods as a hook to also serialize
# #     complex python objects.
# #
# #     :param obj:
# #     :return:
# #     """
# #     return json.dumps(obj, cls=JsonEncoder)
#
# dump = partial(json.dump, cls=JsonEncoder)
# dumps = partial(json.dumps, cls=JsonEncoder)
# load = partial(json.load, object_hook=json_hook)
# loads = partial(json.loads, object_hook=json_hook)
#
#
# # # Decoding function
# # def loads(json_str: str) -> T.Any:
# #     """
# #     Decodes json objects which were encoded with the JsonEncoder.
# #     :param json_str:
# #     :return:
# #     """
# #     return json.loads(json_str, object_hook=json_hook)
