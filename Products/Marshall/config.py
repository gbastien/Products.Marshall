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
$Id: config.py,v 1.2 2004/07/27 22:24:30 dreamcatcher Exp $
"""
import os
from Globals import package_home
PACKAGE_HOME = package_home(globals())

TOOL_ID = 'marshaller_registry'
AT_NS = 'http://plone.org/ns/archetypes/'
CMF_NS = 'http://cmf.zope.org/namespaces/default/'
ATXML_SCHEMA = os.path.join(PACKAGE_HOME, 'validation', 'atxml')
