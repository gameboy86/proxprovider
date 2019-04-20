import unittest

from ..proxy import Proxies


class TestProxies(unittest.TestCase):

    def setUp(self):
        self.prox = Proxies({
            'type_a': ['10.0.0.1:8080', '10.0.0.2:8080'],
            'type_b': ['10.0.1.1:8081', '10.0.1.2:8081'],
        })

    def test_block_unblock_address(self):
        p = self.prox.get_proxy()
        self.assertEqual(len(self.prox.unused), 3)
        self.assertEqual(len(self.prox.used), 1)
        self.assertEqual(len(self.prox.blocked), 0)

        self.prox.block_address(p)
        self.assertEqual(len(self.prox.unused), 3)
        self.assertEqual(len(self.prox.used), 0)
        self.assertEqual(len(self.prox.blocked), 1)

        self.prox.clear_blocked()
        self.assertEqual(len(self.prox.unused), 4)
        self.assertEqual(len(self.prox.used), 0)
        self.assertEqual(len(self.prox.blocked), 0)

    def test_get_proxies(self):
        self.assertEqual(len(self.prox.all), 4)
        self.assertEqual(len(self.prox.unused), 4)
        self.assertEqual(len(self.prox.used), 0)
        used_proxies = self.prox.get_proxies(2)

        self.assertEqual(len(used_proxies), 2)
        self.assertEqual(len(self.prox.unused), 2)
        self.assertEqual(len(self.prox.used), 2)

        used_proxies = self.prox.get_proxies(2)
        self.assertEqual(len(used_proxies), 2)
        self.assertEqual(len(self.prox.unused), 0)
        self.assertEqual(len(self.prox.used), 4)

        used_proxies = self.prox.get_proxies(2)
        self.assertEqual(len(used_proxies), 0)

        used_proxies = self.prox.get_proxies(2, use_used=True)
        self.assertEqual(len(used_proxies), 2)

        self.prox.clear_used()
        used_proxies = self.prox.get_proxies()
        self.prox.block_addresses(used_proxies)

        used_proxies = self.prox.get_proxies()
        self.assertEqual(len(used_proxies), 0)
        self.assertEqual(len(self.prox.unused), 0)
        self.assertEqual(len(self.prox.used), 0)
        self.assertEqual(len(self.prox.blocked), 4)

        used_proxies = self.prox.get_proxies(use_blocked=True)
        self.assertEqual(len(used_proxies), 4)

    def test_get_proxy(self):
        self.prox.get_proxy()
        used_proxy = self.prox.get_proxy()
        self.prox.block_address(used_proxy)
        self.assertEqual(len(self.prox.unused), 2)
        self.assertEqual(len(self.prox.used), 1)
        self.assertEqual(len(self.prox.blocked), 1)

        self.prox.get_proxy()
        self.prox.get_proxy()

        self.assertEqual(len(self.prox.unused), 0)
        self.assertEqual(len(self.prox.used), 3)
        self.assertEqual(len(self.prox.blocked), 1)

        used_proxy = self.prox.get_proxy()

        self.assertIsNone(used_proxy)

        used_proxy = self.prox.get_proxy(use_used=True, use_blocked=True)
        self.assertIsNotNone(used_proxy)
