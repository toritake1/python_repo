# -*- coding: utf_8 -*-  

import urllib
import urllib2
from xml.dom.minidom import parse as parseXML

URL = 'http://ja.wikipedia.org/w/api.php?'
BASIC_PARAMETERS = {'action': 'query',
                    'format': 'xml'}


class WikiHandler(object):
    def __init__(self, parameters, titles=None, url=URL):
        self._url = url if url.endswith('?') else url + '?'

        self._parameters = {}
        self._parameters.update(BASIC_PARAMETERS)
        self._parameters.update(parameters)

        if titles:
            self._parameters['titles'] = titles

        self.rawdata = self._urlfetch(self._parameters)

        if self._parameters['format'] == 'xml':
            self.dom = parseXML(self.rawdata)
            print 'DOM ready.'

    def _urlfetch(self, parameters):
        parameters_list = []

        for key, val in parameters.items():
            if isinstance(val, basestring):
                val = val.encode('utf-8')
            else:
                val = str(val)

            val = urllib.quote(val)
            parameters_list.append('='.join([key, val]))

        url = self._url + '&'.join(parameters_list)

        print 'Accessing...\n', url

        return urllib2.urlopen(url, timeout=20)

def main():
    parameters = {'list': 'categorymembers',
                  'cmlimit': 500,
                  'cmtitle': u'Category:日本の男性声優'}

    page = WikiHandler(parameters)

    elelist = page.dom.getElementsByTagName('cm')

    print elelist.length # 要素数

    for ele in elelist:
        print ele.getAttribute('title')


if __name__ == '__main__':
    main()

