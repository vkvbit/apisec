from setuptools import setup, find_packages

setup(
    name='apisec',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'apisec = apisec.__main__:main'
        ]
    },
    install_requires=[
        "offat"
    ],
)