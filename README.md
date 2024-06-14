**MEI 3 to 5**
=====================================

This repository contains a collection of scripts designed to update MEI 3 files to MEI 5. The current implementation of this repository only supports upgrading MEI files from the Liber Usualis. Future developments may extend this functionality to support additional MEI files.

**Usage**
-----

1. If you do not have it already, install lxml 5.0 using `pip install lxml==5.0`
2. Clone the repository and move the scripts in this repository into the same directory as your MEI files
3. Run the `liberbatch.py` script
   
This will update the Liber Usualis files from MEI 3 to MEI 5.

Nota Bene: pages 0002, 0040, 0050, 0110, 0123, 0514, 0962, 1111, 1851, 2226, and 2340 have errors that need to be corrected manually. Page 0123 has an unexpected `DivLine` inside of a neume component that needs to be removed and added to the `layer` element instead. The remaining, apart from page 1851, have an `lg` element which require a blank `l` element inserted. It is unclear at the moment what the issue with page 1851 is.

