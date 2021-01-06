from setuptools import setup, find_packages

extras_require = {
    'dev': [
        "pytest>=3.10.1",
        "pylint>=2.4.4",
        "mypy>=0.740",
    ],
}

packages = find_packages(exclude=("tests", "tests.*"))
setup(
    name='avro2py',
    packages=[
        'avro2py',
    ],
    platforms='any',
    extras_require=extras_require,
    version="0.0.2",
    description='Avro codegen for Python 3.6+',
    author='H. Chase Stevens',
    author_email='chase@chasestevens.com',
    url='https://github.com/hchasestevens/avro2py',
    license='MIT',
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'avro2py = avro2py.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ]
)
