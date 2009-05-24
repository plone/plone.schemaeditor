Introduction
============

plone.schemaeditor provides a through-the-web interface for modifying Zope 3
schemata (interfaces).

Currently there is support for:

 * adding and removing fields
 * editing attributes of existing fields
 * reordering fields
 * renaming fields

plone.schemaeditor only handles the actual schema editing.  To be useful, it
requires some integration code to take care of the following pieces:

 * traversing to a schema that is used as the context of the editor
 * persisting schema changes across Zope restarts

See plone.app.dexterity (along with plone.dexterity and plone.supermodel) for
one approach to this integration.

The following field types (from zope.schema) are currently supported:

 * TextLine
 * Text
 * Int
 * Float
 * Bool
 * Password
 * Bytes
 * Datetime


Dependencies
============

* Zope 2 (Though the actual forms are z3c.form-based and not Zope 2 dependent, so it shouldn't take
  too much work to refactor to work in Zope 3 as well.)
* z3c.form
* plone.z3cform

Despite the name, Plone is not a dependency.


Credits
=======

Author:

 * David Glick (davidglick@onenw.org)

Thanks to:

 * Nathan Van Gheem
 * Martin Aspeli
 * Alex Limi
