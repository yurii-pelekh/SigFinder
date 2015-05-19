from Sigfinder.sigfinder import SigFinder
from sys import argv

try:
    script, signatureFile, srcDir, destDir, bytesCount = argv
except ValueError:
    print("Wrong arguments. Example: signature_file source_dir destination_dir count_of_bytes (0 - if all)")
    exit()

try:
    bytesCount = int(bytesCount)
    if(bytesCount) == 0: bytesCount = -1
except ValueError:
    bytesCount = -1

requiredExtensions = ['.jpg']

finder = SigFinder(requiredExtensions, signatureFile)
finder.searchInFiles(srcDir, destDir, bytesCount)