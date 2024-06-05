import os
import meichecker
import liberupdatev5
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
