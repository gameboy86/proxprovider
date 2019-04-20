import inspect
from os import path

from .api import ProxProviderApi


__all__ = ['ProxProviderApi']

ProxProviderApi.registry_dir(
    path.join(
        path.split(inspect.getfile(ProxProviderApi))[0], 'providers'
    )
)
ProxProviderApi.loads_models()
