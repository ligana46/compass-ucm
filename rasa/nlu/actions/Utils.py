#coding: utf8

import urllib
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XML, fromstring 

#@TODO: Cambiar nombre de clase por UtlisTracker
class Utils:
    @staticmethod
    def isEntityInTracker(entity, tracker):

        if len(tracker.latest_message['entities']) <= 0:
            return False

        for track in tracker.latest_message['entities']:
            if entity in track["entity"]:
                return True
        return False

    @staticmethod
    def getValueFromEntity(entity, tracker):
        if len(tracker.latest_message['entities']) <= 0:
            return None

        for track in tracker.latest_message['entities']:
            if entity in track["entity"]:
                return track["value"]
        return None
        
    @staticmethod
    def xmlToArray(xmlResponse):
        newLineReg = r'\n |\n'

        xmlResponse = re.sub(newLineReg, '', xmlResponse)

        # tree = ET.ElementTree(ET.fromstring(xmlResponse))
        root = ET.fromstring(xmlResponse)
        myArray=[]

        for child in root:
            tagReg = r'{.+}'
            childTag = re.sub(tagReg, '', child.tag)
            if childTag == 'entry':
                for subchild in child:
                    subchildTag = re.sub(tagReg, '', subchild.tag)
                    infoTags = ['title', 'recordIdentifier']

                    if subchildTag in infoTags:
                        myArray.append([subchildTag, subchild.text])
                    elif subchildTag == 'link':
                        myArray.append([subchildTag, subchild.attrib])

                    elif subchildTag == 'author':
                        for nameTag in subchild:
                            subchildNameTag = re.sub(tagReg, '', nameTag.tag)
                            myArray.append([subchildNameTag, nameTag.text])

        return (str(myArray)) 

    @staticmethod
    def testing():
        title = "chomsky"
        author = "noahm"
        __URLopensearch = "http://www.worldcat.org/webservices/catalog/search/opensearch?"

        type = "kw"

        consulta = {"wskey": "UZHxZYiT35F9kDOsFEm7rR2j9HXASw8kbZjgzxigx25hOr6PHTPQ0wUANf95Hrde5tqhPYzB7D5LuIlg", "count": 10, "start": 0}
        if type == "kw":
            consulta['q'] = 'srw.kw all "' + title + '"'
        elif type == "title":
            consulta['q'] = 'srw.ti all "' + title + '"'
        elif type == "author":
            consulta['q'] = 'srw.au all "' + author + '"'
        elif type == "kw_author":
            consulta['q'] = 'srw.kw all "' + title + '"' + ' and srw.au all "' + author + '"'
        elif type == "title_author":
            consulta['q'] = 'srw.ti all "' + title + '"' + ' and srw.au all "' + author + '"'
        consulta['q'] = consulta['q'] + 'and srw.li all "' + "S9M"
        consulta['q'] = consulta['q'] + '" and srw.la all "spa"'
        URL = __URLopensearch + urllib.parse.urlencode(consulta)

        return URL