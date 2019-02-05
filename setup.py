import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

VERSION="0.3.0"

setuptools.setup(
    name="foxlib",
    version=VERSION,
    description="First package",
    author="Moonyoung Kang",
    author_email="yerihyo@gmail.com",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/foxytrixy-com/foxlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)