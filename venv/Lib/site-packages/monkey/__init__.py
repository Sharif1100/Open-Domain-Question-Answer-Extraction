import inspect
import sha

class PatchException(Exception):
    pass

def verify(target, *signatures):
    source = inspect.getsource(target)
    signature = sha.new(source).hexdigest()

    if signature not in signatures:
        raise PatchException(
            "%s is not a valid signature for %s" % (signature, target))

def patch(target, *signatures):
    """
    A decorator to patch an existing method.
    
       >>> class Dummy(object):
       ...     def test(self, arg1, arg2, arg3=None):
       ...         u'A rather simple method'
       ...         return arg1, arg2, arg3

    Output before we patch the method.
     
       >>> Dummy().test(1, 2, 3)
       (1, 2, 3)
       
    Now we'll define our patch; we provide the original method as well
    as a digest of that method.
     
       >>> @patch(Dummy.test, 'ea05c0292cbb74701ae4ed032281c95775226a74')
       ... def test(self, arg1, arg2, arg3=None):
       ...     return arg3, arg2, arg1

    The patching itself is straight-forward.

       >>> Dummy.test = test
       >>> Dummy().test(1, 2, 3)
       (3, 2, 1)

    The docstring is carried over:
    
       >>> Dummy.test.__doc__
       u'A rather simple method'
       
    If another patch is attempted, a digest on the first patch will
    have to be provided.

       >>> @patch(Dummy.test, 'd96b8cc378a8f95b8908b7e58a46a98075acf0df') 
       ... def test(self, arg1, arg2, arg3=None):
       ...     return arg2, arg3, arg1 # doctest: +NORMALIZE_WHITESPACE
       Traceback (most recent call last):
        ...
       PatchException: e3dde2d6f8f6a7dd503beedc15dfe05130227bfd
       is not a valid signature for <unbound method Dummy.wrapper>

       >>> @patch(Dummy.test, 'e3dde2d6f8f6a7dd503beedc15dfe05130227bfd')
       ... def test(self, arg1, arg2, arg3=None):
       ...     return arg2, arg3, arg1

    We are allowed to provide several digests, corresponding to
    various bona fide versions of the patched method.

       >>> @patch(Dummy.test,
       ...     'd96b8cc378a8f95b8908b7e58a46a98075acf0df',
       ...     'e3dde2d6f8f6a7dd503beedc15dfe05130227bfd')
       ... def test(self, arg1, arg2, arg3=None):
       ...     return arg2, arg3, arg1

       >>> Dummy.test = test
       >>> Dummy().test(1, 2, 3)
       (2, 3, 1)

    """

    verify(target, *signatures)
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__doc__ = target.__doc__

        return wrapper

    return decorator

def wrap(target, *signatures):
    """
    A decorator to wrap an existing method.
    
       >>> class Dummy(object):
       ...     def test(self, arg1, arg2, arg3=None):
       ...         return '%d, %d, %d' % (arg1, arg2, arg3)

    Output before we patch the method.
     
       >>> Dummy().test(1, 2, 3)
       '1, 2, 3'

    We'll define a wrapper that shifts the arguments of the call.

       >>> @wrap(Dummy.test, 'c6959b44c232e0d2ff1d2f018f7932260efde27c')
       ... def shift(func, self, arg1, arg2, arg3=None):
       ...     return func(self, arg3, arg2, arg1)

       >>> Dummy.test = shift
       >>> Dummy().test(1, 2, 3)
       '3, 2, 1'
       
    """

    p = patch(target, *signatures)

    def decorator(func):
        f = p(func)
        def wrapper(*args, **kwargs):
            return f(target, *args, **kwargs)

        wrapper.__doc__ = target.__doc__

        return wrapper
    return decorator

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

