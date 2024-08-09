**MEI 3 to 5**
=====================================

This repository contains a collection of scripts designed to update MEI 3 files to MEI 5. The current implementation of this repository only supports upgrading MEI files from the Liber Usualis. Future developments may extend this functionality to support additional MEI files.

**Usage**
-----

1. If you do not have it already, install lxml 5.0 using `pip install lxml==5.0`
2. Clone the repository and move the scripts in this repository into the same directory as your MEI files
3. Run the `liberbatch.py` script
   
This will update the Liber Usualis files from MEI 3 to MEI 5.

**IIIF Folder Contents**

The images in this folder are high-quality scans of the Liber Usualis pages, intended for eventual integration with an IIIF image server.

**Image Titling Conventions**

We've used the following suffixes to indicate specific processing details for each image:

* `_scaled`: These images required resizing to achieve optimal display quality.
* `_unscaled`: Unfortunately, these images had irreparable size issues that couldn't be resolved through scaling.
* **No suffix**: These images were perfect from the start, requiring no adjustments.