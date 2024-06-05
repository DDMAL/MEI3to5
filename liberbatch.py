import os
import meichecker
import liberupdatev5

error_message = ""

for me_file in os.listdir("."):
    file_name = os.fsdecode(me_file)
    if file_name.endswith("corr.mei"):
        liberupdatev5.main(file_name)
        print(f"{file_name} has been updated")
        error_message += f"{meichecker.main(file_name[:-4] + ' - mei 5.mei')}\n"
        print(f"{file_name} has been checked")

print(error_message)