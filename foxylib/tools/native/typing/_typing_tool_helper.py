# https://stackoverflow.com/a/55504010

import inspect
import sys
import typing
import collections.abc

__all__ = ['is_instance', 'is_subtype', 'python_type', 'is_generic', 'is_base_generic', 'is_qualified_generic']

### Added by Moon
if sys.version_info >= (3, 8):
    Protocol_ = typing.Protocol
else:
    Protocol_ = typing._Protocol  # pragma: no cover
### End of Addition


# ============================================================================
# Internal helpers rewritten for Python 3.8+ / 3.12-safe behavior
# ============================================================================

def _origin(cls):
    """
    Wrapper around typing.get_origin for readability.
    e.g. list[int] -> list, dict[str,int] -> dict,
         Callable[[...], R] -> collections.abc.Callable,
         int | str -> types.UnionType
    """
    return typing.get_origin(cls)


def _args(cls):
    """
    Wrapper around typing.get_args.
    e.g. list[int] -> (int,),
         dict[str,int] -> (str,int),
         Callable[[int,str], float] -> ([int,str], float),
         int | str -> (int, str)
    """
    return typing.get_args(cls)


def _is_typing_like(cls):
    """
    Heuristic: is this thing a 'typing style' annotation?
    We treat things with origin, Any, or a TypeVar as typing-ish.
    """
    if _origin(cls) is not None:
        return True
    if cls is typing.Any:
        return True
    if isinstance(cls, typing.TypeVar):
        return True
    return False


def _is_generic(cls):
    """
    ORIGINAL INTENT (from the old code):
      Detects any kind of generic, for example `List` or `List[int]`.
      Includes special forms like Union and Tuple (anything subscriptable).
    OUR NEW LOGIC:
      - Builtin container classes like list/dict/tuple/set/frozenset/type
        count as generic "bases".
      - typing-ish annotations (list[int], dict[str,int], Union[int,str], etc.)
        also count.
      - Plain non-container classes like int, str -> not generic.
    """
    if isinstance(cls, type):
        # Treat container-like builtins & 'type' as generic-capable
        if cls in (list, dict, tuple, set, frozenset, type):
            return True
        # Other normal classes, like int/str, are not "generic"
        return False

    # Not a plain class → could be typing stuff
    return _is_typing_like(cls)


def _is_base_generic(cls):
    """
    ORIGINAL INTENT:
      Detects generic *base classes*, e.g. `List` but not `List[int]`.
    OUR NEW LOGIC:
      - 'base generic' means "generic without concrete type parameters".
      - For builtins like `list`, `dict`, `tuple`, `set`, `frozenset`, `type`:
            True
      - For typing.Callable, typing.Dict, etc. without args:
            True
      - For qualified forms like list[int], dict[str,int], Callable[[...],R]:
            False
      - For Any, or bare TypeVar: treat as base-like (True).
    """
    origin = _origin(cls)
    args = _args(cls)

    # Plain concrete classes
    if isinstance(cls, type):
        if cls in (list, dict, tuple, set, frozenset, type):
            return True
        return False

    # A bare TypeVar like T, or Any, is effectively "unbound generic"
    if isinstance(cls, typing.TypeVar):
        return True
    if cls is typing.Any:
        return True

    # If it has an origin, i.e. parametric like list[int] or callable[[...],R]
    if origin is not None:
        # qualified vs base = "do you have args?"
        return (len(args) == 0)

    # No origin.
    # Could be the unsubscripted typing.Callable / typing.Dict / etc.
    if cls in (
        typing.Callable,
        typing.Tuple,
        typing.List,
        typing.Dict,
        typing.Set,
        typing.FrozenSet,
        typing.Deque,
        typing.DefaultDict,
        typing.Counter,
        typing.ChainMap,
        typing.Mapping,
        typing.MutableMapping,
        typing.Sequence,
        typing.MutableSequence,
        typing.Collection,
        typing.AbstractSet,
        typing.KeysView,
        typing.ValuesView,
        typing.ItemsView,
        typing.AsyncIterable,
        typing.MappingView,
        typing.Type,
    ):
        return True

    # Otherwise not treated as a base generic.
    return False


