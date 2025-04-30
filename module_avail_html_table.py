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
import validators

def create_libraries_table_html(libraries_table, libraries):
    """
    create a text file with a html table of the libraries.
    Inputs:
        libraries_table          The path and filename as a string
        libraries                The list of libraries as a list of dictionaries
    Outputs:
        None
    """

    table_start = "<table>\n"
    table_style1 = "\t<style scoped>\n"
    table_style2 = "\t\ttable {\n\t\t\twidth: 100%;\n\t\t\tborder-collapse: collapse;\n\t\t}\n"
    table_style3 = "\t\tth, td {\n\t\t\tborder: 1px solid black;\n\t\t\tpadding: 8px;\n\t\t}\n"
    table_style4 = "\t\tth {\n\t\t\tbackground-color: #f6f6f6;\n\t\t}\n"
    table_style5 = "\t\ttr:nth-child(even) {\n\t\t\tbackground-color: #f2f2f2;\n\t\t}\n"
    table_style6 = "\t\tth:nth-child(even),td:nth-child(even) {\n" \
                   "\t\t\tbackground-color: rgba(150, 212, 212, 0.4);\n\t\t}\n"
    table_style7 = "\t\ttr:hover {\n\t\t\tbackground-color: #D6EEEE;\n\t\t}\n"
    table_style8 = "\t</style>\n"
    table_end = "</table>\n"
    table_header_start = "\t<thead>\n"
    table_header_end = "\t</thead>\n"
    table_body_start = "\t<tbody>\n"
    table_body_end = "\t</tbody>\n"

    row_start = "\t\t<tr>\n"
    row_end = "\t\t</tr\n>"
    #header_cell_start = "<th style=\"border:1px solid black\">"
    header_cell_start = "\t\t\t<th>\n\t\t\t\t"
    header_cell_end = "\t\t\t</th>\n"
    #body_cell_start = "<td style=\"border:1px solid black\">"
    body_cell_start = "\t\t\t<td>\n\t\t\t\t"
    body_cell_end = "\t\t\t</td>\n"

    caption_start = "\t<caption>\n"
    caption_end = "\t</caption>\n"

    now = time.strftime("%c")
    caption = (
                f"\t\t<b>Libary Modules on Aire Table:</b> "
                f"This table of libraries was automatically created {now}.\n"
                )



    #sp = ' '
    nl = '\n'

    tables = change_file_extension_add_date(libraries_table, "html")

    with open(tables, 'w', encoding="utf-8") as fout:
        fout.write(table_start)
        fout.write(table_style1)
        fout.write(table_style2)
        fout.write(table_style3)
        fout.write(table_style4)
        fout.write(table_style5)
        fout.write(table_style6)
        fout.write(table_style7)
        fout.write(table_style8)
        fout.write(caption_start)
        fout.write(caption)
        fout.write(caption_end)
        fout.write(table_header_start)

        fout.write(row_start)
        fout.write(header_cell_start + "Module" + nl + header_cell_end)
        fout.write(header_cell_start + "Version" + nl + header_cell_end)
        fout.write(header_cell_start + "Description" + nl + header_cell_end)
        fout.write(header_cell_start + "License" + nl + header_cell_end)
        fout.write(header_cell_start + "URL" + nl + header_cell_end)
        fout.write(header_cell_start + "Path (compile-time dependancies)" + nl + header_cell_end)
        fout.write(row_end)

        fout.write(table_header_end)

        fout.write(table_body_start)

        for item in libraries:
            fout.write(row_start)
            fout.write(body_cell_start + item['name'] + nl + body_cell_end)
            fout.write(body_cell_start + item['version'] + nl + body_cell_end)
            fout.write(body_cell_start + item['summary'] + nl + body_cell_end)
            fout.write(body_cell_start + item['license'] + nl + body_cell_end)
            url_string = item['URL']
            #print(validators.url(item['URL']))
            #print("validators.url(item['URL']): {validators.url(item['URL'])}\n")
            if validators.url(item['URL']):
                url_string = (f"<a href={url_string}>{url_string}</a>")
            fout.write(body_cell_start + url_string + nl + body_cell_end)
            fout.write(body_cell_start + item['path'] + nl + body_cell_end)
            fout.write(row_end)

        fout.write(table_body_end)
        fout.write(table_end)



