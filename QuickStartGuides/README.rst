Quick Start Guide Scripts - A set pdf files showing scripts for finding selected information from the mocks
===========================================================================================================
A Quick Start Guide shows how to find selected information from a WBEM Server that supports SMI-S 1.8.0.

WHAT IS A QUICK START GUIDE
---------------------------

SMI-S is 2516 pages of reading spread across 8 books, plus it references another 14 or so DMTF profiles which amount to another 660 pages of reading. So, the question is where do you start? We have come up with a series of Quick Start Guides that are designed to help you get started by illustrating how to find useful SMI-S information in mock servers (mock ups of SMI-S server implementations). The Quick Start Guides don't illustrate EVERYTHING in the 3176 pages, but they give you a head start at finding some important items in SMI-S.

We currently have quick start guides for:

* The Interop Namespace - What is it and what does it tell us?

* Performance Information - Where do I find performance information in an SMI-S Server?

* Capacity Information - Where do I find storage capacity information in an SMI-S Server?

* Hardware Information - Where do I find hardware information in an SMI-S Server?

* Product Information - Where do I find product information in an SMI-S 

* Software Information - Where do I find software information in an SMI-S Server?

TOOL USED FOR THE QUICK START GUIDE ILLUSTRATION
------------------------------------------------

The tool used for illustrating how to find information in SMI-S is the pywbemcli (part of pywbemtools). It is a command line interface for accessing any WBEM Server. It uses pywbem, an interface for python program access to any WBEM Server. The pywbemtools (and the pywbemcli) and pywbem are python programs that use a set of python packages. Pywbem and the pywbemtools are actively being maintained and are available on Github.

We will be using the latest version of the pywbemcli in these guides. You can find documentation on the pywbemcli at the following website:
`pywbemcli documentation <https://pywbemtools.readthedocs.io/en/latest/>`_


THE MOCK IMPLEMENTATIONS
------------------------

The mock implementations mock selected autonomous profiles and some of their component profiles in SMI-S 1.8.0.
We currently have mock ups for the following autonomous profiles:

* The SNIA Server Profile

* The DMTF WBEM Server Profile

* The Array Profile

* The NAS Head Profile

And we plan on doing a Fabric (and Switch) mock up.

We chose to do mock ups of the SMI-S 1.8.0 versions of these profiles to illustrate differences between 1.8.0 and 1.6.1. We don't mock everything that is new in 1.8.0, but we do highlight some key changes ... like the DMTF WBEM Server profile, new indications and Advance Metrics (performance) for Arrays.