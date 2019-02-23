

import json
import unittest
from datetime import datetime

import pytz

from ..serialization import JsonerSerializable
from ..serialization import DictConvertible
from ..serialization import StrConvertible
from ..serialization import JsonEncoder
from ..registry import encoders
from ..registry import decoders


class TestJsonSerializable(unittest.TestCase):

    def test_000_primitive_type(self):
        self.assertFalse(isinstance(42, JsonerSerializable))

    def test_001_registered_type(self):
        class Dummy:
            pass

        encoders.add(Dummy, 42)
        decoders.add(Dummy, 42)

        self.assertTrue(isinstance(Dummy(), JsonerSerializable))

        del encoders[Dummy]
        del decoders[Dummy]

    def test_002_registered_type(self):
        class Dummy:
            pass

        encoders.add(Dummy, 42)
        decoders.add(Dummy, 42)

        self.assertFalse(isinstance(Dummy, JsonerSerializable))

        del encoders[Dummy]
        del decoders[Dummy]

    def test_003_registered_type(self):
        class Dummy:
            pass

        encoders.add(Dummy, 42)
        decoders.add(Dummy, 42)

        self.assertTrue(issubclass(Dummy, JsonerSerializable))

        del encoders[Dummy]
        del decoders[Dummy]

    def test_000_dict_convertible(self):
        class A:
            def to_dict(self) -> dict:
                return {}

            def from_dict(self, d: dict) -> 'A':
                return A()

        self.assertTrue(isinstance(A(), JsonerSerializable))
        self.assertTrue(issubclass(A, JsonerSerializable))


class TestDictConvertible(unittest.TestCase):
    def test_000_dict_convertible(self):
        class A:
            def to_dict(self) -> dict:
                return {}

            def from_dict(self, d: dict) -> 'A':
                return A()

        self.assertTrue(isinstance(A(), DictConvertible))
        self.assertTrue(issubclass(A, DictConvertible))


class TestStrConvertible(unittest.TestCase):
    def test_000_str_convertible(self):
        class A:
            def to_str(self) -> str:
                return ''

            def from_str(self, s: str) -> 'A':
                return A()

        self.assertTrue(isinstance(A(), StrConvertible))
        self.assertTrue(issubclass(A, StrConvertible))


class Dummy:
    pass


class DummyDictConvertible:
    def to_dict(self) -> dict:
        return {}

    def from_dict(self, d: dict) -> 'DummyDictConvertible':
        return self.__class__()


class DummyStrConvertible:
    def to_str(self) -> str:
        return ''

    def from_str(self, s: str) -> 'DummyStrConvertible':
        return self.__class__()


class TestJsonEncoder(unittest.TestCase):
    # def test_000_encode_dict(self):
    #     json_str = dumps({'test': 123})
    #
    #     self.assertEqual(json_str, '{"test": 123}')
    #
    # def test_001_encode_list(self):
    #     json_str = dumps([1, 2, 3, 4, 5])
    #
    #     self.assertEqual(json_str, '[1, 2, 3, 4, 5]')
    #
    def test_000_default_pass_dict(self):
        encoder = JsonEncoder()

        result = encoder.encode({'foo': 42})
        expected = '{"foo": 42}'

        self.assertEqual(result, expected)

    def test_001_default_pass_int(self):
        encoder = JsonEncoder()

        result = encoder.encode(42)
        expected = '42'

        self.assertEqual(result, expected)

    def test_002_pass_dict_convertible_object(self):
        encoder = JsonEncoder()

        result = encoder.encode(DummyDictConvertible())
        result = json.loads(result)
        expected = '{"__obj_cls__": "jsoner.tests.test_serialization.DummyDictConvertible", ' \
                   '"__json_data__": {}}'
        expected = json.loads(expected)

        self.assertDictEqual(result, expected)

    def test_003_pass_str_convertible_object(self):
        encoder = JsonEncoder()

        result = encoder.encode(DummyStrConvertible())
        result = json.loads(result)
        expected = '{"__obj_cls__": "jsoner.tests.test_serialization.DummyStrConvertible", ' \
                   '"__json_data__": ""}'
        expected = json.loads(expected)

        self.assertDictEqual(result, expected)

    def test_004_in_registry(self):
        encoder = JsonEncoder()

        class A:
            pass

        @encoders.register(A)
        def encode(obj: A) -> str:
            return ''

        @decoders.register(A)
        def decode(data: str) -> A:
            return A()

        result = encoder.encode(A())

        expected = {
            '__obj_cls__' : A.__module__ + '.' + A.__qualname__,
            '__json_data__': ''
        }
        self.assertDictEqual(json.loads(result), expected)

        del encoders[A]
        del decoders[A]

    def test_005_in_registry(self):
        encoder = JsonEncoder()

        class A:
            pass

        encoders.add(A, 42)
        decoders.add(A, A())

        result = encoder.encode(A())
        expected = {
            '__obj_cls__': A.__module__ + '.' + A.__qualname__,
            '__json_data__': 42
        }

        self.assertDictEqual(json.loads(result), expected)

        del encoders[A]
        del decoders[A]

    def test_006_encode_cls(self):
        encoder = JsonEncoder()

        encoders.add(Dummy, 42)
        decoders.add(Dummy, Dummy())

        self.assertTrue(issubclass(Dummy, JsonerSerializable))

        result = encoder.encode(Dummy)
        expected = {'__cls__': Dummy.__module__ + '.' + Dummy.__qualname__}
        self.assertDictEqual(json.loads(result), expected)

        del encoders[Dummy]
        del decoders[Dummy]

    def test_007_encode_str(self):
        encoder = JsonEncoder()

        result = encoder.encode('foo')
        expected = "foo"
        self.assertEqual(json.loads(result), expected)

    def test_008_not_in_registry(self):
        encoder = JsonEncoder()

        class Dummy:
            pass

        self.assertRaises(TypeError, encoder.encode, Dummy())
