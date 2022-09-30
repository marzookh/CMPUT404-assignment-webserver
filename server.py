#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        received_data = self.data.decode('utf-8')

        # return status code of 405 for any method we cannot handle
        if 'POST' in received_data or 'PUT' in received_data or 'DELETE' in received_data:
            send_data = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            self.request.sendall(send_data.encode())
            return


        # returns status code of 301 after checking file path
        file_content = ''
        response_data = ''
        local_path = received_data.splitlines()[0].split()[1]
        current_local_path = os.getcwd() + '/www' + local_path

        if (local_path.endswith('/')):
            file_path = os.path.abspath(current_local_path + 'index.html')
        else:
            file_path = os.path.abspath(current_local_path)
        

        resource_path = os.path.exists(os.path.abspath(current_local_path))

        if (not os.path.isfile(file_path) and resource_path):
            response_data = "HTTP/1.1 301 Moved Permenantly\r\n"
            response_data += "Location: http://127.0.0.1:8080{}/\r\n".format(local_path)
            response_data += "Content-Type: text/html; charset=utf-8\r\n"

        # returns status code of 404
        elif(os.getcwd() not in file_path):
            response_data = "HTTP/1.1 404 Not Found\r\n"

        
        else:
            if os.path.exists(file_path):
                with open(file_path,'r') as file:
                    print('file exists')
                    file_content = file.read()
                    response_data = "HTTP/1.1 200 OK\r\n"

                    # check mime type
                    if file_path.endswith(".css"):
                        mime_type = 'text/css'
                    else:
                        mime_type = 'text/html'
                    
                    response_data += 'Content-Type: '+ mime_type+ '; charset=utf-8\r\n'
            
            else:
                response_data = "HTTP/1.1 404 Not Found\r\n"

            response_data += "Content-Length: {}\r\n\r\n".format(len(file_content))
            response_data += file_content
        
        self.request.sendall(response_data.encode())
        self.request.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)
    
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
