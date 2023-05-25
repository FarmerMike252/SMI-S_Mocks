#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ArrayMockLoad.py
#
#  Copyright 2022 FarmerMike <FarmerMike252@Yahoo.com>
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
Sample python script to create a repository with two namespaces (interop
and device).
This installs all of the qualifier declarations and the classes and 
their dependencies defined by the variable leaf_classes.

NOTE: This script only  works with python version >=3.5 and with pywbemtools
1.0.0.

To use this script with pywbemtools mock scripting. load the script and
save it into connections file

pywbemcli -o table --mock-server ArrayMockLoad.py --default-namespace device
pywbemcli > connection save arraymockload

From then on the cached arraymockload will be used unless the file or any
of its dependent files is changed and then it will be recompiled.

This should speed up loading from many seconds to less than a second.
"""

import sys
import os
import xml.etree.ElementTree as ET
import pywbem
import pywbem_mock
import six

# Get the directory containing this file. This is where the dependent
# files and directories should also exist.
SCRIPT_DIR = os.path.dirname(__file__)


def setup(conn, server, verbose):
    # pylint: disable=unused-argument
    """
    Setup for this mock script.
    Parameters:
      conn (FakedWBEMConnection): Connection
      server (PywbemServer): Server
      verbose (bool): Verbose flag
    """

    if sys.version_info >= (3, 5):
        this_file_path = __file__
    else:
        print ('This mock does not support python versions below 3.5')
        
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

    profile_fullname = 'SNIA_Array'

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
    # default class which is device.

    print('Loading classes into the default namespace')

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
    interop_ns='interop'
    numberofnamespaces=2
    if conn.default_namespace=='root/interop':
        interop_ns='root/interop'
        numberofnamespaces=1
    else:
        if conn.default_namespace=='interop':
            interop_ns='interop'
            numberofnamespaces=1
        else:
            numberofnamespaces=2   
    print(numberofnamespaces)
    print('The interop namespace is: ' + interop_ns)

    # Register files that would trigger a rebuild of the mock if any
    # one changes.
    directory_path = os.getcwd()
    regstring = ''
    dep_path = '' 
    print("My current directory is : " + directory_path) 
    # dep_path = os.path.join(os.path.dirname(directory_path), 'ArrayMockLoad.py')
    # To register the path you must modify the following statement to include the complete path to the file
    # dep_path = '.../.../.../ArrayMockLoad.py'
    conn.provider_dependent_registry.add_dependents(directory_path, dep_path)
    print (dep_path)
    # dep_path = os.path.join(os.path.dirname(directory_path), 'SNIA_Array_leaflist.xml')
    # To register the path you must modify the following statement to include the complete path to the file
    # dep_path = '.../.../.../SNIA_Array_leaflist.xml'
    conn.provider_dependent_registry.add_dependents(directory_path, dep_path)
    print (dep_path) 
    if numberofnamespaces==2:
        # dep_path = 'MockSNIA_ArrayMNSInstances.mof'
        # To register the path you must modify the following statement to include the complete path to the file
        # dep_path = '.../.../.../MockSNIA_ArrayMNSInstances.mof'
        conn.provider_dependent_registry.add_dependents(directory_path, dep_path)
        print("The trigger files include : " + dep_path)
    else:
        # dep_path = 'MockSNIA_ArrayInstances.mof'
        # To register the path you must modify the following statement to include the complete path to the file
        # dep_path = '.../.../.../MockSNIA_ArrayInstances.mof'
        conn.provider_dependent_registry.add_dependents(directory_path, dep_path)
        print("The trigger files include : " + dep_path)
    # regstring = pywbem_mock.ProviderDependentRegistry.__repr__(self)
    # print("The trigger files are : " + regstring)

    # Add the interop namespace and load the classes in it as well

    if numberofnamespaces==2:
        print('Loading classes into the ' + interop_ns + ' namespace')
        conn.add_namespace(interop_ns)
        conn.compile_schema_classes(
            unique_classes,
            schema.schema_pragma_file,
            namespace=interop_ns,
            verbose=False)
    else:
        print('Classes Loaded')

    if verbose:
        conn.display_repository()

    """
    Next we compile the instance mofs into our mock repository
    """
    numberofnamespaces=2
    if conn.default_namespace=='interop':
        numberofnamespaces=1
    else:
        if conn.default_namespace=='root/interop':
            numberofnamespaces=1
    if numberofnamespaces==2:
        print('Loading instances into the Mock Repository')
        dev_name=profile_fullname + 'MNS'
        mock_mof = "Mock{}Instances.mof".format(dev_name)
        # REMOVED mock_mof = 'Mock' + fullname + 'Instances.mof'
        mock_mof = os.path.join(SCRIPT_DIR, mock_mof)
        conn.compile_mof_file(mock_mof, verbose=False)
        # print('Loading interop instances into the Mock Repository')
        # int_name=profile_fullname + 'Int'
        # mock_mof = "Mock{}Instances.mof".format(int_name)
        # REMOVED mock_mof = 'Mock' + fullname + 'Instances.mof'
        # mock_mof = os.path.join(SCRIPT_DIR, mock_mof)
        # conn.compile_mof_file(mock_mof,namespace=interop_ns, verbose=False)
        # print('Loading cross namespace associations into the Mock Repository')
        # both_name=profile_fullname + 'Both'
        # mock_mof = "Mock{}Instances.mof".format(both_name)
        # REMOVED mock_mof = 'Mock' + fullname + 'Instances.mof'
    else:
        print('Loading instances into the Mock Repository')
        mock_mof = "Mock{}Instances.mof".format(profile_fullname)
        # REMOVED mock_mof = 'Mock' + fullname + 'Instances.mof'
        mock_mof = os.path.join(SCRIPT_DIR, mock_mof)
        conn.compile_mof_file(mock_mof, verbose=False)
        # conn.compile_mof_file(mock_mof,namespace=interop_ns, verbose=False)
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
