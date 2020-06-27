# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '2.1.1'

setup(
    name='plone.schemaeditor',
    version=version,
    description="Provides through-the-web editing of a zope schema/interface.",
    long_description=open("README.rst").read() + "\n" +
    open("CHANGES.rst").read(),
    classifiers=[
        "Development Status :: 6 - Mature",
        "Framework :: Zope2",
        "Framework :: Zope :: 4",
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
    keywords='plone schema ttw',
    author='David Glick',
    author_email='dglick@gmail.com',
    url='https://github.com/plone/plone.schemaeditor',
    license='BSD',
    packages=find_packages(),
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'six',
        'Zope2',
        'zope.cachedescriptors',
        'zope.component',
        'zope.container',
        'zope.globalrequest',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.schema',
        'zope.publisher',
        'z3c.form',
        'plone.z3cform',
        'plone.autoform',
    ],
    extras_require={'test': [
        'plone.app.dexterity',
        'plone.app.testing',
        'plone.app.robotframework',
    ]},
)
