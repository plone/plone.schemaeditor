Introduction
============

plone.schemaeditor provides a through-the-web interface for modifying Zope 3
schemata (interfaces).

Currently there is support for:

 * adding and removing fields
 * editing attributes of existing fields
 * reordering fields
 * renaming fields
 * organizing fields into fieldsets

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
 * Datetime
 * Choice (with simple list of values)
 * List of Choice (with simple list of values)

Third-party packages can make additional field types available by registering
new IFieldFactory utilities.

Dependencies
============

* Zope 2
* z3c.form
* plone.z3cform

Despite the namespace, Plone is not a dependency.

Note: This package is released under a BSD license. Contributors, please do not
add dependencies on GPL code.

Credits
=======

Author:

 * David Glick (dglick@gmail.com)

Contributors:

 * Nathan Van Gheem
 * Martin Aspeli
 * Alex Limi
 * Ross Patterson
 * Steve McMahon
 * Thomas Desvenain

