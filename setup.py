import io
from setuptools import setup, find_packages

requirements = []

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

setup(
    name="discord_data",
    version="0.1.0",
    url="https://github.com/seanbreckenridge/discord_data",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=("""Library to parse the Discord GDPR export"""),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=find_packages(include=["discord_data"]),
    install_requires=requirements,
    keywords="discord data",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
