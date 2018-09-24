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
import boto3
import argparse
from Utils.ModuleManager import AIRKModuleManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='AWS Incident Response Kit (AIRK).')
    parser.add_argument('--module', required=False,
                        help='Specify the module (action) you want to run.')
    parser.add_argument('--listmodules', required=False,
                        action='store_true',
                        help='Lists all of the available modules (actions).')
    parser.add_argument('--moduledetails', required=False,
                        action='store_true',
                        help='Lists descriptions of the available modules.')
    parser.add_argument('--values',nargs='+', required=False)

    args = parser.parse_args()

    values = args.values
    
    module_name = args.module
    module_path = os.path.join(os.getcwd(), "modules")
    module_values = args.values

    airk = AIRKModuleManager(module_name, module_path)

    if args.listmodules:
        airk.listModules()
    
    elif args.moduledetails:
        airk.detailedModule()

    elif args.module is not None:
        try:
            module = airk.load_module()
        except (ModuleNotFoundError) as e:
            print(e)
            exit(0)
    
        print(module.Module(module_values).execute())
        
    else:
        print("Nothing to do. Specify a module action.")
        exit(0)