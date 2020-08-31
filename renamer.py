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


def getPath(flags):
    """ Get starting directory for file renaming"""
    # Get path to the location of this python script
    workingDir = os.path.dirname(os.path.abspath(__file__))
    print(workingDir)

    # If there is no path given, set PATH to location of this file
    if len(sys.argv) == 1 + flags:
        PATH = workingDir

    # Allow user defined path, and checks for relative paths
    elif len(sys.argv) == 2 + flags:
        PATH = sys.argv[1]

        # Add code to convert relative path to absolute path
        if PATH.startswith("."):
            pass

        # Removes trailing slashes
        if PATH.endswith("/"):
            PATH = PATH[:-1]

    # If too many arguments are entered, quit the program
    elif len(sys.argv) > 2 + flags:
        print("\nToo many arguments. Exiting program.\n")
        exit()

    print("\nRenaming files in directory {}".format(PATH))

    # Provide the option to quit the program
    cont = str(input("CONFIRM PATH BEFORE CONTINUING... To quit press Q: "))
    if cont.lower() == "q":
        exit()

    return PATH


def cleanFilename(fName, fNum):
    """ This function will attempt to remove or change any restricted characters
    in a filename or directory name.  Where Num keeps track of
    """
    fName, fExt = checkExtension(fName)  # Separate filename from extension
    fName = checkRestricted(fName)  # Fixes any invalid filenames
    fName = fName.strip()  # Removes any whitespace from the filename

    # Removes any periods from the end of the file name
    while True:
        if fName.endswith("."):
            fName = fName[:-1]
        else:
            break

    # A check to ensure names are not renamed to be blank
    if len(fName) < 1:
        fName = "unnamed" + str(fNum)
        fNum += 1

    # Add extension if present
    fName = fName + fExt

    return fName, fNum


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


def checkRestricted(fName):
    # List of restricted filenames
    rNames = [
        'AUX', 'PRN', 'NUL', 'CON', 'COM0', 'COM1', 'COM2', 'COM3', 'COM4',
        'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT0', 'LPT1', 'LPT2', 'LPT3',
        'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9', '.lock', 'desktop.ini',
        '_vti_'
    ]

    if fName in rNames or '_vti_' in fName:
        fName = fName + "-renamed"

    # Replacing or deleting restricted characters
    rChars = [['?', ''], ['*', ''], ['<', ''],
              ['>', ''], ['|', ''], [r':', '-'],
              ['\"', '\''], ['\\', '.'], ['/', '.']]
    for entry in rChars:
        fName = fName.replace(entry[0], entry[1])

    return fName


def rename(root, oldName, newName, outputLog, fType, dupNum, logOnly):
    oldPath, newPath = os.path.join(root, oldName), os.path.join(root, newName)
    date, time = str(datetime.now())[:-3].split(" ")

    # if the filename has not been changed
    if oldPath == newPath:
        return False

    # If the filename HAS been changed
    else:
        if os.path.exists(newPath):
            newPath = newPath + str(dupNum)
            dupNum += 1

        # Rename the file
        if logOnly is False:
            shutil.move(oldPath, newPath)

        output = [date, time, root + "\\", "{" + oldName + "}",
                  "-->", "{" + newName + "}", fType]

        outputLog.append(",".join(output))
        print("{} {} was renamed to {}".format(fType, output[3], output[5]))

        return True


def main():
    """ Main function to check for incorrectly named files/folders
    and rename them
    """

    # Initialising variables
    logMode = True  # Set to log mode by default
    fileNum = 1  # Counter for renaming blank filenames
    dupNum = 1  # Counter for renaming duplicate filenames
    renamed = False  # Check whether any files were renamed
    outLog = []  # List to contain each line of the output log file
    flags = 0  # Number of input arguments
    excludePrefix = ('.', '__')

    # Setup runtime arguments
    argRename = ["rename", "-r"]  # Turn off the default log only mode

    # Set whether files are renamed or not
    if [flag for flag in sys.argv if flag in argRename]:
        logMode = False
        flags = 1
    else:
        print("\n---- LOG ONLY ENABLED ----\n")

    # Get path to directory
    PATH = getPath(flags)

    # ISSUE - The program currently does not rename files and folders with
    # a leading period (hidden folders and files), however it will still
    # rename files or folders within hidden folders

    for root, dirs, files in os.walk(PATH, topdown=False):
        # Don't rename any hidden files or folders
        files = [f for f in files if not f.startswith(excludePrefix)]
        dirs = [dr for dr in dirs if not dr.startswith(excludePrefix)]

        for f in files:
            fName, fileNum = cleanFilename(f, fileNum)

            # Rename file and check when a file is renamed
            if rename(root, f, fName, outLog, "file", dupNum, logMode):
                renamed = True

        # Cycle through any directories in the current folder and rename
        for dr in dirs:
            dName, fileNum = cleanFilename(dr, fileNum)

            # Runs rename function and checks wheter a file was renamed
            if rename(root, dr, dName, outLog, "dr", dupNum, logMode):
                renamed = True

    # Try to open (or overwrite) log file
    try:
        with open("logfile.csv", "w") as logfile:
            for line in outLog:
                logfile.write(line + "\n")
    # If file is already open, throw warning and save a copy of the logfile
    except PermissionError:
        print("\n---- WARNING - Cannot access logfile.csv ----\n"
              + "--- Please ensure logfile.csv is not open ---\n"
              + "----- Logfile saved as logfile_copy.csv -----\n")

        with open("logfile_copy.csv", "w") as logfile:
            for line in outLog:
                logfile.write(line + "\n")

    if not renamed:
        print("No files or folders were renamed\n")


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()
    main()
