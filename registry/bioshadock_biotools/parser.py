import logging
from string import Template
import sys
import re
import pprint
import os
from xml.sax.saxutils import escape

class Parser(object):

    def __init__(self, dockerFile):
        self.dockerFile = dockerFile

    def parse(self, templFile, outFile=None):
        dFile = open(self.dockerFile, "r")
        dockf=dFile.read()
        dFile.close()
        lines=dockf.split("\n")
        mdata= dict()
        for line in lines:
            lb=line.split("LABEL")
            if line.strip().startswith("LABEL") and len(lb)>1:
                tupl=lb[1].strip().split("=")
                if len(tupl)>1:
                    mdkey=tupl[0].strip()
                    mdval=tupl[1].strip()

                    if mdval.startswith('"'):
                        mdval = mdval[1:]
                    if mdval.endswith('"'):
                        mdval = mdval[:-1]
                    mdata[mdkey]=escape(mdval)

            lb=line.split("MAINTAINER")
            if line.strip().startswith("MAINTAINER") and len(lb)>1:
                 p = re.compile('[^<>]*<([^<>]*)')
                 m = p.match(line.strip())

                 if m != None and len(m.group())>1:
                     mdval=m.group(1).strip()
                     mdkey="contactEmail"
                     mdata[mdkey]=escape(mdval)

        tFile = open(templFile, "r")
        templ=tFile.read()
        tFile.close()

        desc = Template(templ).safe_substitute(mdata)

        if outFile is None:
            print desc
        else:
            f = open(outFile, 'w')
            f.write(desc)
            f.close()
