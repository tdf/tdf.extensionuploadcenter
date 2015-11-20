from tdf.extensionuploadcenter import MessageFactory as _
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema
from Products.Five import BrowserView
from Acquisition import aq_inner
from plone import api


class IEUpCenter(model.Schema):

    """ An Extension Upload Center for LibreOffice extensions.
    """



    title= schema.TextLine(
        title=_(u"Name of the Extensions Center"),
    )

    description=schema.Text(
        description=_(u"Description of the Extensions Center"),
    )

    product_description=schema.Text(
        description=_(u"Description of the features of extensions")
    )


    product_title = schema.TextLine(
        title=_(u"Extension Product Name"),
        description=_(u"Name of the Extension product, e.g. only Extensions or LibreOffice Extensions"),
    )


    development_status = schema.List(title=_(u"Development Status"),
        default=['Planing',
                 'Pre-Alpha',
                 'Alpha',
                 'Beta',
                 'Production/Stable',
                 'Mature',
                 'Inactive'],
        value_type=schema.TextLine()
    )


    available_category = schema.List(title=_(u"Available Categories"),
        default=['Gallery Contents',
                 'Language Tools',
                 'Dictionary',
                 'Writer_Extension',
                 'Calc_Extension',
                 'Impress_Extension',
                 'Draw_Extension',
                 'Base_Extension',
                 'Math_Extension',
                 'Extension_Building',
                 'All modules'],

        value_type=schema.TextLine())


    available_licenses =schema.List(title=_(u"Available Licenses"),
        default=['GPL (GNU General Public License)',
                 'GNU-GPL-v3 (General Public License Version 3)',
                 'LGPL (GNU Lesser General Public License)',
                 'LGPL-v3+ (GNU Lesser General Public License Version 3 and later)',
                 'BSD (BSD License (revised))',
                 'MPL-v1.1 (Mozilla Public License Version 1.1',
                 'CC-by-sa-v3 (Creative Commons Attribution-ShareAlike 3.0)',
                 'Public Domain',
                 'OSI (Other OSI Approved)'],
        value_type=schema.TextLine())

    available_versions = schema.List(title=_(u"Available Versions"),
        default=['LibreOffice 3.3',
                 'LibreOffice 3.4',
                 'LibreOffice 3.5',
                 'LibreOffice 3.6',
                 'LibreOffice 4.0',
                 'LibreOffice 4.1',
                 'LibreOffice 4.2',
                 'LibreOffice 4.3',
                 'LibreOffice 4.4',
                 'LibreOffice 5.0'],
        value_type=schema.TextLine())

    available_platforms = schema.List(title=_(u"Available Platforms"),
        default=['All platforms',
                 'Linux',
                 'Linux-x64',
                 'Mac OS X',
                 'Windows',
                 'BSD',
                 'UNIX (other)'],
         value_type=schema.TextLine())



    model.primary('install_instructions')
    install_instructions = RichText(
        title=_(u"Extension Installation Instructions"),
        default=_(u"Fill in the install instructions"),
        required=False
    )

    model.primary('reporting_bugs')
    reporting_bugs = RichText(
        title=_(u"Instruction how to report Bugs"),
        required=False
    )

    title_legaldisclaimer = schema.TextLine(
        title=_(u"Title for Legal Disclaimer and Limitations"),
        default=_(u"Legal Disclaimer and Limitations"),
        required=False
    )


    title_legaldownloaddisclaimer = schema.TextLine(
        title=_(u"Title of the Legal Disclaimer and Limitations for Downloads"),
        default=_(u"Legal Disclaimer and Limitations for Downloads"),
        required=False
    )

    model.primary('legal_downloaddisclaimer')
    legal_downloaddisclaimer = RichText(
        title=_(u"Text of the Legal Disclaimer and Limitations for Downlaods"),
        description=_(u"Enter any legal disclaimer and limitations for downloads that should appear on each page for dowloadable files."),
        default=_(u"Fill in the text for the legal download disclaimer"),
        required=False
    )


# Views

class EUpCenterView(BrowserView):



    def eupprojects(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return catalog(object_provides=IEUpProject.__identifier__,
             path='/'.join(context.getPhysicalPath()),
             sort_order='sortable_title')



    def get_latest_program_release(self):
        """Get the latest version from the vocabulary. This only
        goes by string sorting so would need to be reworked if the
        LibreOffice versions dramatically changed"""

        versions = list(self.context.available_versions)
        versions.sort(reverse=True)
        return versions[0]


    def category_name(self):
        category = list(self.context.available_category)
        return category



    def eupproject_count(self):
        """Return number of projects
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return len(catalog(portal_type='tdf.extensionuploadcenter.eupproject'))


    def euprelease_count(self):
        """Return number of downloadable files
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name='portal_catalog')

        return len(catalog(portal_type='tdf.extensionuploadcenter.euprelease'))
