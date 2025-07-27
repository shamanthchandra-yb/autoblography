from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="autoblography",
    version="1.0.0",
    author="AI Hackathon 2025 Team",
    author_email="team@autoblography.ai",
    description="AI-powered blog generator that transforms Slack conversations and Google Documents into professional blog posts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shamanthchandra-yb/autoblography",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "autoblography=ai_hackathon_2025.main:main",
        ],
    },
    keywords="ai, blog, generator, slack, google-docs, vertex-ai, content-generation",
    project_urls={
        "Bug Reports": "https://github.com/shamanthchandra-yb/autoblography/issues",
        "Source": "https://github.com/shamanthchandra-yb/autoblography",
        "Documentation": "https://github.com/shamanthchandra-yb/autoblography/blob/main/README.md",
    },
)