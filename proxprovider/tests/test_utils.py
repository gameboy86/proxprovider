import unittest

from ..utils import convert_name


class TestUtils(unittest.TestCase):
    def test_convert_name(self):
        self.assertEqual(convert_name('TestProxy'), 'test_proxy')
        self.assertEqual(convert_name('testProxy'), 'test_proxy')
        self.assertEqual(convert_name('testproxy'), 'testproxy')
        self.assertEqual(convert_name('Testproxy'), 'testproxy')
