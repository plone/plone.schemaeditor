from setuptools import setup, find_packages
import os

version = '1.0a3'

setup(name='plone.schemaeditor',
      version=version,
      description="Provides through-the-web editing of a zope 3 schema/interface.",
      long_description=open(os.path.join('plone', 'schemaeditor', "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope2",
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone schema ttw',
      author='David Glick',
      author_email='davidglick@onenw.org',
      url='http://svn.plone.org/svn/plone/plone.schemaeditor',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # Zope 2,
          'zope.interface',
          'zope.component',
          'zope.schema',
          'zope.publisher',
          'zope.app.schema',
          'z3c.form',
          'plone.z3cform',
          'plone.i18n',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
