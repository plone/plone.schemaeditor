Changelog
=========

2.0.13 (2017-01-01)
-------------------

Bug fixes:

- Test-Fix: Support latest zope.i18nmessageid.
  [jensens]


2.0.12 (2016-11-09)
-------------------

Bug fixes:

- Add coding headers on python files.
  [gforcada]

- Update code follow Plone styleguide.
  [gforcada]

2.0.11 (2016-08-15)
-------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


2.0.10 (2016-06-07)
-------------------

Fixes:

- Fix tests for fieldset ordering changes in plone.supermodel.
  [thet]

- Update url in setup.py to point to github.
  [esteele]


2.0.9 (2016-01-08)
------------------

Fixes:

- Remove unused locales folder, translations are now in plone.app.locales
  [vincentfretin]


2.0.8 (2015-12-03)
------------------

Fixes:

- Use plone domain for translations.
  [gforcada]


2.0.7 (2015-09-07)
------------------

- Make ``plone.protect.utils.addTokenToUrl`` a soft dependency, making this
  package usable in Plone < 5.0.
  [thet]


2.0.6 (2015-07-18)
------------------

- Supports additionalSchemata in field Add form.
  [ebrehault]


2.0.5 (2015-06-05)
------------------

- Add undeclared zope.cachedescriptors dependency.
  [timo]

- Fix javascript to reorder fields. It was conflicting with
  mockup jquery.event.(drag|drop).
  [vangheem]

- Add support for non-destructive editing of attributes with i18n
  Message values
  [datakurre]

- Add a "protected" method to IFieldFactory that may be used to determine
  if a particular field must be non editable and not movable using the editor
  (just like a behavior field).
  Override it for custom behavior in a subclass.
  [ebrehault]

2.0.4 (2015-05-13)
------------------

- Allow to hide the 'Save defaults' button
  [ebrehault]

- Fix delete method (it used to return html and it produced a plone.protect warning)
  [ebrehault]


2.0.3 (2015-05-04)
------------------

- Fix translation and sorting of field names.
  [MacYET, davisagli]

- pat-modal pattern has been renamed to pat-plone-modal
  [jcbrand]


2.0.2 (2015-03-13)
------------------

- Clean up testing setup. This solves some serious test isolation issues.
  [timo]

- Update markup and javscript for Plone 5.
  [davisagli]

- Make fieldset creation optional
  [ebrehault]

- Add CSRF protection token
  [ebrehault]


2.0.1 (2014-10-23)
------------------

- Fix schemaeditor.js to work with jQuery 1.9+.
  [bloodbare]

- Internationalize delete field confirmation message.
  [thomasdesvenain]

- We can set a fieldset description.
  [thomasdesvenain]

- We can set that field is required or not required on add form.
  [thomasdesvenain]


2.0 (2014-04-01)
----------------

- Fix test failures on Jenkins.
  [timo]

- Fix tests.
  [davisagli]

- On the listing, respect the SchemaContext label if supplied. Otherwise,
  build one based on the title. This gives us more label flexibility
  outside the dexterity schemaeditor context.
  [smcmahon]

- Integrated addTokenToUrl from plone.protect.utils on generated delete url.
  [Luke Brannon]

- Add fieldsWhichCannotBeDeleted attribute to SchemaContext, which can be
  used to disallow removal of certain fields.
  [davisagli]

- Fix removeField for EditableSchema to allow for the case where there
  is no fieldset on the schema
  [ianderso]


1.3.7 (2014-03-02)
------------------

- Fix packaging error.
  [esteele]


1.3.6 (2014-03-02)
------------------

- Use a different id for field edit form and listing form, to ease
  reuse of overlay behaviours.
  [thomasdesvenain]

- Fix French translation.
  [thomasdesvenain]

- Don't depend on popupform.js
  [davisagli]

1.3.5 (2014-01-27)
------------------

- Add an "editable" method to IFieldFactory that may be used to determine
  if a particular field is editable. Rationale: fields customized via XML
  editing are sometimes not going to be editable via schemaeditor due to
  an inability to handle custom vocabularies or sources. The field factory
  utility is a very convenient place to test this since it's already
  used to determine available fields and their addability.

  editable(fieldInstance) returns True in the base class. Override it for
  custom behavior in a subclass.
  [smcmahon]

