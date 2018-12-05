import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="heatzy",
    version="0.0.4",
    author="Thomas MONZIE",
    author_email="thomas.monzie@gmail.com",
    description="Controller for Heatzy products",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tmz42/heatzy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests","paho-mqtt"],
    scripts=['bin/heatzy-cli', 'bin/heatzy-mqtt']
)