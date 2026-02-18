import json

from ifcld.parsers.p21 import Part21 as p21
from ifcld.parsers.ifc import OFFSETS, ORDERED

from ifcld.interpreters.params import Param as IfcSimpleParam
from ifcld.interpreters.namespaces import (
    IFC_MODEL,
    IFC_CONCEPTS,
    MEASURES,
    IFC_CLASS,
    IFC_PROP,
    namespace_manager as nm,
    UNIT_TYPES,
    QUDT_QUANT,
    UNITS,
    PREFIXES,
    QUDT_SCHEMA,
    QUDT_UNIT,
    QUDT_PREFIX,
)


class P21File:
    def to_json(self, graph):
        P21Header.to_json(self.header, graph)
        for s in self.sections:
            Section.to_json(s, graph)


class P21Header:
    @staticmethod
    def to_json(self, graph):
        header = {
            "@id": "ifc-model:header",
            "@type": ["step:FileName", "step:FileDescription", "step:FileSchema"],
        }
        file_name_params = [
            "name",
            "time_stamp",
            "author",
            "organization",
            "preprocessor_version",
            "originating_system",
            "authorization",
        ]
        fn = HeaderEntity.to_json(self.file_name, graph, file_name_params)
        header.update(**fn)

        fd = HeaderEntity.to_json(
            self.file_description,
            graph,
            ["description", "implementation_level"],
        )
        header.update(**fd)

        fs = HeaderEntity.to_json(self.file_schema, graph, ["schema_identifiers"])
        header.update(**fs)

        if self.extra_headers:
            print(self.extra_headers)
            raise Exception("Extra headers currently not processed")

        graph.append(header)


class HeaderEntity:
    @staticmethod
    def to_json(self, graph, param_names):
        entity = dict()
        for param, name in zip(self.params, param_names):
            entity[name] = param
        return entity


class Section:
    @staticmethod
    def to_json(self, graph):
        for entity in self.entities:
            SimpleEntity.to_json(entity, graph)


class SimpleEntity:
    @staticmethod
    def to_json(self, graph):
        entity = {
            "@id": nm.curie(IFC_MODEL[self.ref[1:]]),
            "@type": self.type_name,
        }

        offsets = OFFSETS[self.type_name.lower()]
        if len(offsets) != len(self.params):
            print(offsets)
            print(self.params)
            raise Exception("Wrong number of offsets")

        if self.type_name.lower() in ORDERED:
            print(self.type_name, "ORDERED")

        for name, param in zip(offsets, self.params):
            param_name = "{}".format(name)
            if isinstance(param, p21.TypedParameter):
                param_t = TypedParameter.to_json(param)
                entity[param_name] = param_t
            elif isinstance(param, list):
                value_list = ParamList.to_json(param, param_name)
                entity[param_name] = value_list
            else:
                entity[param_name] = SimpleParameter.to_json(param)

        if self.type_name in ["IFCSIUNIT", "IFCCONVERSIONBASEDUNIT"]:
            UnitEntity.transform_to_qudt(entity)
        graph.append(entity)


class UnitEntity:
    @staticmethod
    def to_json(params, offsets):
        pass

    @staticmethod
    def transform_to_qudt(entity):
        unit_type = entity["unittype"]
        entity["unittype"] = QUDT_QUANT[UNIT_TYPES[unit_type]]
        prefix = entity.get("prefix")
        name = entity.get("name").upper()
        if prefix is not None:
            entity["prefix"] = QUDT_PREFIX[PREFIXES[prefix]]
            entity[QUDT_SCHEMA["scalingOf"]] = QUDT_UNIT[UNITS[name]]
            entity["name"] = QUDT_UNIT[prefix.capitalize() + UNITS[name]]
        else:
            entity["name"] = QUDT_UNIT[UNITS[name]]


class ComplexEntity:
    @staticmethod
    def to_json(self, graph):
        pass


class TypedParameter:
    @staticmethod
    def to_json(self, debug=False):
        if self.type_name == "IFCREAL":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "xsd:double"}
        elif self.type_name == "IFCBOOLEAN":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "xsd:boolean"}
        elif self.type_name == "IFCLOGICAL":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            if isinstance(param, str):
                param_type = "xsd:string"
            else:
                param_type = "xsd:boolean"
            return {"@value": param, "@type": param_type}
        elif self.type_name in ["IFCINTEGER", "IFCPOSITIVEINTEGER"]:
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "xsd:integer"}
        elif self.type_name in ["IFCLABEL"]:
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "rdfs:label"}
        elif self.type_name == "IFCTIMESTAMP":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {self.type_name: param}
        elif self.type_name == "IFCDURATION":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "xsd:duration"}
        elif self.type_name == "IFCDATETIME":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "xsd:dateTime"}
        elif self.type_name == "IFCDATE":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "xsd:date"}
        elif self.type_name == "IFCTIME":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "xsd:time"}
        elif self.type_name == "IFCIDENTIFIER":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "dcterms:identifier"}
        elif self.type_name == "IFCTEXT":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "xsd:string"}
        elif self.type_name in MEASURES:
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": QUDT_QUANT[self.type_name]}
        elif self.type_name == "IFCURIREFERENCE":
            assert len(self.params) == 1
            param = SimpleParameter.to_json(self.params[0])
            return {"@value": param, "@type": "@id"}
        else:
            param_t = {self.type_name: self.params}
            if debug:
                print(self.type_name)
                for param in self.params:
                    print("\t", param, type(param))
            return param_t


class ParamList:
    @classmethod
    def to_json(cls, param, param_name):

        value_list = list()
        for value in param:
            if isinstance(value, list):
                value_list.append(ParamList.to_json(value, param_name))
            else:
                value_list.append(SimpleParameter.to_json(value))
        return value_list


class SimpleParameter(IfcSimpleParam):
    @classmethod
    def to_json(cls, param):
        if isinstance(param, str):
            if cls.is_reference(param):
                return nm.curie(IFC_MODEL[param[1:]])
            elif cls.is_null(param):
                return None
            elif cls.is_boolean(param):
                if param == ".T.":
                    return True
                else:
                    return False
            elif cls.is_enum(param):
                # TODO Check later if this might be worth converting to a separate node in the graph (e.g. as @type)
                if param == ".U.":
                    value = "UNKNOWN"
                else:
                    value = param[1:-1]
            else:
                value = param
            return value
        elif isinstance(param, float):
            return param
        elif isinstance(param, int):
            return param
        elif isinstance(param, p21.TypedParameter):
            return TypedParameter.to_json(param)
        elif isinstance(param, list):
            raise Exception("Param is list!")
        else:
            print(param)
            raise Exception("Unexpected param type")


class Interpreter:
    def parse(self, source, **kwargs):
        graph = list()
        step_ast = self._parse(source)
        P21File.to_json(step_ast, graph)

        prov = self._add_provenance("fpm-model:fpm", **kwargs)
        return graph, prov

    def _parse(self, source):
        p21_parser = p21.Parser()
        try:
            return p21_parser.parse(source)
        except Exception as e:
            print(e)

    def _add_provenance(self, file_name, **kwargs):
        from rdflib import PROV, DCTERMS
        import datetime as dt

        gen_date = dt.datetime.now().isoformat()
        provenance = {
            "title": file_name,
            "@type": "dcterms:ProvenanceStatement",
            PROV.generatedAtTime: gen_date,
            PROV.wasDerivedFrom: "ifc-model:ifc-ld",
            DCTERMS.conformsTo: "ifc",
        }

        return provenance
