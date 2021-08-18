from json.decoder import JSONDecodeError
import requests
requests.urllib3.disable_warnings()
from xml.etree import cElementTree as ET
from xml.dom import minidom
import pandas as pd
from tabulate import tabulate
import json
import getpass
import stdiomask
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import Requester
import datetime
import dateutil.parser
import textwrap
from pprint import pprint

def FETCHER(IPaddr):
    """  
    Usually when Dealing with Request's , Intrepreter Might Raise warning about Insecure Connection Request, In order to Resolve thiis warning and Make most user friendly script we must ignore this Warning using the Following snippet ! 
    """
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # global IP
    IP_Addr=IPaddr   #input("\nEnter the Setup IP : ")
    IP=IP_Addr.strip().split('/')[-1] 
    USERNAME=input("\nEnter the Username :") #"ucspe"#input("Enter the Username :") 
    PASSWORD=getpass.getpass(prompt='\nEnter your Password : ', stream=None) #"ucspe"#getpass.getpass(prompt='Enter your Password : ', stream=None)
    """
    XML_ALTERNATOR Function takes XML_CODE as an Argument and Makes Request to the Specified IP Using POST Requests Library and Return XML_Response Code
    """
    def XML_ALTERNATOR(Response):
        Login_Response = Response
        XML_Element_Tree = ET.fromstring(Login_Response)
        COOKIE=XML_Element_Tree.attrib['outCookie']
        configResolveClass_Server_Query ='<configResolveClasses cookie="1617209698/8bf08bee-8e3c-463a-bb7a-b51c59545cf0" inHierarchical="true"> <inIds> <Id value="computeItem"/> <Id value="computeRackUnit" /> </inIds> </configResolveClasses>'
        DOM = minidom.parseString(configResolveClass_Server_Query)
        ELEMENT = DOM.getElementsByTagName('configResolveClasses')
        ELEMENT[0].setAttribute('cookie', COOKIE)
        CONFIG_QUERY_WITH_NEW_COOKIE=DOM.toprettyxml(indent='    ')
        return CONFIG_QUERY_WITH_NEW_COOKIE
    """
    FI_FETCHER Function takes Response Returned from XML_ALTERNATOR Function Which Mainly Replaces the New Response Cookie Returned from UCS Login Request
    """
    def FI_FETCHER(Response):
        Login_Response = Response
        XML_Element_Tree = ET.fromstring(Login_Response)
        COOKIE=XML_Element_Tree.attrib['outCookie']
        configResolveClass_FI_Query='<configResolveClasses cookie="1619182011/9a5812e8-3bf5-4565-b027-b450668a12e6" inHierarchical="true"> <inIds> <Id value="computeItem"/> <Id value="networkElement" /> </inIds> </configResolveClasses>'
        DOM1 = minidom.parseString(configResolveClass_FI_Query)
        ELEMENT1 = DOM1.getElementsByTagName('configResolveClasses')
        ELEMENT1[0].setAttribute('cookie', COOKIE)
        FI_CONFIG_QUERY_WITH_NEW_COOKIE=DOM1.toprettyxml(indent='    ')
        return FI_CONFIG_QUERY_WITH_NEW_COOKIE
    """Login Request XML Code"""
    Login_Query=f'<aaaLogin inName= {USERNAME} inPassword= {PASSWORD} ></aaaLogin>'
    Login_Response = Requester.REQUESTER(Login_Query,IP)
    Config_Response=Requester.REQUESTER(XML_ALTERNATOR(Login_Response),IP)
    Fi_Response=Requester.REQUESTER(FI_FETCHER(Login_Response),IP)
    Server_ElementTree=ET.ElementTree(ET.fromstring(Config_Response))
    FI_ElementTree=ET.ElementTree(ET.fromstring(Fi_Response))
    SERVERS={}
    FI={}
    DUP=[]
    FI_counter=0
    counter=0
    """
    This Section of Code Extracts the Specific Fabric Interconnect Attributes from the ConfigResolveClasses XML Response and Save's in the Nested Dictionary Format
    """
    for node in FI_ElementTree.findall('.//outConfigs/'):
        FI_counter += 1
        if node.tag=="networkElement":
            FI[FI_counter]={
                                "UCS IP":IP,
                                "FI Name":node.attrib['dn'],
                                "FI Model":node.attrib['model'],
                                "FI Serial":node.attrib['serial'],
                                "IP Address":node.attrib['oobIfIp'],
                                "Subnet Mask":node.attrib['oobIfMask'],
                                "Default Gateway":node.attrib['oobIfGw']
                         }
        else:
            break
    """
    This Section of Code Extracts the Specific Server Attributes from the ConfigResolveClasses XML Response and Save's in the Nested Dictionary Format
    """        
    for node in Server_ElementTree.findall('.//outConfigs/*'):
        counter +=1
        for computeboard in node.findall('.//computeBoard/storageController/storageLocalDisk'):
            for controller in node.findall('.//computeBoardController'):
                for adapter in node.findall('.//adaptorUnit'):
                    if node.tag == "computeBlade" and node.attrib['serverId'] not in DUP:
                        SERVERS[counter] = {                "UCS IP":IP,
                                                            "Server ID" : node.attrib['serverId'],
                                                            "Server Type": "Blade Server",
                                                            "Model" : node.attrib['model'],
                                                            "Serial" : node.attrib['serial'],
                                                            "CPU's" : node.attrib['numOfCpus'],
                                                            "Core's" : node.attrib['numOfCores'],
                                                            "Adapter's" : node.attrib['numOfAdaptors'],
                                                            "Adapter Model": adapter.attrib['model'],
                                                            "Adapter Serial": adapter.attrib['serial'],
                                                            "Board Controller":controller.attrib['model'],
                                                            "Storage Local Disk Model":computeboard.attrib['model'],
                                                            "Storage Local Disk Serial":computeboard.attrib['serial']
                                            }
                        DUP.append(node.attrib['serverId'])    
                    elif node.tag == "computeRackUnit" and node.attrib['serverId'] not in DUP:
                        SERVERS[counter] = {                "UCS IP":IP,
                                                            "Server ID" : node.attrib['serverId'],
                                                            "Server Type": "Rack Server",
                                                            "Model" : node.attrib['model'],
                                                            "Serial" : node.attrib['serial'],
                                                            "CPU's" : node.attrib['numOfCpus'],
                                                            "Core's" : node.attrib['numOfCores'],
                                                            "Adapter's" : node.attrib['numOfAdaptors'],
                                                            "Adapter Model": adapter.attrib['model'],
                                                            "Adapter Serial": adapter.attrib['serial'],
                                                            "Board Controller":controller.attrib['model'],
                                                            "Storage Local Disk Model":computeboard.attrib['model'],
                                                            "Storage Local Disk Serial":computeboard.attrib['serial']
                                            }
                        DUP.append(node.attrib['serverId'])
    Sip=str(IP_Addr)
    Sip={Sip: {"Servers: ":SERVERS,"FI:":FI,"Timestamp: ":str(datetime.datetime.now())}}

    return Sip

