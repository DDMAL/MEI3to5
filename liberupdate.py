import re


def main(filename):
#    filename = input("Enter file name: ")
    #filename = "0371_corr.mei"
    MEIfile = open(filename).read().split("\n")
    newfilename = filename[:-4]+ "NEW.mei"
    newfile = open(newfilename, "w")

    divDict = {"minor": "maior", "major": "maxima", "final": "finalis", "small": "minima"}
    epiDict = {"horizontal": "h", "vertical": "v"}
    epis = ""
    TheresAnEpisema = False
    flag= False
    extra=""
    skip= False

    for line in MEIfile:

        if re.search("<layout", line): #ignores anything inside a layout element
            if re.search("><layout", line):
               line= re.search(".*?><layout", line).group()[:-7]
               newfile.write(line+"\n")
            skip= True
            continue

        if re.search("</layout", line):
            skip= False
            continue
        if skip:
            continue
        if re.search("><", line):
            line=re.sub("><",">\n<", line)       
        if re.search("<graphic", line): #changes some stuff in the headers
            line = re.sub("xlink:href", "target", line)
        if re.search("meiversion", line):
            line = re.sub("meiversion=\".*\"", "meiversion=\"5.0+Neumes\"",line)

        if re.search("<pb", line): #adds in the pagebreak and systembreak info we ignored up above
            pageref=re.search("pageref=\".*?\"", line).group().lstrip("pageref=")
            for lone in MEIfile:
                if re.search("<page", lone):
                    print(re.search("xml:id=\".*?\"", lone).group())
                if re.search(pageref, lone):
                    n=re.search("n=\".*?\"", lone).group().lstrip("n=")
                    break
            line=re.sub("pageref=\".*?\"", "n="+n, line)
        if re.search("<sb", line):
            systemref=re.search("systemref=\".*?\"", line).group().lstrip("systemref=")

            for lone in MEIfile:
                if re.search(systemref, lone):
                    facs=re.search("facs=\".*?\"", lone).group().lstrip("facs=")
                    break
            line=re.sub("systemref=\".*?\"", "facs="+facs,line)
           
        if re.search("<nc", line): #the nc element in the 2011 version of MEI doesn't correspond to the nc element in MEI 5.0. The only pertinent information is put inside the string called extra
            extra=re.sub("<nc xml:id=\".*?\"","",line.rstrip().lstrip().rstrip(">"))
            if len(extra)>0:

                flag = True
            continue

        if re.search("</nc>", line):
            continue

        if re.search("<dot", line):
            line = re.sub("dot", "signifLet", line)
            line = re.sub("form=\".*?\"", "", line)
            

        if re.search("<division", line): #divisions in MEI 2011 are replaced by divLines in MEI 5.0, and have different syntax for their form
            line = re.sub("<division", "<divLine", line)
            form = re.search("form=\".*?\"", line).group()[6:-1]
            newform = divDict[form]
            line = re.sub("form=\".*?\"", "form=\""+newform+"\"", line)
            
        if re.search("<neume", line):
            newfile.write("<syllable>\n") #neumes have to be inside syllables (even though the MEI website doesn't say that?)
            line = re.sub("name","type", line) #names are replaced by types and are technically optional, but I figured I'd add them in just to help when the search gets updated 
            
        if re.search("</neume", line):
            newfile.write(line + "\n")
            newfile.write("</syllable>\n")
            continue

        if re.search("<accid", line):
            line = re.sub("oct=\".*?\"","", line) #accids don't have octs in MEI 5.0
            
        if re.search("<episema", line): #episemas (episemae?) need to get moved to the first nc inside a neume
            TheresAnEpisema = True
            epis = re.sub("startid=\".*?\"","",line)
            epis = re.sub("endid=\".*?\"","",epis)
            form = re.search("form=\".*?\"", epis).group()[6:-1]
            newform = epiDict[form]
            epis = re.sub("form=\".*?\"", "form=\""+newform+"\"", epis)
            continue
        
        if re.search("<note", line): #ncs in MEI 5.0 replace what would be notes in MEI 2011

            if flag: #flag notifies whether there's anything extra
                flag=False
                if re.search("/>",line):
                    line=line.rstrip().rstrip("/>")+ extra + "/>\n"
                else:
                    line=line.rstrip().rstrip(">")+ extra + ">\n"

            line = re.sub("note","nc",line)
            line = re.sub("inclinatum=\"true\"","tilt=\"se\"",line) #tilt replaces inclinatum
            if TheresAnEpisema: #adds episema to first nc
                TheresAnEpisema = False
                newfile.write(line+"\n")
                newfile.write(epis+"\n")
                epis = ""
                continue
            
        if re.search("</note", line):
            line = re.sub("note","nc",line)
        newfile.write(line+"\n")
    newfile.close()
            
