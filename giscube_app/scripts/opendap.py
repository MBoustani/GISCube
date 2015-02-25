from pydap.client import open_url
from netcdftime import utime
import numpy as np
import urllib

from giscube.config import MEDIA_ROOT, MEDIA_URL

def opendap_metadata(opendap_url):
    response = urllib.urlopen(opendap_url + ".das")
    return response.read()

def load(url, frm, name):
    if url.split(".")[-1] != "gz":
        url = url + "gz"
    if frm == "ASCII":
        urllib.urlretrieve ("{0}.ascii".format(url), "{0}{1}".format(MEDIA_ROOT + MEDIA_URL, "{0}.ascii".format(name)))
    elif frm == "nc3":
        urllib.urlretrieve ("{0}.nc".format(url), "{0}{1}".format(MEDIA_ROOT + MEDIA_URL, "{0}.nc".format(name)))
    elif frm == "nc4":
        urllib.urlretrieve ("{0}.dap.nc4".format(url), "{0}{1}".format(MEDIA_ROOT + MEDIA_URL, "{0}.nc".format(name)))