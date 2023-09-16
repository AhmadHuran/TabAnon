from setuptools import setup, find_packages

setup(
    name='tabanon',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tabanon=tabanon.main:main',
        ],
    },
    install_requires=[
        'pandas',
        'openpyxl',
        'cryptography',
    ],
)

