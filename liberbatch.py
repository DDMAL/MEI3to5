import os, liberupdate, meichecker

directory = os.fsencode("C:\\Users\\cole_\\Downloads\\liberUsualis - Copy\\liber")
err=""
for mefile in os.listdir(directory):
    filename = os.fsdecode(mefile)
    if filename.endswith("corr.mei"):
        liberupdate.main(filename)
        print(filename +" has been updated")
        err= err+ (meichecker.main(filename[:-4]+"NEW.mei")+"\n")
#        print(err)
        print(filename +" has been checked")

print(err)
