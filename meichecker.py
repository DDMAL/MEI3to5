from lxml import etree


def main(filename: str) -> str:
    """
    Validates an MEI file against the MEI 5.0 schema.

    Args:
        filename: The path to the MEI file to be validated.

    Returns:
        A string representation of the validation error log.
    """
    # Parse the MEI 5.0 schema (mei-all.rng)
    doc = etree.parse("mei-all.rng")

    # Create a RelaxNG validator from the parsed schema
    relaxng = etree.RelaxNG(doc)

    # Parse the MEI file to be validated
    foil = etree.parse(filename)

    # Validate the MEI file against the schema
    relaxng.validate(foil)

    # Get the validation error log as a string
    error_log = relaxng.error_log.__str__()

    # Print and return the error log
    print(error_log)
    return error_log
