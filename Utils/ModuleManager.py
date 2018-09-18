'''
The MIT License (MIT)

Copyright (c) 2018 Patrick Olsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Author: Patrick Olsen
'''

import os
import io
import sys
import importlib.util
import pkgutil
import configparser

class AIRKModuleManager(object):
    def __init__(self, module_name=None, module_path=None):
        self.module_name = module_name
        self.module_path = module_path

    def gatherallModules(self):
        allModules = []
        for module in os.listdir(self.module_path):
            if module.endswith(".py") and module[:-3] != "__init__":
                module_name = module[:-3]
                allModules.append(module_name)
        return (allModules)

    def listModules(self):
        for module in self.gatherallModules():
            print(module)

    def detailedModule(self):
        #dict = {}

        for module_doc in os.listdir(self.module_path):
            if module_doc.endswith(".module"):
                module_doc_path = os.path.join(self.module_path, module_doc)
                config = configparser.RawConfigParser(allow_no_value=True)
                config.read_file(open(module_doc_path))
                try:
                    module = config.get("Documentation", "Module")
                    author = config.get("Documentation", "Author")
                    version = config.get("Documentation", "Version")
                    date = config.get("Documentation", "Date")
                    description = config.get("Documentation", "Description")
                    
                    print("{0}".format(module.upper()))
                    print("{0:>10}: {1:>15}".format("Module", module))
                    print("{0:>10}: {1:>18}".format("Author", author))
                    print("{0:>11}: {1:>7}".format("Version", version))
                    print("{0:>8}: {1:>17}".format("Date", date))
                    print("{0:>15}: {1}".format("Description", description))

                except configparser.NoOptionError:
                    module_name = module_doc.upper()[:-7]
                    print(module_name + " does not have a proper .module config file.")

    def load_module(self):
        for finder, name, ispkg in pkgutil.iter_modules([self.module_path]):
            found = finder.find_spec(fullname=name)
        
        return(importlib.import_module("." + self.module_name, package='modules'))


