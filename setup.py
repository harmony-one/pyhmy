import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='pyhmy',
    use_incremental=True,
    license='MIT',
    description="A library for interacting and working the Harmony blockchain and related codebases.",
    long_description=README,
    long_description_content_type="text/markdown",
    author='Daniel Van Der Maden',
    author_email='daniel@harmony.one',
    url="http://harmony.one/",
    packages=find_packages(),
    keywords=['Harmony', 'blockchain', 'protocol'],
    install_requires=[
        'pexpect',
        'requests',
        'incremental',
        'eth-rlp',
        'eth-account',
        'eth-utils',
        'hexbytes',
        'cytoolz'
    ],
    setup_requires=[
        'incremental',
        'pytest',
        'pytest-ordering',
        'click',
        'twisted',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
