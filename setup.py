from setuptools import setup

import cv


def readme():
    with open('README.md', 'r', encoding='utf8') as f:
        return f.read()


setup(
    name='cv',
    version=cv.__version__,
    py_modules=['cv'],
    author='mdrachuk',
    author_email='misha@drach.uk',
    description="Check version of a Python module",
    long_description=readme(),
    long_description_content_type='text/markdown',
    url="https://github.com/mdrachuk/cv",
    license="MIT",
    keywords="python packaging version pypi ci",
    python_requires=">=3.7",
    scripts=['cv'],
    zip_safe=False,
    project_urls={
        'Pipelines': 'https://dev.azure.com/misha-drachuk/cv',
        'Source': 'https://github.com/mdrachuk/cv/',
        'Issues': 'https://github.com/mdrachuk/cv/issues',
    },
    install_requires=[],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Typing :: Typed",
    ],
)
