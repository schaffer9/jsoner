from unittest import TestCase

from jsoner.registry import Registry, SubclassRegistry, import_object


class TestRegistry(TestCase):
    def test_000_init(self):
        r = Registry()

        self.assertDictEqual(r.registry, {})

    def test_001_add(self):
        r = Registry()
        r.add('A', 42)

        self.assertEqual(r['A'], 42)
        self.assertDictEqual(dict(r.registry), {'A': 42})

    def test_002_add_causes_error_if_key_exists(self):
        r = Registry()
        r.add('A', 42)

        self.assertRaises(KeyError, r.add, 'A', 42)

    def test_003_register_decorator(self):
        r = Registry()

        @r.register('A')
        def foo():
            return 42

        self.assertEqual(r['A'](), 42)

    def test_004_register_same_key_twice(self):
        """
        If the same key is registered twice, a :exc:`KeyError` is raised.
        Returns
        -------

        """
        r = Registry()

        def foo():
            return 42
        foo()
        r.register('A')(foo)

        self.assertIs(r.get('A'), foo)
        with self.assertRaises(KeyError):
            r.register('A')(foo)

    def test_005_add_none(self):
        r = Registry()

        r.add('A', None)

        self.assertEqual(r['A'], None)

    def test_006_get(self):
        r = Registry()

        r.add('A', 42)

        self.assertEqual(r.get('A'), 42)

    def test_007_get_key_not_found(self):
        r = Registry()

        self.assertIsNone(r.get(42))


class DummyObject:
    pass


class TestSubclassRegistry(TestCase):
    def test_000_get_subclass_of_class(self):
        class A:
            pass

        class B(A):
            pass

        r = SubclassRegistry()
        r.add(A, 42)

        self.assertEqual(r.get(A), 42)
        self.assertEqual(r.get(B), 42)

    def test_001_get_subclass_of_object(self):
        class A:
            pass

        class B(A):
            pass

        r = SubclassRegistry()
        r.add(A, 42)

        a = A()
        b = B()

        self.assertEqual(r.get(a), 42)
        self.assertEqual(r.get(b), 42)

    def test_002_register_as_string(self):
        r = SubclassRegistry()
        r.add('jsoner.tests.test_registry.DummyObject', 42)

        self.assertEqual(r.get(DummyObject), 42)

    def test_003_register_as_type_and_get_as_string(self):
        r = SubclassRegistry()
        r.add(DummyObject, 42)

        self.assertEqual(r.get('jsoner.tests.test_registry.DummyObject'), 42)

    def test_004_register_normal_string(self):
        r = SubclassRegistry()
        r.add('abc', 42)

        self.assertEqual(r.get('abc'), 42)

    def test_005_register_normal_string(self):
        r = SubclassRegistry()

        self.assertEqual(r.get('abc'), None)

    def test_006_not_existing_module(self):
        r = SubclassRegistry()
        r.add('foo.bar', 42)

        self.assertEqual(r.get('foo.bar'), 42)
        self.assertIsNone(r.get(DummyObject))

    def test_007_add_integer_as_key(self):
        r = SubclassRegistry()
        r.add(42, 'foo')

        self.assertEqual(r.get(42), 'foo')
        self.assertIsNone(r.get(DummyObject))

    def test_008_pass_list(self):
        r = SubclassRegistry()

        self.assertEqual(r.get((1, 2, 3)), None)
        self.assertIsNone(r.get(DummyObject))


class TestImportObject(TestCase):
    def test_000_import_dummy_object(self):
        obj = import_object('jsoner.tests.test_registry.DummyObject')
        self.assertIs(obj, DummyObject)

    def test_001_invalid_str(self):
        with self.assertRaises(ImportError):
            import_object('foo')

    def test_001_pass_invalid_module(self):
        with self.assertRaises(ImportError):
            import_object('foo.bar')

    def test_002_pass_invalid_argument(self):
        with self.assertRaises(ImportError):
            import_object('jsoner.tests.test_registry.Bar')
