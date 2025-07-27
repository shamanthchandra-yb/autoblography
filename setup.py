"""
Setup script for AutoBlography
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().splitlines()

setup(
    name="autoblography",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered blog generation from Slack threads and Google Docs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autoblography",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "autoblography=autoblography.__main__:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="blog generation ai slack google-docs content automation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/autoblography/issues",
        "Source": "https://github.com/yourusername/autoblography",
        "Documentation": "https://github.com/yourusername/autoblography#readme",
    },
) 