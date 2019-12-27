import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='pyhmy',
    version='0.11',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Daniel Van Der Maden',
    author_email='daniel@harmony.one',
    url="http://harmony.one/",
    packages=['pyhmy'],
    install_requires=['pexpect', 'requests'],
)
