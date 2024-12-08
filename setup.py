"""Setup configuration for the Banana Math Puzzle game."""

from setuptools import setup, find_packages

setup(
    name='banana_math_puzzle',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'kivy==2.2.1',
        'colorlog==6.8.0',
        'aiohttp==3.9.3',
        'bcrypt==4.1.2',
        'filelock==3.13.1',
        'netifaces==0.11.0',  # Network interface information
        'requests==2.31.0',   # Backup HTTP library
        'python-dateutil==2.8.2',
        'typing-extensions==4.9.0',
        'numpy==1.24.3',
        'python-dotenv==1.0.0',
        'dataclasses==0.8; python_version < "3.7"',
        'asyncio==3.4.3',
        'cachetools==5.3.3',
        'structlog==24.1.0',
        'cryptography==42.0.5'
    ],
    extras_require={
        'dev': [
            'black==23.12.1',
            'mypy==1.8.0',
            'pytest==8.0.2',
            'pytest-cov==4.1.0',
            'pylint==3.0.3',
            'flake8==7.0.0',
            'isort==5.13.2',
            'pre-commit==3.6.2'
        ]
    },
    python_requires='>=3.9,<3.12',
    entry_points={
        'console_scripts': [
            'banana-math-puzzle=main:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    description='An educational math puzzle game with banana-themed challenges',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Banana Math Puzzle Team',
    author_email='support@bananamathpuzzle.com',
    url='https://github.com/yourusername/banana-math-puzzle'
)
