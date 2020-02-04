import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="pycalc-micro",
    version="1.0.0",
    url="https://github.com/jjbeto/pycalc-micro",
    license="Apache 2.0",
    maintainer="Jose Jouberto Fonseca Lopes",
    maintainer_email="jjbeto@gmail.com",
    description="A pycalc basic project to demonstrate a microservice environment.",
    long_description=readme,
    packages=find_packages(),
    zip_safe=False,
    install_requires=['requests', 'flask'],
    extras_require={"test": ["pytest==3.0.6", "coverage"]},
)
