import binascii
import os
import random
from collections import defaultdict, OrderedDict, Iterable


def generate_random_bits(length):
    return binascii.b2a_hex(os.urandom(length // 8)).decode()


def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


def atoi(s):
    int_max = 2147483647
    int_min = -2147483648
    result = 0

    if not s:
        return result

    i = 0
    while i < len(s) and s[i].isspace():
        i += 1

    sign = 1
    if s[i] == "+":
        i += 1
    elif s[i] == "-":
        sign = -1
        i += 1

    while i < len(s) and '0' <= s[i] <= '9':
        if result > (int_max - (ord(s[i]) - ord('0'))) / 10:
            return int_max if sign > 0 else int_min
        result = result * 10 + ord(s[i]) - ord('0')
        i += 1

    return sign * result


def infinite_dict():
    return defaultdict(infinite_dict)


class OrderedDefaultDict(OrderedDict):
    def __init__(self, default_callable=None, *a, **kw):
        if (default_callable is not None and not callable(default_callable)):
            raise TypeError('First argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_callable = default_callable

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_callable is None:
            raise KeyError(key)
        self[key] = value = self.default_callable()
        return value

    def copy(self):
        return type(self)(self.default_callable, self)

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_callable,
                                               OrderedDict.__repr__(self))


def infinite_ordered_dict():
    return OrderedDefaultDict(infinite_ordered_dict)


def flatten(items, ignore_types=(str, bytes)):
    for item in items:
        if isinstance(item, Iterable) and not isinstance(item, ignore_types):
            yield from flatten(item, ignore_types)
        else:
            yield item


def generator_random_uint32(start=0, end=4294967294):
    while True:
        yield random.randint(start, end)
