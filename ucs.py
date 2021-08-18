#!/usr/bin/env python3

from fetcher import FETCHER
from json.decoder import JSONDecodeError
import requests
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


print("-"*120)
heading="Cisco UCS Fetcher".center(125,' ')
print(heading)
print("-"*120)

exitstatement="Press CTRL + C to Exit the Program!!!"
align=exitstatement.center(120)
print(align)

try:
    while True:
        def main():
            IP=input("\nEnter the Setup IP : ")
            def updater():
                    print("\nFetching the Details!!")
                    striip=str(IP)
                    try:
                        Sip=FETCHER(IP)
                    except requests.exceptions.RequestException:
                        print("\n Incorrect IP or Connection Error ")
                        quit()
                    newdata=[]
                    with open("setups1.json","r+") as f:
                        data=json.load(f)
                    for x in data:
                        for i,j in x.items():
                            if i!=striip:
                                newdata.append(x)
                    newdata.append(Sip)
                    with open("setups1.json","w") as f1:
                        json.dump(newdata,f1,indent=4)
                        print("\nFetched Successfully!!")
                    searcher()

            def searcher(ip=IP):
                print(f'\nSearching in {ip} Setup ')
                with open("setups1.json","r") as f:
                    data=json.load(f)
                    preips=[]
                    for x in data:
                        for key,value in x.items():
                            preips.append(key)
                    ipdicts={}
                    counter=1
                    for x in data:
                        for key,value in x.items():
                            ipdicts[counter]=key
                            counter+=1
                            
                def printer(datas):
                    headers=["UCS IP","Server ID","Server Type","Model","Serial","CPU's","Core's","Adapter's","Adapter Model","Adapter Serial","Board Controller","Storage Local Disk Model","Storage Local Disk Serial"]
                    df=pd.DataFrame.from_dict(datas,orient='index')
                    TABULAR_DATA=tabulate(df,tablefmt='fancy_grid')
                    print(TABULAR_DATA)
                        
                def adapter():
                    print("\nYou have Selected Adapter  ")
                    query=input("\nEnter the Adapter to be Searched : ")
                    if query:
                        with open("setups1.json","r") as f:
                            data=json.load(f)
                            adaps=[]
                            for x in data:
                                for i in x.keys():
                                    if i==ip:
                                        for x1k,x1v in x[i].items():
                                            if x1k=="Servers: ":
                                                for v1,v2 in x1v.items():
                                                    adaps.append(v2["Adapter Model"])
                                                for v1,v2 in x1v.items():
                                                    if query:
                                                        if query in adaps and query==v2["Adapter Model"]:
                                                            printer(v2)
                                                        elif query not in adaps:
                                                            print("\nAdapter Model Not found in this Setup")
                                                            print("\n A . Do you want to Fetch from Any of the Pre-Fetched Setup IP's? ")
                                                            print("\n B . Do you want to Fetch from New IP ")
                                                            userchoice=input("\nEnter your Choice (A/B) : ")
                                                            if userchoice.lower()=="a":
                                                                for i,v in ipdicts.items():
                                                                    print("\t\t",i,"-",v)
                                                                choice=int(input("\nEnter the S No of the IP you want to Search : "))
                                                                searcher(ipdicts[choice])
                                                            elif userchoice.lower()=="b":
                                                                main()
                                                            else:
                                                                print("\n Please Enter the Correct Choice ")
                                                            break
                    elif not query:
                        print("\nPlease Enter the Query you want to Search!! ")
                        
                def fi():
                    fichoice=input("\nHow do you want to Search FI via [IP]/[Model] ? ")
                    if fichoice.lower()=="model":
                        attrib="FI Model"
                    elif fichoice.lower()=="ip":
                        attrib="UCS IP"
                        
                    query=input("\nEnter the FI to be Searched : ")
                    if query:
                        with open("setups1.json","r") as f:
                            data=json.load(f)
                            fis=[]
                            for x in data:
                                for i in x.keys():
                                    if i==IP:
                                        for x1k,x1v in x[i].items():
                                            if x1k=="FI:":
                                                for v1,v2 in x1v.items():
                                                    fis.append(v2[attrib])
                                                for v1,v2 in x1v.items():
                                                    if query:
                                                        if query in fis and query==v2[attrib]:
                                                            printer(v2)
                                                        elif query not in fis:
                                                            print("\nFI Model Not found in this Setup")
                                                            print("\n A . Do you want to Fetch from Any of the Pre-Fetched Setup IP's? ")
                                                            print("\n B . Do you want to Fetch from New IP ")
                                                            userchoice=input("\nEnter your Choice (A/B) : ")
                                                            if userchoice.lower()=="a":
                                                                for i,v in ipdicts.items():
                                                                    print("\t\t",i,"-",v)
                                                                choice=int(input("\nEnter the S No of the IP you want to Search : "))
                                                                searcher(ipdicts[choice])
                                                            elif userchoice.lower()=="b":
                                                                main()
                                                            else:
                                                                print("\n Please Enter the Correct Choice ")
                                                        break
                    elif not query:
                        print("\nPlease Enter the Query you want to Search!! ")
                        
                def rack():
                    query=input("\nEnter the Rack Model to be Searched : ")
                    if query:
                        with open("setups1.json","r") as f:
                            data=json.load(f)
                            racks=[]
                            for x in data:
                                for i in x.keys():
                                    if i==IP:
                                        for x1k,x1v in x[i].items():
                                            if x1k=="Servers: ":
                                                for v1,v2 in x1v.items():
                                                    if v2["Server Type"]=="Rack Server":
                                                        racks.append(v2["Model"])
                                                for v1,v2 in x1v.items():
                                                    if query:
                                                        if query in racks and query==v2["Model"]:
                                                            printer(v2)
                                                        elif query not in racks:
                                                            print("\nRack Model Not found in this Setup")
                                                            print("\n A . Do you want to Fetch from Any of the Pre-Fetched Setup IP's? ")
                                                            print("\n B . Do you want to Fetch from New IP ")
                                                            userchoice=input("\nEnter your Choice (A/B) : ")
                                                            if userchoice.lower()=="a":
                                                                for i,v in ipdicts.items():
                                                                    print("\t\t",i,"-",v)
                                                                choice=int(input("\nEnter the S No of the IP you want to Search : "))
                                                                searcher(ipdicts[choice])
                                                            elif userchoice.lower()=="b":
                                                                main()
                                                            else:
                                                                print("\n Please Enter the Correct Choice ")
                                                            break
                    elif not query:
                        print("\nPlease Enter the Query you want to Search!! ")
                    
                def blade():
                    query=input("\nEnter the Blade Model to be Searched : ")
                    if query:
                        with open("setups1.json","r") as f:
                            data=json.load(f)
                            blades=[]
                            for x in data:
                                for i in x.keys():
                                    if i==IP:
                                        for x1k,x1v in x[i].items():
                                            if x1k=="Servers: ":
                                                for v1,v2 in x1v.items():
                                                    if v2["Server Type"]=="Blade Server":
                                                        blades.append(v2["Model"])
                                                for v1,v2 in x1v.items():
                                                    if query:
                                                        if query in blades and query==v2["Model"]:
                                                            printer(v2)
                                                        elif query not in blades:
                                                            print("\nBlade Model Not found in this Setup")
                                                            print("\n A . Do you want to Fetch from Any of the Pre-Fetched Setup IP's? ")
                                                            print("\n B . Do you want to Fetch from New IP ")
                                                            userchoice=input("\nEnter your Choice (A/B) : ")
                                                            if userchoice.lower()=="a":
                                                                for i,v in ipdicts.items():
                                                                    print("\t\t",i,"-",v)
                                                                choice=int(input("\nEnter the S No of the IP you want to Search : "))
                                                                searcher(ipdicts[choice])
                                                            elif userchoice.lower()=="b":
                                                                main()
                                                            else:
                                                                print("\n Please Enter the Correct Choice ")
                                                            break
                    elif not query:
                        print("\nPlease Enter the Query you want to Search!! ")
                        
                def controller():
                    print("\nYou have Selected Controllers  ")
                    query=input("\nEnter the Controller Model to be Searched : ")
                    if query:
                        with open("setups1.json","r") as f:
                            data=json.load(f)
                            controllers=[]
                            for x in data:
                                for i in x.keys():
                                    if i==IP:
                                        for x1k,x1v in x[i].items():
                                            if x1k=="Servers: ":
                                                for v1,v2 in x1v.items():
                                                    controllers.append(v2["Board Controller"])
                                                for v1,v2 in x1v.items():
                                                    if query:
                                                        if query in controllers and query==v2["Board Controller"]:
                                                            printer(v2)
                                                        elif query not in controllers:
                                                            print("\nController Model Not found in this Setup")
                                                            print("\n A . Do you want to Fetch from Any of the Pre-Fetched Setup IP's? ")
                                                            print("\n B . Do you want to Fetch from New IP ")
                                                            userchoice=input("\nEnter your Choice (A/B) : ")
                                                            if userchoice.lower()=="a":
                                                                for i,v in ipdicts.items():
                                                                    print("\t\t",i,"-",v)
                                                                choice=int(input("\nEnter the S No of the IP you want to Search : "))
                                                                searcher(ipdicts[choice])
                                                            elif userchoice.lower()=="b":
                                                                main()
                                                            else:
                                                                print("\n Please Enter the Correct Choice ")
                                                            break
                    elif not query:
                        print("\nPlease Enter the Query you want to Search!! ")
                        
                choice=input("\nEnter the Equipment you want to Search: (Adapter/Rack Server/Blade Server/FI/Controller): ")
                if choice.lower()=="adapter":
                    adapter()
                elif choice.lower()=="fi":
                    fi()
                elif choice.lower()=="rack server":
                    rack()
                elif choice.lower()=="blade server":
                    blade()
                elif choice.lower()=="controller":
                    controller()
                else:
                    print("\nPlease Enter the Correct Choice")

            try:
                with open("setups1.json","r") as f:
                    try:
                        data=json.load(f)
                        ips=[]
                        for x in data:
                            for key,value in x.items():
                                ips.append(key)
                        for x in data:
                            for i in x.keys():                        
                                if i==IP and i in ips:
                                    for x1k,x1v in x[i].items():
                                        if x1k=="Timestamp: ":
                                            print(f'\nSetup Details Already Present Fetched on {x[i][x1k]}')
                                            choice=input("\nDo you Still Want to Update the Details?   (Yes/No)  : ")
                                            if choice.lower()=="yes":
                                                updater()
                                            elif choice.lower()=="no":
                                                print("\nProceeding for Searching the Equipment  ")
                                                searcher()
                                            else:
                                                print("\nPlease Enter the Correct Choice")
                        if IP not in ips:
                            print("\nData Not Available in our Setup File")
                            updater()
                            
                    except JSONDecodeError:
                        print("JSON Parsing Error")
            except FileNotFoundError:
                Sip=FETCHER(IP)
                temp=[Sip]
                with open("setups1.json","a") as f:
                    json.dump(temp,f,indent=4)
        main()

except KeyboardInterrupt:
    bye="Program is Exciting Now !! Bye!!"
    alignbye=bye.center(80)
    print(alignbye)
 