def _get_base_generic(cls):
    """
    ORIGINAL INTENT:
      get_base_generic(List[int]) -> List
    OUR NEW LOGIC:
      use typing.get_origin().

    For example:
        list[int] -> list
        dict[str,int] -> dict
        Callable[[...], R] -> collections.abc.Callable
    """
    if not is_qualified_generic(cls):
        raise TypeError('{} is not a qualified Generic and thus has no base'.format(cls))

    origin = _origin(cls)
    if origin is not None:
        return origin

    raise TypeError('Cannot determine base of {}'.format(cls))


def _get_python_type(cls):
    """
    ORIGINAL INTENT:
      "Like `python_type`, but only works with `typing` classes."
      i.e. typing.List[int] -> list, typing.Dict[str,int] -> dict, etc.

    OUR NEW LOGIC:
      - If it's literally a class (list/dict/etc), return it.
      - Else, if it has an origin, return that.
      - Else, map known typing.* base names to runtime ABC / builtin.
      - Else, fallback to object for Any/TypeVar.
    """
    # direct class?
    if isinstance(cls, type):
        return cls

    origin = _origin(cls)
    if origin is not None:
        # e.g. list[int] -> list
        #      dict[str,int] -> dict
        #      Callable[...,R] -> collections.abc.Callable
        return origin

    # Special: Any -> object
    if cls is typing.Any:
        return object

    # Special: bare TypeVar -> object (best effort)
    if isinstance(cls, typing.TypeVar):
        return object

    # Map some unsubscripted typing.* names to concrete runtime types.
    mapping_like = {
        typing.Dict: dict,
        typing.List: list,
        typing.Set: set,
        typing.FrozenSet: frozenset,
        typing.Tuple: tuple,
        # typing.Deque: collections.abc.Deque,
        # typing.DefaultDict: collections.abc.DefaultDict,
        # typing.Counter: collections.abc.Counter,
        # typing.ChainMap: collections.abc.ChainMap,
        typing.Mapping: collections.abc.Mapping,
        typing.MutableMapping: collections.abc.MutableMapping,
        typing.Sequence: collections.abc.Sequence,
        typing.MutableSequence: collections.abc.MutableSequence,
        typing.Collection: collections.abc.Collection,
        typing.AbstractSet: collections.abc.Set,
        typing.KeysView: collections.abc.KeysView,
        typing.ValuesView: collections.abc.ValuesView,
        typing.ItemsView: collections.abc.ItemsView,
        typing.AsyncIterable: collections.abc.AsyncIterable,
        # typing.MappingView: collections.abc.MappingView if hasattr(collections.abc, "MappingView") else collections.abc.Mapping,
        typing.Callable: collections.abc.Callable,
        typing.Type: type,
    }
    # Deque: only add if collections.abc has it
    if hasattr(typing, "Deque") and hasattr(collections.abc, "Deque"):
        mapping_like[typing.Deque] = collections.abc.Deque

    # DefaultDict: no ABC. Treat like dict (close enough for runtime isinstance)
    if hasattr(typing, "DefaultDict"):
        mapping_like[typing.DefaultDict] = dict

    # Counter / ChainMap: live in collections, not collections.abc
    if hasattr(typing, "Counter") and hasattr(_collections, "Counter"):
        mapping_like[typing.Counter] = _collections.Counter

    if hasattr(typing, "ChainMap") and hasattr(_collections, "ChainMap"):
        mapping_like[typing.ChainMap] = _collections.ChainMap

    # MappingView: may not exist as ABC in 3.12; fall back to Mapping
    if hasattr(typing, "MappingView"):
        if hasattr(collections.abc, "MappingView"):
            mapping_like[typing.MappingView] = collections.abc.MappingView
        else:
            mapping_like[typing.MappingView] = collections.abc.Mapping
    # --- END: safe mapping construction ---

    if cls in mapping_like:
        return mapping_like[cls]

    raise NotImplementedError("Cannot determine python type of {}".format(cls))


