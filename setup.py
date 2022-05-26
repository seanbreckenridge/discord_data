import io
from pathlib import Path
from setuptools import setup, find_packages

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

reqs = Path("requirements.txt").read_text().strip().splitlines()
pkg = "discord_data"


def main() -> None:
    setup(
        name=pkg,
        version="0.1.1",
        url="https://github.com/seanbreckenridge/discord_data",
        author="Sean Breckenridge",
        author_email="seanbrecke@gmail.com",
        description=("""Library to parse the Discord GDPR export"""),
        long_description=long_description,
        long_description_content_type="text/markdown",
        license="http://www.apache.org/licenses/LICENSE-2.0",
        install_requires=reqs,
        packages=find_packages(include=[pkg]),
        package_data={pkg: ["py.typed"]},
        python_requires=">=3.7",
        keywords="discord data",
        entry_points={"console_scripts": ["discord_data = discord_data.__main__:main"]},
        classifiers=[
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
        ],
    )


if __name__ == "__main__":
    main()
