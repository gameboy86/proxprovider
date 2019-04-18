import requests

from . import ProxyProviderModelBase


class BuyProxies(ProxyProviderModelBase):
    """
    Provider for http://buyproxies.org/.
    Required parameters:
        pid, key: credentials required for provider api
    Additional parameters:
        timeout: http timeout (default: 2s)
    """
    def proxies(self, pid, key, timeout=2):
        url = "http://api.buyproxies.org/?a=showProxies&pid={}&key={}".format(
            pid, key
        )
        out = []
        for line in requests.get(url, timeout=timeout).text.splitlines():
            line = line.split(':')
            if len(line) != 4:
                continue
            out.append("http://{login}:{passwd}@{host}:{port}".format(
                login=line[3], passwd=line[2], host=line[0],
                port=line[1]
            ))
        return out
