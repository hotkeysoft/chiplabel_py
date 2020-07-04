import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chiplabel",
    version="1.0.0",
    author="Dominic Thibodeau",
    author_email="dev@hotkeysoft.net",
    description="Chip label generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hotkeysoft/chiplabel_py",
    packages=setuptools.find_packages(),
    include_package_data = True,
    package_data={'chiplabel': ['fonts/*', 'chips/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['Pillow', 'PyYAML'],
    #scripts = ['bin/chip_label.py'],
    entry_points={
        'console_scripts': ['chip_label=chiplabel.__main__:main']
    },    
 )
