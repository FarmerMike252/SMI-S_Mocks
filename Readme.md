SMI-S_Mocks - A set of mock WBEM servers that support SMI-S 1.8.0 storage management servers
============================================================================================
This is storage for a set of SMI-S mocks. It is used for publishing the mocks. It uses
python, pywbem and pywbemtools. The update to 2.0 will add multiple namespace mocks, the 
first of which is for the Array mock.

Overview
--------

Pywbem (and pywbemtools) provide a mechanism for mocking a WBEM server locally on your own
system. The mocks use this mechanism. They are developed using Python 3.8, Pywbem 1.1.1 and
pywbemtools 0.8.0. For multiple namespace mocks it will be necessary to upgrade pywbem to 1.6.1 
and upgrade pywbemtools to 1.2.0.

The Mocks
---------

Each mock has it's own directory. Each directory contains three files that make up the mock:

A py file (Python program), an xml file and an instance mof file.

* The xml file is named [Org]_[Profile Name]_leaflist.xml. Examples are SNIA_Array_leaflist.xml and SNIA_NAS Head_leaflist.xml.
  The xml leaflist file holds all the leaf classes for a complete implementation of an autonomous profile. That is, all 
  classes in the autonomous profile and its component profiles. It is based on all classes identified by SMI-S 1.8.0.

* The mof file is named Mock[Org]_[Profile Name]Instances.mof. Examples are MockSNIA_ArrayInstances.mof and MockSNIA_NAS     HeadInstances.mof.
  The mof files contain instance mofs for all instances that are to be mocked. There are two instance mof files. One is for
  the single namespace mock and the other is for the multiple namespace mock. The mock load program uses the single namespace
  mock if the default namespace is set to 'interop'. Otherwise it uses the multiple namespace mock.

* The python program is named [Profile Name]MockLoad.py. Examples are ArrayMockLoad.py and NASHeadMockLoad.py.
  The python program (py file) is to be used to establish (and name) a mock. The program reads in the class lists 
  for both the WBEM Server Profile and the SNIA Server Profile and combine those lists with the class list for the 
  device profile (e.g., Array or NAS Head). It uses the combined list to load class definitions in the mock. It then 
  reads the mof file to load instances into the mock.

Quick Start Guides
------------------

The Quick Start Guides directory contains pdf files. The pdf files are Quick Start Guides for finding information in the mocks. 
The guides include text describing what we are looking for, the pywbemcli commands to get that information and the 
output produced from the mocks.
Currently guides are only provided for the Array mocks (both the single and multiple namespace mocks). Future releases will
add guides (scripts) for other mocks. For device mocks only multiple namespace mock guides will be provided.


<a href="https://trackgit.com">
<img src="https://us-central1-trackgit-analytics.cloudfunctions.net/token/ping/kpvda3s4nywsirokjdkp" alt="trackgit-views" />
</a>
