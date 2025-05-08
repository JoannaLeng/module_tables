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
import os
import sys
import argparse
import validators

def create_category_table_html(path_out, catergory_software_list, category_name):
    """
    create a text file with a html table of the software in the catergory_software_list.
    Inputs:
        path_out                 The path and filename as a string
        catergory_software_list  The list of software in the named category
                                 as a list of dictionaries
        category_name            The name of the category as a string
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
                f"\t\t<b>{category_name} Modules on Aire Table:</b> "
                f"This table of {category_name} was automatically created {now}.\n"
                )



    #sp = ' '
    nl = '\n'

    tables = change_file_extension_add_date(path_out, "html")

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


def check_item(item_dictionary, strength):
    """
    Check to see if all the item_dictionary values which are items of the
    software module list are full and valid.
    Inputs:
        item_dictionary          The software item as a dictionary
        strength                 The strength of the checking test as an int
                                 0 is for a basic check of the item
                                 1 is for a full check of the item
    Outputs:
        int                      The number of items that are not valid in
                                 the item_dictionary, 0 is a valid score
    """
    valid_score = 0
    best_score = len(item_dictionary)
    #print(item_dictionary)
    #library item tend to have all the values set so use strength 1
    if strength == 1:
        for key in item_dictionary:
            if item_dictionary[key] == "":
                valid_score = valid_score + 1
    # tools tend to have just title and summary set so use strength 0
    if strength == 0:
        for key in item_dictionary:
            if key != "title" and key != "summary":
                if item_dictionary[key] == "":
                    valid_score = valid_score + 1
    #print("valid_score: %s" % (valid_score))
    print("valid_score: %s" % (valid_score))
    return valid_score

def check_item_at_item_end(software_item):
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
                note_start = "title is not set!,"
            elif software_item[key] != "":
                note_start = (f"Title: {software_item[key]}, ")
        if software_item[key] == "":
            valid_score = valid_score + 1
            note_details = (note_details+f" {key} is not set,")
    #print("valid_score: %s" % (valid_score))
    log_notes = (note_start+f"score: {valid_score}, "+note_details)
    print(f"log_notes: {log_notes}")
    return log_notes


def check_line_add_to_software_list(line,
                                    software_item,
                                    next_item,
                                    last_item,
                                    index,
                                    software_list):
    """
    Check to see if the line given at the command line is valid.
    Inputs:
        line            A line from the input file as a string
        software_item   A software item as a dictionary
        next_item       The next software item as a dictionary
        last_item       The last software item as a dictionary
        index           The index of the software item in the list
        software_list   The list of software items as a list of dictionaries
        strength        The strength of the checking test as an int
                         0 is for a basic check of the item
                         1 is for a full check of the item
    Outputs:
        index           Updated index of the software item in the list
        next_item       Updated next software item as a dictionary
        last_item       Updated last and last software items as dictionaries
        software_list   Updated list of software items as a list of dictionaries
    """
    #print(f"1, line: {line}\n")
    #print(f"2, last_item: {last_item}\n")
    #print(f"3, next_item: {next_item}\n")
    #print(f"4, index: {index}\n")

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

    if 'module help' in line:
        check_item_at_item_end(next_item)
        #print("item checked: next_item: {next_item} ")
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

    #print(f"4, last_item: {last_item}\n")
    #print(f"5, next_item: {next_item}\n")
    #print(f"6, index: {index}\n")
    #print(f"7, software_list: {software_list}\n")


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

    """
    if args.LES_path_out is not None:
        path_out=args.LES_path_out+r"//"+resultsdir
    if args.LES_path_out is None:
        path_out=path_in+r"//"+resultsdir
    os.makedirs(path_out)

    path_out = check_path(args.path_out)

    if args.file_in is None:
    if os.path.split(args.geom_file_name)[0] == '':
        sys.exit("ERROR; There is no geometry file provided")
    elif os.path.split(args.geom_file_name)[0] != '':
        geom_files_dir=os.path.split(args.geom_file_name)[0]
    """


    # =============================================================================
    # The descriptions in the input file are created by a script that uses the
    # "module whatis" command.
    # =============================================================================

    #filename_desc = "./"+host+"/whatis_"+host+".txt"
    #filename_desc = "/home/jo/code_projects/examples/"+host+"/whatis_"+host+".txt"
    #filename_desc = "/home/jo/code_projects/examples/module_tables/modules_example.txt"

    file_in = os.path.abspath(file_in)
    print(f"file_in: {file_in} \n")

    #results_file_name = "module_table"
    #change_file_extension_add_date(libraries_table, "html")

    file_out = os.path.abspath(path_out)+r"/modules_table"


    #filename_in = "/home/jo/code_projects/examples/module_tables/modules-login2.aire.lee.alces.network-2025_04_30-09_58.txt"
    filename_in = file_in
    libraries_table = "/home/jo/code_projects/examples/module_tables/libraries_table.txt"
    libraries_table1 = "/home/jo/code_projects/examples/module_tables/libraries__table1.html"
    print(f"filename_in: {filename_in} \n")
    print("\n\n")


    #f_loc = r"/home/jo/code_projects/examples/"+host+".txt"
    #if not os.path.exists(f_loc):
    #    open(f_loc, 'w').close()


    #compilers = []
    libraries = []
    tools = []
    software_item = {"title": "",
                     "name": "",
                     "version": "",
                     "summary": "",
                     "license": "",
                     "URL": "",
                     "path": ""}
    compilers_flag = bool(False)
    libraries_flag = bool(False)
    tools_flag = False
    interpreters_flag = False
    applications_flag = False
    #libs = bool(False)
    #tools = []
    #interpreters = []
    #applications = []

    with open(filename_in, encoding="utf-8") as f_in:
        last_app__name="    "
        app__name="    "
        next_item = software_item.copy()
        last_item = software_item.copy()
        index_libraries = 0
        index_tools = 0
        index = 0
        #next_tools_item = software_item.copy()
        #last_tools_item = software_item.copy()
        #first_time = False
        for line in f_in:
            #print(f"{index}: libraries_flag: {libraries_flag}  tools_flag: {tools_flag}  "
            #       f"compilers_flag: {compilers_flag}  interpreters_flag: {interpreters_flag}  "
            #       f"applications_flag: {applications_flag}")
            index = index+1
            if '--- /opt/apps/etc/modulefiles/compilers' in line:
                print("started reading compilers")
                compilers_flag = True
                libraries_flag = False
                tools_flag = False
                interpreters_flag = False
                applications_flag = False
                next_item = software_item.copy()
                last_item = software_item.copy()
            if '--- /opt/apps/etc/modulefiles/libraries' in line:
                print("started reading libaries")
                libraries_flag = True
                compilers_flag = False
                tools_flag = False
                interpreters_flag = False
                applications_flag = False
                next_item = software_item.copy()
                last_item = software_item.copy()
            if '--- /opt/apps/etc/modulefiles/tools' in line:
                print("started reading tools")
                tools_flag = True
                compilers_flag = False
                libraries_flag = False
                interpreters_flag = False
                applications_flag = False
                next_item = software_item.copy()
                last_item = software_item.copy()
            if '--- /opt/apps/etc/modulefiles/interpreters' in line:
                print("started reading interpreters")
                interpreters_flag = True
                compilers_flag = False
                libraries_flag = False
                tools_flag = False
                applications_flag = False
                next_item = software_item.copy()
                last_item = software_item.copy()
            if '--- /opt/apps/etc/modulefiles/applications' in line:
                print("started reading applications")
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
                                                                libraries)
            if tools_flag and not libraries_flag and not compilers_flag and not interpreters_flag and not applications_flag:
                #print(f"tools_flag: {tools_flag} in tools")
                #print(line)
                (index_tools,
                 next_item,
                 last_item,
                 tools) = check_line_add_to_software_list(line,
                                                            software_item,
                                                            next_item,
                                                            last_item,
                                                            index_tools,
                                                            tools)

            if '--- /opt/apps/etc/modulefiles/compilers' in line:
                print("started reading compilers")
                compilers_flag = True
                libraries_flag = False
                tools_flag = False
                interpreters_flag = False
                applications_flag = False
            if '--- /opt/apps/etc/modulefiles/libraries' in line:
                print("started reading libaries")
                libraries_flag = True
                compilers_flag = False
                tools_flag = False
                interpreters_flag = False
                applications_flag = False
            if '--- /opt/apps/etc/modulefiles/tools' in line:
                print("started reading tools")
                tools_flag = True
                compilers_flag = False
                libraries_flag = False
                interpreters_flag = False
                applications_flag = False
            if '--- /opt/apps/etc/modulefiles/interpreters' in line:
                print("started reading interpreters")
                interpreters_flag = True
                compilers_flag = False
                libraries_flag = False
                tools_flag = False
                applications_flag = False
            if '--- /opt/apps/etc/modulefiles/applications' in line:
                print("started reading applications")
                applications_flag = True
                compilers_flag = False
                libraries_flag = False
                tools_flag = False
                interpreters_flag = False
        f_in.close()

    print("\n\nLIBRARIES\n\n")

    for index, item in enumerate(tools):
        print(f"{index} {item} \n")

    print(f"len(tools): {len(tools)}\n")

    if format == 1:
        print("format 1")
        if len(libraries) > 0:
            print(f"len(libraries): {len(libraries)}")
            libraries_out = file_out+r"_libraries"
            print(f"libraries_out: {libraries_out}")
            create_category_table_html(libraries_out, libraries, "Libraries")
        elif len(libraries) == 0:
            print(f"len(libraries): {len(libraries)}")
            print(f"No libraries found in {filename_in}")

        if len(tools) > 0:
            print(f"len(tools): {len(tools)}")
            tools_out = file_out+r"_tools"
            print(f"tools_out: {tools_out}")
            create_category_table_html(tools_out, tools, "Tools")
        elif len(libraries) == 0:
            print(f"len(tools): {len(tools)}")
            print(f"No tools found in {filename_in}")
    elif format == 2:
        print("format 2")
        create_libraries_table_md(libraries_table, libraries)
    elif format == 3:
        print("format 3")
        print("format 3 is being created\n.")

    #create_libraries_table_md(libraries_table, libraries)

    #create_libraries_table_html(libraries_table1, libraries)





    descriptions = []

    with open(filename_in, encoding="utf-8") as f_in:
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

    tables = change_file_extension(filename_in, "html")

    with open(filename_in, 'r', encoding="utf-8") as fin:
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
