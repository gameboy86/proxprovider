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

