import os, meichecker, liberupdatev5
PATH = "your path here"

directory = os.fsencode(PATH)
err=""

for mefile in os.listdir(directory):
    filename = os.fsdecode(mefile)
    if filename.endswith("corr.mei"):
        liberupdatev5.main(filename)
        print(filename +" has been updated")
        err= err+ (meichecker.main(filename[:-4]+"NEW2.mei")+"\n")
#        print(err)
        print(filename +" has been checked")
print(err)
