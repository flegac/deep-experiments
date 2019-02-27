from setuptools import setup, find_packages

setup(
    name='hyper-search',
    version='0.1.0.dev0',
    packages=find_packages(),
    description='ML hyper-parameters search engine',
    install_requires=[line for line in open('requirements.txt')],
    include_package_data=True,
)
