from setuptools import setup
from setuptools import find_packages

install_requires = [
    'appdirs == 1.4.3',
    'falcon == 1.1.0',
    'packaging == 16.8',
    'pyparsing == 2.2.0',
    'python-mimeparse == 1.6.0',
    'redis == 2.10.5',
    'six == 1.10.0'
]
setup(
    name='falcon-redis',
    version='0.1',
    packages=find_packages(exclude='test'),
    url='https://github.com/luzhongqiu/falcon-redis',
    license='MIT',
    author='luzhongqiu',
    author_email='zq.lu@foxmail.com',
    description='falcon redis cache',
    install_requires=install_requires
)
