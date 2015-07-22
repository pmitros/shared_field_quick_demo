"""Setup for shared_field_demo XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='shared_field_demo-xblock',
    version='0.1',
    description='shared_field_demo XBlock',   # TODO: write a better description.
    packages=[
        'shared_field_demo',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'shared_field_demo = shared_field_demo:SharedFieldDemoXBlock',
        ]
    },
    package_data=package_data("shared_field_demo", ["static", "public"]),
)
