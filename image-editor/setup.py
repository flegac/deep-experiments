from setuptools import setup, find_packages

setup(
    name='image-image',
    version='0.1.0.dev0',
    packages=find_packages(),
    description='Image image',
    install_requires=[line for line in open('requirements.txt')],
    include_package_data=True,
)
