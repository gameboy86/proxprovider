proxprovider
============
.. image:: https://travis-ci.org/gameboy86/proxprovider.svg?branch=master
   :target: https://travis-ci.org/gameboy86/proxprovider



``proxprovider`` is a module witch help to use many source of proxy (called providers)
in simply and consist way.

Usage
-----

.. code-block:: python

    >>> from proxprovider import ProxProviderApi
    >>> prox = ProxProviderApi()
    >>> proxies_list = prox.proxies()
    >>> print(proxies_list)
    (total: 300, unused: 300, used: 0, blocked: 0)
    >>> addresses = proxies_list.get_proxies(count=10)
    >>> print(addresses)
    [ProxyAddress(type='github_clarketm', address='68.183.39.251:80'),
     ProxyAddress(type='github_clarketm', address='36.37.89.98:32323'),
     ProxyAddress(type='github_clarketm', address='172.245.52.197:80'),
     ProxyAddress(type='github_clarketm', address='119.52.28.130:8080'),
     ProxyAddress(type='github_clarketm', address='144.76.45.24:8080'),
     ProxyAddress(type='github_clarketm', address='78.186.169.88:8080'),
     ProxyAddress(type='github_clarketm', address='221.126.249.100:8080'),
     ProxyAddress(type='github_clarketm', address='80.211.36.44:3128'),
     ProxyAddress(type='github_clarketm', address='177.11.116.199:8080'),
     ProxyAddress(type='github_clarketm', address='103.31.251.202:8080')]
    >>> print(proxies_list, type(proxies_list))
    (total: 300, unused: 290, used: 10, blocked: 0),  <class 'proxprovider.proxy.Proxies'>


Providers
---------

Providers are classes witch return proxies from different sources. By default,
proxprovider contains:

.. code-block:: python

    >>> ProxProviderApi.available_providers()
    ['proxy_list', 'github_clarketm', 'from_file', 'buy_proxies']
    >>> ProxProviderApi.imported_providers()
    [{'doc': "Provider for https://www.proxy-list.download.\n    Required parameters:\n        protocols: List, acceptable values are 'http', 'https'\n        types: List, acceptable values are 'anonymous', 'elite'\n    Additional parameters:\n        timeout: http timeout (default: 2s)\n    ",
      'name': 'proxy_list'},
     {'doc': "\n    Simple provider witch download proxies from github 'Clarketm'\n    Additional parameters:\n        timeout: http timeout (default: 2s)\n    ",
      'name': 'github_clarketm'},
     {'doc': '\n    Simple provider with reading proxies from file. There must be only one\n    proxy for line.\n    Required parameters:\n        file_path: Path to file\n    ',
      'name': 'from_file'},
     {'doc': '\n    Provider for http://buyproxies.org/.\n    Required parameters:\n        pid, key: credentials required for provider api\n    Additional parameters:\n        timeout: http timeout (default: 2s)\n    ',
      'name': 'buy_proxies'}]


New providers can be created in simply way. It mast be class witch inherit from
`ProxyProviderModelBase` and implement `proxies` method. For example:

.. code-block:: python

    >>> from proxprovider.providers import ProxyProviderModelBase
    >>> class SimpleProvider(ProxyProviderModelBase):
            def proxies(self):
                return ['129.168.1.1:8080']
    >>> ProxProviderApi.available_providers()
    ['simple_provider',
     'proxy_list',
     'github_clarketm',
     'from_file',
     'buy_proxies']
    >>> prox = ProxProviderApi(providers=['simple_provider'])
    >>> proxies_list = prox.proxies()
    >>> print(proxies_list)
    (total: 1, unused: 1, used: 0, blocked: 0)
    >>> proxies_list.get_proxies()
    [ProxyAddress(type='simple_provider', address='129.168.1.1')]


If, there is need to pass some additional data to providers, its must be
specified in `proxies` method and passed to `ProxProviderApi` on initiation step.
If data will not be pass but they are required by method `proxies`,
provider will be skipped and another providers will be used

.. code-block:: python

    >>> class SimpleProvider(ProxyProviderModelBase):
            def proxies(self, add_proxies):
                if (
                    isinstance(add_proxies, list)
                ):
                    add_proxies.append('10.0.1.1:8080')
                return add_proxies
    >>> prox = ProxProviderApi(providers=['simple_provider'])
    >>> proxies_list = prox.proxies()
    WARNING:root:provider 'simple_provider' proxies() missing 1 required positional argument: 'add_proxies'
    >>> print(proxies_list)
    (total: 0, unused: 0, used: 0, blocked: 0)
    >>> prox = ProxProviderApi(providers=['simple_provider'], providers_config={
                   'simple_provider': {'add_proxies': ['10.0.10.10:8808']}
               })
    >>> proxies_list = prox.proxies()
    >>> print(proxies_list)
    (total: 2, unused: 2, used: 0, blocked: 0)

