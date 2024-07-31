import lxml.etree as ET
import uuid


def main(filename: str) -> None:
    """
    Converts an MEI file to MEI 5.0 format.

    Args:
        filename: The path to the MEI file to be converted.
    """
    # ET.register_namespace("", "http://www.music-encoding.org/ns/mei")

    tree = ET.parse(filename)
    root = tree.getroot()

    # Dictionaries for mapping attribute values
    div_dict = {
        "minor": "maior",
        "minior": "maior",
        "major": "maxima",
        "final": "finalis",
        "small": "minima",
        "comma": "virgula",
    }
    epi_dict = {"horizontal": "h", "vertical": "v"}

    # Flags for tracking certain conditions
    theres_an_episema = False
    theres_a_pb = False
    theres_a_sb = False
    theres_a_quilisma = False
    nc_flag = False
    neume_flag = False
    first_def = True

    pa_bre = []
    sy_bre = []

    type = ""

    nc_index = 0

    # Extra attributes for neumes and notes
    extra_nc = {}
    extra_neume = {}

    # Set MEI version to 5.0
    root.attrib["meiversion"] = "5.0"

    # Iterate over all elements in the tree
    for child in root.iter("*"):
        child.tag = ET.QName(child).localname

        if child.get("facs") is not None:
            child.set("facs", "#" + child.get("facs"))

        # Handle accid elements (remove oct and pname attributes)
        if child.tag.endswith("accid"):
            if child.get("oct") is not None:
                child.attrib.pop("oct")
            if child.get("pname") is not None:
                child.attrib.pop("pname")
        
        elif child.tag.endswith("clef"):
            child.attrib["dis"] = "8"
            child.attrib["dis.place"] = "above"

        # Handle division elements (become divLine)
        elif child.tag.endswith("division"):
            if child.get("form") is not None:
                child.set("form", div_dict[child.get("form")])

        # Handle dot elements (temporary fix until morae get added to MEI)
        elif child.tag.endswith("dot"):
            child.tag = "signifLet"
            if child.get("form") is not None:
                child.attrib.pop("form")

        # Handle episema elements
        elif child.tag.endswith("episema"):
            child.tag = "apisema"
            theres_an_episema = True
            if child.get("form") is not None:
                child.set("form", epi_dict[child.get("form")])
            if child.get("startid") is not None:
                child.attrib.pop("startid")
            if child.get("endid") is not None:
                child.attrib.pop("endid")
            epis = ET.tostring(child)
            child.tag = "TODELETE"

        # Handle graphic elements (e.g., change href to target)
        elif child.tag.endswith("graphic"):  # changes some stuff in the headers
            for att in list(child.attrib):
                if att.endswith("href"):
                    child.set("target", child.attrib.pop(att))

        # Handle layer elements
        elif child.tag.endswith("layer"):
            if theres_a_pb:
                theres_a_pb = False
                for pa in pa_bre:
                    child.insert(0, ET.fromstring(pa))
                    pa_bre = []
            if theres_a_sb:
                for sy in sy_bre:
                    child.insert(0, ET.fromstring(sy))
                    pa_bre = []

        # Handle lg elements
        elif child.tag.endswith("lg"):
            if len(list(child)) == 0:
                child.insert(0, ET.Element("l"))

        # Handle neume elements (become syllables, ncs become neumes, and notes become ncs)
        elif child.tag.endswith("neume"):
            child.insert(
                0,
                ET.Element(
                    "syl",
                    {
                        "{http://www.w3.org/XML/1998/namespace}id": f"m-{str(uuid.uuid4())}"
                    },
                ),
            )
            extra_neume = dict(child.attrib)
            child.attrib.clear()
            neume_flag = True
            for att in extra_neume:
                if att.endswith("id"):
                    child.set(att, extra_neume.pop(att))
                    break

        # Handle nc elements
        elif child.tag.endswith("nc"):
            nc_index = 0
            extra_nc = dict(child.attrib)
            child.attrib.clear()
            nc_flag = True
            if neume_flag:
                neume_flag = False
                child.attrib.update(extra_neume)
                extra_nc["facs"] = child.attrib.pop("facs")
            if child.get("name") is not None:
                child.set("type", child.attrib.pop("name"))
            if child.get("variant") is not None:
                child.set("type", child.attrib["type"] + child.attrib.pop("variant"))
            for att in extra_nc:
                if att.endswith("id"):
                    child.set(att, extra_nc.pop(att))
                    break
            type = child.get("type")

        # Handle note elements
        elif child.tag.endswith("note"):
            nc_index += 1
            if nc_flag:
                nc_flag = False
                child.attrib.update(extra_nc)
            if theres_a_quilisma:
                theres_a_quilisma = False
                child.insert(0, ET.Element("quilisma"))
            if child.get("inclinatum") is not None:
                child.set("tilt", "se")
                child.attrib.pop("inclinatum")
            if child.get("quilisma") is not None:
                child.attrib.pop("quilisma")
                theres_a_quilisma = True
            if theres_an_episema:
                theres_an_episema = False
                child.insert(0, ET.fromstring(epis))
            if type == "ancus":
                if nc_index == 1:
                    child.set("tilt", "n")
                elif nc_index == 3:
                    child.insert(0, ET.Element("liquescent"))
            elif type == "cephalicus":
                if nc_index == 1:
                    child.set("tilt", "n")
                elif nc_index == 2:
                    child.insert(0, ET.Element("liquescent"))
            elif type == "clivis" and nc_index == 1:
                child.set("tilt", "n")
            elif type == "epiphonus" and nc_index == 2:
                child.insert(0, ET.Element("liquescent"))
            elif type.startswith("porrectus"):
                if nc_index <= 2:
                    child.set("ligated", "true")
            elif type == "scandicus" and nc_index == 3:
                child.set("tilt", "n")
            elif type == "torculusresupinus":
                if nc_index in range(2, 4):
                    child.set("ligated", "true")
            elif type == "virga":
                child.set("tilt", "s")

        # Handle page breaks
        elif child.tag.endswith("pb"):

            if child.get("pageref") is not None:
                pageref = child.attrib.pop("pageref")
            for child_2 in root.iter():
                for attr, value in child_2.attrib.items():
                    if attr.endswith("id") and value == pageref:
                        child.set("n", child_2.attrib["n"])
                        break
            if not child.getparent().tag.endswith("layer"):
                pa_bre.append(ET.tostring(child))
                theres_a_pb = True
                child.tag = "TODELETE"

        # Handle staffDef elements
        elif child.tag.endswith("staffDef"):
            child.set("lines", "4")
            child.set("notationtype", "neume")

            if first_def:
                first_def = False
            else:
                child.tag = "TODELETE"

        # Handle sb elements
        elif child.tag.endswith("sb"):

            if child.get("systemref") is not None:
                systemref = child.attrib.pop("systemref")
            for child_2 in root.iter():
                for attr, value in child_2.attrib.items():
                    if attr.endswith("id") and value == systemref:
                        child.set("facs", child_2.attrib["facs"])
                        break
            if not child.getparent().tag.endswith("layer"):
                sy_bre.append(ET.tostring(child))
                theres_a_sb = True
                child.tag = "TODELETE"

        # Handle zone elements (adjusts negative ulx and lrx attributes)
        elif child.tag.endswith("zone"):
            if child.get("ulx") is not None and int(child.get("ulx")) < 0:
                child.set("ulx", "0")
            if child.get("lrx") is not None and int(child.get("lrx")) < 0:
                child.set("lrx", "0")

    # Create a new root element with MEI 5.0 namespace
    new_root = ET.Element(root.tag)
    new_root.attrib["xmlns"] = "http://www.music-encoding.org/ns/mei"
    new_root.attrib["meiversion"] = "5.0"

    # Handle multiple staff elements

    # Create a new <staff> element to merge all the others into
    merged_staff = ET.Element("staff")
    merged_layer = ET.SubElement(
        merged_staff, "layer"
    )  # create a single <layer> element
    first_staff = True

    for child in root.iter("*"):
        if child.tag.endswith("staff"):

            for child2 in child:
                if child2.tag.endswith("layer"):
                    for child3 in child2:
                        merged_layer.append(child3)

            if first_staff:
                first_staff = False
            else:
                child.tag = "TODELETE"

    for child in root.iter("*"):
        child.tag = ET.QName(child).localname
        if child.tag.endswith("staff"):
            child.getparent().replace(child, merged_staff)
            break

    # Create processing instructions
    pi1 = ET.ProcessingInstruction(
        "xml-model",
        'href="https://music-encoding.org/schema/5.0/mei-all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"',
    )
    pi2 = ET.ProcessingInstruction(
        "xml-model",
        'href="https://music-encoding.org/schema/5.0/mei-all.rng" type="application/xml" schematypens="http://purl.oclc.org/dsdl/schematron"',
    )

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
            new_child.text = child.text
            new_element.append(new_child)
            stack.append((new_child, child))

    # Write the new tree to a file
    new_tree = ET.ElementTree(new_root)
    ET.indent(new_tree, space="    ", level=0)
    new_tree.write(filename[:-4] + " - mei5.mei", encoding="utf8", xml_declaration=True)
