import os
import xml.etree.ElementTree as ET

# Initialize an empty set to store unique type attributes
unique_types = set()

# Loop through all files in the directory
for filename in os.listdir("."):
    # Check if the file has a .mei extension
    if filename.endswith('.mei'):
        # Parse the XML file using ElementTree
        tree = ET.parse(filename)
        root = tree.getroot()
        
        # Find all elements with a 'type' attribute
        for elem in root.iter():
            if elem.tag.endswith("strophicus") or elem.tag.endswith("liquescent"):
                print(filename)
                print(elem.tag)