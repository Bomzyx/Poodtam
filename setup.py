import os

from setuptools import setup, find_packages

requires = []
with open("requirements.txt", "r") as fp:
    requires = [t.strip() for t in fp.read().split("\n") if len(t.strip()) > 0]

init = os.path.join(os.path.dirname(__file__), "poodtam", "__init__.py")
version_line = list(filter(lambda l: l.startswith("__version__"), open(init)))[0]
VERSION = version_line.split("=")[-1].replace("'", "").strip()

setup(
    name="poodtam",
    version=0.1,
    description="",
    # long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="",
    author_email="",
    url="",
    keywords="",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite="poodtam",
    entry_points={
        "console_scripts": [
            "poodtam-web = poodtam.cmd.web:main",
            "poodtam-worker=poodtam.cmd.worker:main"
        ]
    },
)
