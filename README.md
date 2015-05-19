Python script that can find files in source directory with special signature.
Signature must be in hex. For example: 4a464946 - this signature allows you to find all pictures (jpg).
You can put 'x' if you don't know the value of octet. For example: 4a464x46, or 4a464xx6, etc.
Notice: values of octets must be in lowercase (a, not A)
To run script you must use these parameters: handler.py  signature_file source_dir destination_dir count_of_bytes (0 - if all)
Where:
signature_file - path to file with signature;
source_dir - path to source directory where you want to search files
destination_dir - path to destination directory where all acceptable files will be copied
count_of_bytes - this count of bytes will be taken from file, and searching will take place only in this piece of file (use '0' if you want to search in whole file)
