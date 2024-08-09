from setuptools import setup

setup(
    name='moobius',
    version='1.4.1',
    description='Moobius SDK',
    packages=['moobius'],
    scripts=['bin/moobius'], #https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
    install_requires=[
        'requests',
        'aioprocessing',
        'aiohttp',
        'APScheduler',
        'dacite',
        'redis',
        'websockets',
        'loguru',
    ],
)