def _get_name(cls):
    """
    ORIGINAL INTENT:
      Return a stable short name of the typing object base.
      Old code used ._name or class metadata.
      Used mainly to pick a validator from _SPECIAL_INSTANCE_CHECKERS.

    NEW LOGIC:
      - Union -> 'Union'
      - Callable -> 'Callable'
      - Type -> 'Type'
      - Any -> 'Any'
      else fallback to cls.__name__ or str(cls).
    """
    origin = _origin(cls)

    # Union[int, str] / int | str
    if origin is typing.Union or (
        getattr(origin, "__module__", "") == "types"
        and getattr(origin, "__name__", "") == "UnionType"
    ):
        return 'Union'

    # Callable[..., ...]
    if origin in (typing.Callable, collections.abc.Callable):
        return 'Callable'

    # type[T]
    if origin is type:
        return 'Type'

    # Any
    if cls is typing.Any:
        return 'Any'

    if isinstance(cls, type):
        return cls.__name__

    return str(cls)


def _get_subtypes(cls):
    """
    ORIGINAL INTENT:
      Return "type arguments" of generics:
        List[int] -> (int,)
        Dict[str,int] -> (str,int)
        Tuple[int,str] -> (int,str)
        Callable[[int,str], float] -> ((int,str), float)
        Union[int,str] -> (int,str)
        Type[int] -> (int,)
    """
    origin = _origin(cls)
    args = _args(cls)

    # Callable is special: get_args(Callable[[A,B], R]) == ([A,B], R)
    if origin in (typing.Callable, collections.abc.Callable):
        if len(args) == 2:
            params, ret = args
            if params is Ellipsis:
                return (Ellipsis, ret)
            else:
                return (tuple(params), ret)
        return args

    return args


# ============================================================================
# Public-facing helpers (names kept identical to your original code)
# ============================================================================

def is_generic(cls):
    """
    Detects any kind of generic, for example `List` or `List[int]`. This includes "special" types like
    Union and Tuple - anything that's subscriptable, basically.
    """
    return _is_generic(cls)


def is_base_generic(cls):
    """
    Detects generic base classes, for example `List` (but not `List[int]`)
    """
    return _is_base_generic(cls)


def is_qualified_generic(cls):
    """
    Detects generics with arguments, for example `List[int]` (but not `List`)
    """
    return is_generic(cls) and not is_base_generic(cls)


def get_base_generic(cls):
    if not is_qualified_generic(cls):
        raise TypeError('{} is not a qualified Generic and thus has no base'.format(cls))
    return _get_base_generic(cls)


def get_subtypes(cls):
    return _get_subtypes(cls)


# ============================================================================
# Instance checking guts (ported from your original but updated)
# ============================================================================

def _instancecheck_iterable(iterable, type_args):
    if len(type_args) != 1:
        raise TypeError("Generic iterables must have exactly 1 type argument; found {}".format(type_args))

    (elem_type,) = type_args
    return all(is_instance(val, elem_type) for val in iterable)


def _instancecheck_mapping(mapping, type_args):
    if len(type_args) != 2:
        raise TypeError("Generic mappings must have exactly 2 type arguments; found {}".format(type_args))
    key_type, value_type = type_args
    return all(is_instance(k, key_type) and is_instance(v, value_type) for k, v in mapping.items())


def _instancecheck_itemsview(itemsview, type_args):
    if len(type_args) != 2:
        raise TypeError("Generic mappings must have exactly 2 type arguments; found {}".format(type_args))
    key_type, value_type = type_args
    return all(is_instance(k, key_type) and is_instance(v, value_type) for k, v in itemsview)


def _instancecheck_tuple(tup, type_args):
    # This version matches tuple[int,str] : fixed-length positional check
    if len(tup) != len(type_args):
        return False
    return all(is_instance(v, t) for v, t in zip(tup, type_args))

_ORIGIN_TYPE_CHECKERS = {}

