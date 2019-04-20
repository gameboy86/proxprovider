import functools

from ..api import ProxyApi
from ..exceptions import ProviderException


def exception(function):
    """
    A decorator that wraps the passed in function and convert any Exception
    to ProviderException
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            raise ProviderException(e)

    return wrapper


class ProxyProviderModelsRegister(type):
    def __init__(cls, name, bases, class_dict):
        if bases:
            ProxyApi.registry_provider(cls)

        super().__init__(
            name, bases, class_dict
        )


class ProxyProviderModelBase(metaclass=ProxyProviderModelsRegister):
    def __new__(cls, *args, **kwargs):
        cls.proxies = exception(cls.proxies)
        return super().__new__(cls)

    def proxies(self, **kwargs):
        raise NotImplementedError
