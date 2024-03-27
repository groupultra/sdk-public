from setuptools import setup

setup(
    name='moobius',
    version='1.1.x',
    description='Moobius SDK',
    packages=['moobius'],
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
