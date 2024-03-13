from setuptools import setup

setup(
    name='moobius',
    version='1.0.0',
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
