# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Oct  2 16:35:03 2017

Copyright (c) Joanna Leng in 2017.

This is a script that runs on a Linux system that uses modules to allow
users to access software and creates a table in mark down that can be
copied and pasted into a word press webpage.

Execute as:
    python module_avail_html_table.py

@author: menjle - Joanna Leng - j.leng@leeds.ac.uk
"""

import re
import time
import os
import sys
import argparse
import validators

def create_category_table_html(path_out, catergory_software_list, category_name, log_file):
    """
    create a text file with a html table of the software in the catergory_software_list.
    Inputs:
        path_out                 The path and filename as a string
        catergory_software_list  The list of software in the named category
                                 as a list of dictionaries
        category_name            The name of the category as a string
        log_file                 The log file as a file object
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
    category_name = category_name.replace(category_name[0], category_name[0].upper(), 1)
    caption = (
                f"\t\t<b>{category_name} Modules on Aire Table:</b> "
                f"This table of {category_name} was automatically created {now}.\n"
                )



    #sp = ' '
    nl = '\n'

    tables = change_file_extension_add_date(path_out, "html")

    print(f"\n\nCreating table file for {category_name} in {tables}\n")
    log_file.write(f"\n\nCreating table file for {category_name} in {tables}\n")

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

        for item in catergory_software_list:
            fout.write(row_start)
            fout.write(body_cell_start + item['title'] + nl + body_cell_end)
            fout.write(body_cell_start + item['version'] + nl + body_cell_end)
            fout.write(body_cell_start + item['summary'] + nl + body_cell_end)
            fout.write(body_cell_start + item['license'] + nl + body_cell_end)
            url_string = item['URL']
            #print(validators.url(item['URL']))
            #print("validators.url(item['URL']): {validators.url(item['URL'])}\n")
            if validators.url(item['URL']):
                url_string = (f"<a href={url_string}>{url_string}</a>")
            else:
                log_file.write(f"WARNING: the software with title: {item['title']}"
                               f" the URL: {item['URL']} is not a valid URL\n")
            fout.write(body_cell_start + url_string + nl + body_cell_end)
            fout.write(body_cell_start + item['path'] + nl + body_cell_end)
            fout.write(row_end)

        fout.write(table_body_end)
        fout.write(table_end)
        fout.close()



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
        f_out.write("| **Title** | **Version** | **Summary** | **License** | **URL** | **Path** |\n")
        f_out.write("|:--------:|:-----------:|:-----------:|:-----------:|:-------:|:--------:|\n")
        for item in libraries:
            f_out.write(
                f"| {item['title']} "
                f"| {item['version']} "
                f"| {item['summary']} "
                f"| {item['license']} "
                f"| {item['URL']} "
                f"| {item['path']} |\n"
            )
        f_out.write(caption_text)


def check_item_at_item_end(software_item, log_file):
    """
    Check to see which of the values in the software_item dictionary are set and valid.
    Inputs:
        software_item           The software item as a dictionary
    Outputs:
        log_notes               The items that are not set in the software_item
                                as a string.
    """
    valid_score = 0
    #print(software_item)
    note_start = ""
    note_details = ""
    for key in software_item:
        if key == "title":
            if software_item[key] == "":
                note_start = "Title is not set!, "
            else:
                note_start = (f"Title: {software_item[key]}, ")
        if software_item[key] == "":
            valid_score = valid_score + 1
            note_details = (note_details+f" {key} is not set,")

    if note_details.endswith(','):
        note_details = note_details[:-1]

    log_notes = (note_start+f"score: {valid_score}\n  "+note_details+"\n")
    log_file.write(log_notes)
    if valid_score > 0:
        print(f"\nWARNING: {software_item['title']} is not set fully")
        print(note_details)
    #print(f"log_notes: {log_notes}")
    return log_notes


def check_line_add_to_software_list(line,
                                    software_item,
                                    next_item,
                                    last_item,
                                    index,
                                    software_list,
                                    log_file):
    """
    Check to see if the line given at the command line is valid.
    Inputs:
        line            A line from the input file as a string
        software_item   A software item as a dictionary
        next_item       The next software item as a dictionary
        last_item       The last software item as a dictionary
        index           The index of the software item in the list
        software_list   The list of software items as a list of dictionaries
        log_file        The log file as a file object
    Outputs:
        index           Updated index of the software item in the list
        next_item       Updated next software item as a dictionary
        last_item       Updated last and last software items as dictionaries
        software_list   Updated list of software items as a list of dictionaries
    """

    if "Title:" in line:
        # Title is the first item in the software item that first
        # in the module whatis output. We need a read software_item
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

    if 'module help' in line:
        check_item_at_item_end(next_item, log_file)

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

    return path_string


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
    #print(root)
    now = time.strftime("%Y-%m-%d")
    # Create the new file path with date in filename and the new extension
    new_file_path = f"{root}-{now}.{new_extension}"
    #print(new_file_path)
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

