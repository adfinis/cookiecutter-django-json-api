"""Setuptools package definition."""

from setuptools import find_packages, setup

setup(
    name="{{cookiecutter.project_name}}",
    version="0.0.0",
    author="Adfinis SyGroup AG",
    author_email="https://adfinis-sygroup.ch/",
    description="{{cookiecutter.description}}",
    url="https://adfinis-sygroup.ch/",
    packages=find_packages(),
)
