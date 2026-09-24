def assert_true(x, msg=None):
    if not x:
        raise AssertionError(msg or f"Expected truthy, got {x!r}")

def assert_false(x, msg=None):
    if x:
        raise AssertionError(msg or f"Expected falsy, got {x!r}")

def assert_equal(a, b, msg=None):
    if a != b:
        raise AssertionError(msg or f"{a!r} != {b!r}")
    
def assert_not_equal(a, b, msg=None):
    if a == b:
        raise AssertionError(msg or f"Did not expect {a!r} == {b!r}")
    
def assert_greater(a, b, msg=None):
    if not (a > b):
        raise AssertionError(msg or f"Expected {a!r} > {b!r}")

def assert_greater_equal(a, b, msg=None):
    if not (a >= b):
        raise AssertionError(msg or f"Expected {a!r} >= {b!r}")

def assert_less(a, b, msg=None):
    if not (a < b):
        raise AssertionError(msg or f"Expected {a!r} < {b!r}")
    
def assert_less_equal(a, b, msg=None):
    if not (a <= b):
        raise AssertionError(msg or f"Expected {a!r} <= {b!r}")

def assert_is_not_none(x, msg=None):
    if x is None:
        raise AssertionError(msg or "Expected value to be not None")
    
def assert_is_none(x, msg=None):
    if x is not None:
        raise AssertionError(msg or f"Expected None, got {x!r}")
    
def assert_in(member, container, msg=None):
    try:
        ok = member in container
    except Exception:
        ok = False
    if not ok:
        raise AssertionError(
            msg or f"Expected {member!r} to be in {container!r}"
        )
    
def assert_not_in(member, container, msg=None):
    try:
        ok = member in container
    except Exception as e:
        raise AssertionError(msg or f"Membership test failed: {e!r}")
    if ok:
        raise AssertionError(
            msg or f"Did not expect {member!r} to be in {container!r}"
        )

def assert_is(a, b, msg=None):
    if a is not b:
        raise AssertionError(msg or f"Expected {a!r} is {b!r}")