#!/usr/bin/env python2.7

#Name    : Server_anavale.py (Programming assignment 1)
#Purpose : Web Server 
#Date    : 09/10/2015
#Version : 7.9

import socket
import os
import re
import time
import select
import queue

size=1024

class CombinedData:       #creating a object to store a socket with the requested data
    def __init__(self, socket, data):
         self.socket = socket
         self.data = data

class CombinedError:      #creating a object to store a socket with error data that should be displayed on Web browser 
    def __init__(self, socket, code):
         self.socket = socket
         self.code = code


def fetch_conf_data():    # Fetching the data from the ws.conf file i.e. port no., root dir, default html file, supported types
    conf=open("ws.conf")
    confData=conf.read()
    conf.close()
    Port=re.search(r'(?<=Listen )?\d+', confData)
    if hasattr(Port, 'group'):
        ServerPort=Port.group(0)
    else:
        ServerPort="Server Port is not found in ws.conf file"
    
    Root=re.search(r'(?<=DocumentRoot ").+(?=")', confData)
    if hasattr(Root, 'group'):
        RootDir=Root.group(0)
    else:
        RootDir="Root Directory is not found in ws.conf file"
    
    Default=re.search(r'(?<=DirectoryIndex )\w+.html', confData)
    if hasattr(Default, 'group'):
        DefaultHTML=Default.group(0)
    else:
        DefaultHTML="Default HTML file is not found in ws.conf file"
    
    readline=open("ws.conf",'r')
    getdatanow=0
    DataTypes=[]
    DataTypeDes=[]
    for line in readline:
        finddata=re.search(r'#Content-Type which the server handles', line)
        if (getdatanow==1):
            findtype=re.search('\.\w+', line)
            findtypeDes=re.search('\w+/\w+', line)
            if hasattr(findtype, 'group'):
                type=findtype.group(0)
                DataTypes.append(type)
            else:
                print("types not found")
            if hasattr(findtypeDes, 'group'):
                typeDes=findtypeDes.group(0)
                DataTypeDes.append(typeDes)
            else:
                print("type description not found")
        if hasattr(finddata,'group'):
            getdatanow=1        
    readline.close()
    print("Server Port                       : "+ServerPort)
    print("Root Directory is                 : "+RootDir)
    print("Default HTML File                 : "+DefaultHTML)
    print("Supported Data Types:             : "+str(DataTypes))
    print("Supported Data Types Description  : "+str(DataTypeDes))
    return(ServerPort, RootDir, DefaultHTML, DataTypes, DataTypeDes)
    
def Create_Server(ServerPort): #starting the Main server on the given port number in ws.conf file
    ServerPort=int(ServerPort)
    host=''
    backlog=5
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.bind((host,ServerPort))
    Server.listen(backlog)
    print("Server is created and running on Port number :" +str(ServerPort))
    return Server

def parse_Request(data,DefaultHTML):    #parsing the request for VERSION, METHOD, URL errors
    data=str(data)
    datalist=data.split()
    if(datalist[0]=="GET" or datalist[0]=="POST" or datalist[0]=="HEAD"):
        RequestMethod=datalist[0]
    else:
        RequestMethod="400 Bad Request : Invalid Method: "+datalist[0]
        
    if(datalist[2]=="HTTP/1.1"):
        RequestVer=datalist[2]
    else:
        RequestVer="400 Bad Request : Invalid HTTP-Version: "+datalist[2]
  
  
    findspace=re.search(r'\s',datalist[1])
    findbackslash=re.search(r'\%',datalist[1])
    
    if hasattr(findspace,'group') or hasattr(findbackslash,'group'):
        URL="400 Bad Request : Invalid URI: "+datalist[1]
    else:
        if (datalist[1]=="/"):
            URL="/"+DefaultHTML
        else:
            URL=datalist[1]

    return RequestMethod, RequestVer, URL        

