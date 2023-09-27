from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in demo4/__init__.py
from demo4 import __version__ as version

setup(
	name="demo4",
	version=version,
	description="demo4",
	author="erpcloudsystems",
	author_email=" ",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