_ORIGIN_TYPE_CHECKERS[list] = _instancecheck_iterable
_ORIGIN_TYPE_CHECKERS[set] = _instancecheck_iterable
_ORIGIN_TYPE_CHECKERS[frozenset] = _instancecheck_iterable
_ORIGIN_TYPE_CHECKERS[tuple] = _instancecheck_tuple
_ORIGIN_TYPE_CHECKERS[dict] = _instancecheck_mapping

# conditionally register ABC-based validators
abc = collections.abc  # shorthand

if hasattr(abc, "Mapping"):
    _ORIGIN_TYPE_CHECKERS[abc.Mapping] = _instancecheck_mapping
if hasattr(abc, "MutableMapping"):
    _ORIGIN_TYPE_CHECKERS[abc.MutableMapping] = _instancecheck_mapping
if hasattr(abc, "ItemsView"):
    _ORIGIN_TYPE_CHECKERS[abc.ItemsView] = _instancecheck_itemsview
if hasattr(abc, "KeysView"):
    _ORIGIN_TYPE_CHECKERS[abc.KeysView] = _instancecheck_iterable
if hasattr(abc, "ValuesView"):
    _ORIGIN_TYPE_CHECKERS[abc.ValuesView] = _instancecheck_iterable
if hasattr(abc, "Deque"):
    _ORIGIN_TYPE_CHECKERS[abc.Deque] = _instancecheck_iterable
if hasattr(abc, "Collection"):
    _ORIGIN_TYPE_CHECKERS[abc.Collection] = _instancecheck_iterable
if hasattr(abc, "Sequence"):
    _ORIGIN_TYPE_CHECKERS[abc.Sequence] = _instancecheck_iterable
if hasattr(abc, "MutableSequence"):
    _ORIGIN_TYPE_CHECKERS[abc.MutableSequence] = _instancecheck_iterable
if hasattr(abc, "Set"):
    _ORIGIN_TYPE_CHECKERS[abc.Set] = _instancecheck_iterable
if hasattr(abc, "MutableSet"):
    _ORIGIN_TYPE_CHECKERS[abc.MutableSet] = _instancecheck_iterable
if hasattr(abc, "AsyncIterable"):
    _ORIGIN_TYPE_CHECKERS[abc.AsyncIterable] = _instancecheck_iterable


def _instancecheck_callable(value, type_):
    if not callable(value):
        return False

    if is_base_generic(type_):
        # Callable without concrete signature -> any callable is fine
        return True

    param_types, ret_type = get_subtypes(type_)  # ((argtypes...), rettype) or (Ellipsis, rettype)
    sig = inspect.signature(value)

    missing_annotations = []

    # parameters
    if param_types is not Ellipsis:
        if len(param_types) != len(sig.parameters):
            return False

        for param, expected_type in zip(sig.parameters.values(), param_types):
            ann = param.annotation
            if ann is inspect.Parameter.empty:
                # follow original behavior: allow now but complain later
                missing_annotations.append(param)
                continue

            if not is_subtype(ann, expected_type):
                return False

    # return value
    ret_ann = sig.return_annotation
    if ret_ann is inspect.Signature.empty:
        missing_annotations.append('return')
    else:
        if not is_subtype(ret_ann, ret_type):
            return False

    if missing_annotations:
        # original behavior: raise if any missing annotations
        raise ValueError("Missing annotations: {}".format(missing_annotations))

    return True


def _instancecheck_union(value, type_):
    types_ = get_subtypes(type_)
    return any(is_instance(value, t) for t in types_)


def _instancecheck_type(value, type_):
    # Type[T] check: value must be a class, then subclass-check
    if not isinstance(value, type):
        return False

    if is_base_generic(type_):
        # bare Type[...] means "any type is fine"
        return True

    type_args = get_subtypes(type_)
    if len(type_args) != 1:
        raise TypeError("Type must have exactly 1 type argument; found {}".format(type_args))

    return is_subtype(value, type_args[0])


