import unittest


from ..providers import ProxyProviderModelBase
from ..api import ProxProviderApi
from ..utils import convert_name


class TestProxProviderApi(unittest.TestCase):
    def setUp(self):
        pass

    def test_registry_provider(self):
        class TestProvider(ProxyProviderModelBase):
            """TEST DOC"""
            def proxies(self):
                return ['192.168.1.1:8081']

        name = convert_name(TestProvider.__name__)
        self.assertTrue(name in ProxProviderApi.available_providers())
        pro = next(
            (
                d for d in ProxProviderApi.imported_providers()
                if d['name'] == name
            ),
            None
        )

        self.assertEqual(pro['doc'], 'TEST DOC')
