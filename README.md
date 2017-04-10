# Generate NCIT code based ICDO <-> NCIT mapping

This script needs a mapping file as an input, the file should be provided either as an URL(google doc) or a local file.

* For google doc, please use the following to convert to CSV format : 

`https://<i></i>edocs.google.com/spreadsheets/d/[your file id]/export?format=csv`

* For locoal file, please also privde in CSV format.

* The script has a built in defaut url for the mapping file, user can specifiy a file source with arguments.

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