def format_1_controller(software_list, file_in, file_out, category_name, log_file):
    """
    This function controls the format 1 optoion which is to create a
    html table for each category of software.
    Inputs:
        software_list       The list of software items as a list of dictionaries
        file_in             The input file as a string
        file_out            The output file as a string
        category_name       The name of the category as a string
    Outputs:
        None
    """

    print("\n\n"+category_name.upper()+"\n")

    if len(software_list) > 0:
        print(f"len(software_list): {len(software_list)}\n")
        software_list_out = file_out+r"_"+category_name
        for index, item in enumerate(software_list):
           print(f"{index} {item} \n")
        #print(f"\nsoftware_list_out: {software_list_out}")
        create_category_table_html(software_list_out, software_list, category_name, log_file)
    elif len(software_list) == 0:
        print(f"len(software_list): {len(software_list)}")
        print(f"No {category_name} found in {file_in}\n")

    return None

def start_log_file(log_file):
    """
    Start the log file with the date and time.
    Inputs:
        log_file       The path and filename as a string
    Outputs:
        log_file       The log file with the date and time as a string
    """
    now = time.strftime("%c")
    host = os.uname()[1]
    log_file.write(f"\nLog file for module_tables created on {now} on {host}\n\n")
    log_file.write("This log gives information on the resulting tables.\n")
    log_file.write("A score of 0 for a software item means the 5 elements of the table "
                   "were set in modules. An integer value of 1 is added to zero for each "
                   "missing element")
    return log_file


def parse_arguments():
    """
    Handles the command line flags/args.
    """
    parser = argparse.ArgumentParser(
        description="""This is a script that runs on a Linux system that uses modules to allow
                        users to access software and creates a table in mark down that can be
                        copied and pasted into a word press webpage."""
    )



    parser.add_argument("-i",
                        "--in",
                        type=str,
                        dest="file_in",
                        metavar="FILE_IN",
                        #action="store",
                        required=True,
                        help=("Text file to process must be provided with the content of "
                              "the command \'module whatis << module_listing.txt\'. "
                              "See README for details of adding with hostname and date "
                              "to the filename.")
                        )

    parser.add_argument("-o",
                        "--out",
                        type=str,
                        default=os.getcwd(),
                        dest="path_out",
                        metavar="PATH_OUT",
                        #action="store",
                        required=False,
                        help="Path for output files, default is HOME."
                        )

    parser.add_argument("-f",
                        "--format",
                        type=int,
                        default=1,
                        choices=[1, 2, 3],
                        #dest="formating",
                        metavar="FORMAT",
                        #action="store",
                        required=False,
                        help=("Format for the output file: "
                              "1 is for html long table for each catergory; "
                              "2 is for html table for each module; "
                              "and 3 is for a markdown table for each category.")
                        )

    return parser.parse_args()





