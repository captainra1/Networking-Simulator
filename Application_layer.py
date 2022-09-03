from ftplib import FTP
ftp = FTP('ftp.us.debian.org')  # connect to host, default port
ftp.login()                     # user anonymous, passwd anonymous@
ftp.cwd('debian') # change into "debian" directory
print("Using FTP protocol with default port:")
print("File transfer using ftp protocol")
print("Files present at the directory : ftp.us.debian.org/debian")


ftp.encoding = "utf-8"
ftp.dir()
filename = 'README.mirrors.txt'
print("----------------------------------------------------------------")
print("Downloading the file : "+filename)



with open(filename, 'wb') as fp:
    ftp.retrbinary(f"RETR {filename}", fp.write)

print("----------------------------------------------------------------")
print("Content in downloaded file : ")

file= open(filename, "r")
print('File Content:', file.read())

ftp.quit()


print("Http protocol:")
print("-----------------------------------------------------------------------------------------")

from http import HTTPStatus
HTTPStatus.OK

HTTPStatus.OK == 200

HTTPStatus.OK.value

HTTPStatus.OK.phrase

HTTPStatus.OK.description

print("http codes:")
print(list(HTTPStatus))

import http.client
conn = http.client.HTTPSConnection("www.python.org")
conn.request("GET", "/")
r1 = conn.getresponse()
print(r1.status, r1.reason)

data1 = r1.read()  # This will return entire content.
# The following example demonstrates reading data in chunks.
conn.request("GET", "/")
r1 = conn.getresponse()
while chunk := r1.read(200):
    print(repr(chunk))
    pass


# Example of an invalid request
conn = http.client.HTTPSConnection("docs.python.org")
conn.request("GET", "/parrot.spam")
r2 = conn.getresponse()
print(r2.status, r2.reason)

data2 = r2.read()
conn.close()