def create_libraries_table_md(libraries_table, libraries):
    """
    create a text file with a mark down table of the libraries.
    Inputs:
        libraries_table          The path and filename as a string
        libraries                The list of libraries as a list of dictionaries
    Outputs:
        None
    """
    now = time.strftime("%c")
    caption_text = (
                    f"**Libary Modules on Aire Table:** " \
                    f"This table of libraries was automatically created {now}."
    )


    with open(libraries_table, 'w', encoding="utf-8") as f_out:
        f_out.write("| **Name** | **Version** | **Summary** | **License** | **URL** | **Path** |\n")
        f_out.write("|:--------:|:-----------:|:-----------:|:-----------:|:-------:|:--------:|\n")
        for item in libraries:
            f_out.write(
                f"| {item['name']} "
                f"| {item['version']} "
                f"| {item['summary']} "
                f"| {item['license']} "
                f"| {item['URL']} "
                f"| {item['path']} |\n"
            )
        f_out.write(caption_text)


def check_item(item_dictionary):
    """
    Check to see if all the item_dictionary values which are items of the
    software module list are full and valid.
    Inputs:
        item_dictionary          The item as a string
    Outputs:
        int                      The number ofitems that are not valid in
                                 the item_dictionary
    """
    valid_score = 0
    #print(item_dictionary)
    for key in item_dictionary:
        if item_dictionary[key] == "":
            valid_score = valid_score + 1
    #print("valid_score: %s" % (valid_score))
    #print("valid_score: %s" % (valid_score))
    return valid_score

def check_line_add_to_software_list(line, software_item, next_item, last_item, index, software_list):
    """
    Check to see if the line given at the command line is valid.
    Inputs:
        String          The path as a string
    Outputs:
        None
    """
    #print(line)
    #print(item_dictionary)

    if "Title:" in line:
        # Title is the first item in the software item that first
        # in the module whatis output. We need a reash software_item
        # for the next item to be added to the list
        next_item = software_item.copy()
        next_item['title'] = (line.split(': '))[1].strip()
    if 'Name:' in line:
        next_item['name'] = (line.split(': '))[1].strip()
    if 'Version:' in line:
        next_item['version'] = (line.split(': '))[1].strip()
    if 'Summary:' in line:
        next_item['summary'] = (line.split(': '))[1].strip()
    if 'License:' in line:
        next_item['license'] = (line.split(': '))[1].strip()
    if 'URL:' in line:
        next_item['URL'] = (line.split(': '))[1].strip()
    if 'Package path:' in line:
        next_item['path'] = (line.split(': '))[1].strip()

    if check_item(next_item) == 0:
        #print("next_item: %s " % (next_item))
        #print(f"line: {line} ")
        if index > 0 and next_item != last_item:
            software_list.append(next_item)
            index = index + 1
            last_item = next_item.copy()
            next_item = software_item.copy()
        elif index == 0:
            software_list.append(next_item)
            index = index + 1
            last_item = next_item.copy()

    return (index, next_item, last_item, software_list)


def check_path(path_string):
    """
    Check to see if the path given at the command line is valid.
    Inputs:
        String          The path as a string
    Outputs:
        None
    """
    if os.path.isdir(path_string):
        print(f"Path {path_string} is valid.")
    else:
        sys.exit(f"Path {path_string} is an invalid value!!!")

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