def main():
    """
    The main funtion does the work: it exectutes the module commands and formats the
    output of that.
    """
    args = parse_arguments()

    print("\nmodule_tables is executing\n\n")

    #file_in = ""
    #path_out = ""
    #format = 1

    if args.file_in is not None:
        file_in = args.file_in
        print(f"file_in: {file_in}")
    if args.file_in is None:
        sys.exit("ERROR; There is no input file provided")
    if args.path_out is not None:
        path_out = args.path_out
        print(f"path_out: {path_out}")
    if args.path_out is None:
        path_out = os.getcwd()
        print(f"path_out: {path_out}")
    if args.format is not None:
        format = args.format
        print(f"format: {format}")
    if args.format is None:
        sys.exit("ERROR; There is no format provided")
    if args.format not in [1, 2, 3]:
        sys.exit("ERROR; The format provided is not valid")

    print("\n\n")

    # =============================================================================
    # File handling admin - setting paths, names etc.
    # =============================================================================

    log_file_filename = (os.path.abspath(path_out)+r"/modules_table_log-"+time.strftime("%Y-%m-%d")+r"log.txt")

    log_file = open(log_file_filename, 'w', encoding="utf-8")
    start_log_file(log_file)

    file_in = os.path.abspath(file_in)
    log_file.write(f"\n\nfile_in: {file_in} \n")

    file_out = os.path.abspath(path_out)+r"/modules_table"
    log_file.write(f"file_out: {file_out} \n")

    log_file.write(f"format: {format} \n")



    #f_loc = r"/home/jo/code_projects/examples/"+host+".txt"
    #if not os.path.exists(f_loc):
    #    open(f_loc, 'w').close()


    # =============================================================================
    # The descriptions in the input file are created by a script that uses the
    # "module whatis" command.
    # =============================================================================

    compilers = []
    libraries = []
    tools = []
    interpreters = []
    applications = []
    software_item = {"title": "",
                     "name": "",
                     "version": "",
                     "summary": "",
                     "license": "",
                     "URL": "",
                     "path": ""}
    compilers_flag = bool(False)
    libraries_flag = bool(False)
    tools_flag = bool(False)
    interpreters_flag = bool(False)
    applications_flag = bool(False)

    index_libraries = 0
    index_tools = 0
    index_interpreters = 0
    index_applications = 0
    index = 0



    with open(file_in, encoding="utf-8") as f_in:
        next_item = software_item.copy()
        last_item = software_item.copy()
        for line in f_in:
            #print(f"{index}: libraries_flag: {libraries_flag}  tools_flag: {tools_flag}  "
            #       f"compilers_flag: {compilers_flag}  interpreters_flag: {interpreters_flag}  "
            #       f"applications_flag: {applications_flag}")
            index = index+1
            if '--- /opt/apps/etc/modulefiles/compilers' in line:
                print("\n\nREADING COMPILERS:\n")
                log_file.write("\nReading compilers:\n")
                compilers_flag = True
                libraries_flag = False
                tools_flag = False
                interpreters_flag = False
                applications_flag = False
                next_item = software_item.copy()
                last_item = software_item.copy()
            if '--- /opt/apps/etc/modulefiles/libraries' in line:
                print("\n\nREADING LIBRARIES\n")
                log_file.write("\nReading libraries:\n")
                libraries_flag = True
                compilers_flag = False
                tools_flag = False
                interpreters_flag = False
                applications_flag = False
                next_item = software_item.copy()
                last_item = software_item.copy()
            if '--- /opt/apps/etc/modulefiles/tools' in line:
                print("\n\nREADING TOOLS\n")
                log_file.write("\nReading tools:\n")
                tools_flag = True
                compilers_flag = False
                libraries_flag = False
                interpreters_flag = False
                applications_flag = False
                next_item = software_item.copy()
                last_item = software_item.copy()
            if '--- /opt/apps/etc/modulefiles/interpreters' in line:
                print("\n\nREADING INTERPRETERS\n")
                log_file.write("\nReading interpreters:\n")
                interpreters_flag = True
                compilers_flag = False
                libraries_flag = False
                tools_flag = False
                applications_flag = False
                next_item = software_item.copy()
                last_item = software_item.copy()
            if '--- /opt/apps/etc/modulefiles/applications' in line:
                print("\n\nREADING APPLICATIONS\n")
                log_file.write("\nReading applications:\n")
                applications_flag = True
                compilers_flag = False
                libraries_flag = False
                tools_flag = False
                interpreters_flag = False
                next_item = software_item.copy()
                last_item = software_item.copy()
            if libraries_flag:
                (index_libraries,
                 next_item,
                 last_item,
                 libraries) = check_line_add_to_software_list(line,
                                                                software_item,
                                                                next_item,
                                                                last_item,
                                                                index_libraries,
                                                                libraries,
                                                                log_file)
            if tools_flag:
                (index_tools,
                 next_item,
                 last_item,
                 tools) = check_line_add_to_software_list(line,
                                                            software_item,
                                                            next_item,
                                                            last_item,
                                                            index_tools,
                                                            tools,
                                                            log_file)
            if interpreters_flag:
                (index_interpreters,
                 next_item,
                 last_item,
                 interpreters) = check_line_add_to_software_list(line,
                                                            software_item,
                                                            next_item,
                                                            last_item,
                                                            index_interpreters,
                                                            interpreters,
                                                            log_file)
            if applications_flag:
                (index_applications,
                 next_item,
                 last_item,
                 applications) = check_line_add_to_software_list(line,
                                                            software_item,
                                                            next_item,
                                                            last_item,
                                                            index_applications,
                                                            applications,
                                                            log_file)
        f_in.close()


    if format == 1:
        print("format 1")
        format_1_controller(libraries, file_in, file_out, "libraries", log_file)
        format_1_controller(tools, file_in, file_out, "tools", log_file)
        format_1_controller(interpreters, file_in, file_out, "interpreters", log_file)
        format_1_controller(applications, file_in, file_out, "applications", log_file)

    elif format == 2:
        print("format 2")
        create_libraries_table_md(libraries_table, libraries)
    elif format == 3:
        print("format 3")
        print("format 3 is being created\n.")

    #create_libraries_table_md(libraries_table, libraries)

    #create_libraries_table_html(libraries_table1, libraries)





    descriptions = []

    with open(file_in, encoding="utf-8") as f_in:
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

    tables = change_file_extension(file_in, "html")

    with open(file_in, 'r', encoding="utf-8") as fin:
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


            log_file.close()

if __name__ == "__main__":
    main()