_SPECIAL_INSTANCE_CHECKERS = {
    'Union': _instancecheck_union,
    'Callable': _instancecheck_callable,
    'Type': _instancecheck_type,
    'Any': lambda v, t: True,
}


def is_instance(obj, type_):
    """
    Runtime isinstance-like check extended for typing annotations.

    Behavior mirrors original intent:
      - supports List[int], Dict[str,int], Tuple[int,str],
        Callable[[int,str], float], Union[int,str], Type[int], Any
    """

    # Handle special forms first (Union, Callable, Type, Any)
    if is_generic(type_):
        if is_qualified_generic(type_):
            base_generic = get_base_generic(type_)
        else:
            base_generic = type_

        name = _get_name(base_generic)
        validator = _SPECIAL_INSTANCE_CHECKERS.get(name)
        if validator:
            return validator(obj, type_)

    # Base generic (unsubscripted) → check simple isinstance
    if is_base_generic(type_):
        py_type = _get_python_type(type_)
        return isinstance(obj, py_type)

    # Qualified generic (with args) → origin-based validation
    if is_qualified_generic(type_):
        py_type = _get_python_type(type_)
        if not isinstance(obj, py_type):
            return False

        base = get_base_generic(type_)
        type_args = get_subtypes(type_)

        # Try to find a validator for this base (list, dict, tuple, etc.)
        validator = _ORIGIN_TYPE_CHECKERS.get(base)
        if validator is None:
            # No validator for this container kind → we can at least assert base match.
            return True

        return validator(obj, type_args)

    # Fallback to normal isinstance
    return isinstance(obj, type_)


# ============================================================================
# Subtype checking (issubclass-like for typing)
# ============================================================================

def _is_subtype_tuple(sub_type, super_type):
    """
    tuple[...] subtype relation:
      - tuple[T, ...] vs tuple[S, ...] : covariant in T
      - tuple[T1,T2,...] vs tuple[S1,S2,...] : elementwise covariant
    """
    sub_o = _origin(sub_type)
    sup_o = _origin(super_type)
    if sub_o is not tuple or sup_o is not tuple:
        return False

    sub_args = _args(sub_type)
    sup_args = _args(super_type)

    # variadic form: tuple[T, ...]
    if len(sub_args) == 2 and sub_args[1] is Ellipsis:
        if not (len(sup_args) == 2 and sup_args[1] is Ellipsis):
            return False
        return is_subtype(sub_args[0], sup_args[0])

    # fixed length: elementwise
    if len(sub_args) != len(sup_args):
        return False

    return all(is_subtype(sa, ta) for sa, ta in zip(sub_args, sup_args))


def _is_subtype_callable(sub_type, super_type):
    """
    Callable subtype rule (simplified but closer to typing semantics):
      - Return type: covariant
      - Parameter types: contravariant
        (subtype's param types must be *broader* or equal)
    """
    sub_o = _origin(sub_type)
    sup_o = _origin(super_type)
    if sub_o not in (typing.Callable, collections.abc.Callable):
        return False
    if sup_o not in (typing.Callable, collections.abc.Callable):
        return False

    sub_params, sub_ret = get_subtypes(sub_type)
    sup_params, sup_ret = get_subtypes(super_type)

    # return covariant: sub_ret <: sup_ret
    if not is_subtype(sub_ret, sup_ret):
        return False

    # If super is Callable[..., R], then no param restriction
    if sup_params is Ellipsis:
        return True

    # If sub is Callable[..., R] but super is concrete -> cannot guarantee
    if sub_params is Ellipsis:
        return False

    # Arity must match
    if len(sub_params) != len(sup_params):
        return False

    # contravariant in params:
    # each super_param must be subtype of sub_param
    for sp_sub, sp_super in zip(sub_params, sup_params):
        if not is_subtype(sp_super, sp_sub):
            return False

    return True


