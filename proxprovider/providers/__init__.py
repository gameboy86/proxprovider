import functools

from ..api import ProxProviderApi
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


def remove_extra_parameters(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            kwargs.pop('omit_cache')
        except KeyError:
            pass
        return function(*args, **kwargs)
    return wrapper


class ProxProviderModelsRegister(type):
    def __init__(cls, name, bases, class_dict):
        if bases:
            ProxProviderApi.registry_provider(cls)

        super().__init__(
            name, bases, class_dict
        )


class ProxProviderModelBase(metaclass=ProxProviderModelsRegister):
    def __new__(cls, *args, **kwargs):
        cls.proxies = remove_extra_parameters(exception(cls.proxies))
        return super().__new__(cls)

    def proxies(self, **kwargs):
        raise NotImplementedError
