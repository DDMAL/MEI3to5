import xml.etree.ElementTree as ET
ET.register_namespace("mei","http://www.music-encoding.org/ns/mei")
def main(filename):

    tree=ET.parse(filename)
    root = tree.getroot()
    # ... (assuming root is the root element of the original XML file)
    divDict = {"minor": "maior", "minior": "maior", "major": "maxima", "final": "finalis", "small": "minima", "comma": "virgula"}
    epiDict = {"horizontal": "h", "vertical": "v"}
    epis = ""
    TheresAnEpisema = False
    flag= False
    neume_flag = False
    extra_nc={}
    extra_neume={}
    skip= False
    root.attrib["meiversion"]="5.0+Neumes"

    for child in root.iter("*"):

        if child.tag.endswith("graphic"): #changes some stuff in the headers

            for att in list(child.attrib):
                
                if att.endswith("href"):                    
                    child.attrib['target'] = child.attrib.pop(att)
        
        if child.tag.endswith("pb"): #adds in pagebreak info from layout element (which gets deleted later)
            
            for att in child.attrib:
                
                if att.endswith("pageref"):                    
                    pageref = child.attrib.pop(att)
                    break

            for child_2 in root.iter():
              
              for attr, value in child_2.attrib.items():
                
                if attr.endswith("id") and value==pageref:
                       child.attrib["n"]= child_2.attrib["n"]
                       break


        if child.tag.endswith("sb"): #adds in systembreak info from layout element (which gets deleted later)
            
            for att in child.attrib:
                if att.endswith("systemref"):                    
                    systemref = child.attrib.pop(att)
                    break
            for child_2 in root.iter():
               
              for attr, value in child_2.attrib.items():
                if attr.endswith("id") and value==systemref:
                       child.attrib["facs"]= child_2.attrib["facs"]
                       break
        if child.tag.endswith("zone"):
             label = ""
             for attr, value in child.attrib.items():
                if attr.endswith("ulx") and int(value)<0:
                       
                       child.attrib["label"] = label + "ulx = " + value + " " #some boxes have x-coordinates below 0. This makes them 0 and adds a label listing the original value
                       child.attrib[attr] = str(0)
                       break
             for attr, value in child.attrib.items():
                if attr.endswith("lrx") and int(value)<0:
                       
                       child.attrib["label"] = label + "lrx = " + value + " " #ditto
                       child.attrib[attr] = str(0)
                       break

        if child.tag.endswith("dot"): #temporary fix until morae get added to MEI
            child.tag="signifLeft"
            for att in child.attrib:
                if att.endswith("form"):
                    child.attrib.pop(att)
                    break

        #neumes become syllables, ncs become neumes, and notes become ncs. Relevant info from each goes into the other

        if child.tag.endswith("neume"):
            extra_neume= dict(child.attrib)
            child.attrib.clear()
            neume_flag = True

            for att in extra_neume:
                if att.endswith("name"):                    
                    extra_neume['type'] = extra_neume.pop(att)
                    break
            for att in extra_neume:
                if att.endswith("id"):                    
                    child.attrib['xml:id'] = extra_neume.pop(att)
                    break
        
        if child.tag.endswith("nc"):
            extra_nc=dict(child.attrib)
            child.attrib.clear()
            if neume_flag:
                neume_flag = False
                child.attrib.update(extra_neume)
            for att in extra_nc:
                if att.endswith("id"):                    
                    child.attrib["xml:id"] = extra_nc.pop(att)
                    break
            flag = True

        if child.tag.endswith("division"): #division is replaced by divLine
            for att, value in child.attrib.items():
                if att.endswith("form"):
                    child.attrib[att] = divDict[value]


        if child.tag.endswith("note"):
                        if flag:
                            flag = False
                            child.attrib.update(extra_nc)
                        for att, value in child.attrib.items():
                            if att.endswith("inclinatum"):
                                child.attrib["tilt"]="se"
                                child.attrib.pop(att)
                                break
                        if TheresAnEpisema:
                            TheresAnEpisema=False
                            child.append(ET.fromstring(epis))

       #accids don't have octs or pnames in MEI 5.0

        if child.tag.endswith("accid"):
            for att in child.attrib:
                if att.endswith("oct"):                    
                    child.attrib.pop(att)
                    break
            for att in child.attrib:
                if att.endswith("pname"):                    
                    child.attrib.pop(att)
                    break
            
        if child.tag.endswith("episema"): #episemas (episemae?) need to get moved to the first nc inside a neume
            
            child.tag="apisema" 
            TheresAnEpisema = True
            for att, value in child.attrib.items():
                if att.endswith("form"):                    
                    att= epiDict[value]
            epis = ET.tostring(child)
            child.tag = "TODELETE"


  
    new_root = ET.Element(root.tag)
    stack = [(new_root, root)]  # stack of (new_element, old_element) pairs

    while stack:
        new_element, old_element = stack.pop()
        for child in old_element:
            tag = child.tag

            if tag.endswith("layout"): #delete some elements
                continue
            if tag.endswith("TODELETE"):
                continue

            if tag.endswith("neume"): #rename some others
                tag = "syllable"
            elif tag.endswith("nc"):
                tag = "neume"    
            elif tag.endswith("note"):
             tag = "nc"
            if tag.endswith("apisema"):
             tag = "episema"
            if tag.endswith("division"):
             tag = "divLine"


            new_child = ET.Element(tag, child.attrib)
            new_element.append(new_child)
            stack.append((new_child, child))

    new_tree = ET.ElementTree(new_root)
    new_tree.write(filename[:-4] + "NEW2.mei", encoding="unicode", xml_declaration=True)