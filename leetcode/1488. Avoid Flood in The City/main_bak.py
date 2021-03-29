# from collections import defaultdict,OrderedDict,Callable
from collections import Callable
from itertools import dropwhile


def get_last_key(dict_now):
    return next(reversed(dict_now))


# try:
#     from thread import get_ident as _get_ident
# except ImportError:
#     try:
#          from dummy_thread import get_ident as _get_ident
#     except ImportError:
#          from _dummy_thread import get_ident as _get_ident

try:
    from _abcoll import KeysView, ValuesView, ItemsView
except ImportError:
    pass


class OrderedDict(dict):
    'Dictionary that remembers insertion order'

    # An inherited dict maps keys to values.
    # The inherited dict provides __getitem__, __len__, __contains__, and get.
    # The remaining methods are order-aware.
    # Big-O running times for all methods are the same as for regular dictionaries.

    # The internal self.__map dictionary maps keys to links in a doubly linked list.
    # The circular doubly linked list starts and ends with a sentinel element.
    # The sentinel element never gets deleted (this simplifies the algorithm).
    # Each link is stored as a list of length three:  [PREV, NEXT, KEY].

    def __init__(self, *args, **kwds):
        '''Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.
        '''
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root

        except AttributeError:
            self.__root = root = []  # sentinel node
            root[:] = [root, root, None]
            self.__map = {}
        self.__update(*args, **kwds)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        'od.__setitem__(i, y) <==> od[i]=y'
        # Setting a new item creates a new link which goes at the end of the linked
        # list, and the inherited dictionary is updated with the new key/value pair.
        if key not in self:
            root = self.__root
            last = root[0]
            last[1] = root[0] = self.__map[key] = [last, root, key]
        dict_setitem(self, key, value)

    def __delitem__(self, key, dict_delitem=dict.__delitem__):
        'od.__delitem__(y) <==> del od[y]'
        # Deleting an existing item uses self.__map to find the link which is
        # then removed by updating the links in the predecessor and successor nodes.
        dict_delitem(self, key)
        link_prev, link_next, key = self.__map.pop(key)
        link_prev[1] = link_next
        link_next[0] = link_prev

    def __iter__(self):
        'od.__iter__() <==> iter(od)'
        root = self.__root
        curr = root[1]
        while curr is not root:
            yield curr[2]
            curr = curr[1]

    def __reversed__(self):
        'od.__reversed__() <==> reversed(od)'
        root = self.__root
        curr = root[0]
        while curr is not root:
            yield curr[2]
            curr = curr[0]

    def clear(self):
        'od.clear() -> None.  Remove all items from od.'
        try:
            for node in self.__map.itervalues():
                del node[:]
            root = self.__root
            root[:] = [root, root, None]
            self.__map.clear()
        except AttributeError:
            pass
        dict.clear(self)

    def popitem(self, last=True):
        '''od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.
        '''
        if not self:
            raise KeyError('dictionary is empty')
        root = self.__root
        if last:
            link = root[0]
            link_prev = link[0]
            link_prev[1] = root
            root[0] = link_prev
        else:
            link = root[1]
            link_next = link[1]
            root[1] = link_next
            link_next[0] = root
        key = link[2]
        del self.__map[key]
        value = dict.pop(self, key)
        return key, value

    # -- the following methods do not depend on the internal structure --

    def keys(self):
        'od.keys() -> list of keys in od'
        return list(self)

    def values(self):
        'od.values() -> list of values in od'
        return [self[key] for key in self]

    def items(self):
        'od.items() -> list of (key, value) pairs in od'
        return [(key, self[key]) for key in self]

    def iterkeys(self):
        'od.iterkeys() -> an iterator over the keys in od'
        return iter(self)

    def itervalues(self):
        'od.itervalues -> an iterator over the values in od'
        for k in self:
            yield self[k]

    def iteritems(self):
        'od.iteritems -> an iterator over the (key, value) items in od'
        for k in self:
            yield (k, self[k])

    def update(*args, **kwds):
        '''od.update(E, **F) -> None.  Update od from dict/iterable E and F.
        If E is a dict instance, does:           for k in E: od[k] = E[k]
        If E has a .keys() method, does:         for k in E.keys(): od[k] = E[k]
        Or if E is an iterable of items, does:   for k, v in E: od[k] = v
        In either case, this is followed by:     for k, v in F.items(): od[k] = v
        '''
        if len(args) > 2:
            raise TypeError('update() takes at most 2 positional '
                            'arguments (%d given)' % (len(args),))
        elif not args:
            raise TypeError('update() takes at least 1 argument (0 given)')
        self = args[0]
        # Make progressively weaker assumptions about "other"
        other = ()
        if len(args) == 2:
            other = args[1]
        if isinstance(other, dict):
            for key in other:
                self[key] = other[key]
        elif hasattr(other, 'keys'):
            for key in other.keys():
                self[key] = other[key]
        else:
            for key, value in other:
                self[key] = value
        for key, value in kwds.items():
            self[key] = value

    __update = update  # let subclasses override update without breaking __init__

    __marker = object()

    def pop(self, key, default=__marker):
        '''od.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised.
        '''
        if key in self:
            result = self[key]
            del self[key]
            return result
        if default is self.__marker:
            raise KeyError(key)
        return default

    def setdefault(self, key, default=None):
        'od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od'
        if key in self:
            return self[key]
        self[key] = default
        return default

    def __reduce__(self):
        'Return state information for pickling'
        items = [[k, self[k]] for k in self]
        inst_dict = vars(self).copy()
        for k in vars(OrderedDict()):
            inst_dict.pop(k, None)
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def copy(self):
        'od.copy() -> a shallow copy of od'
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        '''OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).
        '''
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    def __eq__(self, other):
        '''od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.
        '''
        if isinstance(other, OrderedDict):
            return len(self) == len(other) and self.items() == other.items()
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other

    # -- the following methods are only used in Python 2.7 --

    def viewkeys(self):
        "od.viewkeys() -> a set-like object providing a view on od's keys"
        return KeysView(self)

    def viewvalues(self):
        "od.viewvalues() -> an object providing a view on od's values"
        return ValuesView(self)

    def viewitems(self):
        "od.viewitems() -> a set-like object providing a view on od's items"
        return ItemsView(self)

    # NOTE(ugo): I ported this method from the Python3.2 source.
    def move_to_end(self, key, last=True):
        '''Move an existing element to the end (or beginning if last==False).
        Raises KeyError if the element does not exist.
        When last=True, acts like a fast version of self[key]=self.pop(key).
        '''
        link_prev, link_next, key = link = self.__map[key]
        link_prev[1] = link_next
        link_next[0] = link_prev
        root = self.__root
        if last:
            last = root[0]
            link[0] = last
            link[1] = root
            last[1] = root[0] = link
        else:
            first = root[1]
            link[0] = root
            link[1] = first
            root[1] = first[0] = link

    # NOTE(ugo): I ported this method from the Python3.2 source.
    def popitem(self, last=True):
        '''od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.
        '''
        if not self:
            raise KeyError('dictionary is empty')
        root = self.__root
        if last:
            link = root[0]
            link_prev = link[0]
            link_prev[1] = root
            root[0] = link_prev
        else:
            link = root[1]
            link_next = link[1]
            root[1] = link_next
            link_next[0] = root
        key = link[2]
        del self.__map[key]
        value = dict.pop(self, key)
        return key, value

    def get_previous_key(self, key):
        return self.__map[key][0][2] if key in self.__map else None

    def get_next_key(self, key):
        return self.__map[key][1][2] if key in self.__map else None


