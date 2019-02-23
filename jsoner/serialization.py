# -*- coding: utf-8 -*-

import abc
import json
import typing as T
from collections import UserDict
from functools import partial
from datetime import datetime
from importlib import import_module
import pydoc

import pytz

from .registry import decoders
from .registry import encoders
from .registry import import_object


class DictConvertible(abc.ABC):
    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, data_dict: dict):
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, other_cls: type):
        is_dict_convertible = (hasattr(other_cls, 'to_dict') and
                               hasattr(other_cls, 'from_dict'))
        return is_dict_convertible


class StrConvertible(abc.ABC):
    @abc.abstractmethod
    def to_str(self):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_str(cls, json_str: str):
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, other_cls: type):
        is_str_convertible = (hasattr(other_cls, 'to_str') and
                              hasattr(other_cls, 'from_str'))
        return is_str_convertible


class JsonerSerializable(abc.ABC):
    """
    The :class:`JsonerSerializable` serves as a abstract class
    which indicated if instances can be serialized by *Jsoner*.
    Therefore it implements the :meth:`__subclasshook__` method.

    A object is serializable by *Jsoner* if it is in the encoding, decoding
    registry or if it is convertible to a dict or to a string.
    """
    @classmethod
    def __subclasshook__(cls, other_cls: type):
        try:
            is_serializable = other_cls in decoders and other_cls in encoders
        except TypeError:
            return False

        if not is_serializable:
            is_serializable |= (issubclass(other_cls, StrConvertible) or
                                issubclass(other_cls, DictConvertible))

        return is_serializable


def _is_instance_of_type(obj: T.Union[object, type]) -> bool:
    is_a_cls = isinstance(obj, type)
    is_a_cls &= '<locals>' not in obj_spec(obj)

    return is_a_cls


def obj_spec(obj: T.Union[object, type]) -> str:
    if isinstance(obj, type):
        path = obj.__module__ + '.' + obj.__qualname__
    else:
        path = obj.__class__.__module__ + '.' + obj.__class__.__qualname__
    return path


class JsonEncoder(json.JSONEncoder):
    """
    JsonEncoder will decode datetime objects and all objects,
    which implement either `to_dict` and `from_dict` or
    `to_json` and `from_json`.

    If you want to implement to_json, you can use the  json encoder.
    This way, all objects which implement one of those methods will also be
    serialized and you don't have to consider them.
    """
    def default(self, obj, *args, **kwargs):
        """

        :param obj:
        :return:
        """

        if isinstance(obj, JsonerSerializable):
            obj_dict = {
                '__obj_cls__': obj_spec(obj),
                '__json_data__': None
            }
            if isinstance(obj, DictConvertible):
                obj_data = obj.to_dict()
            elif isinstance(obj, StrConvertible):
                obj_data = obj.to_str()
            else:
                encoder = encoders.get(obj)
                if isinstance(encoder, T.Callable):
                    obj_data = encoder(obj)
                else:
                    obj_data = encoder
            obj_dict['__json_data__'] = obj_data
            return obj_dict

        elif _is_instance_of_type(obj):
            return {'__cls__': obj_spec(obj)}

        else:
            return super().default(obj)


# def json_hook(primitive: T.Any) -> T.Any:
#     """
#     This function will restore a object which was encoded by using the
#     JsonEncoder.
#     :param primitive:
#     :return:
#     """
#
#     if isinstance(primitive, T.Dict):
#         if '__cls__' in primitive:
#             _cls = primitive.get('__cls__')
#             cls = import_object(_cls)
#             return cls
#
#         if '__obj_cls__' in primitive:
#             _cls = primitive.get('__obj_cls__')
#             cls = import_object(_cls)
#
#         else:
#             return primitive
#
#         data = primitive.get('__json_data__')
#
#
#         else:
#             if issubclass(cls, StrConvertible):
#                 return cls.from_str(data)
#
#             elif issubclass(cls, DictConvertible):
#                 # obj_dict = json.loads(json_data)
#                 return cls.from_dict(data)
#         if cls in decoders:
#             decoder = decoders.get(cls)
#             if isinstance(decoder, T.Callable):
#                 return decoder(data, cls)
#             else:
#                 return decoders
#     # else also for inner block:
#     return primitive

#
# dump = partial(json.dump, cls=JsonEncoder)
# dumps = partial(json.dumps, cls=JsonEncoder)
# load = partial(json.load, object_hook=json_hook)
# loads = partial(json.loads, object_hook=json_hook)
