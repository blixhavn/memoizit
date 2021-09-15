__version__ = "1.0.0"

import hashlib
import inspect
import logging
import pickle
from typing import Any, Callable, List, Optional, Tuple, Union

from storage import StorageBackend, PythonBackend, RedisBackend

log = logging.getLogger(__name__)


class Memoizer:
    def __init__(self, backend: str = "python", **kwargs):
        self.storage: StorageBackend = {
            "python": PythonBackend,
            "redis": RedisBackend,
        }.get(backend, PythonBackend)(**kwargs)

    def memoize(
        self,
        expiration: int = 300,
        unique_on: List[str] = None,
        conditions: List[Tuple[str, Any]] = None,
    ):
        """
        Decorator to cache function results for <expiration> seconds.

        :param expiration (int): Time in seconds before the cached value is invalidated.
        :param unique_on (list[str]): list of argument names to use for caching. Can be
        used to ignore irrelevant arguments such as database connector
        :param conditions (list[tuple[str, Any]]): list of paired argument names and
        a conditional value. Can be used for both args and kwargs.

        !! IMPORTANT !!
        Must be put directly above the function to be cached, not above any other decorators.
        If not, the decorator below will be cached instead. Not ideal.
        """
        unique_on = unique_on or []
        conditions = conditions or [("", None)]

        def decorator(function: Callable):
            def wrapper(*args, **kwargs):
                # Get all args, including default arguments, for checking
                # against conditions
                all_args = self._extract_all_args(
                    function, args, kwargs, from_decorator=True
                )
                for (arg, val) in conditions:
                    if all_args.get(arg) != val:
                        return function(*args, **kwargs)

                # Remove arguments not present in unique_on
                filtered_args = {
                    key: value for key, value in all_args.items() if key in unique_on
                }
                cache_args = filtered_args or all_args

                # Create hash key and memoize
                hashed_args = [
                    hashlib.md5(repr(value).encode()).hexdigest()
                    for value in cache_args.values()
                ]

                key: str = "memoize_" + function.__name__ + "_" + "_".join(hashed_args)
                pickled_value = self.storage.get(key)
                if pickled_value is not None:
                    return pickle.loads(pickled_value)
                else:
                    value = function(*args, **kwargs)
                    try:
                        self.storage.set(
                            key, pickle.dumps(value), expiration=expiration
                        )
                    except AttributeError:
                        log.debug(
                            f"Could not cache function call for {key} - result not serializable"
                        )
                    return value

            return wrapper

        return decorator

    def invalidate_memoize(self, function_name: str, *args, **kwargs):
        """
        Function to invalidate memoized function calls. Implements a limited wildcard functionality,
        where arguments and keyword arguments can be provided to specify which cache entries to delete,
        but only in a left-to-right order. Example:

        function definition: perform_miracle(country_id, miracle_type, target="cats")
        memoized function call: perform_miracle(2, "divine", target="dogs")

        matching delete: redis_invalidate_memoize('perform_miracle', 2, "divine")
        not matching: redis_invalidate_memoize("perform_miracle", 2, target="dogs")
        """

        hashed_args = [
            hashlib.md5(repr(value).encode()).hexdigest()
            for value in (list(args) + list(kwargs.values()))
        ]

        key_start: str = "memoize_" + function_name + "_" + "_".join(hashed_args)
        keys = self.storage.keys_startswith(key_start)
        for key in keys:
            self.storage.delete(key)
        return len(keys)

    @staticmethod
    def _extract_all_args(
        function,
        args: Optional[Union[list, tuple]] = None,
        kwargs: Optional[dict] = None,
        from_decorator: bool = False,
    ):
        """
        Extract default arguments from function definition and combine with provided args and kwargs,
        returning a complete dict of all arguments.

        """
        args = list(args) if args else []
        kwargs = kwargs or {}
        function_spec = inspect.getfullargspec(function)

        # We're not interested in the `self` argument
        all_arg_names = function_spec.args
        if all_arg_names and all_arg_names[0] == "self":
            all_arg_names.pop(0)

            # If called from within a decorator, the args are fetched implicitly and will contain the self
            # object in arguments. We'll remove this.
            if from_decorator:
                args.pop(0)

        # Gotcha: def fun(one, two, three=3) will put `two` in kwargs if called as fun(one, two=4, three=6)
        # The only thing we know about arguments with default values is that they are always last. Therefore, we
        # apply the default values from the back.

        reverse_arg_names = all_arg_names[::-1]
        reverse_defaults = (
            list(function_spec.defaults)[::-1] if function_spec.defaults else []
        )

        # Make the value list as long as the key list, pad with None
        reverse_defaults.extend(
            [None] * (len(reverse_arg_names) - len(reverse_defaults))
        )

        # Combine keys and values, undo the reversion and transform back into a
        # dict.
        args_with_values = dict(list(zip(reverse_arg_names, reverse_defaults))[::-1])

        # Arguments provided in `args` are always left-to-right in the overall
        # args list, so we can apply them as such.
        for i, arg in enumerate(args):
            args_with_values[all_arg_names[i]] = arg

        # Arguments in `kwargs` however, are not, so we need to match by
        # argument name.
        for key, value in kwargs.items():
            args_with_values[key] = value

        return args_with_values
