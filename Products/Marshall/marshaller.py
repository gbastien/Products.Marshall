# Marshall: A framework for pluggable marshalling policies
# Copyright (C) 2004 Enfold Systems, LLC
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
$Id: marshaller.py,v 1.2 2004/07/27 22:24:30 dreamcatcher Exp $
"""

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Marshall import Marshaller
from Products.Marshall.config import TOOL_ID
from Products.Marshall.registry import getComponent
from Products.Marshall.exceptions import MarshallingException
from Acquisition import ImplicitAcquisitionWrapper

def getContext(obj, REQUEST=None):
    context = getattr(obj, 'aq_parent', None)
    if context is not None or REQUEST is None:
        return obj
    # Nasty hack:
    # Try to find context through REQUEST.SESSION
    # which has a pointer back to the app root.
    root = REQUEST.SESSION.aq_chain[-2]
    path = REQUEST.PATH_INFO
    path = '/'.join(path.split('/')[:-1])
    return root.restrictedTraverse(path)

class ControlledMarshaller(Marshaller):

    def delegate(self, method, obj, data=None, **kw):
        context = getContext(obj, kw.get('REQUEST'))
        if context is not obj:
            # If the object is being created by means of a PUT
            # then it has no context, and some of the stuff
            # we are doing here may require a context.
            # Wrapping it in an ImplicitAcquisitionWrapper should
            # be safe as long as nothing tries to persist
            # a reference to the wrapped object.
            obj = ImplicitAcquisitionWrapper(obj, context)
        tool = getToolByName(obj, TOOL_ID, None)
        if tool is None:
            # Couldn't find a context to get
            # hold of the tool. Should probably raise
            # an error or log somewere.
            return
        info = kw.copy()
        info['data'] = data
        info['mode'] = method
        components = tool.getMarshallersFor(obj, **info)
        # We just use the first component, if one is returned.
        if not components:
            raise MarshallingException, ("Couldn't get a marshaller for"
                                         "%r, %r" % (obj, kw))
        marshaller = getComponent(components[0])
        args = (obj,)
        if method == 'demarshall':
            args += (data,)
        method = getattr(marshaller, method)
        return method(*args, **kw)

    def marshall(self, obj, **kw):
        if not 'data' in kw:
            kw['data'] = ''
        return self.delegate('marshall', obj, **kw)

    def demarshall(self, obj, data, **kw):
        return self.delegate('demarshall', obj, data, **kw)
