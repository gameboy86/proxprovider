import requests

from . import ProxProviderModelBase


class ProxyList(ProxProviderModelBase):
    """Provider for https://www.proxy-list.download.
    Required parameters:
        protocols: List, acceptable values are 'http', 'https'
        types: List, acceptable values are 'anonymous', 'elite'
    Additional parameters:
        timeout: http timeout (default: 2s)
    """
    def proxies(self, protocols, types, timeout=2):
        protocols = protocols or ['http', 'https']
        types = types or ['anonymous', 'elite']

        out = []
        for (p, t) in [(a, b) for a in protocols for b in types]:
            response = requests.get(
                'https://www.proxy-list.download/api/'
                'v1/get?type={}&anon={}'.format(
                    p, t
                ),
                timeout=timeout
            )
            contents = response.text.split('\r\n')
            out.extend([item for item in contents if item])
        return out
