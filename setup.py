import setuptools
from foxylib.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "future==0.17.1",
    "nose==1.3.7",
    "Pillow==6.2.1",
    "pyyaml==5.2",
    "python-dateutil==2.8.0",
    "Jinja2==2.10.1",
    "ply==3.11",

    "uritemplate==3.0.0",
    "google-api-python-client==1.7.8",
    "google-auth==1.8.1",
    "google-auth-httplib2==0.0.3",
    "google-auth-oauthlib==0.4.1",

    "oauth2client==4.1.3",
    "pytz==2019.3",
    "requests==2.22.0",
    "numpy==1.16.2",
    "elasticsearch==7.0.1",
    "beautifulsoup4==4.7.1",
    "frozendict==1.2",
    "dill==0.3.0",
    "pymongo==3.8.0",
    "pytz==2019.3",
    "iso3166==1.0",
    "pytest==5.2.2",
    "PyGithub==1.44.1",
    # "python-magic==0.4.15",
    # "filetype==1.0.5",
    "notebook==6.0.2",
    "slackclient==2.5.0",
    "sendgrid==6.1.0",
    "stripe==2.41.1",
    "connexion[swagger-ui]==2.6.0",

    "authlib==0.13",

    "pyhwp==0.1b12",
    "xlutils==2.0.0",
    "WTForms==2.2.1",

    "python-coveralls==2.9.3",
    "pytest-cov==2.8.1",

    "cachetools==3.1.1",
    # "aiohttp==3.6.2",
    #"async-timeout==3.0.1",
    #"overwatch-api==0.5",
    # "oauthlib==3.1.0",
    # "pyvirtualdisplay==0.2.1",
    # "selenium==3.141.0",
]


setuptools.setup(
    name="foxylib",
    version=__version__,
    description=("First package"),
    author="Moonyoung Kang",
    author_email="yerihyo@gmail.com",
    long_description="foxylib",
    #long_description_content_type="text/markdown",
    url="https://github.com/foxytrixy-com/foxylib",
    install_requires=install_requires,

    packages=setuptools.find_namespace_packages(exclude=["scripts*","venv*"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
