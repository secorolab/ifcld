# ifcld

Model-to-model transformation between IFC and JSON-LD.


## Differences to ifcld-service

This project has some key conceptual and implementation differences from the [ifcld-service](https://github.com/devonsparks/ifcld-service):

- Unlike the [ifcld schema](https://ifc-ld.org/releases/0.2/spec.html), we do not assume a closed-world definition in the models. In fact, our intention in generating a JSON-LD representation is precisely to enable their use and composition with other external models.
- While it would be great to not have to rely on the STEP language, we acknowledge it is historically a widely used representation. As such, we do not aim to replace the syntax used in the IFC models, but to provide a JSON-LD representation of _the same model_ and enable its composition with other models.
- Implementation-wise, we have removed the web-based components to keep a minimal and reimplemented the core ideas for a more pythonic processing of the STEP file. 
- The interpretation aims to be as close as possible to "pure JSON", i.e., we use a [compact document form](https://www.w3.org/TR/json-ld/#compacted-document-form) with the `@context` providing the JSON-LD description.
- We also have stripped down the interpretation: we do not create the JSON-LD file via RDF (specifically [rdflib](http://rdflib.readthedocs.io), but instead rely on a predefined `@context` and the use of the `@vocab` key to allow a more flexible interpretation of the concepts. Technically, this would allow for a version-independent interpretation; however, the STEP syntax often uses positional arguments (which can change from version to version), so this still requires the use of solutions such as the [offsets](https://ifc-ld.org/schemas/ifc4.offsets.json) in `ifcld-service` (at least, for now).
- The resulting graph is a 1:1 match to the STEP model, with each entity represented as its own node. We currently do not use named graphs like `ifcld-service` does.
- And as a result of our JSON-LD-based interpretation, our generated JSON-LD file results in far fewer `BNodes` -- which often result in issues when using other JSON-LD tools (e.g., for framing) --  and reducing model size considerably. 
- Another benefit of the `@context` definition is that we can make use of [aliased keywords](https://www.w3.org/TR/json-ld/#aliasing-keywords) to
  - Reuse existing concepts from other ontologies (e.g., [QUDT](http://qudt.org) for units and prefixes based on [this available mapping](https://github.com/qudt/qudt-public-repo/blob/main/src/main/rdf/community/mappings/SSSOM/IFC/qudt-ifc-mapping.tsv))


## Future work

- The `@context` is not complete, and currently covers only a subset of the concepts and properties. This is a potential advantage, as one can define the context for only the subset of relevant elements for a given application.
- While using the offsets, some semantics are missing (see IfcCartesianPoint -> coordinates which is missing the IfcLengthMeasure because it's not explicit in the STEP file)
- [JSON-LD node type indexing](https://www.w3.org/TR/json-ld/#node-type-indexing) for quantity kinds and values (aka measurements), and other typed parameters
- SHACL for validating the models. Here `ifcld-service` is also a good starting point.
- Using [bsdd](https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/). Note: only a subset of concepts are included as IFC classes. The [GitHub Repository](https://github.com/buildingSMART/bSDD/blob/master/Documentation/bSDD-IFC%20documentation.md) has more information and potential links to RDF.
- Non-specified units default to the project's units (but there's no explicit link). 
- Derived properties
- [Unit conversion](https://github.com/qudt/qudt-public-repo/wiki/User-Guide-for-QUDT#5-unit-conversion-example-in-qudt)

## Differences to ifcOwl

## Acknowledgements

This project is based on the work of Devon Sparks (devonsparks.com), especially the [ifcld-service](https://github.com/devonsparks/ifcld-service) project.
The [P21 parser](src/ifcld/parsers/p21) is taken directly and used without modification from its original authors.
For now, we also use the unmodified versions of the [offsets](https://ifc-ld.org/schemas/ifc4.offsets.json) and [ordered](https://ifc-ld.org/schemas/ifc4.ordered.json) data structures of the [ifc-ld 2.0 schema](https://ifc-ld.org/releases/0.2/spec.html) for parsing (see [parsers/ifc](src/ifcld/parsers/ifc)).
