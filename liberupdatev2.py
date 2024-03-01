import re, xml.etree.ElementTree as ET

ET.register_namespace("","http://www.music-encoding.org/ns/mei")
def main(filename):

    tree=ET.parse(filename)
    root = tree.getroot()
    tree_2=ET.parse(filename)
    root_2 = tree_2.getroot()

    divDict = {"minor": "maior", "major": "maxima", "final": "finalis", "small": "minima"}
    epiDict = {"horizontal": "h", "vertical": "v"}
    epis = ""
    TheresAnEpisema = False
    flag= False
    extra={}
    skip= False
    root.attrib["meiversion"]="5.0+Neumes"
    for child in root.iter():
        '''
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
        '''
        if child.tag  == "layout":
            root.remove(child)
        '''
        
        if re.search("<graphic", line): #changes some stuff in the headers
            line = re.sub("xlink:href", "target", line)
        if re.search("meiversion", line):
            line = re.sub("meiversion=\".*\"", "meiversion=\"5.0+Neumes\"",line)
        '''
        if child.tag == "graphic":
            child.attrib['target'] = child.attrib.pop('href')
        '''
       if re.search("<pb", line): #adds in the pagebreak and systembreak info we ignored up above
            pageref=re.search("pageref=\".*?\"", line).group().lstrip("pageref=")
            for lone in MEIfile:
                if re.search("<page", lone):
                    print(re.search("xml:id=\".*?\"", lone).group())
                if re.search(pageref, lone):
                    n=re.search("n=\".*?\"", lone).group().lstrip("n=")
                    break
            line=re.sub("pageref=\".*?\"", "n="+n, line)
        '''
        if child.tag == "pb":
            pageref=child.attrib.pop("pageref")
            for child_2 in root_2.iter():
               if child_2.attrib["xml:id"]==pageref:
                   child.attrib["n"]= child_2.attrib["n"]
                   break

        '''
        if re.search("<sb", line):
            systemref=re.search("systemref=\".*?\"", line).group().lstrip("systemref=")

            for lone in MEIfile:
                if re.search(systemref, lone):
                    facs=re.search("facs=\".*?\"", lone).group().lstrip("facs=")
                    break
            line=re.sub("systemref=\".*?\"", "facs="+facs,line)
           
 
        '''
        if child.tag == "sb":
            
            systemref=child.attrib.pop("sytemref")
            for child_2 in root_2.iter():
               if child_2.attrib["xml:id"]==systemref:
                   child.attrib["facs"]= child_2.attrib["facs"]
                   break
        '''
        if re.search("<nc", line): #the nc element in the 2011 version of MEI doesn't correspond to the nc element in MEI 5.0. The only pertinent information is put inside the string called extra
            extra=re.sub("<nc xml:id=\".*?\"","",line.rstrip().lstrip().rstrip(">"))
            if len(extra)>0:

                flag = True
            continue

        if re.search("</nc>", line):
            continue


        '''
        if child.tag == "nc":
            extra=child.attrib
            extra.pop("xml:id")
            flag = True
            for grandchild in child:
                root.subElement(root, grandchild.tag, attrib = grandchild.attrib)
            root.remove(child)

        '''
 
        if re.search("<dot", line):
            line = re.sub("dot", "signifLet", line)
            line = re.sub("form=\".*?\"", "", line)


        '''
        if child.tag =="dot":
            child.tag="signifLeft"
            child.pop("form")

        '''

       if re.search("<neume", line):
            newfile.write("<syllable>\n") #neumes have to be inside syllables (even though the MEI website doesn't say that?)
            line = re.sub("name","type", line) #names are replaced by types and are technically optional, but I figured I'd add them in just to help when the search gets updated 

        if re.search("</neume", line):
            newfile.write(line + "\n")
            newfile.write("</syllable>\n")
            continue
        '''
        if child.tag == "neume":
            root.SubElement(root,"syllable").append(child)
            child.attrib['type'] = child.attrib.pop('name')
            
            
        '''                    
        if re.search("<accid", line):
            line = re.sub("oct=\".*?\"","", line) #accids don't have octs in MEI 5.0

        '''
        if child.tag == "accid":
            child.pop("oct")

        '''

            
        if re.search("<episema", line): #episemas (episemae?) need to get moved to the first nc inside a neume
            TheresAnEpisema = True
            epis = re.sub("startid=\".*?\"","",line)
            epis = re.sub("endid=\".*?\"","",epis)
            form = re.search("form=\".*?\"", epis).group()[6:-1]
            newform = epiDict[form]
            epis = re.sub("form=\".*?\"", "form=\""+newform+"\"", epis)
            continue
        
        '''
        if child.tag=="episema": #episemas (episemae?) need to get moved to the first nc inside a neume
            child.tag="apisema" #should be named episema but the code is set up to delete any elements called episema
            TheresAnEpisema = True
            child.attrib["form"] = epiDict[child.attrib("form")]
            epis = ET.tostring(child)
            root.remove(child)


        '''
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

        '''
        if child.tag=="note":
            child.tag="nec" # should be named nc but the code is set up to delete any elements called nc
            if flag:
                flag = False
                child.attrib.append(extra)

            if child.attrib["inclinatum"]=="true":
                child.attrib["tilt"]="se"
                child.attrib.pop("inclinatum")
            if TheresAnEpisema:
                TheresAnEpisema=False
                child.Subelement(ET.XML(epis))

    for child in root.iter(): #rename any elements that had been given a different name to avoid deletion in the previous loop
        if child.tag == "nec":
            child.tag="nc"
        if child.tag == "apisema":
            child.tag ="episema"

    tree.write(filename[:-4]+ "NEW2.mei")
'''        
    
#    filename = input("Enter file name: ")
    #filename = "0371_corr.mei"
    MEIfile = open(filename).read().split("\n")
    newfilename = filename[:-4]+ "NEW.mei"
    newfile = open(newfilename, "w")

    for line in MEIfile:
       
        if re.search("><", line):
            line=re.sub("><",">\n<", line)
        newfile.write(line+"\n")
    newfile.close()
'''         