- Add an "available" method to IFieldFactory that may be used to determine
  if a field factory is actually available in the current context. This always
  returns True in the base class. Override it if a field factory isn't useful
  unless conditions are met. Example: we can't use a field factory for
  RelationChoice unless the relationfield is activated in the Plone
  instance.
  [smcmahon]

- Fixed: on a multi selection field with a vocabulary name,
  when the field had been generated from a model,
  the vocabulary name was not selected on edit form.
  [thomasdesvenain]

1.3.4 (2013-12-07)
------------------

- Fixed drag and drop fields in fieldsets when form tabbing is disabled:
  we can drop a field into the fieldset legend (for example, when the fieldset is empty),
  or directly positioning it beside fields of the new fieldset.
  [thomasdesvenain]

- i18n fixes.
  [thomasdesvenain]

- Better string normalization when setting field id from field title
  (change accented or special characters with corresponding letters).
  [cedricmessiant]

- Added robot tests.
  [davisp, cedricmessiant, thomasdesvenain at toulouse-sprint]

- We can select a vocabulary factory on a choice field,
  among all registered vocabularies.
  We don't have an error anymore
  when we edit a choice field with a vocabulary factory.
  [thomasdesvenain]

- Fixed deleting field from fieldset.
  [kroman0]

1.3.3 (2013-08-13)
------------------

- Correct packaging issues in 1.3.2.
  [esteele]

1.3.2 (2013-08-13)
------------------

- Fieldsets wysiwyg management.
  We can add fieldsets to a schema.
  We can change the fieldset of a field by drag and drop.
  Fields reorder now works when we have fieldsets.
  [thomasdesvenain]

- Updated fr translation.
  [thomasdesvenain]

- Added pt_BR translation.
  [ericof]


1.3.1 (2013-03-05)
------------------

- Quote attribute value in xtags attribute style jquery selector used
  in prepOverlay for field settings. Absence of quote was causing a js error
  on clicking "Settings in schema editor.
  [smcmahon]


1.3.0 (2013-01-17)
------------------

- Use a *set* of choice fields for the "multiple choice" field option in the UI,
  instead of a *list* of choice fields. The latter is orderable and is a less
  common use case (plus we need a better widget for it).
  [davisagli]

- Make it possible for schema contexts to restrict the fields that can be added
  by defining an allowedFields property.
  [davisagli]

- Add more specific events for when a field is added or removed.
  [davisagli]

- I18n improved by adding many missing strings
  [giacomos]


1.2.1 (2012-08-29)
------------------

* Use zope.lifecycleevent.
  [hannosch]

* The field edit form now respects autoform hints. Additional schemata can
  be provided by registering an adapter of the schema context and field to
  ``plone.schemaeditor.interfaces.IFieldEditorExtender``.
  [davisagli]


1.2.0 - 2012-02-20
------------------

* Display fields from behaviors in the schema preview too.
  [davisagli]

* Prevent the user from creating fields with names that are reserved for
  Dublin Core metadata. ``title`` and ``description`` can still be used
  as long as the fields are of the correct type.
  [davisagli]

* Remove unhelpful help text for min_length and max_length fields.
  [davisagli]

* The schema listing preview now respects autoform hints (such as custom
  widgets).
  [davisagli]

* Make new boolean fields use the radio widget by default. The field now
  appears as "Yes/No" in the list of field types.
  [davisagli]

* Hide the 'read only' setting for fields.
  [davisagli]

* Edit field defaults from the schema listing instead of in the field
  overlays. This simplifies making sure that the default can't be set
  to invalid values.
  [davisagli]

* Limit the height of text areas in the schema listing to avoid extra
  scrolling.
  [davisagli]

* Fall back to normal traversal if a field isn't found when traversing the
  schema context. This fixes inline validation for forms on the schema
  context.
  [davisagli]

* Make it possible to make the schemaeditor not be the default view of the
  schema context, by specifying the ``schemaEditorView`` attribute on the
  schema context.
  [davisagli]

* Added Spanish translation.
  [hvelarde]

1.1.2 - 2011-11-26
------------------

