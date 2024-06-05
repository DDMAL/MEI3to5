import os
import meichecker
import liberupdatev5
<<<<<<< 8-remove-commented-code-from-scripts
PATH = "your path here"

directory = os.fsencode(PATH)
err=""

for mefile in os.listdir(directory):
    filename = os.fsdecode(mefile)
   
    liberupdatev5.main(filename)
    print(filename +" has been updated")
    err += f"{meichecker.main(filename[:-4]+"NEW2.mei} \n"
    print(filename +" has been checked")

print(err)
=======

error_message = ""

for me_file in os.listdir("."):
    file_name = os.fsdecode(me_file)
    if file_name.endswith("corr.mei"):
        liberupdatev5.main(file_name)
        print(f"{file_name} has been updated")
        error_message += f"{meichecker.main(file_name[:-4] + ' - mei 5.mei')}\n"
        print(f"{file_name} has been checked")

print(error_message)
>>>>>>> main
