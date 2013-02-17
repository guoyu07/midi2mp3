import urllib, os, os.path, httplib,re
try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")




def fetchMidi(id):
  host = '173.164.157.189'
  port = 80
  conn = httplib.HTTPConnection(host, port)
  headers = { 'Host': 'www.freehandmusic.com'}
  base_url = 'http://www.freehandmusic.com/webservices/webservice.asmx/GetProduct_xml'
  method = 'GET'
  body = ''
  url = base_url + '?prodid='+str(id)
  conn.request(method, url, body, headers)
  resp = conn.getresponse()
  tree = etree.parse(resp)
  conn.close()
  midi_url = tree.findtext('.//midi_preview_url')
  file_loc = os.getcwd()
  urllib.urlretrieve(midi_url, os.path.join(file_loc,str(id)+'.mid'))
  




