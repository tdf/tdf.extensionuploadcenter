from tdf.extensionuploadcenter import MessageFactory as _
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema
from Products.Five import BrowserView
from Acquisition import aq_inner
from plone import api
from collective import dexteritytextindexer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import directlyProvides
import re
from plone.namedfile.field import NamedBlobImage
from zope.interface import Invalid, invariant



def vocabCategories(context):
    # For add forms

    # For other forms edited or displayed
    from tdf.extensionuploadcenter.eupcenter import IEUpCenter
    while context is not None and not IEUpCenter.providedBy(context):
        #context = aq_parent(aq_inner(context))
        context = context.__parent__

    category_list = []
    if context is not None and context.available_category:
        category_list = context.available_category

    terms = []
    for value in category_list:
        terms.append(SimpleTerm(value, token=value.encode('unicode_escape'), title=value))

    return SimpleVocabulary(terms)
directlyProvides(vocabCategories, IContextSourceBinder)



def isNotEmptyCategory(value):
    if not value:
        raise Invalid(u'You must choose at least one category for your project.')
    return True




checkEmail = re.compile(
    r"[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}").match

def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u"Invalid email address"))
    return True


class ProvideScreenshotLogo(Invalid):
    __doc__ =  _(u"Please add a Screenshot or a Logo to your project")



class MissingCategory(Invalid):
    __doc__ = _(u"You have not chosen a category for the project")



class IEUpProject(model.Schema):


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
    model.primary('details')
    details = RichText(
        title=_(u"Full Project Description"),
        required=False
    )



    dexteritytextindexer.searchable('category_choice')
    category_choice = schema.List(
        title=_(u"Choose your categories"),
        description=_(u"Please mark one or using the 'CTRL' key two and more entry on the left side and use the arrows in the middle to choose them and get them into the selected items box on the right side."),
        value_type=schema.Choice(source=vocabCategories),
        constraint = isNotEmptyCategory,
        required=True
    )


    contactAddress=schema.ASCIILine(
        title=_(u"Contact email-address"),
        description=_(u"Contact email-address for the project."),
        constraint=validateEmail
    )

    homepage=schema.URI(
        title=_(u"Homepage"),
        description=_(u"If the project has an external home page, enter its URL (example: 'http://www.mysite.org')."),
        required=False
    )

    documentation_link=schema.URI(
        title=_(u"URL of documentation repository "),
        description=_(u"If the project has externally hosted documentation, enter its URL (example: 'http://www.mysite.org')."),
        required=False
    )

    project_logo = NamedBlobImage(
        title=_(u"Logo"),
        description=_(u"Add a logo for the project (or organization/company) by clicking the 'Browse' button."),
        required=False,
    )

    screenshot = NamedBlobImage(
        title=_(u"Screemshot of the Extension"),
        description=_(u"Add a screenshot by clicking the 'Browse' button."),
        required=False,
    )


    @invariant
    def missingScreenshotOrLogo(data):
        if not data.screenshot and not data.project_logo:
            raise ProvideScreenshotLogo(_(u'Please add a Screenshot or a Logo to your project page'))



class EUpProjectView(BrowserView):
    pass


