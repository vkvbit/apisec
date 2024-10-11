from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='apisec',
    version='1.0',
    packages=['apisec'],
    url='https://github.com/vkvbit/apisec',
    download_url='https://github.com/vkvbit/apisec',
    license='MIT',
    author='Vaibhav Kumar',
    author_email='myselfv@hotmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['apisec', 'rest', 'graphql', 'soap', 'restful, api', 'security', 'scanner', 'tool', "vulnerability"],    
    entry_points={
        'console_scripts': [
            'apisec = apisec.__main__:main'
         ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'offat',
        'argparse',
        'os',
        'sys'
    ],
)
