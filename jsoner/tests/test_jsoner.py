#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `jsoner` package."""

import json
import unittest
from datetime import datetime

import pytz

from jsoner import jsoner
from jsoner.errors import JsonEncodingError

# ##################
# # Testing objects
# ##################
# class DummyObject1:
#     def to_json(self):
#         return '1234'
#
#     @classmethod
#     def from_json(cls, json_str):
#         return cls()
#
#
# class DummyObject2:
#     def to_dict(self):
#         return {}
#
#     @classmethod
#     def from_dict(cls, json_dict):
#         return cls()
#
#
# class DummyObject3:
#     def __init__(self):
#         self.embedded_obj1 = DummyObject1()
#         self.embedded_obj2 = DummyObject2()
#
#     def to_dict(self):
#         return {
#             'embedded_obj1': self.embedded_obj1,
#             'embedded_obj2': self.embedded_obj2
#         }
#
#     @classmethod
#     def from_dict(cls, json_dict):
#         obj = cls()
#         obj.embedded_obj1 = json_dict['embedded_obj1']
#         obj.embedded_obj2 = json_dict['embedded_obj2']
#         return obj
#
#
# class DummyObject4:
#     def __init__(self):
#         self.embedded_obj1 = DummyObject1()
#         self.embedded_obj2 = DummyObject2()
#
#     def to_json(self):
#         return jsoner.dumps({
#             'embedded_obj1': self.embedded_obj1,
#             'embedded_obj2': self.embedded_obj2
#         })
#
#     @classmethod
#     def from_json(cls, json_str):
#         obj = cls()
#         json_data = jsoner.loads(json_str)
#         obj.embedded_obj1 = json_data['embedded_obj1']
#         obj.embedded_obj2 = json_data['embedded_obj2']
#         return obj
#
#
# class DummyObject5:
#     a = 5
#
# ###########################
#
#
# class TestDictToDatetime(unittest.TestCase):
#     def test_000_dict_to_datetime(self):
#         dd_dict = {
#             # '__obj_module__': 'datetime',
#             # '__type__': 'datetime',
#             'epoch': 1539785575.303671,
#             'tz': 'UTC'
#         }
#
#         dt = jsoner.dict_to_datetime(dd_dict)
#
#         self.assertEqual(dt.timestamp(), dd_dict['epoch'])
#         self.assertEqual(str(dt.tzinfo), 'UTC')
#
#     def test_001_dict_to_datetime(self):
#         dd_dict = {
#             # '__type__': 'datetime.datetime',
#             'epoch': 1539785575.303671,
#         }
#
#         dt = jsoner.dict_to_datetime(dd_dict)
#
#         self.assertEqual(dt.timestamp(), dd_dict['epoch'])
#         self.assertIsNone(dt.tzinfo)
#
#
# class TestJsonEncoder(unittest.TestCase):
#     def test_000_encode_dict(self):
#         json_str = jsoner.dumps({'test': 123})
#
#         self.assertEqual(json_str, '{"test": 123}')
#
#     def test_001_encode_list(self):
#         json_str = jsoner.dumps([1, 2, 3, 4, 5])
#
#         self.assertEqual(json_str, '[1, 2, 3, 4, 5]')
#
#     def test_002_encode_datetime(self):
#         dd = datetime.now(tz=pytz.UTC)
#
#         json_str = jsoner.dumps(dd)
#
#         self.assertEqual(
#             json.loads(json_str),
#             json.loads('{{"__obj_module__": "datetime", "__type__": '
#                        '"datetime", "__json_data__": {{"epoch": {}, "tz": "UTC"}}'
#                        '}}'.format(dd.timestamp()))
#         )
#
#     def test_003_encode_datetime_without_timezone(self):
#         dd = datetime.now()
#
#         json_str = jsoner.dumps(dd)
#
#         self.assertDictEqual(
#             json.loads(json_str),
#             json.loads('{{"__obj_module__": "datetime", "__type__":'
#                        ' "datetime", "__json_data__": {{"epoch": {}, '
#                        '"tz": null}}'
#                        '}}'.format(dd.timestamp()))
#         )
#
#     def test_004_encode_dummy_obj(self):
#         dummy = DummyObject1()
#         json_str = jsoner.dumps(dummy)
#         self.assertEqual(
#             json.loads(json_str),
#             json.loads('{"__type__": "DummyObject1", "__json_data__": "1234", '
#                        '"__obj_module__": "test_jsoner"}')
#         )
#
#     def test_005_encode_dummy_obj(self):
#         dummy = DummyObject2()
#         json_str = jsoner.dumps(dummy)
#         self.assertEqual(
#             json.loads(json_str),
#             json.loads('{"__type__": "DummyObject2", "__json_data__": {}, '
#                        '"__obj_module__": "test_jsoner"}')
#         )
#
#     def test_006_to_json_returns_no_str(self):
#         class Dummy:
#             def to_json(self):
#                 return 1
#
#             @classmethod
#             def from_json(cls):
#                 return cls()
#
#         self.assertRaises(JsonEncodingError, jsoner.dumps, Dummy())
#
#
# class TestJsonDecoder(unittest.TestCase):
#     def test_000_decode_list(self):
#         json_str = "[1, 2, 3, 4, 5]"
#         result = jsoner.loads(json_str)
#
#         self.assertEqual(result, [1, 2, 3, 4, 5])
#
#     def test_001_decode_dict(self):
#         json_str = '{"test": 123}'
#         result = jsoner.loads(json_str)
#
#         self.assertDictEqual(result, {'test': 123})
#
#     def test_002_decode_datetime(self):
#         dt = datetime.now()
#         json_str = jsoner.dumps(dt)
#         result = jsoner.loads(json_str)
#
#         self.assertEqual(result, dt)
#
#     def test_003_decode_embedded_object_from_dict(self):
#
#         obj = DummyObject3()
#         json_str = jsoner.dumps(obj)
#         result = jsoner.loads(json_str)
#
#         self.assertIsInstance(result.embedded_obj1, DummyObject1)
#         self.assertIsInstance(result.embedded_obj2, DummyObject2)
#         self.assertIsInstance(result, DummyObject3)
#
#     def test_004_decode_embedded_object_from_json(self):
#         obj = DummyObject4()
#         json_str = jsoner.dumps(obj)
#         result = jsoner.loads(json_str)
#
#         self.assertIsInstance(result.embedded_obj1, DummyObject1)
#         self.assertIsInstance(result.embedded_obj2, DummyObject2)
#         self.assertIsInstance(result, DummyObject4)
#
#     def test_005_decode_similar_dict(self):
#         """
#         Tests if the decoding works if a dict has the keys
#         `__obj_type__`, `__type__` and `__json_data__` but broken
#         data.
#
#         :return:
#         """
#         obj_dict = '{  \
#             "__obj_module__": "some.not_existing.module", \
#             "__type__": "some_not_existing_type",  \
#             "__json_data__": "empty"  \
#         }'
#         result = jsoner.loads(obj_dict)
#
#         self.assertDictEqual(result, json.loads(obj_dict))
#
#     def test_006_decode_similar_dict(self):
#
#         obj_dict = '{  \
#             "__obj_module__": "test", \
#             "__type__": null,  \
#             "__json_data__": null  \
#         }'
#         result = jsoner.loads(obj_dict)
#
#         self.assertDictEqual(result, json.loads(obj_dict))
#
#     def test_007_register_function_for_serialization(self):
#         @jsoner.encoding_registry(DummyObject5)
#         def encode(obj: DummyObject5):
#             return None
#
#         @jsoner.decoding_registry(DummyObject5)
#         def decode(data, obj_type):
#             self.assertIsNone(data)
#             return DummyObject5()
#
#         obj = DummyObject5()
#         json_str = jsoner.dumps(obj)
#
#         decoded_obj = jsoner.loads(json_str)
#
#         self.assertEqual(decoded_obj.a, obj.a)
