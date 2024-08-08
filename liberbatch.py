import os
import csv
import meichecker
import liberupdatev5

"""
Updates and validates all MEI files in the current directory.

This script updates each MEI file using liberupdatev5 and then validates
the updated file using meichecker.
"""

with open("image_dimensions.csv", "r") as f:
    reader = csv.reader(f)
    csv_dict = {row[0]: [row[1], row[2]] for row in reader}

default = ["0","0"]
error_message = ""

for me_file in os.listdir("."):
    file_name = os.fsdecode(me_file)
    if file_name.endswith("corr.mei"):
        dimensions = csv_dict.get(file_name.split("_")[0], default)
        # Update the MEI file using liberupdatev5
        liberupdatev5.main(file_name, dimensions)
        print(f"{file_name} has been updated")

        # Validate the updated MEI file using meichecker
        error_log = meichecker.main(file_name[:-4] + " - mei5.mei")
        error_message += f"{error_log}\n"
        print(f"{file_name} has been checked")

# Print the accumulated error messages
print(error_message)
