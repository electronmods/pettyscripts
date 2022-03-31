#!/usr/bin/env python3

from collections.abc import Iterable

def andify(inlist, quotestr=False, skipinvis=False):
    # if isinstance(inlist, Iterable) is False or type(inlist) is str:
    if isinstance(inlist, Iterable) is False:
        raise ValueError('Must be a list/tuple/iterable')
    if len(inlist) == 0:
        raise ValueError('Input iterable is empty')
    if quotestr:
        inlist = list(map(repr, inlist))
    else:
        inlist = list(map(str, inlist))
    if len(inlist) == 1:
        return inlist[0]
    elif len(inlist) == 2:
        return ' and '.join(inlist)
    else:
        bstr = ', '.join(inlist[:-1])
        bstr += ', and ' + inlist[-1]
        return bstr

if __name__ == '__main__':
    import random
    import string
    
    print(andify([random.randint(0,10) for _ in range(5)]))
    print(andify([''.join(random.choices(string.ascii_letters, k=random.randint(3,10))) for _ in range(20)]))
    print(andify('michael jordan', quotestr=True))
    print(andify('to'))
    print(andify((100,)))
    print(andify((None, 22, 'facts', '', 4.444), quotestr=True))
    
