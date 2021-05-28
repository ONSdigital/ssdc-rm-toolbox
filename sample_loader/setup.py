from pathlib import Path

import setuptools

setuptools.setup(
    name="ssdc-rm-toolbox",
    version="",
    description="Scripts to load samples",
    long_description=Path('README.md').read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/ONSdigital/ssdc-rm-toolbox",
    packages=setuptools.find_packages(),
)
