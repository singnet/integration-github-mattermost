from setuptools import setup

from mattermost import __version__

setup(
    name="integration-github-mattermost",
    author="SingularityNET",
    author_email="",
    version=__version__,
    description="Library to provide integration with Mattermost",
    packages=[
        "mattermost",
    ],
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
