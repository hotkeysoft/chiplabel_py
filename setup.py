import setuptools
from distutils.util import convert_path

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

version_info = {}
ver_path = convert_path('chiplabel/_version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), version_info)

setuptools.setup(
    name = "chiplabel",
    version = version_info['__version__'],
    author = version_info['__author__'],
    author_email = version_info['__author_email__'],
    description = version_info['__description__'],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = version_info['__url__'],
    packages=setuptools.find_packages(include=['chiplabel']),
    include_package_data = True,
    package_data={'chiplabel': ['fonts/*', 'chips/*']},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires = '>=3.6',
    install_requires = ['Pillow', 'PyYAML'],
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    entry_points = {
        'console_scripts': ['chip_label=chiplabel.__main__:main']
    },
 )
