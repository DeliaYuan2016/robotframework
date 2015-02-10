import unittest

from robot.utils.asserts import assert_equal, assert_not_equal, assert_raises
from robot.utils import DotDict, OrderedDict


class TestDotDict(unittest.TestCase):

    def setUp(self):
        self.dd = DotDict([('z', 1), (2, 'y'), ('x', 3)])

    def test_get(self):
        assert_equal(self.dd[2], 'y')
        assert_equal(self.dd.x, 3)
        assert_raises(KeyError, self.dd.__getitem__, 'nonex')
        assert_raises(AttributeError, self.dd.__getattr__, 'nonex')

    def test_equality_with_normal_dict(self):
        assert_equal(self.dd, {'z': 1, 2: 'y', 'x': 3})

    def test_set(self):
        self.dd.x = 42
        self.dd.new = 43
        self.dd[2] = 44
        self.dd['n2'] = 45
        assert_equal(self.dd, {'z': 1, 2: 44, 'x': 42, 'new': 43, 'n2': 45})

    def test_del(self):
        del self.dd.x
        del self.dd[2]
        self.dd.pop('z')
        assert_equal(self.dd, {})
        assert_raises(KeyError, self.dd.__delitem__, 'nonex')
        assert_raises(AttributeError, self.dd.__delattr__, 'nonex')

    def test_same_str_and_repr_as_with_normal_dict(self):
        d = {'foo': 'bar', '"\'': '"\'', '\n': '\r', 1: 2, (): {}, True: False}
        assert_equal(str(DotDict(d)), str(d))
        assert_equal(repr(DotDict(d)), repr(d))

    def test_is_ordered(self):
        assert_equal(list(self.dd), ['z', 2, 'x'])
        self.dd.z = 'new value'
        self.dd.a_new_item = 'last'
        self.dd.pop('x')
        assert_equal(self.dd.items(), [('z', 'new value'), (2, 'y'),
                                       ('a_new_item', 'last')])
        self.dd.x = 'last'
        assert_equal(self.dd.items(), [('z', 'new value'), (2, 'y'),
                                       ('a_new_item', 'last'), ('x', 'last')])

    def test_order_does_not_affect_equality(self):
        d = dict(a=1, b=2)
        od1 = OrderedDict(sorted(d.items()))
        od2 = OrderedDict(reversed(d.items()))
        dd1 = DotDict(sorted(d.items()))
        dd2 = DotDict(reversed(d.items()))
        for d1, d2 in [(dd1, d), (dd2, d), (dd1, od1), (dd1, od2),
                       (dd2, od1), (dd2, od2), (dd1, dd2)]:
            assert_equal(d1, d2)
            assert_equal(d2, d1)
        assert_not_equal(od1, od2)


if __name__ == '__main__':
    unittest.main()