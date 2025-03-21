# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:35:03 2017

@author: menjle
"""

import re
import time
#import socket

# MAKE THIS NEXT BLOCK OF CODE ACTIVE IF YOU WISH TO RUN IT ON THE ARC SYSTEM
# WHERE THE MODULES ARE
#host_name=(socket.gethostname())
#print(host_name)
#host= (host_name.split('.'))[1].strip()


host = "arc3"

# =============================================================================
# These urls link to documentation pages for specific software on the arc
# website.
# I have used url rather than link as this is an overused word.
# =============================================================================
f_urls = ["./urls/applications_urls.txt","./urls/libraries_urls.txt","./urls/compilers_urls.txt","./urls/utilities_urls.txt"]


app_urls = []

for file in f_urls:
    with open(file, 'r') as f_urls:
        for line in f_urls:
         i = line.count(',')
         if i == 1:
             app_name = (line.split(','))[0].strip()
             url = (line.split(','))[1].strip()
             arr=[app_name,url]
             app_urls.append(arr)



# =============================================================================
# These descriptions are created by a script that uses the "module whatis"
# command.
# =============================================================================

filename_desc = "./"+host+"/whatis_"+host+".txt"

descriptions = []

with open(filename_desc) as f_in:
    last_app__name="    "
    app__name="    "
    for line in f_in:
        i = line.count(':')
        if i == 1:
            app__name = (line.split(':'))[0].strip()
            desc = (line.split(':'))[1].strip()
            if app__name.strip() != last_app__name.strip():
                arr=[app__name,desc]
                descriptions.append(arr)
        if i > 1:
            app__name = (line.split(':'))[0].strip()
            s1 = (line.split(':'))[1].strip()
            s2 = (line.split(':'))[2].strip()
            desc = s1 + s2
            if app__name.strip() != last_app__name.strip():
                arr=[app__name,desc]
                descriptions.append(arr)
        last_app__name = app__name
f_in.close()


# =============================================================================
# Creates an html table which is written into individual files for each category.
# =============================================================================


lineStart = "<table class=\"table table-striped\" bgcolor=\"#E6E6FA\" style=\"border:1px solid black; border-collapse:collapse;\">\n"
lineEnd = "</table>\n"
lineTheadStart = " <thead>\n"
lineTheadEnd = " </thead>\n"
lineTbodyStart = " <tbody>\n"
lineTbodyEnd = " </tbody>\n"

rowStart = "<tr>"
rowEnd = "</tr>"
headCellStart = "<th style=\"border:1px solid black\">"
headCellEnd = "</th>"
bodyCellStart = "<td style=\"border:1px solid black\">"
bodyCellEnd = "</td>"

captionStart = "<caption>"
captionEnd = "</caption>"

now = time.strftime("%c")

sp = ' '
nl = '\n'

sp = ' '
nl = '\n'

last_app = ""


app=""
last_app=""

r=0
descrip=""

with open("./"+host+"/modules_"+host+".txt", 'r') as fin:
    with open("./module_table_out_"+host+".html", 'w') as fout:
        for line in fin:
            t_title = False
            t_body = False
            t_end = False
            n=line.count('/')

            if n > 1:
                category = re.sub(':$', '', (line.split('/'))[n].strip())
                app = ""
                t_title = True
                if r != 0:
                    t_end = True

            if n == 0:
                app = line.strip()
                for d in descriptions:
                    if app == d[0]:
                        descrip = d[1]
                        break

                version = ""
                t_body = True
            if n == 1:
                app = (line.split('/'))[0].strip()
                for d in descriptions:
                    if app == d[0]:
                        descrip = d[1]
                        break

                for a in app_urls:
                    if app == a[0]:
                        app = a[1]
                        break

                version = (line.split('/'))[1].strip()
                t_body = True
            if category != "architecture":
                if t_end:
                    fout.write( nl+lineTbodyEnd )
                    fout.write( lineEnd +nl+nl)
                    t_end = False
                if t_title:
                    fout.write( "<h2>"+category.title()+"</h2>"+nl+nl)
                    fout.write( nl+lineStart )
                    fout.write( nl+captionStart+"This table of "+category+" was automatically created "+now+captionEnd )
                    fout.write( nl+lineTheadStart )
                    fout.write( sp+sp+rowStart + headCellStart + "Module" + headCellEnd )
                    fout.write( nl+sp+sp+ headCellStart + "Version(s)" + headCellEnd )
                    fout.write( nl+sp+sp+ headCellStart + "Description" + headCellEnd)
                    fout.write( nl+sp+sp+rowEnd+lineTheadEnd+nl+lineTbodyStart+nl)
                    t_title = False
                if t_body:
                    if last_app != app:
                        fout.write( sp+sp+rowStart + headCellStart + app + headCellEnd )
                    else:
                        fout.write( sp+sp+rowStart + headCellStart + "" + headCellEnd )
                    fout.write( nl+sp+sp+bodyCellStart + version + bodyCellEnd )
                    if last_app != app:
                        fout.write( nl+sp+sp+bodyCellStart + descrip + bodyCellEnd )
                    else:
                        fout.write( nl+sp+sp+bodyCellStart + "" + bodyCellEnd )
                    fout.write( nl+sp+sp+rowEnd+nl )
                    t_body = False
                r=r+1
                last_app=app


        fout.write( nl+lineTbodyEnd )
        fout.write( lineEnd +nl+nl)
