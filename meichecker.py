from lxml import etree

def main(filename):
    doc = etree.parse("mei-Neumes2.rng")
    relaxng = etree.RelaxNG(doc)
    foil = etree.parse(filename)
    relaxng.validate(foil)
    print(relaxng.error_log.__str__())
    return relaxng.error_log.__str__()
        