* Add .mo files which were missing in 1.1.1.
  [davisagli]

1.1.1 - 2011-11-26
------------------

* Added internationalization and extracted messages for main languages.
  [thomasdesvenain]

* Added French translation.
  [thomasdesvenain]

* Added Italian translation.
  [giacomos]

1.1 - 2011-09-24
----------------

* Avoid errors when expanding the range of `min` and `max` attributes on a
  field, and when entering a `default` outside the range.
  [davisagli]

* Validate input for the `default` attribute of Choice fields based on the
  field's vocabulary.
  [davisagli]

* Removed support for setting the `missing_value` attribute of fields through
  the web.
  [davisagli]

* Add a date-only field with no time component.
  [davisagli]

* Bugfix: Validate short names of fields.
  [davisagli]

1.0.3 - 2011-06-15
------------------

* Fix test.
  [davisagli]

1.0.2 - 2011-06-14
------------------

* Make FieldFactory do a deep copy of its arguments to avoid problems with
  mutable defaults getting shared between field instances.
  This fixes http://code.google.com/p/dexterity/issues/detail?id=133
  [davisagli]

* Remove dependency on zope.app.schema.
  [davisagli]

1.0.1 - 2011-05-20
------------------

* Relicense under the BSD license.
  See http://plone.org/foundation/materials/foundation-resolutions/plone-framework-components-relicensing-policy
  [davisagli]

* On multiple choice fields (List of Choice), read/write attributes other than
  ``values`` in the correct place (on the List rather than its value_type
  Choice).
  [davisagli]

* Remove unneeded dependency on plone.i18n.
  [davisagli]

1.0 - 2011-04-30
----------------

* In addition to the normal object events raised when fields are added, edited,
  and removed, raise a SchemaModifiedEvent on the schema context. This greatly
  simplifies writing code to serialize schema changes, and makes it possible to
  track of the schema origin so that we know where to serialize it.
  [davisagli]

* Support non-ASCII characters in vocabularies for Choice fields.
  [davisagli]

* Change js event used to dynamically set id from title from keyup to change;
  autocompletion does not raise a keyup event, but does fire change.
  [smcmahon]

* jslintify schemaeditor.js
  [smcmahon]

* Honor cancel button in field editor popup.
  [smcmahon]

1.0b2 - 2011-01-22
------------------

* Add another possible base to try for our fixed IDatetime, since
  plone.app.z3cform may change which one takes precedence.
  [davisagli]

* Default to adding Textline fields.
  [davisagli]

1.0b1 - 2010-04-18
------------------

* Added overlay support to the field edit screens.
  [davisagli, limi]

* Revamped UI to show WYSIWYG representation of fields.
  [davisagli, limi]

* Removed the JavascriptFormWrapper.
  [davisagli]

* Major package cleanup.
  [davisagli]

* Omit the 'required' and 'missing_value' fields for Bool fields.
  [davisagli]

* Add the ability to define vocabularies of simple TextLine values.
  Both single and multiple select fields are provided.
  [rossp]

* Override base field interfaces to get the correct field types for the default
  and missing_value fields, rather than using the MetaFieldWidgetFactory.
  [rossp]

* Make sure that normalized ids for new fields use _ instead of -, so that they
  can be accessed without using getattr.
  [davisagli]

* Fix issue with moving fields to position 0 in a schema.
  [davisagli]

* List the available field type vocabulary alphabetically.
  [davisagli]

* No longer provide a field factory for zope.schema.Bytes, since
  plone.namedfile provides a better file field and now registers its own field
  factories.
  [davisagli]

* Fix inline validation for the field edit form.
  [davisagli]

* Added ReadOnlySchemaListing for listing fields without making them editable.
  [davisagli]

* CSS tweaks
  [davisagli]


1.0a2 - 2009-07-12
------------------

* Changed API methods and arguments to mixedCase to be more consistent with
  the rest of Zope. This is a non-backwards-compatible change. Our profuse
  apologies, but it's now or never. :-/

  If you find that you get import errors or unknown keyword arguments in your
  code, please change names from foo_bar too fooBar, e.g. add_field() becomes
  addField().
  [optilude]

1.0a1 - 2009-05-23
------------------

* Initial release
