from setuptools import setup, find_packages

setup(
    name='cloud-lib',
    version='1.0.0',
    packages=find_packages(),
    description='Cloud lib',
    install_requires=[line for line in open('requirements.txt')],
    include_package_data=True,
)