def is_subtype(sub_type, super_type):
    """
    issubclass-like check extended for typing annotations.

    Behavior mirrors original intent:
      - base classes: issubclass
      - parameterized generics: origins must align, then compare type args
      - Callable / Tuple / Union handled specially
      - Any is top type
    """

    # super Any is top
    if super_type is typing.Any:
        return True

    # Handle TypeVar on left
    if isinstance(sub_type, typing.TypeVar):
        # If it has constraints, all constraints must be subtype of super_type
        if sub_type.__constraints__:
            return all(is_subtype(c, super_type) for c in sub_type.__constraints__)
        # If it has a bound, that bound must be subtype of super_type
        if sub_type.__bound__:
            return is_subtype(sub_type.__bound__, super_type)
        # Unconstrained TypeVar ~ Any
        return is_subtype(typing.Any, super_type)

    # Handle TypeVar on right
    if isinstance(super_type, typing.TypeVar):
        # sub_type must satisfy that var
        if super_type.__constraints__:
            return any(is_subtype(sub_type, c) for c in super_type.__constraints__)
        if super_type.__bound__:
            return is_subtype(sub_type, super_type.__bound__)
        # otherwise unconstrained -> everything allowed
        return True

    sub_o = _origin(sub_type)
    sup_o = _origin(super_type)

    # super_type is Union[...] (or X|Y). sub_type must be subtype of at least one arm.
    if sup_o is typing.Union or (
        getattr(sup_o, "__module__", "") == "types"
        and getattr(sup_o, "__name__", "") == "UnionType"
    ):
        return any(is_subtype(sub_type, arm) for arm in _args(super_type))

    # sub_type is Union[...] : every arm must be subtype of super_type
    if sub_o is typing.Union or (
        getattr(sub_o, "__module__", "") == "types"
        and getattr(sub_o, "__name__", "") == "UnionType"
    ):
        return all(is_subtype(arm, super_type) for arm in _args(sub_type))

    # both plain classes -> direct issubclass
    if sub_o is None and sup_o is None and isinstance(sub_type, type) and isinstance(super_type, type):
        return issubclass(sub_type, super_type)

    # Callable special case
    if _is_subtype_callable(sub_type, super_type):
        return True

    # tuple[...] special case
    if sub_o is tuple and sup_o is tuple:
        return _is_subtype_tuple(sub_type, super_type)

    # General parameterized generics case
    if sub_o is not None and sup_o is not None:
        py_sub = python_type(sub_type)
        py_sup = python_type(super_type)

        if not issubclass(py_sub, py_sup):
            return False

        sup_args = _args(super_type)
        if not sup_args:
            # e.g. list[int] <: list
            return True

        sub_args = _args(sub_type)
        if not sub_args:
            # super is qualified (like list[object]) but sub is not -> no
            return False

        if len(sub_args) != len(sup_args):
            return False

        # covariant per-type-arg
        return all(is_subtype(sa, ta) for sa, ta in zip(sub_args, sup_args))

    # sub is a plain class, super is parameterized generic
    if sub_o is None and isinstance(sub_type, type) and sup_o is not None:
        py_sup = python_type(super_type)
        return issubclass(sub_type, py_sup)

    # sub is parameterized generic, super is plain class
    if sub_o is not None and sup_o is None and isinstance(super_type, type):
        py_sub = python_type(sub_type)
        return issubclass(py_sub, super_type)

    # fallback
    return False


# ============================================================================
# python_type (public) - kept same name and docstring style
# ============================================================================

def python_type(annotation):
    """
    Given a type annotation or a class as input, returns the corresponding python class.

    Examples:

    ::
        >>> python_type(typing.Dict)
        <class 'dict'>
        >>> python_type(typing.List[int])
        <class 'list'>
        >>> python_type(int)
        <class 'int'>
    """
    # If it's already a class (like int, list, dict...), just return it.
    if isinstance(annotation, type):
        return annotation

    # Otherwise, try the origin.
    origin = _origin(annotation)
    if origin is not None:
        return origin

    # Any -> object
    if annotation is typing.Any:
        return object

    # bare TypeVar -> object
    if isinstance(annotation, typing.TypeVar):
        return object

    # For unsubscripted typing.Dict, typing.List, etc.
    return _get_python_type(annotation)