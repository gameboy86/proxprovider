import inspect
from os import path

from .api import ProxyApi


__all__ = ['ProxyApi']

ProxyApi.registry_dir(
    path.join(
        path.split(inspect.getfile(ProxyApi))[0], 'providers'
    )
)
ProxyApi.loads_models()