class DefaultOrderedDict(OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
                not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)

        self.default_factory = default_factory
        self.next_valid = {}

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory,
                          copy.deepcopy(self.items()))

    def __repr__(self):
        return 'OrderedDefaultDict(%s, %s)' % (self.default_factory,
                                               OrderedDict.__repr__(self))


def range_dict(start_key, dict_now):
    for key in dropwhile(lambda k: k != start_key, dict_now):
        yield key


import copy


class MyOrderedDict(object):
    def __init__(self):
        self.data = DefaultOrderedDict(list)
        self.parents = {}
        self.child = {}

    def check(self):
        for key in self.data:
            for p in self.parents[key]:
                assert p in self.child, 'p={}'.format(p)
                assert self.child[p] == key, 'real p={},real child={}, wrong child={}'.format(p, key, self.child[p])

    def new_key(self, key):
        # print('new_key_before',key)
        # self.check()
        self.data[key] = []
        self.parents[key] = [key]
        self.child[key] = key
        pre_key = self.data.get_previous_key(key)
        while (not pre_key is None) and len(self.data[self.child[pre_key]]) == 0:
            # print(pre_key,key)
            self.parents[key].append(pre_key)
            self.child[pre_key] = key
            if len(self.parents[pre_key]) > 0 and pre_key == self.parents[pre_key][0]:
                self.parents[pre_key].pop(0)
            pre_key = self.data.get_previous_key(pre_key)

        # print('new_key',key)
        # self.check()

    def append(self, key, value):
        if not key in self.data:
            self.new_key(key)
        self.data[key].append(value)
        pre_key = key
        while (not pre_key is None) and len(self.data[self.child[pre_key]]) == 0:
            self.parents[key].append(pre_key)
            self.child[pre_key] = key
            if len(self.parents[pre_key]) > 0 and pre_key == self.parents[pre_key][0]:
                self.parents[pre_key].pop(0)
            pre_key = self.data.get_previous_key(pre_key)

    def get_child(self, key):
        if not key in self.child:
            return (None, None)
        child_key = self.child[key]

        if len(self.data[child_key]) == 0:
            if key == child_key:
                return (None, None)
            else:
                re1, re2 = self.get_child(self.get_child(child_key))
                if not re1 is None:
                    self.child[key] = re1
                    self.parents[re1].append(key)
                    return re1, re2
                else:
                    return (None, None)
        else:
            return (self.child[key], self.data[self.child[key]].pop(0))
        # return (self.child[key],self.data[self.child[key]].pop(0)) if key in self.child  and len(self.child[key])>0 else (None,None)

    def pop_update(self, pop_key, reduce_key, reduce_value):
        if len(self.data[reduce_key]) == 0:

            next_key = self.data.get_next_key(reduce_key)
            if not next_key is None:
                # print(reduce_key,len(self.parents[reduce_key]))
                ll = copy.copy(self.parents[reduce_key])
                # length = len(ll)
                for p in ll:
                    # print(length,len(ll))
                    # print('hh',next_key,len(ll))
                    self.child[p] = self.child[next_key]
                    self.parents[self.child[next_key]].append(p)
            self.parents[reduce_key] = []

        previous_key = self.data.get_previous_key(pop_key)

        next_key = self.data.get_next_key(pop_key)

        pop_data = self.data.pop(pop_key)
        pop_parents = self.parents.pop(pop_key)
        pop_child = self.child.pop(pop_key)
        # print(pop_key,pop_child,self.parents[pop_child])
        if pop_child in self.parents:
            if len(self.parents[pop_child]) > 0:
                self.parents[pop_child].remove(pop_key)
        if previous_key is None:
            pass
        else:
            if len(pop_data) > 0:
                self.data[previous_key] += pop_data
                if pop_key in pop_parents:
                    pop_parents.remove(pop_key)

                self.parents[previous_key] += pop_parents
                for kk in pop_parents:
                    self.child[kk] = previous_key

                self.child[previous_key] = previous_key
                self.parents[previous_key].append(previous_key)
            else:

                if not next_key is None:
                    # print(reduce_key,len(self.parents[reduce_key]))

                    for p in pop_parents:
                        # print(next_key,len(ll))
                        self.child[p] = self.child[next_key]
                        self.parents[self.child[next_key]].append(p)

    def __len__(self):
        return len(self.data)


