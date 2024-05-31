import os, meichecker, liberupdatev5

directory = os.fsencode("C:\\Users\\cole_\\Downloads\\liberUsualis - Copy\\liber")
err=""

i = 0 #for debugging
for mefile in os.listdir(directory):
    filename = os.fsdecode(mefile)
    if filename.endswith("corr.mei"):
        liberupdate.main(filename)
        print(filename +" has been updated")
        err= err+ (meichecker.main(filename[:-4]+"NEW2.mei")+"\n")
#        print(err)
        print(filename +" has been checked")
     #   i+=1

    #if i>=100:
    #    break
print(err)
