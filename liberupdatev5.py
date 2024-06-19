import lxml.etree as ET

def main(filename: str) -> None:
    """
    Converts an MEI file to MEI 5.0 format.

    Args:
        filename: The path to the MEI file to be converted.
    """
    ET.register_namespace("mei", "http://www.music-encoding.org/ns/mei")

    tree = ET.parse(filename)
    root = tree.getroot()

    # Dictionaries for mapping attribute values
    div_dict = {"minor": "maior", "minior": "maior", "major": "maxima", "final": "finalis", "small": "minima", "comma": "virgula"}
    epi_dict = {"horizontal": "h", "vertical": "v"}

    # Flags for tracking certain conditions
    theres_an_episema = False
    theres_a_pb = False
    theres_a_sb = False
    nc_flag = False
    neume_flag = False

    # Extra attributes for neumes and notes
    extra_nc = {}
    extra_neume = {}

    # Set MEI version to 5.0
    root.attrib["meiversion"] = "5.0"

    # Iterate over all elements in the tree
    for child in root.iter("*"):
        child.tag = ET.QName(child).localname

        # Handle graphic elements (e.g., change href to target)
        if child.tag.endswith("graphic"): #changes some stuff in the headers
            for att in list(child.attrib):
                if att.endswith("href"):                    
                    child.set('target', child.attrib.pop(att))
        
        # Handle page breaks
        elif child.tag.endswith("pb"): #adds in pagebreak info from layout element (which gets deleted later)
            child.tag = "peeb"
            for att in child.attrib:                
                if att.endswith("pageref"):                    
                    pageref = child.attrib.pop(att)
                    break
            for child_2 in root.iter():
              for attr, value in child_2.attrib.items():               
                if attr.endswith("id") and value == pageref:
                        child.set("n", child_2.attrib["n"])
                        break                 
            pa_bre = ET.tostring(child)
            theres_a_pb = True
            child.tag = "TODELETE"
        
        # Handle system breaks
        elif child.tag.endswith("sb"):
            child.tag = "seeb"
            for att in child.attrib:
                if att.endswith("systemref"):                    
                    systemref = child.attrib.pop(att)
                    break
            for child_2 in root.iter():               
              for attr, value in child_2.attrib.items():
                if attr.endswith("id") and value == systemref:
                        child.set("facs", child_2.attrib["facs"])
                        break
            sy_bre = ET.tostring(child)           
            theres_a_sb = True
            child.tag = "TODELETE"

        # Moves system breaks and page breaks inside layer
        elif child.tag.endswith("layer"):
            if theres_a_pb:
                theres_a_pb = False
                child.insert(0, ET.fromstring(pa_bre))
            if theres_a_sb:
                theres_a_sb = False
                child.insert(0, ET.fromstring(sy_bre))

        # Handle zone elements (adjusts negative ulx and lrx attributes)
        elif child.tag.endswith("zone"):
            label = ""
            for attr, value in child.attrib.items():
                if attr.endswith("ulx") and int(value) < 0:
                    child.set(attr, "0")
                    break
            for attr, value in child.attrib.items():
                if attr.endswith("lrx") and int(value) < 0:
                    child.set(attr, "0")
                    break
        
        # Handle dot elements (temporary fix until morae get added to MEI)
        elif child.tag.endswith("dot"):
            child.tag = "signifLet"
            for att in child.attrib:
                if att.endswith("form"):
                    child.attrib.pop(att)
                    break
        
        # Handle empty lg elements
        elif child.tag.endswith("lg"):
            if len(list(child)) == 0:
                child.insert(0, ET.Element('l'))

        # Handle neume elements (become syllables, ncs become neumes, and notes become ncs)
        elif child.tag.endswith("neume"):
            child.insert(0, ET.Element("syl"))
            extra_neume= dict(child.attrib)
            child.attrib.clear()
            neume_flag = True
            for att in extra_neume:
                if att.endswith("name"):                    
                    child.set('type', extra_neume.pop(att))
                    break
            for att in extra_neume:
                if att.endswith("variant"):                    
                    child.set('type',  child.attrib['type'] + extra_neume.pop(att))
                    break
            for att in extra_neume:
                if att.endswith("id"):                    
                    child.set(att, extra_neume.pop(att))
                    break

        #Handle nc elements
        elif child.tag.endswith("nc"):
            extra_nc = dict(child.attrib)
            child.attrib.clear()
            nc_flag = True
            if neume_flag:
                neume_flag = False
                child.attrib.update(extra_neume)
            for att in extra_nc:
                if att.endswith("id"):                    
                    child.set(att, extra_nc.pop(att))
                    break

        # Handle division elements (become divLine)
        elif child.tag.endswith("division"):
            for att, value in child.attrib.items():
                if att.endswith("form"):
                    child.set(att, div_dict[value])

        # Handle note elements
        elif child.tag.endswith("note"):
            if nc_flag:
                nc_flag = False
                child.attrib.update(extra_nc)
            for att, value in child.attrib.items():
                if att.endswith("inclinatum"):
                    child.set("tilt", "se")
                    child.attrib.pop(att)
                    break
            for att in child.attrib:
                if att.endswith("quilisma"):
                    child.attrib.pop(att)
                    child.insert(0, ET.Element("quilisma"))
                    break
            if theres_an_episema:
                theres_an_episema = False
                child.insert(0, ET.fromstring(epis))

        # Handle accid elements (remove oct and pname attributes)
        elif child.tag.endswith("accid"):
            for att in child.attrib:
                if att.endswith("oct"):
                    child.attrib.pop(att)
                    break
            for att in child.attrib:
                if att.endswith("pname"):
                    child.attrib.pop(att)
                    break

        # Handle episema elements
        elif child.tag.endswith("episema"):
            child.tag = "apisema"
            theres_an_episema = True
            for att, value in child.attrib.items():
                if att.endswith("form"):
                    child.set(att, epi_dict[value])
            for att in child.attrib:
                if att.endswith("startid"):
                    child.attrib.pop(att)
                    break
            for att in child.attrib:
                if att.endswith("endid"):
                    child.attrib.pop(att)
                    break
            epis = ET.tostring(child)
            child.tag = "TODELETE"


    # Create a new root element with MEI 5.0 namespace
    new_root = ET.Element(root.tag)
    new_root.attrib["xmlns"] = "http://www.music-encoding.org/ns/mei"
    new_root.attrib["meiversion"] = "5.0"

    # Create processing instructions
    pi1 = ET.ProcessingInstruction('xml-model', 'href="https://music-encoding.org/schema/5.0/mei-all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"')
    pi2 = ET.ProcessingInstruction('xml-model', 'href="https://music-encoding.org/schema/5.0/mei-all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"')

    # Add processing instructions to the tree
    new_root.addprevious(pi1)
    new_root.addprevious(pi2)

    # Recursively build the new tree
    stack = [(new_root, root)]
    while stack:
        new_element, old_element = stack.pop()
        for child in old_element:
            tag = child.tag
            if tag.endswith("layout"):  # delete some elements
                continue
            if tag.endswith("TODELETE"):
                continue

            if tag.endswith("neume"):  # rename some others
                tag = "syllable"
            elif tag.endswith("nc"):
                tag = "neume"
            elif tag.endswith("note"):
                tag = "nc"
            elif tag.endswith("apisema"):
                tag = "episema"
            elif tag.endswith("peeb"):
                tag = "pb"
            elif tag.endswith("seeb"):
                tag = "sb"
            elif tag.endswith("division"):
                tag = "divLine"

            new_child = ET.Element(tag, child.attrib)
            new_element.append(new_child)
            stack.append((new_child, child))

    # Write the new tree to a file
    new_tree = ET.ElementTree(new_root)
    new_tree.write(filename[:-4] + " - mei5.mei", encoding="utf8", xml_declaration=True)