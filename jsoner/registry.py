from collections import UserDict
import typing as T
from importlib import import_module


class Registry(UserDict):
    @property
    def registry(self):
        return self.data

    def add(self, key, value):
        if key in self.data:
            msg = 'Key `{}` is already in the registry!'.format(key)
            raise KeyError(msg)

        self.data[key] = value

    def register(self, key):
        def inner(func):
            self.add(key, func)
            return inner
        return inner


class SubclassRegistry(Registry):
    def get(self, object_or_type: T.Any) -> T.Any:
        """
        Returns the registered function for the given object or type
        :param object_or_type:
        :return:
        """
        value = super().get(object_or_type)
        if value is not None:
            return value

        if isinstance(object_or_type, str):
            try:
                obj_type = import_object(object_or_type)
            except ImportError:
                return None

        elif isinstance(object_or_type, type):
            obj_type = object_or_type
        else:
            obj_type = object_or_type.__class__

        try:
            return self.data[obj_type]
        except KeyError:
            pass

        mro = obj_type.mro()
        # walk mro
        for cls in mro:
            for registered_cls, value in self.data.items():
                if isinstance(registered_cls, str):
                    try:
                        registered_cls = import_object(registered_cls)
                    except ImportError:
                        continue
                if cls is registered_cls:
                    return value
        else:
            return None


def import_object(path: str) -> type:
    module, _, obj = path.rpartition('.')
    if not module:
        module = import_module('__main__')
    else:
        try:
            module = import_module(module)
        except (ValueError, ModuleNotFoundError):
            msg = 'Empty module name. ' \
                  'Could not import object `{}`'.format(path)
            raise ImportError(msg)
    try:
        return getattr(module, obj)
    except AttributeError:
        msg = 'Could not import object `{}`'.format(path)
        raise ImportError(msg)

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
