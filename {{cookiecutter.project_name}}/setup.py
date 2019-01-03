"""Setuptools package definition."""

from setuptools import find_packages, setup

setup(
    name="{{cookiecutter.project_name}}",
    version="0.0.0",
    author="{{cookiecutter.organization_slug}}",
    description="{{cookiecutter.description}}",
    url="{{cookiecutter.url}}",
    packages=find_packages(),
)
