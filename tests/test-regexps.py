#!/usr/bin/python3
##
## Copyright (C) 2008-2010 Nokia. All rights reserved.
##
## Contact: Marius Vollmer <marius.vollmer@nokia.com>
##
## This library is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public License
## version 2.1 as published by the Free Software Foundation.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public
## License along with this library; if not, write to the Free Software
## Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
## 02110-1301 USA

import sys
import os
# Otherwise env.py won't be found when running tests inside a VPATH build dir
sys.path.insert(0, os.getcwd())

try: import env
except: pass

import unittest
from subprocess import getstatusoutput
from cltool import CLTool
from tempfile import mkdtemp

class Regexps(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
        
    def testStringMimes1(self):
        # only the general
        (status, output) = getstatusoutput("lca-tool --string --printmimes foo")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("general-1") != -1)
        self.assertTrue(output.find("special-1a") == -1)
        self.assertTrue(output.find("special-1b") == -1)

        # general and one special case
        (status, output) = getstatusoutput("lca-tool --string --printmimes foobar")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("special-1a") != -1)
        self.assertTrue(output.find("general-1") != -1)
        self.assertTrue(output.find("special-1b") == -1)
        # verify the order
        self.assertTrue(output.find("special-1a") < output.find("general-1"))

        # general and another special case
        (status, output) = getstatusoutput("lca-tool --string --printmimes foobazxx")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("special-1b") != -1)
        self.assertTrue(output.find("general-1") != -1)
        self.assertTrue(output.find("special-1a") == -1)
        # verify the order
        self.assertTrue(output.find("special-1b") < output.find("general-1"))

    def testStringMimes2(self):
        # only the general
        (status, output) = getstatusoutput("lca-tool --string --printmimes cat")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("general-2") != -1)
        self.assertTrue(output.find("special-2") == -1)
        self.assertTrue(output.find("superspecial-2") == -1)

        # general and one special case
        (status, output) = getstatusoutput("lca-tool --string --printmimes catdog")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("general-2") != -1)
        self.assertTrue(output.find("special-2") != -1)
        self.assertTrue(output.find("superspecial-2") == -1)
        # verify the order
        self.assertTrue(output.find("special-2") < output.find("general-2"))

        # general and both special cases
        (status, output) = getstatusoutput("lca-tool --string --printmimes catdogzebra")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("general-2") != -1)
        self.assertTrue(output.find("special-2") != -1)
        self.assertTrue(output.find("superspecial-2") != -1)
        # verify the order
        self.assertTrue(output.find("special-2") < output.find("general-2"))
        self.assertTrue(output.find("superspecial-2") < output.find("special-2"))

    def testActionsForString(self):
        (status, output) = getstatusoutput("lca-tool --string --print www.foo.com")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("browser") != -1)
        self.assertTrue(output.find("special-browser") == -1)

        (status, output) = getstatusoutput("lca-tool --string --print http://example.com")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("special-browser") != -1)
        self.assertTrue(output.find("browser") != -1)
        self.assertTrue(output.find("special-browser") < output.find("browser"))

    def testDefaultActionForString(self):
        (status, output) = getstatusoutput("lca-tool --string --printdefault www.foo.com")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("browser") != -1)

        (status, output) = getstatusoutput("lca-tool --string --printdefault http://example.com")
        self.assertTrue(status == 0)
        self.assertTrue(output.find("special-browser") != -1)

def runTests():
    suite = unittest.TestLoader().loadTestsFromTestCase(Regexps)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return len(result.errors + result.failures)

if __name__ == "__main__":
    sys.exit(runTests())
