# Memoizit ![Build badge](https://github.com/blixhavn/memoizit/actions/workflows/ci.yml/badge.svg)  [![codecov](https://codecov.io/gh/blixhavn/memoizit/branch/main/graph/badge.svg?token=FAY3S48JGU)](https://codecov.io/gh/blixhavn/memoizit)

A memoize library which can be used standalone, or plugged into key/value stores such as Redis. Also contains functionality to invalidate cache based on function name and arguments.

## Why use this one?
There are already several python libraries providing memoizing in some form, ranging from very basic dict caches, more [performance focused](https://github.com/gsakkis/memoized), to [very advanced](https://github.com/DreamLab/memoize), comprehensive libraries. However, I've caught myself writing this particular implementation in two separate projects, and I gathered I should extract it to a separate library. It has a couple of strengths:

* **It is flexible** - the two arguments `unique_on` and `conditions` provide a powerful configurability in how and what you actually want to memoize, making it ideal in situations where memoization is introduced to speed up legacy code. Paired with the `invalidate_memoize` function, there's no limit to how specific you can have your caching be.

* **It is extendable** - currently shipped only with support for dict-type cache and Redis, it is very easy to write new extensions for other storage alternatives. The test blueprints are even already written!

## Basic installation
Using Memoizit completely bare with in-memory caching:
```
pip install memoizit
```

#### With Redis
If you want to (be able to) use Redis as cache storage:

```
pip install memoizit[redis]
```


## Setup
```
from memoizit import Memoizer

m = Memoizer()

@m.memoize()
def heavy_calculation(n):
    return n**n
```

#### With Redis
Default configuration looks for Redis at `localhost:6379`. If this matches your setup, simply run
```
m = Memoizer(backend="redis")
```

Otherwise, Redis can be configured using either keyword arguments in the class constructor, or by setting environment variables:
```
REDIS_HOST
REDIS_PORT
REDIS_USERNAME
REDIS_PASSWORD
```
```
m = Memoizer(
    backend="redis",
    host="redis",
    port="63791",
    username="johndoe",
    password="hunter2"
)
```

## Usage

#### Memoize
The memoize decorator has three arguments:
* **expiration** - seconds until the memoized value is invalidated (default 300 - 5 minutes).
* **unique_on** - arguments to include in the cache key. Can be both args and kwargs (mainly useful to avoid `self` arguments in class methods). If ignored, all arguments will be used.
* **conditions** - list of arguments and conditional values that need to match in order to apply memoization.


##### Example use case
```
class Office:

    @m.memoize(
        expiration=60*60*24,
        unique_on=['department', 'include_management'],
        conditions=[('with_sideeffects', False)]
    )
    def get_employees(self, department, include_management=False, with_sideeffects=False):
        <expensive external requests>
        <possible sideeffects>
        return employees
```

> ⚠ **NB**: Note that omitting `self` from `unique_on` might pollute other class instances with incorrect cache.

#### Invalidate memoize
This library includes the strange function `invalidate_memoize`. This implements a limited wildcard functionality, where arguments and keyword arguments can be provided to specify which cache entries to delete, but only in a left-to-right order. Example:

```
@m.memoize()
perform_miracle(country_id, miracle_type, target="cats"):
    <miracle>
```
This function is then called with the following arguments:
```
perform_miracle(2, "divine", target="dogs")
```

This will find the cache entry and delete it (specifying argument name is optional):
```
m.invalidate_memoize('perform_miracle', 2, "divine")
```
While this will not work:
```
m.invalidate_memoize("perform_miracle", 2, target="dogs")
```

This function can be particulary useful when memoizing `read` functions from an API wrapper, where you want to invalidate the cache on `update` or `delete`.

## Contributing
Clone repo:
```
git clone git@github.com:blixhavn/memoizit.git
cd memoizit
```
Set up virtual environment and activate it:
```
python3 -m virtualenv venv
source venv/bin/activate
```
Install with dev requirements:

```
pip install -e .[dev]
```

Run tests and code checks as follows:
```
black .
mypy .
flake8
pytest 
```
The Redis tests are skipped unless Redis is available at `localhost:6379`.

Then, create a pull request with your work! For your convenience there is also a `pre-commit` file that can be copied into `.git/hooks/`, which will run black, mypy and flake8 before allowing commits. Note however that this does not work in Windows.

## License

Memoizit is released under the MIT license. Have at it.