class Solution:
    def avoidFlood(self, rains):
        chain = MyOrderedDict()
        # chain.append('a',1)
        # chain.append('b',2)
        # print(len(chain))
        # exit()

        # 维护一个列表，列表元素为在rains中遇到的元素，同时用字典存储每个元素后的空格出现的位置
        # chain = DefaultOrderedDict(list)

        # chain.update({"a": 1, "b": 2, "h": 55 })
        # print(chain)
        # print(chain.get_previous_key('a'))
        # print(chain.get_previous_key('b'))
        # print(chain.get_previous_key('h'))
        # print(chain.get_previous_key('c'))
        # print(get_pre_key('a',chain))
        # print(get_pre_key('b',chain))
        # print(get_pre_key('h',chain))
        # print(get_pre_key('c',chain))
        # exit()
        # for key in range_dict('b',chain):
        #     print(key)
        # exit()

        # store = defaultdict(list)
        ans = [-1 if r > 0 else 1 for r in rains]
        for i in range(len(rains)):
            lake_index = rains[i]
            # print(lake_index,chain.data,chain.child)
            # print(lake_index)
            # wrong_p = 49546
            # wrong_c = 86167
            #
            # if wrong_p in chain.data:
            #     if wrong_c ==  chain.child[wrong_p]:
            #
            #         print('debug2:',i,lake_index,chain.data[wrong_p],chain.child[wrong_p],chain.parents[wrong_p])
            #         for ii, rr in enumerate(rains):
            #             if rr==wrong_c:
            #                 print(ii,rr)
            #         exit()

            # if chain.child[49546] == 86167:
            #     print('debug2:',i,lake_index,chain.data[49546],chain.child[49546],chain.parents[49546])
            #
            #     print(chain.data[chain.child[49546]])
            #     for ii,rr in enumerate(rains):
            #         if rr==86167:
            #             print(ii,rr)
            #     exit()

            if lake_index == 0:
                if len(chain) == 0:
                    continue
                else:
                    chain.append(get_last_key(chain.data), i)
            else:
                if lake_index in chain.data:
                    # print('h1:',chain)
                    # c_i = chain.index(lake_index)

                    # for key in range_dict(lake_index,chain):
                    #     if len(chain[key])>0:
                    #         find=True
                    #         find_index = chain[key].pop(0)
                    #         break
                    find_key, find_index = chain.get_child(lake_index)

                    if find_key is None:
                        print(lake_index)
                        wrong_l = 95392
                        print('debug2:', i, lake_index, chain.data[wrong_l], chain.child[wrong_l],
                              chain.parents[wrong_l])
                        return []

                    # previous_key = chain.get_previous_key(lake_index)
                    # list_now = chain.pop(lake_index)
                    #
                    # if not previous_key is None:
                    #     chain[previous_key]+=list_now

                    chain.pop_update(lake_index, find_key, find_index)
                    ans[find_index] = lake_index

                    # print('h3:',chain,find_index,lake_index)
                # chain[lake_index]=[]
                chain.new_key(lake_index)
        return ans


