# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Oct  2 16:35:03 2017

This is a script that runs on a Linux system that uses modules to allow
users to access software and creates a table in mark down that can be
copied and pasted into a word press webpage.

Execute as:
    python module_avail_html_table.py

@author: menjle - Joanna Leng - j.leng@leeds.ac.uk
"""

import re
import time
import socket
import os
import sys
import argparse

def check_path(path_string):
    """
    Check to see if the path given at the command line is valid.
    Inputs:
        String          The path as a string
    Outputs:
        None
    """
    if os.path.isdir(path_string):
        print("Path %s is valid." % (path_string))
    else:
        sys.exit('Path %s is an invalid value!!!' % (path_string))

def parse_arguments():
    """
    Handles the command line flags/args.
    """
    parser = argparse.ArgumentParser(
        description="""This is a script that runs on a Linux system that uses modules to allow
                        users to access software and creates a table in mark down that can be
                        copied and pasted into a word press webpage."""
    )

    parser.add_argument("-path",
                        type=str,
                        default=os.getenv('HOME'),
                        help="Path for temporary files.")
    return parser.parse_args()

def change_file_extension(file_path, new_extension):
    """
    Change file extension is needed to change the input .txt to output
    .hmtl.
    Inputs:
        String      The path and filename with file extension as a string.
        String      The new file extension (without the ".") as a string.
    Outputs:
        String      The original path and filename but with a new file
                    extension as a string.
    """
    # Split the file path into root and extension
    root, _ = os.path.splitext(file_path)
    print(root)
    # Create the new file path with the new extension
    new_file_path = f"{root}.{new_extension}"
    print(new_file_path)
    # Rename the file
    #os.rename(file_path, new_file_path)
    return new_file_path


def main():
    """
    The main funtion does the work: it exectutes the module commands and formats the
    output of that.
    """
    args = parse_arguments()
    check_path(args.path)

    # MAKE THIS NEXT BLOCK OF CODE ACTIVE IF YOU WISH TO RUN IT ON THE ARC SYSTEM
    # WHERE THE MODULES ARE
    #host_name=(socket.gethostname())
    #print(host_name)
    #host= (host_name.split('.'))[1].strip()


    #host = "arc3"
    host = socket.gethostname()
    print("host: %s" % (host))

    # =============================================================================
    # These urls link to documentation pages for specific software on the arc
    # website.
    # I have used url rather than link as this is an overused word.
    # =============================================================================
    #f_urls = ["./urls/applications_urls.txt",
    #        "./urls/libraries_urls.txt",
    #        "./urls/compilers_urls.txt",
    #        "./urls/utilities_urls.txt"]


    #app_urls = []

    ##for file in f_urls:
    ##    with open(file, 'r', encoding="utf-8") as f_urls:
    ##        for line in f_urls:
    ##            i = line.count(',')
    ##            if i == 1:
    ##                app_name = (line.split(','))[0].strip()
    ##                url = (line.split(','))[1].strip()
    ##                arr=[app_name,url]
    ##                app_urls.append(arr)"




    # =============================================================================
    # These descriptions are created by a script that uses the "module whatis"
    # command.
    # =============================================================================

    #filename_desc = "./"+host+"/whatis_"+host+".txt"
    #filename_desc = "/home/jo/code_projects/examples/"+host+"/whatis_"+host+".txt"
    filename_desc = "/home/jo/code_projects/examples/module_tables/modules_example.txt"
    print("filename_desc: %s" % (filename_desc))
    print("\n\n")


    #f_loc = r"/home/jo/code_projects/examples/"+host+".txt"
    #if not os.path.exists(f_loc):
    #    open(f_loc, 'w').close()

    descriptions = []

    with open(filename_desc, encoding="utf-8") as f_in:
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

    print(descriptions)

    # =============================================================================
    # Creates an html table which is written into individual files for each category.
    # =============================================================================


    table_start = """<table class=\"table table-striped\"
                    bgcolor=\"#E6E6FA\"
                    style=\"border:1px solid black;
                    border-collapse:collapse;\">\n"""
    table_end = "</table>\n"
    table_header_start = " <thead>\n"
    table_header_end = " </thead>\n"
    table_body_start = " <tbody>\n"
    table_body_end = " </tbody>\n"

    row_start = "<tr>"
    row_end = "</tr>"
    header_cell_start = "<th style=\"border:1px solid black\">"
    header_cell_end = "</th>"
    body_cell_start = "<td style=\"border:1px solid black\">"
    body_cell_end = "</td>"

    caption_start = "<caption>"
    caption_end = "</caption>"

    now = time.strftime("%c")

    sp = ' '
    nl = '\n'

    last_app = ""


    app=""
    last_app=""

    r=0
    descrip=""
    category=""

    print("\n\n\n")

    tables = change_file_extension(filename_desc, "html")

    with open(filename_desc, 'r', encoding="utf-8") as fin:
        with open(tables, 'w', encoding="utf-8") as fout:
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

                    ###################################################
                    ## When we add urls for link to documentation may #
                    ## want to re-implement this                     ##
                    ###################################################
                    #for a in app_urls:
                    #    if app == a[0]:
                    #        app = a[1]
                    #        break

                    version = (line.split('/'))[1].strip()
                    t_body = True
                if category != "architecture":
                    if t_end:
                        fout.write(nl+table_body_end)
                        fout.write(table_end +nl+nl)
                        t_end = False
                    if t_title:
                        fout.write("<h2>"+category.title()+"</h2>"+nl+nl)
                        fout.write(nl+table_start)
                        fout.write(nl+caption_start+"This table of "+category+
                                " was automatically created "+now+caption_end)
                        fout.write(nl+table_header_start)
                        fout.write(sp+sp+row_start + header_cell_start + "Module" + header_cell_end)
                        fout.write(nl+sp+sp+ header_cell_start + "Version(s)" + header_cell_end)
                        fout.write(nl+sp+sp+ header_cell_start + "Description" + header_cell_end)
                        fout.write(nl+sp+sp+row_end+table_header_end+nl+table_body_start+nl)
                        t_title = False
                    if t_body:
                        if last_app != app:
                            fout.write(sp+sp+row_start + header_cell_start + app + header_cell_end)
                        else:
                            fout.write(sp+sp+row_start + header_cell_start + "" + header_cell_end)
                        fout.write(nl+sp+sp+body_cell_start + version + body_cell_end)
                        if last_app != app:
                            fout.write(nl+sp+sp+body_cell_start + descrip + body_cell_end)
                        else:
                            fout.write(nl+sp+sp+body_cell_start + "" + body_cell_end)
                        fout.write(nl+sp+sp+row_end+nl)
                        t_body = False
                    r=r+1
                    last_app=app


            fout.write( nl+table_body_end )
            fout.write( table_end +nl+nl)

if __name__ == "__main__":
    main()