def change_file_extension_add_date(file_path, new_extension):
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
    now = time.strftime("%Y-%m-%d")
    # Create the new file path with date in filename and the new extension
    new_file_path = f"{root}-{now}.{new_extension}"
    print(new_file_path)
    # Rename the file
    #os.rename(file_path, new_file_path)
    return new_file_path

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
    # Create the new file path with date in filename and the new extension
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
    print(f"host: {host}")

    # =============================================================================
    # These urls link to documentation pages for specific software on the arc
    # website.
    # I have used url rather than link as this is an overused word.
    # =============================================================================
    ## this bit is most likely redundant now.
    ## The module lisitng is now dividied into the sections, in order in the list;
    ## /opt/apps/etc/modulefiles/compilers
    ## /opt/apps/etc/modulefiles/libraries
    ## /opt/apps/etc/modulefiles/tools
    ## /opt/apps/etc/modulefiles/interpreters
    ## /opt/apps/etc/modulefiles/applications
    ##
    ##
    #f_urls = ["./urls/applications_urls.txt",
    #        "./urls/libraries_urls.txt",
    #        "./urls/compilers_urls.txt",
    #        "./urls/utilities_urls.txt"]

    #print(f_urls)

    #app_urls = []

    #for file in f_urls:
    #    with open(file, 'r', encoding="utf-8") as f_urls:
    #        for line in f_urls:
    #            i = line.count(',')
    #            print(line)
    #            if i == 1:
    #                app_name = (line.split(','))[0].strip()
    #                url = (line.split(','))[1].strip()
    #                arr=[app_name,url]
    #                app_urls.append(arr)




    # =============================================================================
    # These descriptions are created by a script that uses the "module whatis"
    # command.
    # =============================================================================

    #filename_desc = "./"+host+"/whatis_"+host+".txt"
    #filename_desc = "/home/jo/code_projects/examples/"+host+"/whatis_"+host+".txt"
    #filename_desc = "/home/jo/code_projects/examples/module_tables/modules_example.txt"
    filename_desc = "/home/jo/code_projects/examples/module_tables/modules-login2.aire.lee.alces.network-2025_04_30-09_58.txt"
    libraries_table = "/home/jo/code_projects/examples/module_tables/libraries_table.txt"
    libraries_table1 = "/home/jo/code_projects/examples/module_tables/libraries__table1.html"
    print(f"filename_desc: {filename_desc} \n")
    print("\n\n")


    #f_loc = r"/home/jo/code_projects/examples/"+host+".txt"
    #if not os.path.exists(f_loc):
    #    open(f_loc, 'w').close()


    #compilers = []
    libraries = []
    software_item = {"title": "",
                     "name": "",
                     "version": "",
                     "summary": "",
                     "license": "",
                     "URL": "",
                     "path": ""}
    libs = bool(False)
    #tools = []
    #interpreters = []
    #applications = []

    with open(filename_desc, encoding="utf-8") as f_in:
        last_app__name="    "
        app__name="    "
        next_item = software_item.copy()
        last_item = software_item.copy()
        index = 0
        for line in f_in:
            if libs:
                (index,
                 next_item,
                 last_item,
                 libraries) = check_line_add_to_software_list(line,
                                                                software_item,
                                                                next_item,
                                                                last_item,
                                                                index,
                                                                libraries)
                """if "Title:" in line:
                    # Title is the first item in the software item that first
                    # in the module whatis output. We need a reash software_item
                    # for the next item to be added to the list
                    next_item = software_item.copy()
                    next_item['title'] = (line.split(': '))[1].strip()
                if 'Name:' in line:
                    next_item['name'] = (line.split(': '))[1].strip()
                if 'Version:' in line:
                    next_item['version'] = (line.split(': '))[1].strip()
                if 'Summary:' in line:
                    next_item['summary'] = (line.split(': '))[1].strip()
                if 'License:' in line:
                    next_item['license'] = (line.split(': '))[1].strip()
                if 'URL:' in line:
                    next_item['URL'] = (line.split(': '))[1].strip()
                if 'Package path:' in line:
                    next_item['path'] = (line.split(': '))[1].strip()

                if check_item(next_item) == 0:
                    print("next_item: %s " % (next_item))
                    print(f"line: {line} ")
                    if item > 0 and next_item != last_item:
                        libraries.append(next_item)
                        item = item + 1
                        last_item = next_item.copy()
                        next_item = software_item.copy()
                    elif item == 0:
                        libraries.append(next_item)
                        item = item + 1
                        last_item = next_item.copy()"""
            if '--- /opt/apps/etc/modulefiles/libraries' in line:
                print("started libaries")
                libs = True
            if '--- /opt/apps/etc/modulefiles/tools' in line and libs:
                break
        f_in.close()

    print("\n\nLIBRARIES\n\n")

    for index, item in enumerate(libraries):
        print(f"{index} {item} \n")

    create_libraries_table_md(libraries_table, libraries)

    create_libraries_table_html(libraries_table1, libraries)





    descriptions = []

    with open(filename_desc, encoding="utf-8") as f_in:
        last_app__name="    "
        app__name="    "
        for line in f_in:
            if '--- /opt/apps/etc/modulefiles/' in line:
                print(line)
            i = line.count(':')
            #print("%d: %s \n" % (i, line))
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

    print(len(descriptions))


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
