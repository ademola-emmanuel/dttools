
from setuptools import setup, find_packages

setup(
    name="dttools",
    version="0.1.0",
    description="A simple library for common date and time manipulations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Emmanuel Ademola",
    author_email="ademola.emmanuel383@gmail.com",
    url="https://github.com/l4christ/dttools",
    packages=find_packages(),
    install_requires=["pytz"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)