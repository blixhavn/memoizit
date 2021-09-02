from setuptools import setup

setup (
    name='advanced-memoize',
    version='1.0.0',
    author='Øystein Blixhavn',
    author_email='oystein@blixhavn.no',
    url='https://github.com/blixhavn/advanced-memoize',
    test_suite="tests",
    keywords = ['memoize', 'library'],
    py_modules = ['memoize'],
    license='MIT',
    description='An advanced memoize library which can be used standalone, or plugged into key/value stores such as redis.'

)