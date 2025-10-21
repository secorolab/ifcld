from rdflib.namespace import Namespace, NamespaceManager
from rdflib import Graph

IFC_MODEL = Namespace("https://secorolab.github.io/models/ifc-model#")
IFC_CLASS = Namespace(
    "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/"
)
IFC_PROP = Namespace(
    "https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/prop/"
)
IFC_CONCEPTS = Namespace("https://secorolab.github.io/metamodels/ifc/")
QUDT_QUANT = Namespace("http://qudt.org/vocab/quantitykind/")
QUDT_UNIT = Namespace("http://qudt.org/vocab/unit/")
QUDT_SCHEMA = Namespace("http://qudt.org/schema/qudt/")

namespace_manager = NamespaceManager(Graph())
namespace_manager.bind("ifc", IFC_CONCEPTS, override=True)
namespace_manager.bind("ifc-class", IFC_CLASS, override=True)
namespace_manager.bind("ifc-prop", IFC_PROP, override=True)
namespace_manager.bind("ifc-model", IFC_MODEL, override=True)
namespace_manager.bind("qudt-schema", QUDT_SCHEMA, override=True)
namespace_manager.bind("qudt-quant", QUDT_QUANT, override=True)
namespace_manager.bind("qudt-unit", QUDT_UNIT, override=True)

MEASURES = {
    "IFCLENGTHMEASURE": QUDT_QUANT["Length"],
    "IFCTHERMODYNAMICTEMPERATUREMEASURE": QUDT_QUANT["Temperature"],
    "IFCPLANEANGLEMEASURE": QUDT_QUANT["Angle"],
    "IFCTHERMALTRANSMITTANCEMEASURE": QUDT_QUANT["ThermalTransmittance"],
    "IFCNORMALISEDRATIOMEASURE": QUDT_QUANT["NormalizedDimensionlessRatio"],
    "IFCPOSITIVERATIOMEASURE": QUDT_QUANT["PositiveDimentionlessRatio"],
    "IFCTHERMALCONDUCTIVITYMEASURE": QUDT_QUANT["ThermalConductivity"],
    "IFCMASSDENSITYMEASURE": QUDT_QUANT["MassDensity"],
    "IFCSPECIFICHEATCAPACITYMEASURE": QUDT_QUANT["SpecificHeatCapacity"],
    "IFCPOSITIVELENGTHMEASURE": QUDT_QUANT["PositiveLength"],
    "IFCAREAMEASURE": QUDT_QUANT["Area"],
    # "": "",
}
