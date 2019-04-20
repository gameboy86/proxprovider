from collections import namedtuple

import random


ProxyAddress = namedtuple('ProxyAddress', 'type address')


class Proxies:
    def __init__(self, proxies_dict):
        self.__proxies_list = set()
        self.__proxies_used = set()
        self.__proxies_blocked = set()

        for p, addresses in proxies_dict.items():
            self.__proxies_list.update(
                [
                    ProxyAddress(
                        type=p,
                        address=address
                    ) for address in addresses
                ]
            )

    def __str__(self):
        return "(total: {}, unused: {}, used: {}, blocked: {})".format(
            len(self.all), len(self.unused), len(self.used), len(self.blocked)
        )

    @property
    def all(self):
        return self.__proxies_list

    @property
    def used(self):
        return self.__proxies_used

    @property
    def blocked(self):
        return self.__proxies_blocked

    @property
    def unused(self):
        return self.__proxies()

    def __proxies(self, use_blocked=False, use_used=False):
        if not use_blocked and not use_used:
            ps = (
                self.__proxies_list ^ (
                    self.__proxies_blocked | self.__proxies_used
                )
            )
        elif use_blocked and use_used:
            ps = self.__proxies_list

        elif use_blocked:
            ps = (
                self.__proxies_list ^ self.__proxies_used
            )
        else:
            ps = (
                self.__proxies_list ^ self.__proxies_blocked
            )
        ps = list(ps)
        random.shuffle(ps)
        return ps

    def block_address(self, address):
        self.block_addresses([address])

    def block_addresses(self, addresses):
        self.__proxies_used -= {*addresses}
        self.__proxies_blocked.update(addresses)

    def clear_blocked(self):
        self.__proxies_blocked = set()

    def clear_used(self):
        self.__proxies_used = set()

    def get_proxy(self, use_blocked=False, use_used=False):
        ps = self.__proxies(use_blocked, use_used)
        if not ps:
            return None
        self.__proxies_used.add(ps[0])
        return ps[0]

    def get_proxies(self, count=None, use_blocked=False, use_used=False):
        ps = self.__proxies(use_blocked, use_used)
        if not ps:
            return []
        if count is not None:
            ps = ps[:count]
        self.__proxies_used.update(ps)
        return ps
