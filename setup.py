from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='airdrums',
    version='1.0',
    author=['Joseíto Oliveira', 'Pedro Cavalcante', 'Rubens Brasil'],
    author_email='youremail@example.com',
    description='A module for playing drums virtually using air gestures',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

