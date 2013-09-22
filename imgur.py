#!/usr/bin/env python2
import webbrowser
import StringIO
import sys
import os
from xml.dom import minidom


try:
    import pycurl
except ImportError:
    sys.exit('Error: pycurl not found')

class XmlResponse:
   def __init__(self):
       self.contents = ''

   def body_callback(self, buf):
       self.contents = self.contents + buf

if len(sys.argv) > 1:
    img = sys.argv[1]
else:
    img = '/tmp/imgur.png'
    os.system('scrot -s %s' % img)
    
t = XmlResponse()	
curl = pycurl.Curl()
values = [
      ("key", "a3793a1cce95f32435bb002b92e0fa5e"),
      ("image", (curl.FORM_FILE, img))]

curl.setopt(curl.URL, "http://imgur.com/api/upload.xml")
curl.setopt(curl.HTTPPOST, values)
curl.setopt(pycurl.WRITEFUNCTION, t.body_callback)
curl.perform()
curl.close()
    
dom = minidom.parseString(t.contents)

settings = {
    'original_image' : dom.getElementsByTagName("original_image")[0].childNodes[0].nodeValue,
    'large_thumbnail' : dom.getElementsByTagName("large_thumbnail")[0].childNodes[0].nodeValue,
    'small_thumbnail' : dom.getElementsByTagName("small_thumbnail")[0].childNodes[0].nodeValue,
    'imgur_page' : dom.getElementsByTagName("imgur_page")[0].childNodes[0].nodeValue,
    'delete_page' : dom.getElementsByTagName("delete_page")[0].childNodes[0].nodeValue,
}

out=''
for i in settings:
    out = out + i + ':\t\t' + settings[i] +'\n'

#print settings['original_image']
os.system('zenity --info --text="Links for image:\n%s"' % out)  
#webbrowser.open_new_tab(settings['original_image'])
