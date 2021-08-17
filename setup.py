from setuptools import find_packages, setup
import re

with open('asyncminehut/meta.py') as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
    name="asyncminehut",
    version=version,
    license="MIT",
    description="An asynchronous wrapper for the Minehut API. https://api.minehut.com/",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/SuperOrca/asyncminehut",
    author="SuperOrca",
    packages=find_packages(),
    install_requires=["aiohttp", "datetime"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Natural Language :: English',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ],
)
