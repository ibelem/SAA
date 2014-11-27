# -*- coding: utf-8 -*-
import os,sys
from optparse import OptionParser
from script import adb, runtimelib, rundavinci

def main():
    parser = OptionParser()
    parser.add_option("-v", "--version", dest="version",
                  help = "The build number of RuntimeLib.apk")
    parser.add_option("-a", "--arch", dest="arch",
                  help = "Ihe architecture (x86 or arm) of RuntimeLib.apk")
    parser.add_option("-d", "--device", dest="device",
              help = "Ihe device ID of the test device. (optional)")
    (options, args) = parser.parse_args()

    runtimelib.install_runtimelib(options.version, options.arch, options.device)
    ##runtimelib.uninstall_runtimelib(options.device)
    rundavinci.main()

if __name__ == '__main__':
    sys.exit(main())

    #python run.py -v 11.39.251.0 -a x86 -d MedfieldC3567E1E