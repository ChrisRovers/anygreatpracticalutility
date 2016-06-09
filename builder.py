import shutil
import re
import markdown
import os
from os import listdir
from os.path import isfile, join, splitext
import moment
from datetime import datetime

def createHtmlFile(outputlocation, templatelines, maincontent, tagscontent, postscontent, disqushtml) :
    print "Creating output file "+outputlocation+".html"
    of = open('output/'+outputlocation+'.html','w')
    for templateline in templatelines:
        if (re.search('<%CONTENT%>',templateline) != None) :
            templateline = re.sub('<%CONTENT%>',maincontent,templateline)
        if (re.search('\<\%TAGS\%\>',templateline) != None) :
            templateline = re.sub('\<\%TAGS\%\>',tagscontent,templateline)
        if (re.search('\<\%RECENTPOSTS\%\>',templateline) != None) :
            templateline = re.sub('\<\%RECENTPOSTS\%\>',postscontent,templateline)                    
        if (re.search('\<\%DISQUS\%\>',templateline) != None) :
            templateline = re.sub('\<\%DISQUS\%\>',disqushtml,templateline)                        
        of.write(templateline);
    of.close();    


# TODO : we do not clear out the output directory and we probably should - a problem for future me

# read in our template index html file - we will use this for all output files
tf = open('template/index.html','r')
templatelines = tf.readlines()
          
posts = [] # posts have location (file name minus extension), tags (tag name list),
            # date, title, htmlcontent
tags = {} # tags have name, list of locations that reference them

markdownfiles = [f for f in listdir('posts') if isfile(join('posts', f))]

# disqus html template 
dhtml =         '<div id="disqus_thread"></div>'
dhtml = dhtml + '<script>'
dhtml = dhtml + 'var disqus_config = function () {'
dhtml = dhtml + 'this.page.url = PAGE_URL; '
dhtml = dhtml + 'this.page.identifier = PAGE_IDENTIFIER;'
dhtml = dhtml + '};'
dhtml = dhtml + '(function() { '
dhtml = dhtml + 'var d = document, s = d.createElement(\'script\');'
dhtml = dhtml + 's.src = \'//chrisrovers.disqus.com/embed.js\';'
dhtml = dhtml + 's.setAttribute(\'data-timestamp\', +new Date());'
dhtml = dhtml + '(d.head || d.body).appendChild(s);'
dhtml = dhtml + '})();'
dhtml = dhtml + '</script>'
dhtml = dhtml + '<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>'

for mdfile in markdownfiles:
    print "Processing file "+mdfile
    f = open('posts/'+mdfile,'r')

    post = {}

    filename, file_extension = splitext(mdfile)
    
    post["location"] = filename

    alllines = f.readlines()
    markdownlines = ""    

    inHeader = True;

    for line in alllines:
        if (inHeader) :
            tmp = line;
            tmp = tmp.strip();
            if (tmp == '+++') :
                inHeader = False
            else :
                # parse the header
                bits = tmp.split('=')
                if (len(bits) > 1) :
                    headername = bits[0]
                    headerval = bits[1]
                    headername.strip()
                    headername = re.sub('\W','',headername)
                    headerval.strip()
                    if (headername == 'tags') :
                        print "TAGS: "+headerval
                        posttags = headerval.split()
                        for posttag in posttags:
                            posttag = re.sub('\W','',posttag)
                            if (posttag not in tags) :
                                tags[posttag] = []
                            tags[posttag].append(post)
                    elif (headername == 'title') :  
                        print "TITLE: "+headerval
                        post['title'] = headerval
                    elif (headername == 'date') :
                        # TODO parse here?
                        print "DATE: "+headerval
                        headerval = headerval.strip()
                        post['date'] = moment.date(headerval)
                        
        else :
            markdownlines = markdownlines + line

    f.close()
    posthtml = '<h2>'+post['title']+'</h2>\n'+'<i>'+post['date'].format("YYYY-M-D")+'</i>\n'+markdown.markdown(markdownlines)
    
    post["html"] = posthtml
    posts.append(post)


# create post lists - 

posts.sort(key=lambda post: post['date'])
posts.reverse()

recentpostshtml = ""
for post in posts :
    recentpostshtml = recentpostshtml + '\n<li><a href="'+post['location']+'.html">'+post['title']+'</a></li>'

# create tags html
taghtml = ""
for tag in tags.keys() :
    taghtml = taghtml + '\n<li><a href="tagpage-'+tag+'.html">'+tag+'</a></li>'

# go through all posts and create their file
for post in posts :
    thisdisqus = re.sub('PAGE_URL',post['location'],dhtml)
    thisdisqus = re.sub('PAGE_IDENTIFIER',post['location'],thisdisqus)
    createHtmlFile(post['location'],templatelines,post['html'],taghtml,recentpostshtml,thisdisqus)

# create about.html
# TODO: combine this with the main post parser, too lazy right now
print "Processing About File about.md"
f = open('about.md','r')

alllines = f.readlines()
markdownlines = ""    

inHeader = True;

for line in alllines:
    if (inHeader) :
        tmp = line;
        tmp = tmp.strip();
        if (tmp == '+++') :
            inHeader = False
    else :
        markdownlines = markdownlines + line

f.close()
abouthtml = markdown.markdown(markdownlines)
createHtmlFile('about', templatelines, abouthtml, taghtml, recentpostshtml,'')

# create index.html - consists of the most recent post, plus some bits
indexhtml = posts[0]['html']
createHtmlFile('index', templatelines, indexhtml, taghtml, recentpostshtml,'')


# create allposts.html
allpostshtml = "<h2>All Posts</h2>\n<ul>\n"
for post in posts :    
    allpostshtml = allpostshtml + '\n<li><a href="'+post['location']+'.html">'+post['title']+'</a> ('+post['date'].format("YYYY-M-D")+')</li>\n'
allpostshtml = allpostshtml + "\n</ul>\n"
createHtmlFile('allposts', templatelines, allpostshtml, taghtml, recentpostshtml,'')

# create alltags.html
alltagshtml = "<h2>All Posts By Tags</h2>\n<ul>\n"
for tag in tags.keys() :
    alltagshtml = alltagshtml + '\n<li>'+tag+'\n<ul>'
    tags[tag].sort(key=lambda post: post['date'])
    for post in tags[tag]:
        alltagshtml = alltagshtml + '\n<li><a href="'+post['location']+'.html">'+post['title']+'</a> ('+post['date'].format("YYYY-M-D")+')</li>\n'
    alltagshtml = alltagshtml + '</ul></li>'
alltagshtml = alltagshtml + "</ul>"
createHtmlFile('alltags', templatelines, alltagshtml, taghtml, recentpostshtml,'')

# create all tag pages
for tag in tags.keys() :
    thistagshtml = '\n<h2>All Posts with the '+tag+' Tag</h2><ul>'
    for post in tags[tag]:
        thistagshtml = thistagshtml + '\n<li><a href="'+post['location']+'.html">'+post['title']+'</a> ('+post['date'].format("YYYY-M-D")+')</li>\n'
    thistagshtml = thistagshtml + '</ul>'
    createHtmlFile('tagpage-'+tag, templatelines, thistagshtml, taghtml, recentpostshtml,'')

# copy the rest of the template
print "Copying remainder of template"
shutil.copy2('template/default.css','output')
shutil.copy2('template/style.css','output')
# copy the images
imagefiles = [f for f in listdir('template/images/') if isfile(join('template/images/', f))]
if not os.path.exists('output/images'):
    os.makedirs('output/images')
for imagefile in imagefiles :
    shutil.copy2('template/images/'+imagefile,'output/images/'+imagefile)
