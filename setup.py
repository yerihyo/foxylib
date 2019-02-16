import setuptools
from version import __version__

# with open("README.md", "r") as fh:
#     long_description = fh.read()

install_requires = [
    "future==0.17.1",
    "nose==1.3.7",
    "Pillow==5.4.1",
    "pyyaml==3.13",
    "python-dateutil==2.8.0",
    "Jinja2==2.10",
    "ply==3.11",
]

setuptools.setup(
    name="foxylib",
    version=__version__,
    description="First package",
    author="Moonyoung Kang",
    author_email="yerihyo@gmail.com",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/foxytrixy-com/foxylib",
    install_requires=install_requires,

    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
