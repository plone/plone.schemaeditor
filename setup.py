from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "4.0.12.dev0"

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)

setup(
    name="plone.schemaeditor",
    version=version,
    description="Provides through-the-web editing of a zope schema/interface.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 6 - Mature",
        "Framework :: Zope",
        "Framework :: Zope :: 5",
        "Framework :: Plone",
        "Framework :: Plone :: Core",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
    keywords="plone schema ttw",
    author="David Glick",
    author_email="dglick@gmail.com",
    url="https://github.com/plone/plone.schemaeditor",
    license="BSD",
    packages=find_packages(),
    namespace_packages=["plone"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "Acquisition",
        "Products.statusmessages",
        "Zope",
        "plone.memoize",
        "plone.protect",
        "plone.supermodel",
        "setuptools",
        "zope.cachedescriptors",
        "zope.component",
        "zope.container",
        "zope.event",
        "zope.globalrequest",
        "zope.i18n",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.lifecycleevent",
        "zope.schema",
        "zope.security",
        "zope.publisher",
        "z3c.form",
        "plone.z3cform",
        "plone.autoform",
    ],
    extras_require={
        "test": [
            "six",
            "Products.Genericsetup",
            "plone.app.testing",
            "plone.app.robotframework",
            "plone.keyring",
            "plone.supermodel",
            "plone.testing",
            "robotsuite",
            "transaction",
        ]
    },
)
