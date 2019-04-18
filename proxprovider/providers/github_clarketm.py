import requests

from . import ProxyProviderModelBase


class GithubClarketm(ProxyProviderModelBase):
    """
    Simple provider witch download proxies from github 'Clarketm'
    Additional parameters:
        timeout: http timeout (default: 2s)
    """
    def proxies(self, timeout=2):
        url = "https://raw.githubusercontent.com/clarketm/" \
              "proxy-list/master/proxy-list.txt"
        out = []
        content = requests.get(
            url,
            timeout=timeout
        ).text.splitlines()
        for line in content:
            line = line.split(' ')
            if len(line) == 4:
                out.append(line[0])
        return out
