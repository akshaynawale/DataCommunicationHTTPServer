###################### AUTHOR ##############################
Name: Akshay Satyendra Navale
Occupation: ITP Student at University of Colorado, Boulder.USA.
Contact Details: akna8887@colorado.edu
Phone Number: 720-345-4053
############################################################


Welcome!!! 
This is a README file for WebServer_anavale.py.
The python code is written in python version 2.7.


###############Placement of ws.cong file##################
Your ws.cong file must present in the same folder from 
where you are running the WebServer_anavale.py file.


###############Supported Web Browser######################
This Server Supports foloowing Web Browsers:
Mozilla Firefox
Google Crome
Internet Explorer

---Tip for internet Explorer Users:
Please use http://localhost:portnumber
portnumber will same as you enter in the ws.conf file.



###############Handling the ws.conf File#################
Donot remove any content in a line which start with the "#"
in ws.conf file.



#################Configuration Change#####################
ws.conf is a configuration file for the Server.
You can change the configuration of Web Server by changing 
the values in the configuration file.

----- to change the Server Port --------------------------
Change the Number after Listen word in the ws.conf file
e.g:
Listen 12345
The server supports 4 and 5 digits port numbers.

------to change the root Directory Path-------------------
To change the root directory path put your path with 
respect to the folder in which your WebServer_anavale.py
file is present.
To change the root directory path, put your path after 
DocumentRoot word. dont forget to put the path in double 
inverted commas.
eg:
#document root
DocumentRoot "/HTMLFiles/"

------to Change the default HTML file on Server----------
To change the default HTML File change the put your default 
html file name after DirectoryIndex  in ws.conf file.
eg:
#default web page
DirectoryIndex ChangedHTML.html

------to add/remove the supported files types -----------
To add supported file types in Web Server you can add file 
types in the following format as shown in the ws.conf file

eg:

#Content-Type which the server handles
.html text/html
.htm text/html
.txt text/plain
.png image/png
.gif image/gif
.jpg image/jpg
.css text/css
.js  text/javascript
.ico image/x-icon

so to remove support of a file type from the web server remove 
the line in ws.conf file for that file type

WORNING:----------------------------------------------------
PUT THE NEW FILE TYPES IN THE NEW LINE AND IN THE SAME FORMAT
AS SHOWN ABOVE.



##########Web Server Handles Following Errors#################
----------INVALID METHOD-------------------------------------
This Server Supports "GET","HEAD","POST" methods only.If the 
method name in the client request is other than this then 
following error will be seen on the Web Browser.
 
400 Bad Request : Invalid Method: <your method>

----------INVALID URL----------------------------------------
If the URL contains spaces or black slash then this error is 
shown on the browser.

400 Bad Request : Invalid URI:<your invalid url>

--------INVALID VERSION-------------------------------------
If the version in the client request is different than "HTTP/1.1" 
following error will be shown on the browser.

400 Bad Request : Invalid HTTP-Version: <your invalid version>

-------File NOT FOUND----------------------------------------
When the file is not found in the root Directory as mention in
the ws.conf file. then foloowing error is shown on the browser.

404 Not Found :<relative path of the requested file>

-------File Type not implemented-----------------------------
when the requested file is not supported by the web server 
following error will be shown.

501 Not Implemented :<relative path of the requested file>


############################################################
Thank You. For your precious time!!!  

 