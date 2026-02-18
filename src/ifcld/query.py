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

building_storeys = """
SELECT ?storey ?storey_name 
WHERE {
    ?rel rdf:type ifc:IFCRELAGGREGATES  .
    ?rel ifc:relatingobject ?parent .
    ?parent rdf:type ifc:IFCBUILDING .
    ?rel ifc:relatedobjects ?storey .
    ?storey rdf:type ifc:IFCBUILDINGSTOREY
    OPTIONAL {?storey ifc:name ?storey_name . }
}
"""

top_sites = """
SELECT ?site ?site_name
WHERE {
    ?project rdf:type ifc:IFCPROJECT .
    ?rel rdf:type ifc:IFCRELAGGREGATES  .
    ?rel ifc:relatingobject ?project .
    ?rel ifc:relatedobjects ?site .
    OPTIONAL {?site ifc:name ?site_name . }
}
"""


spatial_decomposition = """
SELECT ?child ?child_type
WHERE {
    ?rel rdf:type ifc:IFCRELAGGREGATES  .
    ?rel ifc:relatingobject ?parent .
    ?rel ifc:relatedobjects ?child .
    ?child rdf:type ?child_type .
}
"""

spatial_containment = """
SELECT ?contains ?contains_type
WHERE {
    ?rel_contain rdf:type ifc:IFCRELCONTAINEDINSPATIALSTRUCTURE .
    ?rel_contain ifc:relatingstructure ?element .
    ?rel_contain ifc:relatedelements ?contains .
    ?contains rdf:type ?contains_type .
}
"""

full_project_spatial_decomposition = """
SELECT ?parent ?child ?comp_type ?parent_type ?child_type ?parent_name ?child_name ?elevation
WHERE {
    ?rel rdf:type ifc:IFCRELAGGREGATES  .
    ?rel ifc:relatingobject ?parent .
    ?rel ifc:relatedobjects ?child .
    ?child rdf:type ?child_type .
    ?parent rdf:type ?parent_type .
    OPTIONAL {?parent ifc:name ?parent_name .}
    OPTIONAL {?child ifc:compositiontype ?comp_type .}
    OPTIONAL {?child ifc:name ?child_name . }
    OPTIONAL {?child ifc:elevation ?elevation .}
}
"""

mapped_representation_query2 = """
SELECT DISTINCT ?representation ?rep_item ?source ?origin ?shape ?target ?shape_item ?shape_type
WHERE {
        ?representation rdf:type ifc:IFCSHAPEREPRESENTATION .
        ?representation ifc:contextofitems ?context .
        ?context ifc:targetview "MODEL_VIEW" .
        ?context ifc:contextidentifier "Body" .
        ?context ifc:contexttype "Model" .
        ?representation ifc:items ?rep_item .
        ?rep_item rdf:type ifc:IFCMAPPEDITEM .
        ?rep_item ifc:mappingsource ?source .
        ?source ifc:mappingorigin ?origin .
        ?source ifc:mappedrepresentation ?shape .
        ?rep_item ifc:mappingtarget ?target .
        ?shape ifc:items ?shape_item .
        ?shape_item rdf:type ?shape_type .
}
"""

mapped_representation_query = """
SELECT ?rep_item ?source ?origin ?shape ?target ?shape_items ?item_type
WHERE {
        ?rep_item rdf:type ifc:IFCMAPPEDITEM .
        ?rep_item ifc:mappingsource ?source .
        ?source ifc:mappingorigin ?origin .
        ?source ifc:mappedrepresentation ?shape .
        ?rep_item ifc:mappingtarget ?target .
        ?shape ifc:items ?shape_items .
}
"""

shape_aspect = """
SELECT ?shape_aspect ?shape_rep ?shape_name
WHERE {
        ?shape_aspect rdf:type ifc:IFCSHAPEASPECT .
        ?shape_aspect ifc:partofproductdefinitionshape ?source .
        ?shape_aspect ifc:shaperepresentations ?shape_rep . 
        ?shape_aspect ifc:name ?shape_name .
}
"""

cartesian_point = """
SELECT ?measure
WHERE {
        ?point ifc:coordinates/rdf:rest*/rdf:first ?measure .
}
"""
