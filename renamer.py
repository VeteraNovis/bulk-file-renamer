#
# When executed this program will check the name of each file and folder in
# a specified directory, and rename any folder or filenames that are invalid
# with respect to Microsoft OneDrive. The purpose of this script is to bulk
# rename files that are causing upload errors effortlessly.
#

# Python 2/3 compatibility
from __future__ import print_function
from builtins import input

import os  # To navigate the file system
import shutil  # To rename the files and folders
import sys
from datetime import datetime  # For generating the logfile


def checkExtension(fName):
    """Determine whether a given string ends with a specific file extension.

    If the input ends with an extension that is included in extList.txt, the
    function will return the filename and the extension.

    If the input has no file extension, or the extension is not included in
    extList.txt, the function will return the original filename, and an empty
    string.

    >>> checkExtension("test.txt")
    ('test', '.txt')
    >>> checkExtension("test.dll")
    ('test.dll', '')
    >>> checkExtension("test")
    ('test', '')

    """

    # Import list of file extensions from extList.txt
    with open("extList.txt", 'r') as extFile:
        extList = extFile.read().split('\n')

    # Determine whether filename has a listed extension
    if fName.endswith(tuple(extList)):
        fName, fExt = os.path.splitext(fName)[0], os.path.splitext(fName)[1]
        return fName, fExt

    else:
        fExt = ""

    return fName, fExt


def checkRestricted(Name):
    # List of restricted filenames
    rNames = [
        'AUX', 'PRN', 'NUL', 'CON', 'COM0', 'COM1', 'COM2', 'COM3', 'COM4',
        'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT0', 'LPT1', 'LPT2', 'LPT3',
        'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9', '.lock', 'desktop.ini',
        '_vti_'
    ]

    if Name in rNames:
        Name = Name + "-renamed"

    # Replacing or deleting restricted characters
    rChars = [['?', ''], ['*', ''], ['<', ''],
              ['>', ''], ['|', ''], [r':', '-']]
    for entry in rChars:
        Name = Name.replace(entry[0], entry[1])

    return Name


def cleanFilename(Name, Num):
    """ This function will attempt to remove or change any restricted characters
    in a filename or directory name.  Where Num keeps track of
    """
    Name = checkRestricted(Name)  # Fixes any invalid filenames
    Name = Name.strip()  # Removes any whitespace from the filename
    if Name.endswith("."):
        Name = Name[:-1]  # Removes periods from end of filename.

    # A check to ensure names are not renamed to be blank
    if len(Name) < 1:
        Name = "unnamed" + str(Num)
        Num += 1

    return Name, Num


def rename(root, oldName, newName, outputLog, fType, dupNum, logOnly):
    pathToFile = root + "/"
    oldPath, newPath = pathToFile + oldName, pathToFile + newName
    timestamp = str(datetime.now())[:-3].replace(" ", ", ")

    if oldPath == newPath:
        outputLog.append(timestamp + ", ---, " + pathToFile.replace(",", "-")
                         + ", {" + oldName.replace(",", "-") + "}, -->, "
                         + "---, " + fType)
    else:
        if os.path.exists(newPath):
            newPath = newPath + str(dupNum)
            dupNum += 1

        if logOnly is True:
            outputLog.append(timestamp + ", +++, "
                             + pathToFile.replace(",", "-")
                             + ", {" + oldName.replace(",", "-") + "}, -->, {"
                             + newName.replace(",", "-") + "}, " + fType)
        else:
            shutil.move(oldPath, newPath)
            outputLog.append(timestamp + ", +++, "
                             + pathToFile.replace(",", "-")
                             + ", {" + oldName.replace(",", "-")
                             + "}, -->, {" + newName.replace(",", "-")
                             + "}, " + fType)

    return


def getPath():
    # Stores the absolute path name to the specified directory.
    shift = 0
    logOnly = True

    # Determine whether files will be renamed, or just listed in the logfile.
    if sys.argv[-1] == "rename":
        logOnly = False
        shift = 1

    if len(sys.argv) == 1 + shift:
        PATH = os.path.dirname(os.path.abspath(__file__))

    # Allow user defined path, and checks for relative paths
    elif len(sys.argv) == 2 + shift:
        PATH = sys.argv[1]

        if PATH.startswith("."):
            print("Relative paths will not work.  Please use full pathnames")
            exit()

        if PATH.endswith("/"):
            PATH = PATH[:-1]

    # If too many arguments are entered, quit the program
    else:
        print("Multiple arguments found, expecting single argument.\n")
        exit()

    if logOnly is True:
        print("\nLOG ONLY ENABLED")
        print("Renaming files in directory {}".format(PATH))

    else:
        print("\nRenaming files in directory {}".format(PATH))

    # Provide the option to quit the program
    cont = str(input("CONFIRM PATH BEFORE CONTINUING... To quit press Q: "))
    if cont.lower() == "q":
        exit()

    return PATH, logOnly


def main():
    """ Main function to check for incorrectly named files/folders
    and rename them
    """

    # Initialising variables
    PATH, logOnly = getPath()
    fileNum = 1
    dupNum = 1
    renamed = False
    outputLog = []

    for root, dirs, files in os.walk(PATH, topdown=False):
        for f in files:
            # Ignore hidden files
            if f.startswith("."):
                continue

            else:
                # Separate filename from extension if valid extension exists
                fName, fExt = checkExtension(f)

                # Run the function to clean the filename
                fName, fileNum = cleanFilename(fName, fileNum)

                # Recombine the file name and extension
                fName = fName + fExt

                # Logs output, changes name if required
                rename(root, f, fName, outputLog, "file", dupNum, logOnly)

        # Cycle through any directories in the current folder and rename
        for dr in dirs:
            dName, fileNum = cleanFilename(dr, fileNum)
            rename(root, dr, dName, outputLog, "dir", dupNum, logOnly)

    # Create or open logfile.csv and store the output of the script
    with open("logfile.csv", "w") as logfile:
        for line in outputLog:
            logfile.write(line + "\n")

    # Check through the logfile for the files that were changed
    with open("logfile.csv", "r") as logfile:
        output = logfile.readlines()
        for line in output:
            line = line.split(", ")
            if line[2] == "+++":
                print("{} {} was renamed to {}".format(line[7].strip(),
                                                       line[4], line[6]))
                renamed = True

        if renamed is False:
            print("No files or folders were renamed\n")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    exit()
    main()
