# README: HOW TO INSTALL
#
# rm -Rf venv && ~/.pyenv/versions/3.8.8/bin/python -m venv venv
# . venv/bin/activate.fish
# pip install -U pip && pip install wheel && pip install -U setuptools && pip install .

import setuptools
from foxylib.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

# 2026-09-23 정리 — **cakeaholic 이 실제로 import 하는 것만** 남긴다.
#
# 왜: foxylib 은 cakeaholic 의 `backend/foxylib` submodule 로 **소스 소비**된다 (pip 설치 아님).
#   그런데 여기 install_requires 가 60여 개를 들고 있어서, 그게 곧 cakeaholic 의 의존성이 되고
#   Dependabot alert 로 쌓였다 — notebook(Jupyter 전체), authlib, Pillow, elasticsearch, cloudinary,
#   selenium, pytube, ortools, psycopg2, stripe, slackclient, PyGithub, pyhwp, xlutils, WTForms 등은
#   **cakeaholic 에서 import 0건**이었다 (전수 AST 스캔).
#
# 기준: cakeaholic 이 닿는 foxylib 모듈 75개가 요구하는 서드파티만. 버전은 cakeaholic lock 과 같은 하한.
#   botocore/bson/werkzeug 는 boto3/pymongo/flask 가 끌어오므로 따로 적지 않는다.
#
# ⚠ 여기서 뺀 패키지를 쓰는 foxylib 모듈(tools/cdn, tools/selenium, tools/payment 등)은 그대로 있다.
#   그 모듈을 새로 쓰려면 해당 패키지를 **쓰는 쪽에서** 선언해야 한다.
install_requires = [
    "arrow>=0.15.6",
    "beautifulsoup4>=4.7.1",
    "dacite @ git+https://git@github.com/yerihyo/dacite.git@yerihyo-1.0.0",
    "flask>=3.1.3",
    "forex-python>=1.5",
    "future>=1.0.0",
    "google-api-python-client>=2.81.0",
    "google-auth>=2.58.0",
    "google-auth-oauthlib>=1.0.0",
    "jinja2>=3.1.6",
    "logzio-python-handler>=3.0.0",
    "markupsafe>=3.0.3",
    "numpy>=1.26.4",
    "oauth2client>=4.1.3",
    "phonenumbers>=9.0.17",
    "pipetools>=0.3.6",
    "pymongo>=3.11.0",
    "pytest>=9.1.1",
    "python-dateutil>=2.9.0.post0",
    "pytimeparse>=1.1.8",
    "pytz>=2024.2",
    "pyyaml>=6.0.3",
    "requests>=2.34.2",
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
