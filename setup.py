from setuptools import setup

setup(
    name='buckgo',
    version='1.0',
    description='Tool to interact with S3',
    author='Sandjaie',
    py_modules=['buckgo'],
    install_requires=['click', 'boto3'],
    entry_points={
        'console_scripts': [
            'buckgo=buckgo:main',
        ],
    },
)
