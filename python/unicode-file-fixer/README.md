#### Unicode File Tree Fixer

Suppose you have a directory filled with directories and files whose 
names include unicode characters and you want all the names to be 
simple ASCII. If you have such a problem you're in the right place.

Disclaimer:

*USE AT YOUR OWN RISK AND BACK UP YOUR DATA*

---

Usage:
```
./fix.sh <directory-to-fix>
```

Example:
```
./fix.sh /tmp/holder
```

Description:

The ```fix.sh``` script uses two Python scripts. There is a script to 
fix the directory names ```dir_fixer.py``` and one to fix the
file names, ```file_fixer.py```.

```dir_fixer.py```: takes from ```stdin``` a list of directories to fix. 
This list of directories *SHOULD* be the output of:
```
find <some-directory> -depth -type d
```

```file_fixer.py```: takes a directory filled with strangely named files. It
crawls through the directory renaming the files as needed.
