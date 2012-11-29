#!/usr/bin/env python

import urllib
import re

langs = ('python','ruby','perl','java')

url_stem = 'http://stackoverflow.com/questions/tagged/'

counts = {}
for lang in langs:
    resp = urllib.urlopen(url_stem + lang).read()
    m = re.search('summarycount.*>(.*)<', resp)
    count = int(m.group(1).replace(',', ''))
    counts[lang]=count
    print lang, ':', count
sorted_counts = sorted(counts.items(), key=lambda (k,v):(v,k))
sorted_counts.reverse()

print sorted_counts[0][0], 'wins with', sorted_counts[0][1]
