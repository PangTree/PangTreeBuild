import setuptools


setuptools.setup(
    name='poapangenome',
    version='0.2dev',
    author="Paulina Dziakdiewicz",
    author_email="pedziadkiewicz@gmail.com",
    description="Multiple sequence alignment analysis with consensus generation",
    url="https://github.com/meoke/pang",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    install_requires=['biopython', 'numpy', 'jsonpickle', 'ddt', 'networkx', 'six'],
    license='MIT Licence',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)