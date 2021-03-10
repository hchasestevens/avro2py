from pathlib import Path

from setuptools import setup, find_packages

extras_require = {
    'dev': [
        "pytest>=3.10.1",
        "pylint>=2.4.4",
        "mypy>=0.740",
    ],
}

ROOT = Path(__file__).parent
VERSION_PATH = ROOT / 'avro2py' / 'VERSION'
with VERSION_PATH.open('r') as f:
    VERSION = f.read().strip()

packages = find_packages(exclude=("tests", "tests.*"))
setup(
    name='avro2py',
    packages=[
        'avro2py',
    ],
    package_data={'avro2py': ['VERSION']},
    platforms='any',
    extras_require=extras_require,
    version=VERSION,
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
