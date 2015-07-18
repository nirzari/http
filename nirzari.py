from bottle import route, run, get, post, request, response
import socket
import sys
import requests
import threading
import json
import os


#Server_Location is the directory from where the program is being initialized.


#Server Socket is created. It listens on port number 8085. 
try:
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
host = 'localhost'
port = 8085
     
#a simple HTML page with a form which takes the file as an Input and sends it to the server. 
@route('/uploadfile')
def uploadfile():
    return '''
        <form action="/uploadfile" method="post" enctype="multipart/form-data">
  Select a file: <input type="file" name="myfile" />
  <input type="submit" value="Upload" />
</form>
    '''

#function to process the POST request made by the client which uploads the file at the Server_Location.
@route('/uploadfile', method='POST')
def start_upload():
    uploadfile     = request.files.get('myfile')
    name, ext = os.path.splitext(uploadfile.filename)

    storePath = os.getcwd()
    if not os.path.exists(storePath):
           os.makedirs(storePath)

    file_path = "{path}/{myfile}".format(path=storePath, myfile=uploadfile.filename)
    uploadfile.save(file_path) 
    fileOut = open("log.txt",'a')
    response.status = 200
    fileOut.write(str(response.status)+ "\n")
    fileOut.write(str(os.stat(uploadfile.filename))+"\n")
    return "File stored at '{0}'.".format(storePath)
    
	
   
#a simple HTML page with a form which asks for the filename as an Input for downloading.
#The file should be at the Server_Location otherwise it will not be found.

@get('/downloadfile')
def downloadfile():
    return '''
  <form action="/downloadfile" method="POST">
  Select a file: <input type="text" name="mydownloadfile" />
  <input type="submit" value="download" />
  </form>
    '''
#a function to download the file save it in the download directory specified by download_directory.
#change the download_directory for saving the file. 
@post('/downloadfile')
def start_download():
    
    downloadfile   = request.forms.get('mydownloadfile')
    
    fileToDownload = open(os.getcwd()+"/"+downloadfile,'r')
    #Please change the path of download_directory according to the system
    download_directory = "/home/ugupta/Downloads"
    var1 = open(download_directory+"/"+downloadfile,'wb')
    file_content = fileToDownload.read()
    var1.write(file_content) 
    var2=os.path.basename(os.getcwd()+"/"+downloadfile)
    with open("log.txt",'a') as fileOut:
	responseCode = str(response.status)
	if responseCode==200:
      		message = file_content
      		print("File Content is" % message)
	if responseCode==404:
		print("HTTP 404 file not found")
    	fileOut.write("GET - "+responseCode+"\n")
        fileOut.write(str(os.stat(var2))+"\n")

    
     
  
threading.Thread(target=run, kwargs=dict(host='localhost', port=8085)).start()






