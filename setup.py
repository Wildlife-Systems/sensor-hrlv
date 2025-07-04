from setuptools import setup, find_packages

setup(
    name="sensor-hrlv",
    version="0.0.1",
    description="A Python package for reading data from the HRLV sensor.",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/sensor-hrlv",
    packages=find_packages(),
    install_requires=[
        "serial"
    ],
    entry_points={
        "console_scripts": [
            "sensor-dht11=sensor_dht11.sensor:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)