def Check_For_Error(Request):       # checking the request for METHOD, URL, VERSION errors
    Method, Version, URL=parse_Request(Request, DefaultHTML)
    
    if(Method[0:4] == "400"):
        return(Method)
    elif (Version[0:4] == "400"):
        return(Version)
    elif (URL[0:4] == "400"):
        return(URL)
    else:
        return "200"     

def Fetch_File_Error_Check(Reqdata, RootDir, DataTypes, DataTypeDes): # checking error for file not found and not implemented file type
    Method, Version, Path=parse_Request(Reqdata, DefaultHTML)
    Pathparts=Path.split('.')
    print(Pathparts)
    pathext=Pathparts[1]
    pathext="."+pathext
    print("Extention of the file is "+pathext)
    if pathext in DataTypes:
        print("file format is supported")
    else:
        print("not supported file format")
        errorcode="501 Not Implemented :"+Path
        return errorcode
    
    FullPath=RootDir+Path
    FullPath=FullPath.replace("//","/")
    print(FullPath)
    if(FullPath[0:1]=="/"):
        FullPath=FullPath[1:]
        print(FullPath)
    if(os.path.isfile(FullPath)):
        print("requested file found on a server")
    else:
        print("Requested file not found on the server")
        errorcode="404 Not Found :"+Path
        return(errorcode)    
    return("NO ERROR")

def Create_Header_Enc(ContLen,ContType):    # creating a header for successful reply to browser
    head = "HTTP/1.1 200 OK\n"
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S")
    head += 'Date: ' + current_date +'\n'
    head += "Content-Type:"+str(ContType)+"\n"
    head += "Content-Length:"+str(ContLen)+"\n"
    head += 'Connection: close\n\n' 
    head = head.encode()
    return head

def Get_Data_File(FullPath, pathext, DataTypes, DataTypeDes):   #fetch the requested file data from root dir folder 
    TypeInd=DataTypes.index(pathext)
    FileType=DataTypeDes[TypeInd]
    FileTypeList=FileType.split("/")
    print("file type to send is "+FileTypeList[0])
    if(FileTypeList[0]=="image"):
        ImgFile=open(FullPath,"rb")
        ImgData=ImgFile.read()
        ImgFile.close()
        return ImgData
    else:
        print("full path is when to open a text is " + FullPath)
        OtherFile=open(FullPath)
        OtherData=OtherFile.read()
        OtherFile.close()
        OtherData=OtherData.encode()
        print("encoded data:"+str(OtherData))
        return OtherData
    
def Process_Data(ReqData, DataTypes, DataTypesDes, RootDir, DefaultHTML): #process the Client request and find out the content length/type for requested file 
    Method, Version, Path=parse_Request(Reqdata, DefaultHTML)
    FullPath=RootDir+Path
    FullPath=FullPath.replace("//","/")
    print(FullPath)
    if(FullPath[0:1]=="/"):
        FullPath=FullPath[1:]
        print(FullPath)
    ContLen=os.path.getsize(FullPath)
    print("content-Lenth is "+str(ContLen))
    
    Pathparts=Path.split('.')
    pathext=Pathparts[1]
    pathext="."+pathext
    TypeIndex=DataTypes.index(pathext)
    ContType=DataTypesDes[TypeIndex]
    print("Content-Type is "+ContType)
    
    Header=Create_Header_Enc(ContLen,ContType)
    Data= Get_Data_File(FullPath, pathext, DataTypes, DataTypesDes)
    SendData=Header+Data
    return SendData

def Make_Error_Header(msg):     #create a header for a error response 
    list=msg.split()
    response=list[0]+" "+list[1]+" "+list[2]
    head = "HTTP/1.1 "+response+"\n"
    current_date = time.strftime("%a, %d %b %Y %H:%M:%S")
    head += 'Date: ' + current_date +'\n'
    head += 'Connection: close\n\n' 
    head = head.encode()
    return head

