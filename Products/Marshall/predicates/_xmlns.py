"""
$Id: _xmlns.py,v 1.1 2004/07/23 16:16:27 dreamcatcher Exp $
"""

from xml.dom import minidom
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.CMFCore.CMFCorePermissions import ManagePortal
from _base import Predicate
from Products.Marshall.registry import registerPredicate
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

def attrMethod(attr, default=''):
    def boundAttrMethod(self):
        return getattr(self, attr, default)
    return boundAttrMethod

class XMLNS(Predicate):
    """ Predicate matching xml files on a xmlns:attribute pair.
    """

    security = ClassSecurityInfo()
    security.declareProtected(ManagePortal, 'edit', 'getElementId',
                              'getElementNS', 'getElementName',
                              'getAttributeNS', 'getAttributeName',
                              'getValue')
    getElementNS = attrMethod('_element_ns')
    getElementName = attrMethod('_element_name')
    getAttributeNS = attrMethod('_attr_ns')
    getAttributeName = attrMethod('_attr_name')
    getValue = attrMethod('_value', None)

    manage_options = (
        Predicate.manage_options[0],
        {'label':'Settings', 'action':'manage_changeSettingsForm'},
        ) + Predicate.manage_options[1:]

    security.declareProtected('View management screens',
      'manage_changeSettingsForm')

    manage_changeSettingsForm = PageTemplateFile(
        '../www/xmlnsSettings', globals(),
        __name__='manage_changeSettingsForm')

    manage_changeSettingsForm._owner = None

    security.declareProtected(ManagePortal, 'edit')
    def edit(self, element_ns='', element_name='',
             attr_ns='', attr_name='', value='', REQUEST=None):
        """Change settings germane to this predicate
        """

        for n in (element_ns, element_name, attr_ns, attr_name):
            if not isinstance(n, basestring):
                raise TypeError, 'string required, got %r.' % n
        self._value = value
        self._element_ns = element_ns
        self._element_name = element_name
        self._attr_ns = attr_ns
        self._attr_name = attr_name

        if REQUEST is not None:
            message = 'Predicate Settings Changed.'
            return self.manage_changeSettingsForm(
                manage_tabs_message=message,
                management_view='Settings')

    security.declareProtected(ManagePortal, 'edit')
    def apply(self, obj, **kw):
        """ Return component name if the rule matches, else an empty tuple.
        """
        retval = Predicate.apply(self, obj, **kw)
        if not retval:
            return ()
        body = kw.get('data')
        if not body:
            return ()
        try:
            doc = minidom.parseString(body)
        except:
            return ()
        elm_args = filter(None, (self.getElementNS(), self.getElementName()))
        get_elm = (len(elm_args) == 2 and doc.getElementsByTagNameNS
                   or doc.getElementsByTagName)
        elm = get_elm(*elm_args)
        if not elm:
            return ()
        elm = elm[0]
        attr_args = filter(None, (self.getAttributeNS(), self.getAttributeName()))
        if not attr_args:
            get_attr = lambda elm=elm: elm.firstChild.nodeValue.strip()
        else:
            get_attr = (len(attr_args) == 2 and elm.getAttributeNS or
                        elm.getAttribute)
        got = get_attr(*attr_args)
        expected = self.getValue()
        match = got == expected or (expected is None and got)
        return match and retval or ()

InitializeClass(XMLNS)
registerPredicate('xmlns_attr', 'XMLNS Element/Attribute', XMLNS)
