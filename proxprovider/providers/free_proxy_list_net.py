import requests
import bs4

from . import ProxProviderModelBase


class FreeProxyListNet(ProxProviderModelBase):
    """
    Provider for https://free-proxy-list.net/.
    Additional parameters:
        timeout: http timeout (default: 2s)
        only_https: return only https proxy
        anonymity: can be ['elite proxy', 'anonymous', 'transparent']
    """
    def proxies(self, only_https=False, anonymity=None, timeout=2):

        out = []
        soup = bs4.BeautifulSoup(
            requests.get(
                "https://free-proxy-list.net/", timeout=timeout
            ).text,
            'html.parser'
        )
        trs = soup.find('table', attrs={'id': 'proxylisttable'}).find_all('tr')
        for i, tr in enumerate(trs):
            if i == 0:
                # Table header
                continue
            if len(tr) != 8:
                continue

            if tr.find('th'):
                continue

            tds = tr.find_all('td')
            if only_https and tds[6].text == 'no':
                continue

            if anonymity is not None and tds[4].text != anonymity:
                continue

            out.append("http://{host}:{port}".format(
                host=tds[0].text, port=tds[1].text
            ))

        return out
