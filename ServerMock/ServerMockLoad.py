#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ArrayMockLoad.py
#
#  Copyright 2020 FarmerMike <FarmerMike252@Yahoo.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

"""
Sample python script to create a repository. This installs all of the
qualifier declarations and the classes and their dependencies defined by
the variable leaf_classes
"""
""" First we import modules we will need """
import os
import xml.etree.ElementTree as ET
import xml.dom
import xml.dom.minidom
import xml.dom.pulldom
import xml.sax
import xml.parsers.expat
from xml.dom.minidom import parse, parseString, getDOMImplementation
from xml.etree.ElementTree import Element, SubElement, tostring, XML
import collections
import pywbem
import pywbem_mock

global CONN

# version definition of the DMTF schema.  This is the version currently
# installed by default in pywbem github.  Cloning pywbem to get the
# development components means this schema is already installed in the
# directory
#   tests/schema
schema_version = (2, 51, 0)
# print(schema_version)

# definition of the directory where the schema is installed in the
# github clone of pywbem
# You can chose any directory you want to.  If you are using pip to
# install pywbem, chose a directory off the root of your virtual environment.
# I think we will even create the directory if it does not exist.
# TESTSUITE_SCHEMA_DIR = os.path.join('tests', 'schema')
# print(TESTSUITE_SCHEMA_DIR)
TESTSUITE_SCHEMA_DIR = os.path.join('schema')
# print(TESTSUITE_SCHEMA_DIR)

# CONN = pywbem_mock.FakedWBEMConnection(default_namespace='root/cimv2')
# print(CONN)

verbose = False
if verbose is True:
    CONN.display_repository()

fullname = 'SNIA_Server'
# fullname = 'DMTF_WBEM Server'
# fullname = 'SNIA_Array'
# fullname = 'SNIA_NAS Head'

# Open input file
unique_class_list =[]
leaflist = fullname + "_leaflist.xml"
leafentries = ET.parse(leaflist)  # Read the list of leaf classes into dom
llroot = leafentries.getroot()
for leaf in llroot.findall('ENTRY'):
    unique_class_list.append(leaf.attrib['NAME'])

"""
print('Finding CIM_Container in unique_leaf_classes')
print(unique_leaf_classes)
concount = 0
for container in unique_leaf_classes:
    if container == 'CIM_Container':
        concount = concount + 1
        print('CIM_Container found in all_leaf_classes')
if concount == 0:
    print('CIM_Container NOT FOUND in all_leaf_classes')
"""

# Compile dmtf schema version 2.51.0, the qualifier declarations and
# the classes in 'classes' and all dependent classes and keep the
# schema in directory my_schema_dir. This installs the schema into the
# default class which is root/cimv2.

print('Loading classes into the Mock Repository')
# CONN.compile_dmtf_schema(schema_version,
#                         TESTSUITE_SCHEMA_DIR,
#                         unique_class_list,
#                         use_experimental=True,
#                         verbose=False)
if hasattr(CONN, 'compile_schema_classes'):
    schema = pywbem_mock.DMTFCIMSchema(schema_version, TESTSUITE_SCHEMA_DIR,
                           use_experimental=True,
                           verbose=False)
    CONN.compile_schema_classes(
        unique_class_list,
        schema.schema_pragma_file,
        namespace='root/cimv2',
        verbose=False)
else:
    CONN.compile_dmtf_schema(schema_version,
        TESTSUITE_SCHEMA_DIR,
        unique_class_list,
        namespace='root/cimv2',
        verbose=False)
"""
print('Finding CIM_Container class definition in the Repository:')
try:
    clssobj = CONN.GetClass('CIM_Container', namespace='root/cimv2', LocalOnly=False, verbose=False)
    print(clssobj.tomof())
except pywbem.Error as exc:
    print('CIM_Container class NOT FOUND in the Repository')
"""

if verbose is True:
    CONN.display_repository() 

"""
Next we compile the instance mofs into our mock repository
"""
print('Loading instances into the Mock Repository')
mock_mof = 'Mock' + fullname + 'Instances.mof'
CONN.compile_mof_file(mock_mof, verbose=False)
print('DONE Loading instances into the Mock Repository')

# print('Listing Class definitions and their instances')
if verbose is True:
    # CONN.display_repository()
    for clss in unique_leaf_classes:
        if clss == 'CIM_Container':
            try:
                clssobj = CONN.GetClass(clss, namespace='root/cimv2', LocalOnly=False)
            except pywbem.Error as exc:
                print('Operation failed: %s' % exc)
            print(clssobj.tomof())
            print('Trying to collect on CIM_Container instances')
        try:
            insts = CONN.EnumerateInstances(clss, namespace='root/cimv2', LocalOnly=False)
        except pywbem.Error as exc:
            # continue
            print('Operation failed: %s' % exc)
        instcount = 0
        for inst in insts:
            instcount = instcount + 1
            if instcount == 1:
                if clss == 'CIM_Container':
                    print('Trying to GetClass on CIM_Container')
                try:
                    clssobj = CONN.GetClass(clss, namespace='root/cimv2', LocalOnly=False)
                except pywbem.Error as exc:
                    print('Operation failed: %s' % exc)
                print(clssobj.tomof())
            print(inst.tomof())

""" Next we will look for a registered profile in the mock repository
that matches what was requested
print('Listing instances of CIM_ComputerSystem')
try:
    compsyss = CONN.EnumerateInstances('CIM_ComputerSystem', namespace='root/cimv2', LocalOnly=False)
except pywbem.Error as exc:
    print('Operation failed: %s' % exc)

print('Retrieved %s instances' % (len(compsyss)))
for inst in compsyss:
    print('path=%s' % inst.path)
    print(inst.tomof())

print('Listing instances of CIM_Namespace')
try:
    namesps = CONN.EnumerateInstances('CIM_Namespace', namespace='root/cimv2', LocalOnly=False)
except pywbem.Error as exc:
    print('Operation failed: %s' % exc)

print('Retrieved %s instances' % (len(namesps)))
for inst in namesps:
    print('path=%s' % inst.path)
    print(inst.tomof())
"""
