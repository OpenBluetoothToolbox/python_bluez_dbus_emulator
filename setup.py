import os
import platform
import sys
from setuptools import setup, find_packages


setup(
    name='bluez_dbus_emulator',
    version='0.0.1',
    description='Python BlueZ DBus emulator',
    url='https://github.com/OpenBluetoothToolbox/python_bluez_dbus_emulator',
    author='Kevin Dewald',
    packages=find_packages(),
    install_requires=[
        'dbus_next'
    ],
    zip_safe=True,
    python_requires='>=3.5.6'
)
