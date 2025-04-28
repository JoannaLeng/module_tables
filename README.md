## Module Table Readme
============
This project is designed to help with web documentation of Linux systems that use modules to allow users to access software. 

It was started on 2/10/2017 as a github repository.

## Table of Contents
=================

1. [Module Table Readme](#module-table-readme)
2. [Table of Content](#table-of-content)
3. [Version](#version)
4. [Module Table Description](#module-table-description)
5. [Copyright and License](#copyright-and-license)
6. [DEVELOPMENT ENVIRONMENT](#development-environment)




## VERSION
==========

This is version 2.0

## Module Table Description
===========================
This project is designed to help with web documentation of Linux systems that use modules to allow users to access software.

It creates a web-formatted table of each module category or of all the modules categories in mark down language or in html that can be copied and pasted into a webpage. For cybersecurity reasons it is best not to integrate this into the webpage so it is a semi-automated process.

## Copyright and License
========================
Copyright (c) Feb 2018 by Dr Joanna Leng.

Module Table is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Module Table is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Module Table, it is in the file named COPYING.  If not, see <http://www.gnu.org/licenses/>.

To help us, we ask that you cite the research papers on the package.

https://github.com/JoannaLeng/module_tables/

## DEVELOPMENT ENVIRONMENT:
==========================
Version 2 was developed using Python 3.11 and Anaconda, miniforge, on a virtualized Ubuntu 24.04.2 system on a Windows 11 using WSL, Windows subsystem for Linux.

# QUICK START:
===============
Immediately below are a set of instructions that allow you to execute the module table software quickly. There are no explanations of the steps here. Please look at the rest of the README file if you have any problems.

This software uses Anaconda, miniforge, with Python 3 so you will need to install and open an Anaconda shell. Once that is open, move to the top directory of cpt (the directory with the file README.md in it) and type the following the FIRST time you run the cpt software. Not all the instructions are required for later runs:

`conda env create -f env_module_table.yml`

Next, activate the cpt Anaconda environment using the following command:

`conda activate env-module-table`

Now install the module table tools into the module table environment:

pip install --editable . -v


Execution of scripts is in this format.

`average.py`

And to get help on how to use a script:

`module_avail_html_table --help`

If you want to use them to write your own python scripts you can now import them into a script.

`import mt`

# CREATING MODULE INFO FILE:
============================
It is best practice not to run a webserver on an HPC service machine and pass information automatically between them as it can cause cybersecurity issues. This is why the process of creating these tables is semi-automated rather than fully -automated.

Create a text file with information about the software modules using the command:

`module whatis >> module_listing-$(hostname)-$(date +%Y_%m_%d-%H_%M).txt`

Using the `$(hostname)` puts the name of the system in the filename and `(date +%Y_%m_%d-%H_%M)` the date and time in the filename. This makes it easier to manage the files and this information is used in the table caption, although the script will still execute and create tables without this information but the user will not know when the table was last updated. 

# MANAGING THE Module Table ENVIRONMENT:
=======================================
The Anaconda environment, with all the necessary modules, can be set up using the *env_module_table.yml* file. 

To see what conda environments you have, run the command

`conda env list`

To create a new Anaconda environment for cpt, run the command

`conda env create -f env_module_table.yml`

To start using the environment, run the command

`conda activate env-module-tool`

To stop using that environment:

`conda deactivate`

To remove the environment, if you no longer want to use cpt:

`conda remove --name env-module-table --all`

# USAGE: (#Usage)
This will be added when development is complete.

# ACKNOWLEDGEMENT:

This project was created for the ARC service at the University of Leeds and they funded the time needed to do this.