ServerPort, RootDir, DefaultHTML, DataTypes, DataTypeDes=fetch_conf_data()
ServerSoc = Create_Server(ServerPort)

Inputs=[ServerSoc]  #list of Server sockets which are still waiting for Client request
Outputs=[]          #list of Server sockets which required to send data
Exceptions=[]       #List of server sockets for which error ocured and need to display error code
UnprocessedData=[]  #List of objects named CombinedData 
UnprocessedError=[] #List of objects named CombinedData 
ProcessedData=[]    

while Inputs:
    Input, Output, Exception = select.select(Inputs, Outputs, Exceptions)
    for socket in Inputs:
        if socket is ServerSoc:         # if the socket is Server socket wait for client connection
            ServerSocCLI, address = socket.accept()
            Inputs.append(ServerSocCLI)
        elif socket is ServerSocCLI:    # if the socket is client socket reciev the data and send the socket to Outputs queue
            RequestData=ServerSocCLI.recv(size)
            if RequestData:
                RequestData=RequestData.decode()
                print(RequestData)
                RequestTotal=CombinedData(socket, RequestData)
                UnprocessedData.append(RequestTotal)
                Outputs.append(socket)
                Inputs.remove(socket)                
            else:
                #print("ERROR: No request found for a client socket")
                Inputs.remove(socket)
                socket.close()    
        else:
            #print("Socket Type is unrecognizable")
            if socket in Outputs:
                Outputs.remove(socket)
            Inputs.remove(socket)
            socket.close()

    for socket in Outputs:      # if the socket comes in thi queue means it has doeb request to the server
        j=len(UnprocessedData)
        print(str(j))
        i=0
        index=-1
        while(i<j):         # check for the requested data for the socket 
            object=UnprocessedData[i]
            if(object.socket==socket):
                index=i
            i=i+1
        if(index!=-1):
            Reqdata=UnprocessedData[index].data
            code=Check_For_Error(Reqdata)
            if(code=="200"):
                print("Message id good to go for processing")
                code2=Fetch_File_Error_Check(Reqdata, RootDir, DataTypes, RootDir)
                if(code2=="NO ERROR"):
                    print("File detected and no error found so good to go for processsing")
                    dataSend=Process_Data(Reqdata, DataTypes, DataTypeDes, RootDir, DefaultHTML)
                    socket.send(dataSend)       # send the processed data
                    socket.close()
                    Outputs.remove(socket)
                else:                           # if the request contains error (not found / not implemented type ) then push it to exceptions
                    ErrorObj=CombinedError(socket,code2)
                    print("output: print error code2 "+code2)
                    UnprocessedError.append(ErrorObj)
                    Exceptions.append(socket)
                    Outputs.remove(socket)
            else:                               # if the request contains error (invalid URL/VERSION/METHOD) then push it to exceptions
                ErrorObj=CombinedError(socket,code)
                #print("output: print error code "+code)
                UnprocessedError.append(ErrorObj)
                Exceptions.append(socket)
                Outputs.remove(socket)
        else:
            #print("Socket not found in Unproccesed queue")
            Outputs.remove(socket)

    for socket in Exceptions:       #if socket comes to this list means its request contains some errors. 
        j=len(UnprocessedError)
        print("j in exceptions"+str(j))
        i=0
        ErrIndex=-1
        while(i<j):                 #fetch the error code from the list of objects for a perticular socket
            object=UnprocessedError[i]
            if(object.socket == socket):
                ErrIndex=i
            i=i+1
        if(ErrIndex!=-1):
            msg=UnprocessedError[ErrIndex].code
            ErrorHead=Make_Error_Header(msg)        # create error header
            msg=msg.encode()
            senderror=ErrorHead+msg
            #print("Sending error as: "+str(senderror))
            socket.send(senderror)
            socket.close()
            Exceptions.remove(socket)
        else:
            #print("no error found for a socket")
            Exceptions.remove(socket)