import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chiplabel",
    version="1.0.0a1",
    author="Dominic Thibodeau",
    author_email="dev@hotkeysoft.net",
    description="Chip label generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hotkeysoft/chiplabel_py",
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
    python_requires='>=3.6',
    install_requires=['Pillow', 'PyYAML'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['chip_label=chiplabel.__main__:main']
    },
 )
