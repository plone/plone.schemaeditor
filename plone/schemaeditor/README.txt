Introduction
============

plone.schemaeditor provides a through-the-web interface for modifying Zope 3 schemata (interfaces).

Currently field attributes can be modified on simple fields.  Coming soon:

 * adding and removing fields
 * reordering fields
 * (maybe) support for more complicated field types, e.g. Choice

plone.schemaeditor only handles the actual schema editing.  To be useful, it requires some
integration code to take care of the following pieces:

 * traversing to a schema context
 * persisting schema changes across Zope restarts

See plone.app.dexterity (along with plone.dexterity and plone.supermodel) for one approach
to this integration.


Dependencies
============

* Zope 2 (Though the actual forms are z3c.form-based and not Zope 2 dependent, so it shouldn't take
  too much work to refactor to work in Zope 3 as well.)
* z3c.form
* plone.z3cform

Despite the name, Plone is not a dependency.


Navigating to a schema
======================

Let's import some ZCML which will set up a dummy schema context that will allow us
to demonstrate editing the zope.schema.interfaces.IField schema, via the /schemaeditor URL::

    >>> from Products.Five import zcml
    >>> import plone.schemaeditor.tests
    >>> zcml.load_config('tests.zcml', package=plone.schemaeditor.tests)
    
And set up the test browser::
    
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = 'http://nohost'
    >>> browser.handleErrors = False

If we try to access the schema editor without logging in, we should get an Unauthorized
error::

    >>> browser.open(portal_url + '/@@schemaeditor')
    Traceback (most recent call last):
    ...
    Unauthorized: ...You are not authorized to access this resource...
    
We need to log in as a manager, because by default only managers get the 'Manage Schemata' permission::

    >>> self.app.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])
    >>> browser.addHeader('Authorization', 'Basic root:secret')

Now we should be able to navigate to the IField schema in the browser::

    >>> browser.open(portal_url + '/@@schemaeditor')
    >>> 'Edit @@schemaeditor' in browser.contents
    True


Editing a schema field attribute
================================

Now let's navigate to the 'title' field of the IField schema::

    >>> browser.getLink('Title').click()
    >>> browser.url
    'http://nohost/@@schemaeditor/title'
    >>> "Edit Field 'title'" in browser.contents
    True

Now we can change various attributes.  For instance, let's change the field title
(note that this is the title of a field whose id is 'title' -- confusing I know!)::

    >>> browser.getControl('Title').value = 'Moniker'
    
And now click the button to save the change.  This should take us back to the list
of schema fields, which should reflect the change::

    >>> browser.getControl('Save').click()
    >>> browser.url
    'http://nohost/@@schemaeditor'
    >>> 'Moniker' in browser.contents
    True
    
Let's confirm that the new field title was correctly saved to the actual schema::

    >>> from zope.schema.interfaces import IField
    >>> IField['title'].title
    u'Moniker'

Let's go back and try to make an invalid change.  The form won't let us. (Note
that we need to use 'Moniker' instead of 'Title' like we did above, because we have
edited the schema which is actually used to render the field edit form!)::

    >>> browser.getLink('Moniker').click()
    >>> browser.url
    'http://nohost/@@schemaeditor/title'
    >>> browser.getControl('Minimum length').value = 'asdf'
    >>> browser.getControl('Save').click()
    >>> browser.url
    'http://nohost/@@schemaeditor/title'
    >>> 'The entered value is not a valid integer literal.' in browser.contents
    True

We can give up and hit the Cancel button, which should take us back to the schema listing,
without trying to save changes::

    >>> browser.getControl('Cancel').click()
    >>> browser.url
    'http://nohost/@@schemaeditor'
    >>> IField['title'].title
    u'Moniker'


Authors
=======

* David Glick (davidglick@onenw.org)
* Nathan Van Gheem (vangheem@gmail.com)
