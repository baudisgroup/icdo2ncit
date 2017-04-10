# Assignment of NCIT "neoplasm core" codes in arrayMap/Progenetix MongoDB collections, based ICDO (morphology + topography) <-> NCIT mapping

This script needs a mapping file as an input, the file should be provided with either as an URL or a local file.

* The script has a built-in [default URL](https://docs.google.com/spreadsheets/d/1MDTs7jD1D8fSlYfp3lBzCqk8U9F27QxF1PMN40nu454/export?format=csv) of the mapping file, but users can specify an alternative source.

* When using a Google spreadsheet, please use the following address style to download the document and convert this to a CSV input file:

`https://docs.google.com/spreadsheets/d/[your file id]/export?format=csv`

* For direct use of a local file, please provide this in CSV format.

* The script also generates a log file, the defualt name is log.txt

```
Options:
  -u, --url TEXT         Get the mapping from an url
  -f, --file TEXT        Get the mapping from a file
  -l, --log FILENAME     Generate a log file
  -d, --database TEXT    Use a specific database
  -c, --collection TEXT  Use a specific collection
  --help                 Show this message and exit.
```
