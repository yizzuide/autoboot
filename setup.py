from setuptools import find_packages, setup

VERSION = '0.6.0'

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='autoboot',
    version=VERSION,
    author='yizzuide',
    author_email='fu837014586@163.com',
    description='IoC with auto config framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/yizzuide/autoboot',
    keywords=['IoC', "event", 'auto config'],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'python-dotenv>=1.0.0',
        'filetype>=1.2.0',
        'loguru>=0.7.0',
        'pyyaml>=6.0.1',
        'wrapt>=1.14.1',
        'pydantic>=1.10.12',
        'result>=0.14.0',
        'durations>=0.3.3',
    ],
    tests_require=[
        'pytest>=6.2.0',
        'pytest-cov>=2.10.0'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License'
    ],
)