import functools
from importlib import import_module
from os import listdir

from . import utils
from . import proxy
from .exceptions import ProviderException

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


class ProxyApi:
    __registry = {}
    __cache = {}
    __models_dirs = None
    __imported_models = []

    @classmethod
    def registry_dir(cls, dir_path):
        if cls.__models_dirs is None:
            cls.__models_dirs = []
        cls.__models_dirs.append(dir_path)

    @classmethod
    def imported_providers(cls):
        return sorted([
            {
                'name': reg,
                'doc': cls_.__doc__,
            }
            for reg, cls_ in list(cls.__registry.items())
        ], key=lambda x: sorted(x.keys()), reverse=True)

    @classmethod
    def model_by_key(cls, key):
        return cls.__registry.get(key)

    @classmethod
    def available_providers(cls):
        return [p['name'] for p in cls.imported_providers()]

    @classmethod
    def loads_models(cls):
        if cls.__imported_models:
            cls.__imported_models = []

        for dir_ in cls.__models_dirs:
            for name in [
                x for x in listdir(dir_)
                if 'pyc' not in x and '__init__' not in x
            ]:
                try:
                    import_module(
                        'proxprovider.providers.{}'.format(name.split('.')[0])
                    )
                    cls.__imported_models.append(name)
                except ImportError as e:
                    print(e)

    @classmethod
    def clear_cache(cls):
        cls.__cache = {}

    @classmethod
    def registry_provider(cls, cls_obj):
        cls.__registry[
            utils.convert_name(cls_obj.__name__)
        ] = cls_obj

    def __init__(
        self, use_cache=True, providers=None, providers_config=None
    ):
        self.providers = providers
        self.use_cache = use_cache

        for name, class_ in list(self.__registry.items()):
            if providers and name not in providers:
                continue
            kwargs = {'name': name}
            if providers_config and providers_config.get(name):
                kwargs.update(providers_config.get(name))
            if 'proxies' in class_.__dict__:
                setattr(
                    self,
                    '_{}_get_proxies'.format(name),
                    functools.partial(
                        self.__proxies,
                        **kwargs
                    )
                )

    def __str__(self):
        return "({})".format(self.use_cache)

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            self.use_cache
        )

    def __proxies(self, name, *args, **kwargs):
        return self.model_by_key(name)().proxies(*args, **kwargs)

    def proxies(self):
        if self.__cache and self.use_cache:
            return self.__cache

        out = {}
        for name, class_ in list(self.__registry.items()):
            if self.providers and name not in self.providers:
                continue
            try:
                func = getattr(
                    self, '_{}_get_proxies'.format(name)
                )
                out[name] = func()

            except ProviderException as e:
                logging.warning("provider '{}' {}".format(
                    name, e.args[0]
                ))

        self.__cache = proxy.Proxies(out)
        return self.__cache