def check_ans(rains, ans):
    a = []
    for i in range(len(ans)):
        if rains[i] > 0:
            assert ans[i] == -1, 'i={},rain={},ans={}'.format(i, rains[i], ans[i])
            if rains[i] in a:
                print('wrong for i={},rain={}'.format(i, rains[i]))
                for ii, r in enumerate(rains):
                    if r == rains[i]:
                        print(ii, r)
                for ii, l in enumerate(ans):
                    if l == rains[i]:
                        print(ii)
            a.append(rains[i])

        if rains[i] == 0:
            if ans[i] in a:
                a.remove(ans[i])


if __name__ == '__main__':
    import time

    # rains = [1,2,0,0,2,1]
    rains = [1, 2, 0, 0, 2, 1]
    rains = [1, 2, 0, 1, 2]

    # 300
    # 49546
    # 519
    # 49546
    # 229

    rains = [98284, 57875, 0, 0, 94301, 94503, 16548, 0, 0, 37144, 0, 0, 0, 63939, 0, 0, 0, 0, 57020, 47710, 3285,
             71226, 0, 24745, 0, 0, 70243, 0, 51703, 80321, 95971, 22206, 0, 43959, 84602, 77192, 0, 0, 0, 0, 0, 6407,
             6477, 99867, 0, 24520, 0, 0, 0, 0, 9799, 43282, 52055, 96659, 51254, 40585, 79473, 0, 0, 0, 0, 9481, 0, 0,
             0, 35881, 54126, 8792, 0, 0, 0, 22570, 0, 0, 879, 2319, 0, 4889, 46458, 0, 0, 0, 36638, 69875, 57212,
             57875, 0, 0, 96659, 75448, 51766, 6379, 57212, 99867, 86167, 0, 93231, 52568, 16312, 0, 0, 19402, 0, 0,
             8602, 0, 0, 0, 3285, 39361, 36638, 0, 0, 22206, 0, 38549, 94503, 14659, 0, 16548, 0, 0, 54126, 11157,
             70915, 0, 0, 81337, 19893, 54920, 51766, 51244, 17717, 69787, 46075, 0, 42139, 0, 0, 0, 4428, 0, 0, 0, 0,
             0, 9292, 80984, 17717, 54920, 0, 0, 18568, 0, 19946, 0, 69683, 0, 0, 0, 13735, 79530, 42193, 0, 1149,
             78534, 0, 0, 0, 55452, 14864, 24745, 26551, 0, 0, 24233, 0, 79712, 0, 62236, 0, 0, 47800, 0, 6695, 40585,
             0, 52402, 879, 68267, 0, 96631, 64057, 84363, 0, 0, 0, 63335, 96878, 0, 47800, 0, 0, 61952, 0, 0, 24297, 0,
             0, 0, 14584, 0, 42139, 65252, 64136, 11157, 6695, 0, 14877, 0, 0, 0, 44942, 73999, 0, 0, 45572, 0, 86167,
             0, 0, 0, 0, 42193, 0, 84363, 0, 63939, 0, 76503, 0, 51198, 0, 9481, 0, 6407, 0, 64277, 0, 0, 0, 1149, 3072,
             0, 24233, 783, 0, 0, 9036, 39361, 22947, 0, 51703, 0, 0, 52055, 97859, 25989, 0, 0, 0, 0, 77192, 0, 0,
             12234, 57020, 79530, 0, 0, 19946, 0, 0, 0, 0, 61952, 36135, 0, 0, 34886, 0, 97617, 66393, 0, 0, 80321, 0,
             0, 75482, 97859, 49546, 22947, 0, 73999, 0, 0, 68267, 0, 18529, 65252, 2319, 18568, 0, 0, 0, 69939, 508, 0,
             0, 0, 65617, 24520, 82199, 93231, 64015, 0, 39813, 0, 0, 0, 16814, 74810, 0, 0, 55452, 0, 43282, 39813, 0,
             0, 80942, 0, 70915, 4428, 0, 43683, 0, 82199, 90187, 0, 13584, 36135, 0, 74810, 961, 0, 44942, 0, 0, 32578,
             90187, 0, 69683, 0, 38549, 0, 0, 13735, 33424, 0, 59757, 64277, 6477, 0, 0, 94301, 52568, 0, 0, 0, 0, 0, 0,
             0, 63505, 0, 0, 0, 51254, 0, 0, 46458, 64015, 0, 0, 66393, 58429, 0, 64136, 69875, 62236, 0, 0, 0, 0, 4770,
             0, 89776, 0, 961, 34886, 62059, 0, 65617, 0, 0, 81337, 63335, 0, 0, 0, 43683, 0, 45572, 0, 0, 97617, 0,
             9799, 32578, 0, 0, 0, 22570, 95971, 0, 64057, 4770, 0, 46075, 0, 0, 0, 0, 0, 96631, 0, 0, 26551, 0, 8602,
             18529, 0, 0, 0, 0, 0, 60713, 0, 70243, 0, 59757, 75482, 0, 0, 78534, 0, 0, 51198, 16814, 0, 0, 58429, 0, 0,
             9036, 96878, 0, 0, 71226, 51244, 76503, 0, 0, 64319, 0, 24297, 14864, 0, 25989, 12234, 62059, 0, 84602, 0,
             0, 19893, 0, 783, 75448, 69939, 67299, 0, 0, 0, 75087, 0, 0, 37144, 33424, 0, 0, 67299, 0, 0, 20507, 0, 0,
             69787, 49546, 14877, 9292, 0, 0, 14659, 89776, 0, 0, 0, 0, 75087, 35881, 3072, 19402, 14584, 0, 0, 13584,
             508, 0, 80942, 0, 6379, 0, 0, 60713, 0, 0, 4889, 4528, 0, 0, 0, 0, 0, 0, 8792, 0, 79712, 0, 0, 0, 16312, 0,
             47710, 64319, 98284, 0, 4528, 80984, 43959, 79473, 63505, 52402, 20507, 0]
    rains = [1, 2, 0, 2, 3, 0, 1]
    rains = [0, 11475, 23148, 0, 91836, 0, 0, 0, 0, 18987, 0, 3057, 0, 0, 0, 69217, 0, 0, 65289, 0, 0, 0, 35467, 33617,
             0, 0, 0,
             0, 55602, 67935, 0, 0, 2530, 84750, 0, 0, 4411, 0, 0, 81775, 0, 46174, 33617, 0, 60322, 60801, 56836,
             72787, 4022,
             91465, 21256, 0, 0, 0, 0, 0, 2530, 0, 14817, 57045, 0, 0, 0, 2583, 62414, 4452, 28481, 54082, 36928, 25662,
             14817,
             95392, 22974, 1040, 0, 93616, 0, 0, 59731, 0, 61094, 0, 65368, 82028, 22053, 54082, 0, 0, 4452, 81775,
             98696, 0, 0,
             5717, 91465, 0, 0, 20971, 0, 0, 0, 0, 0, 0, 0, 8644, 82028, 55602, 0, 77965, 0, 59578, 0, 0, 0, 42529, 0,
             0, 0, 0,
             0, 36928, 0, 20971, 25671, 0, 0, 0, 59289, 0, 0, 0, 0, 0, 0, 59289, 72266, 0, 0, 0, 92138, 77364, 59578,
             46174, 0,
             2583, 60322, 0, 0, 0, 0, 0, 0, 72787, 4022, 0, 95082, 0, 0, 0, 0, 22974, 22053, 60801, 0, 67634, 27785, 0,
             91836,
             95392, 0, 77364, 28481, 4411, 0, 91988, 0, 0, 0, 27785, 69763, 0, 77965, 7509, 67935, 0, 62414, 18987,
             84750, 0, 0,
             9118, 0, 9118, 64611, 0, 0, 59731, 0, 0, 69217, 0, 65368, 0, 0, 90771, 0, 0, 56836, 8644, 0, 25662, 1040,
             7509,
             90771, 0, 0, 5717, 0, 0, 0, 93616, 0, 0, 92138, 91988, 0, 0, 61094, 57045, 0, 0, 0, 95082, 0, 23148, 0,
             98696,
             25671, 11475, 0, 35467, 21256, 65289, 68210, 69763, 0, 0, 72266, 3057, 67634, 64611, 42529, 68210]
    rains = [98284, 57875, 0, 0, 94301, 94503, 16548, 0, 0, 37144, 0, 0, 0, 63939, 0, 0, 0, 0, 57020, 47710, 3285,
             71226, 0, 24745, 0, 0, 70243, 0, 51703, 80321, 95971, 22206, 0, 43959, 84602, 77192, 0, 0, 0, 0, 0, 6407,
             6477, 99867, 0, 24520, 0, 0, 0, 0, 9799, 43282, 52055, 96659, 51254, 40585, 79473, 0, 0, 0, 0, 9481, 0, 0,
             0, 35881, 54126, 8792, 0, 0, 0, 22570, 0, 0, 879, 2319, 0, 4889, 46458, 0, 0, 0, 36638, 69875, 57212,
             57875, 0, 0, 96659, 75448, 51766, 6379, 57212, 99867, 86167, 0, 93231, 52568, 16312, 0, 0, 19402, 0, 0,
             8602, 0, 0, 0, 3285, 39361, 36638, 0, 0, 22206, 0, 38549, 94503, 14659, 0, 16548, 0, 0, 54126, 11157,
             70915, 0, 0, 81337, 19893, 54920, 51766, 51244, 17717, 69787, 46075, 0, 42139, 0, 0, 0, 4428, 0, 0, 0, 0,
             0, 9292, 80984, 17717, 54920, 0, 0, 18568, 0, 19946, 0, 69683, 0, 0, 0, 13735, 79530, 42193, 0, 1149,
             78534, 0, 0, 0, 55452, 14864, 24745, 26551, 0, 0, 24233, 0, 79712, 0, 62236, 0, 0, 47800, 0, 6695, 40585,
             0, 52402, 879, 68267, 0, 96631, 64057, 84363, 0, 0, 0, 63335, 96878, 0, 47800, 0, 0, 61952, 0, 0, 24297, 0,
             0, 0, 14584, 0, 42139, 65252, 64136, 11157, 6695, 0, 14877, 0, 0, 0, 44942, 73999, 0, 0, 45572, 0, 86167,
             0, 0, 0, 0, 42193, 0, 84363, 0, 63939, 0, 76503, 0, 51198, 0, 9481, 0, 6407, 0, 64277, 0, 0, 0, 1149, 3072,
             0, 24233, 783, 0, 0, 9036, 39361, 22947, 0, 51703, 0, 0, 52055, 97859, 25989, 0, 0, 0, 0, 77192, 0, 0,
             12234, 57020, 79530, 0, 0, 19946, 0, 0, 0, 0, 61952, 36135, 0, 0, 34886, 0, 97617, 66393, 0, 0, 80321, 0,
             0, 75482, 97859, 49546, 22947, 0, 73999, 0, 0, 68267, 0, 18529, 65252, 2319, 18568, 0, 0, 0, 69939, 508, 0,
             0, 0, 65617, 24520, 82199, 93231, 64015, 0, 39813, 0, 0, 0, 16814, 74810, 0, 0, 55452, 0, 43282, 39813, 0,
             0, 80942, 0, 70915, 4428, 0, 43683, 0, 82199, 90187, 0, 13584, 36135, 0, 74810, 961, 0, 44942, 0, 0, 32578,
             90187, 0, 69683, 0, 38549, 0, 0, 13735, 33424, 0, 59757, 64277, 6477, 0, 0, 94301, 52568, 0, 0, 0, 0, 0, 0,
             0, 63505, 0, 0, 0, 51254, 0, 0, 46458, 64015, 0, 0, 66393, 58429, 0, 64136, 69875, 62236, 0, 0, 0, 0, 4770,
             0, 89776, 0, 961, 34886, 62059, 0, 65617, 0, 0, 81337, 63335, 0, 0, 0, 43683, 0, 45572, 0, 0, 97617, 0,
             9799, 32578, 0, 0, 0, 22570, 95971, 0, 64057, 4770, 0, 46075, 0, 0, 0, 0, 0, 96631, 0, 0, 26551, 0, 8602,
             18529, 0, 0, 0, 0, 0, 60713, 0, 70243, 0, 59757, 75482, 0, 0, 78534, 0, 0, 51198, 16814, 0, 0, 58429, 0, 0,
             9036, 96878, 0, 0, 71226, 51244, 76503, 0, 0, 64319, 0, 24297, 14864, 0, 25989, 12234, 62059, 0, 84602, 0,
             0, 19893, 0, 783, 75448, 69939, 67299, 0, 0, 0, 75087, 0, 0, 37144, 33424, 0, 0, 67299, 0, 0, 20507, 0, 0,
             69787, 49546, 14877, 9292, 0, 0, 14659, 89776, 0, 0, 0, 0, 75087, 35881, 3072, 19402, 14584, 0, 0, 13584,
             508, 0, 80942, 0, 6379, 0, 0, 60713, 0, 0, 4889, 4528, 0, 0, 0, 0, 0, 0, 8792, 0, 79712, 0, 0, 0, 16312, 0,
             47710, 64319, 98284, 0, 4528, 80984, 43959, 79473, 63505, 52402, 20507, 0]
    rains = list(range(1, 25001)) + [0] * 50000 + list(range(1, 25001))
    rains = [0, 11475, 23148, 0, 91836, 0, 0, 0, 0, 18987, 0, 3057, 0, 0, 0, 69217, 0, 0, 65289, 0, 0, 0, 35467, 33617,
             0, 0, 0, 0, 55602, 67935, 0, 0, 2530, 84750, 0, 0, 4411, 0, 0, 81775, 0, 46174, 33617, 0, 60322, 60801,
             56836, 72787, 4022, 91465, 21256, 0, 0, 0, 0, 0, 2530, 0, 14817, 57045, 0, 0, 0, 2583, 62414, 4452, 28481,
             54082, 36928, 25662, 14817, 95392, 22974, 1040, 0, 93616, 0, 0, 59731, 0, 61094, 0, 65368, 82028, 22053,
             54082, 0, 0, 4452, 81775, 98696, 0, 0, 5717, 91465, 0, 0, 20971, 0, 0, 0, 0, 0, 0, 0, 8644, 82028, 55602,
             0, 77965, 0, 59578, 0, 0, 0, 42529, 0, 0, 0, 0, 0, 36928, 0, 20971, 25671, 0, 0, 0, 59289, 0, 0, 0, 0, 0,
             0, 59289, 72266, 0, 0, 0, 92138, 77364, 59578, 46174, 0, 2583, 60322, 0, 0, 0, 0, 0, 0, 72787, 4022, 0,
             95082, 0, 0, 0, 0, 22974, 22053, 60801, 0, 67634, 27785, 0, 91836, 95392, 0, 77364, 28481, 4411, 0, 91988,
             0, 0, 0, 27785, 69763, 0, 77965, 7509, 67935, 0, 62414, 18987, 84750, 0, 0, 9118, 0, 9118, 64611, 0, 0,
             59731, 0, 0, 69217, 0, 65368, 0, 0, 90771, 0, 0, 56836, 8644, 0, 25662, 1040, 7509, 90771, 0, 0, 5717, 0,
             0, 0, 93616, 0, 0, 92138, 91988, 0, 0, 61094, 57045, 0, 0, 0, 95082, 0, 23148, 0, 98696, 25671, 11475, 0,
             35467, 21256, 65289, 68210, 69763, 0, 0, 72266, 3057, 67634, 64611, 42529, 68210]
    solution = Solution()
    t = time.time()
    ans = solution.avoidFlood(rains)
    print(time.time() - t)
    # res = "\n".join("{} {}".format(x, y) for x, y in zip(rains, ans))
    print(ans)
    check_ans(rains, ans)
