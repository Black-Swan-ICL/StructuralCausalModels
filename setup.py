import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='StructuralCausalModels',
    version='3.1.0',
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
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Intended Audience :: Science/Research',
    ],
    packages=find_packages(),
    # TODO should pytest and pytest-cov not be separate ?
    install_requires=['numpy', 'scipy', 'pandas', 'pytest', 'pytest-cov'],
    docs_extras=[
        'Sphinx >= 3.5.3',
        'numpy >= 1.20.1',
        'scipy > 1.6.2',
        'pandas >= 1.2.3',
        'pytest >= 6.2.2',
        'pytest-cov>=2.11.1',
    ]
)
