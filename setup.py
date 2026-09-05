#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="aynengine-ai-coding",
    version="4.0.0",
    description="Sovereign 5-Pillar Epistemic Software Engineering Engine Guided by Classical Arabic Lexicas",
    author="AynEngine AI Authors",
    packages=find_packages(),
    scripts=["bin/ayncode"],
    entry_points={
        "console_scripts": [
            "ayncode=bin.ayncode:main",
        ],
    },
    python_requires=">=3.10",
)
