from setuptools import setup, find_packages

setup(
    name='stream-lib',
    version='1.0.0',
    packages=find_packages(),
    description='Fluent Stream library',
    install_requires=[line for line in open('requirements.txt')],
    include_package_data=True,
)
