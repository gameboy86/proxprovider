from concurrent import futures
import functools
from importlib import import_module
import inspect
from os import listdir, path

from . import utils
from . import proxy
from .exceptions import ProviderException

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


class ProxProviderApi:
    __registry = {}
    __cache = {}
    __imported_models = []

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

        for name in [
            x for x in listdir(
                path.join(
                    path.split(
                        inspect.getfile(ProxProviderApi)
                    )[0],
                    'providers'
                )
            )
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
    def clear_cache(cls, providers=None):
        if providers is None:
            cls.__cache = {}
        for prov in providers:
            del cls.__cache[prov]

    @classmethod
    def registry_provider(cls, cls_obj):
        cls.__registry[
            utils.convert_name(cls_obj.__name__)
        ] = cls_obj

    def __init__(
        self, use_cache=True, providers=None, providers_config=None
    ):
        self.providers = providers
        self.providers_config = providers_config
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

    def __provider_from_cache(self, provider):
        return self.__cache.get(provider)

    def __proxies_for_provider(self, provider):
        conf = self.provider_config(provider)

        omit_cache = (
            conf.get('omit_cache')
            if conf else False
        )

        cache = self.__provider_from_cache(provider)
        if self.use_cache and cache and not omit_cache:
            return cache

        try:
            func = getattr(
                self, '_{}_get_proxies'.format(provider)
            )
            proxies = func()

        except ProviderException as e:
            logging.warning("provider '{}' {}".format(
                provider, e.args[0]
            ))
            return
        if self.use_cache and not omit_cache:
            self.__cache[provider] = proxies
        return proxies

    def provider_config(self, provider):
        if self.providers_config:
            return self.providers_config.get(provider)
        return None

    def proxies(self):
        out = {}
        with futures.ThreadPoolExecutor(max_workers=4) as executor:
            to_do = {}

            for name, class_ in list(self.__registry.items()):
                if self.providers and name not in self.providers:
                    continue

                future = executor.submit(self.__proxies_for_provider, name)
                to_do[name] = future

            for name, future in to_do.items():
                f = future
                if f.exception():
                    logging.exception("provider '{}' {}".format(
                        name, f.exception()
                    ))
                else:
                    if f.result():
                        out.update({name: f.result()})
        return proxy.Proxies(out)
