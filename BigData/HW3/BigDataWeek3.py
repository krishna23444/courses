#!/usr/bin/env python

import glob          
import mincemeat



'''
Instructions:

Multiple files representing a bibliography for an article, each line is a reference:
paper-id:::author1::author2::...::authorN:::title

Your task is to compute how many times every term occurs across titles, for each author:

Terms should exclude stop words specified, and single letter words
Hyphens and punctuation should be deleted 

Open:
Lowercase on terms ?
Same reference from two different files should be count once or more? 
'''

# Input file processing 

text_files = glob.glob('hw3data/*') 

def file_contents(file_name):
# Read file and emit its content
    f = open(file_name)
    try:
        return f.read()
    finally:
        f.close()

# Each entry is (k=file name, v=file content, which is all lines of references)       
datasource = dict(((file_name, file_contents(file_name)) 
                   for file_name in text_files))

def mapfn(k, v):
# Mapper: Get (filename, content) and for each reference (line in content) emit per author (author, title)
    for line in v.splitlines():
        line_parts = line.split(':::')
        size = len(line_parts)
        if (size != 3): 
            print("Error in this reference: ", line)
        # doc = line_parts[0]
        authors = line_parts[1]
        title = line_parts[2]
        for author in authors.split('::'):
            yield author, title



def reducefn(k, v):
# Reducer: Get (author, [titles]) and create a local dictionary (term,count) and scan all titles by that author into that structure and save it

    import re
    import stopwords

    def is_ignored(term):
    # Ignore term if it is a stop word or 1 letter
        return (term in stopwords.allStopWords) or (len(term) <= 1)
            
    def make_term(word):
    # Remove punctuation or hyphens and make lower case 
        # p = re.compile('\W*')
        return re.sub('\W+', '', word).lower().strip()

    terms = {}
    for title in v:
        for word in title.split():
            if (not is_ignored(word)):
                term = make_term(word)
                if (term in terms):
                    terms[term] += 1
                else:
                    terms[term] = 1
    return terms 

# Server
s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")

# Write results
out = open('results.txt', 'wt')
try:
    for author in results:
        #print author
        terms = results[author]
        sorted_terms = sorted([(v,k) for (k,v) in terms.items()], reverse=True)
        #print sorted_terms[0][1], sorted_terms[0][0]
        #print sorted_terms[1][1], sorted_terms[1][0]
       
        #for term in sorted_terms:
        #    print term
        #if sorted_terms.length > 1:
        #    print sorted_terms[1] 
        #for term in sorted_terms:
        out.write('%s - ' % author)
        if len(sorted_terms) > 0:
            out.write("%s:%d" % (sorted_terms[0][1], sorted_terms[0][0]))
        if len(sorted_terms) > 1:
            out.write("%s:%d" % (sorted_terms[1][1], sorted_terms[1][0]))
        out.write('\n')
finally:
    out.close()

