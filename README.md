# Bulk Renamer

This program will search through all sub-folders in a given directory and
rename any files or folders that have invalid characters.

## Purpose

I designed this program to assist users with fixing invalid filenames when
backing up large directories to Microsoft OneDrive. By recursively searching
through each file and folder, the program can check that there are no invalid
characters or filenames that would cause an upload error.

## How it works

This program generates a list of all file and folder names in the current directory (or the directory specified) and ensures that the names comply with
Microsoft OneDrive's filename specifications.

### Invalid file or folder names

The following names are not allowed. If they are encountered the program will rename them by appending "-renamed" to the file/folder name.
> .lock, CON, PRN, AUX, NUL, COM0 - COM9, LPT0 - LPT9, \_vti_, desktop.ini

### Invalid characters

The following characters are restricted in Microsoft OneDrive, and so if they
are encountered in any file/folder name, the character will either be deleted or replaced.  All trailing and leading whitespace is removed, and any trailing
periods are also removed.

> " * : < > ? / \ |

### Empty files

If any filenames would be empty after renaming, the program changes the name to
"unnamedX" where X is an incremental number.  This is to ensure that two
unnamed files in the same folder aren't both renamed to "unnamed".

## Authors

* **Callum** - *Initial Work* - [Callum-W](https://github.com/Callum-W)

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

* **[MIT license](http://opensource.org/licenses/mit-license.php)**
