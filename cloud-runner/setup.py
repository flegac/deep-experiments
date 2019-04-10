from setuptools import setup, find_packages

setup(
    name='cloud-runner',
    version='1.0.0',
    packages=find_packages(),
    description='Cloud runner',
    install_requires=[line for line in open('requirements.txt')],
    include_package_data=True,
)
