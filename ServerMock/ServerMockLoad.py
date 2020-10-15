#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ServerMockLoad.py
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

NOTE: This script only  works with python version >=3.5 and with pywbemtools
0.8.0.

To use this script with pywbemtools mock scripting. load the script and
save it into connections file

pywbemcli -m ServrMockLoad.py
pywbemcli > connection save ServerMock

From then on the cached ServerMock will be used unless the file or any
of its dependent files is changed and then it will be recompiled.

This should speed up loading from many seconds to less than a second.
"""
""" First we import modules we will need """
import os
import xml.etree.ElementTree as ET
import pywbem
import pywbem_mock

# Get the directory containing this file. This is where the dependent
# files and directories should also exist.
SCRIPT_DIR = os.path.dirname(__file__)


def setup(conn, server, verbose):
    # version definition of the DMTF schema.  This is the version currently
    # installed by default in pywbem github.  Cloning pywbem to get the
    # development components means this schema is already installed in the
    # directory
    #   tests/schema
    schema_version = (2, 51, 0)

    # Schema directory must be contained in the same directory as this file
    # This is the directory in which the schema will be installed.
    testsuite_schema_dir = os.path.join(SCRIPT_DIR, 'schema')

    if verbose is True:
        conn.display_repository()

    profile_fullname = 'SNIA_Server'

    # Create the list of leaf classes from the leaflist.xml file which must
    # be contained in the current working directory

    profile_leaflist = "{}_leaflist.xml".format(profile_fullname)
    # REMOVE profile_leaflist = profile_fullname + "_leaflist.xml"
    profile_leaflist = os.path.join(SCRIPT_DIR, profile_leaflist)

    # Read the list of leaf classes into a list.
    leafentries = ET.parse(profile_leaflist)
    llroot = leafentries.getroot()
    unique_classes = [leaf.attrib['NAME'] for leaf in llroot.findall('ENTRY')]

    # Replaced with list comprehenshion.
    #for leaf in llroot.findall('ENTRY'):
    #    unique_class_list.append(leaf.attrib['NAME'])

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

    schema = pywbem_mock.DMTFCIMSchema(schema_version,
                                       testsuite_schema_dir,
                                       use_experimental=True,
                                       verbose=False)
    conn.compile_schema_classes(
        unique_classes,
        schema.schema_pragma_file,
        namespace=conn.default_namespace,
        verbose=False)
    """
    print('Finding CIM_Container class definition in the Repository:')
    try:
        clssobj = conn.GetClass('CIM_Container', namespace='root/cimv2',
                                LocalOnly=False, verbose=False)
        print(clssobj.tomof())
    except pywbem.Error as exc:
        print('CIM_Container class NOT FOUND in the Repository')
    """

    if verbose:
        conn.display_repository()

    """
    Next we compile the instance mofs into our mock repository
    """
    print('Loading instances into the Mock Repository')
    mock_mof = "Mock{}Instances.mof".format(profile_fullname)
    # REMOVED mock_mof = 'Mock' + fullname + 'Instances.mof'
    mock_mof = os.path.join(SCRIPT_DIR, mock_mof)
    conn.compile_mof_file(mock_mof, verbose=False)
    print('DONE Loading instances into the Mock Repository')

    # print('Listing Class definitions and their instances')
    if verbose is True:
        # conn.display_repository()
        for clss in unique_classes:
            if clss == 'CIM_Container':
                try:
                    clssobj = conn.GetClass(clss, namespace='root/cimv2',
                                            LocalOnly=False)
                except pywbem.Error as exc:
                    print('Operation failed: %s' % exc)
                print(clssobj.tomof())
                print('Trying to collect on CIM_Container instances')
            try:
                insts = conn.EnumerateInstances(clss, namespace='root/cimv2',
                                                LocalOnly=False)
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
                        clssobj = conn.GetClass(clss, namespace='root/cimv2',
                                                LocalOnly=False)
                    except pywbem.Error as exc:
                        print('Operation failed: %s' % exc)
                    print(clssobj.tomof())
                print(inst.tomof())

    """
    # Next we will look for a registered profile in the mock repository
    # that matches what was requested
    print('Listing instances of CIM_ComputerSystem')
    try:
        compsyss = conn.EnumerateInstances('CIM_ComputerSystem',
                                           namespace='root/cimv2',
                                           LocalOnly=False)
    except pywbem.Error as exc:
        print('Operation failed: %s' % exc)

    print('Retrieved %s instances' % (len(compsyss)))
    for inst in compsyss:
        print('path=%s' % inst.path)
        print(inst.tomof())

    print('Listing instances of CIM_Namespace')
    try:
        namesps = conn.EnumerateInstances('CIM_Namespace',
                                          namespace='root/cimv2',
                                          LocalOnly=False)
    except pywbem.Error as exc:
        print('Operation failed: %s' % exc)

    print('Retrieved %s instances' % (len(namesps)))
    for inst in namesps:
        print('path=%s' % inst.path)
        print(inst.tomof())
    """
