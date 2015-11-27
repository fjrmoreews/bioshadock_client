import os
import requests
import logging
import sys
import json
from lxml import etree as ElementTree
from collections import defaultdict

requests.packages.urllib3.disable_warnings()

class BioTools(object):

    def __init__(self, registerUrl="https://bio.tools/api"):
        self.registerUrl = registerUrl
        pass

    def get_resource(self, options):
        '''
        Gets a resource object with resource name

        :params options: act = action (delete, get, register, update)
                         resname = resource name (optional)
                         resFile = XML resource file path (if resname not provided)
        :type options: object
        :return: dict
        '''
        ressource={}
        if (options.act=="delete" or options.act=="get" )and options.resname!=None:
            ressource['name']=options.resname
        else:
            descFile = open(options.resFile, "r")
            desc=descFile.read()
            descFile.close()

            if desc==None or len(desc)<1:
                raise Exception("descriptor file %s not usable "% ( options.resFile) );
            else:
                ressource= dict()
                if options.xmlTransportFormat==True:
                    parser = ElementTree.XMLParser(recover=True)
                    tree = ElementTree.fromstring(desc, parser)
                    dtree=self.treeToDict(tree)
                    ressource['name']=dtree['resources'][ 'resource']['name']
                else:
                    ddict=json.loads(desc)
                    ressource['name']=ddict['name']

                if 'name' in list(ressource.keys()):
                    if options.verbose:
                        logging.info("Going to manage ressource with name ***%s***" %(ressource['name']))
                else:
                    raise Exception("no attribute name in json object (file %s )"% ( options.resFile) );
        return ressource

    def treeToDict(self, t):
        d = {t.tag: {} if t.attrib else None}
        childr = list(t)
        if childr:
            dd = defaultdict(list)
            for dc in map(self.treeToDict, childr):
                for k, v in dc.iteritems():
                    dd[k].append(v)
            d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
        if t.text:
            text = t.text.strip()
            if childr or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d


    def execLoginCmd(self, username, password):
        r = requests.post(self.registerUrl+"/auth/login", verify=False, data={'username': username, 'password': password})
        status = r.status_code
        if status != 200:
            raise Exception('Login failure: '+str(status))
        return r.json()

    def execRegisterOrUpdateCmd(self, token, resFile, transportFormat):
        headers = {'Authorization': 'Token '+str(token), 'Accept': transportFormat}
        regFile = {'file': (resFile, open(resFile, 'rb'), 'application/xml', {'Expires': '0'})}
        r = requests.post(self.registerUrl+"/tool", headers=headers, verify=False,
                          files=regFile)
        status = r.status_code
        if status != 200:
            raise Exception('RegisterOrUpdate failure: '+str(status))
        res = {}
        try:
            res = r.json()
        except Exception as e:
            logging.debug(str(e))
        return res

    def execDeleteCmd(self, token, affiliation, name):
        headers = {'Authorization': 'Token '+str(token)}
        r = requests.delete(self.registerUrl+"/tool"+"/"+affiliation+"/"+name,
                            verify=False, headers=headers)
        status = r.status_code
        if status != 200:
            raise Exception('RegisterOrUpdate failure: '+str(status))
        res = {}
        try:
            res = r.json()
        except Exception as e:
            logging.debug(str(e))
        return res

    def execGetCmd(self, affiliation, name,transportFormat):
        headers = {'Accept': transportFormat}
        r = requests.get(self.registerUrl+"/tool"+"/"+affiliation+"/"+name,
                         verify=False, headers=headers)
        status = r.status_code
        if status != 200:
            raise Exception('RegisterOrUpdate failure: '+str(status))
        return r.json()
