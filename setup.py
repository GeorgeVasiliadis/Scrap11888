from setuptools import setup
from setuptools import find_packages

setup(
        name="Scrap11888",
        version="4.4",
        description="A simple data scraping utility, used to extract data from 11888.gr",
        long_description=open("README.md", "r").read(),
        long_description_content_type="text/markdown",
        author="George Vasiliadis",
        author_email="geor.vasiliadis@gmail.com",
        url="https://github.com/GeorgeVasiliadis/Scrap11888",
        classifiers=[
            "Intended Audience :: End Users/Desktop",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Topic :: Software Development :: User Interfaces",
            "Topic :: Utilities"
        ],
        install_requires=[
            "requests",
            "openpyxl"
        ],
        entry_points = {
            "console_scripts": ["scrap=Scrap11888:main"]
        },
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False
)
