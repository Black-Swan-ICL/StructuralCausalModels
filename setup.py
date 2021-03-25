import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='StructuralCausalModels',
    version='1.0.1',
    description='A Python package for Structural Causal Models.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/Black-Swan-ICL/PySCMs',
    author='K. M-H',
    author_email='kmh.pro@protonmail.com',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'pandas', 'pytest']
)
