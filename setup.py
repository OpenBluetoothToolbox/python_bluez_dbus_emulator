import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="bluez_dbus_emulator",
    version="0.1.0",
    description="Python BlueZ DBus emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenBluetoothToolbox/python_bluez_dbus_emulator",
    author="Kevin Dewald",
    packages=find_packages(),
    install_requires=["dbus_next"],
    zip_safe=True,
    python_requires=">=3.5.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
