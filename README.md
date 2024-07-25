**MEI 3 to 5**
=====================================

This repository contains a collection of scripts designed to update MEI 3 files to MEI 5. The current implementation of this repository only supports upgrading MEI files from the Liber Usualis. Future developments may extend this functionality to support additional MEI files.

**Usage**
-----

1. If you do not have it already, install lxml 5.0 using `pip install lxml==5.0`
2. Clone the repository and move the scripts in this repository into the same directory as your MEI files
3. Run the `liberbatch.py` script
   
This will update the Liber Usualis files from MEI 3 to MEI 5.



**`l_display.py`**
===============

Many of the Liber Usualis files have typographical errors in their textual content. `l_display.py1` allows one to visualise the text content and edit it

**Usage**
-----

1. Perform the steps listed above.
2. In the `l_display.py` script, replace the image_folder variable with the path to the folder containing your image files.
3. Run the `l_display.py` script.
4. You should see, from left to right:
    * An image of a page with bounding boxes drawn on it
    * A list of text boxes showcasing what the MEI file claims is the content of each bounding box.
    * Two buttons, labelled `-` and `+` respectively, and one button labelled Save.
5. If need be, the slider at the top can be used to adjust the scale of the bounding boxes.
6. The text boxes showcase what should be the content of their associated box. Which bounding box is associated with which text box can be ascertained by its colour. If their is a mistake in the text, simply edit the content of the text box.
7. Once all the text boxes have been modified to your liking, hit the Save button. This will not edit the content of the MEI file, but rather generate a new one.
8. Use the `-` and `+` buttons, or the arrow keys, to go to the previous or next page, respectively.
