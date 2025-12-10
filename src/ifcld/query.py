project_units_query = """
SELECT ?name 
WHERE {
    ?project rdf:type ifc:IFCPROJECT  .
    ?project ifc:unitsincontext/ifc:units ?unit .
    ?unit qudt:hasUnit ?name .
    ?unit qudt:hasQuantityKind quantitykind:Length .
}
"""

units_query = """
SELECT ?unit ?name ?unittype ?prefix ?dimensions
WHERE {
    ?unit rdf:type ifc:IFCSIUNIT  .
    ?unit qudt:hasUnit ?name .
    ?unit qudt:hasQuantityKind ?unittype .
    OPTIONAL { ?unit qudt:prefix ?prefix}
    OPTIONAL{ ?unit ifc:dimensions ?dimensions}
}
"""
convert_units_query = """
SELECT ?unit ?name ?unittype ?prefix ?dimensions ?factor ?new_unit ?factor_value
WHERE {
    ?unit rdf:type ifc:IFCCONVERSIONBASEDUNIT  .
    ?unit qudt:hasUnit ?name .
    ?unit qudt:hasQuantityKind ?unittype .
    OPTIONAL { ?unit qudt:prefix ?prefix}
    OPTIONAL{ ?unit ifc:dimensions ?dimensions}
    OPTIONAL{ 
        ?unit qudt:conversionMultiplier ?factor .
        ?factor ifc:unitcomponent/qudt:hasUnit ?new_unit .
        ?factor ifc:valuecomponent ?factor_value .
    }
}
"""
