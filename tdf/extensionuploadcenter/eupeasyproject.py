from tdf.extensionuploadcenter import MessageFactory as _
import re
from collective import dexteritytextindexer
from plone.supermodel import model
from zope import schema
from plone.app.textfield import RichText
from plone.autoform import directives
from plone.supermodel.directives import primary
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.interface import Invalid, invariant
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder
from plone.namedfile.field import NamedBlobImage, NamedBlobFile


checkfileextension = re.compile(
    r"^.*\.(png|PNG|gif|GIF|jpg|JPG)").match

def validateImageextension(value):
    if not checkfileextension(value.filename):
        raise Invalid(u"You could only add images in the png, gif or jpg file format to your project.")
    return True


checkdocfileextension = re.compile(
    r"^.*\.(pdf|PDF|odt|ODT)").match


checkEmail = re.compile(
    r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match


def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u"Invalid email address"))
    return True

def vocabCategories(context):
    # For add forms

    # For other forms edited or displayed
    from tdf.extensionuploadcenter.eupcenter import IEUpCenter
    while context is not None and not IEUpCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
        context = context.__parent__

    category_list = []
    if context is not None and context.available_category:
        category_list = context.available_category

    terms = []
    for value in category_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)

directlyProvides(vocabCategories, IContextSourceBinder)

def vocabAvailVersions(context):
    """ pick up the program versions list from parent """
    from tdf.extensionuploadcenter.eupcenter import IEUpCenter
    while context is not None and not IEUpCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
        context = context.__parent__

    versions_list = []
    if context is not None and context.available_versions:
        versions_list = context.available_versions

    terms = []
    for value in versions_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))
    return SimpleVocabulary(terms)


directlyProvides(vocabAvailVersions, IContextSourceBinder)

def isNotEmptyCategory(value):
    if not value:
        raise Invalid(u'You have to choose at least one category for your project.')
    return True

def vocabAvailLicenses(context):
    """ pick up licenses list from parent """

    # For other forms edited or displayed
    from tdf.extensionuploadcenter.eupcenter import IEUpCenter
    while context is not None and not IEUpCenter.providedBy(context):
        # context = aq_parent(aq_inner(context))
        context = context.__parent__

    license_list = []
    if context is not None and context.available_licenses:
        category_list = context.available_licenses
    terms = []
    for value in license_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))
    return SimpleVocabulary(terms)

directlyProvides(vocabAvailLicenses, IContextSourceBinder)

def validateextensionfileextension(value):
    if not checkfileextension(value.filename):
        raise Invalid(u'You could only upload LibreOffice extension files with a proper file extension.\n'
                      u'LibreOffice extensions have an \'oxt\' file extension.')
    return True


class IEUpEasyProject(model.Schema):

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Project Title - minimum 5 and maximum 50 characters"),
        min_length=5,
        max_length=50
    )

    dexteritytextindexer.searchable('description')
    description = schema.Text(
        title=_(u"Project Summary"),
    )

    dexteritytextindexer.searchable('details')
    primary('details')
    details = RichText(
        title=_(u"Full Project Description"),
        required=False
    )

    dexteritytextindexer.searchable('category_choice')
    directives.widget(category_choice=CheckBoxFieldWidget)
    category_choice = schema.List(
        title=_(u"Choose your categories"),
        description=_(u"Please select the appropriate categories (one or more) for your project."),
        value_type=schema.Choice(source=vocabCategories),
        constraint=isNotEmptyCategory,
        required=True
    )

    contactAddress = schema.TextLine(
        title=_(u"Contact email-address"),
        description=_(u"Contact email-address for the project."),
        constraint=validateEmail
    )

    screenshot = NamedBlobImage(
        title=_(u"Screenshot of the Extension"),
        description=_(u"Add a screenshot by clicking the 'Browse' button. You could provide an image of the file "
                      u"format 'png', 'gif' or 'jpg'."),
        required=False,
        constraint=validateImageextension
    )

    releasenumber = schema.TextLine(
        title=_(u"Release Number"),
        description=_(u"Release Number (up to twelf chars)"),
        default=_(u"1.0"),
        max_length=12,
    )

    directives.widget(compatibility_choice=CheckBoxFieldWidget)
    compatibility_choice = schema.List(
        title=_(u"Compatible with versions of LibreOffice"),
        description=_(u"Please mark one or more program versions with which this release is compatible with."),
        value_type=schema.Choice(source=vocabAvailVersions),
        required=True,
        default=[]
    )

    file = NamedBlobFile(
        title=_(u"The first file you want to upload."),
        description=_(u"Please upload your file."),
        required=True,
        constraint=validateextensionfileextension,
    )