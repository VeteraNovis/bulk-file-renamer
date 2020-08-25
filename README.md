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

The following names are not allowed. If they are encountered the program will rename them by adding "-renamed" to the
file or folder.
> .lock, CON, PRN, AUX, NUL, COM0 - COM9, LPT0 - LPT9, \_vti_, desktop.ini

### Invalid characters

* *Work in progress*

## Authors

* **Callum** - *Initial Work* - [Callum-W](https://github.com/Callum-W)

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

* **[MIT license](http://opensource.org/licenses/mit-license.php)**
