from setuptools import find_packages, setup

VERSION = '0.2.0'

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
    keywords=['IoC', 'auto config'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-dotenv>=1.0.0',
        'filetype>=1.2.0',
        'loguru>=0.7.0',
        'pyyaml>=6.0.1',
        'wrapt>=1.14.1',
        'pydantic>=1.10.12'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
)