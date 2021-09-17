import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="memoizit",
    version="0.1.0",
    author="Øystein Blixhavn",
    author_email="oystein@blixhavn.no",
    description="A memoize library which can be used standalone, or plugged into key/value stores such as redis. \
    Also contains functionality to invalidate cache based on function name and arguments.",
    keywords=[
        "memoize",
        "memoizing",
        "cache",
        "redis",
        "memory",
        "in-memory",
        "invalidate",
    ],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blixhavn/advanced-memoize",
    project_urls={
        "Bug Tracker": "https://github.com/blixhavn/advanced-memoize/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages("."),
    python_requires=">=3.6",
    install_requires=[
        "redis>=3.5.3",
    ],
)
