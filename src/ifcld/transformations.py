import os

from pyld import jsonld
from ifcld.interpreters.jsonld import Interpreter
from ifcld.utils import save_jsonld_file, load_json
from ifcld.metamodels import PROV_METAMODEL, METAMODEL

FPM_MODEL_BASE_URI = "https://secorolab.github.io/models/"


def get_jsonld_interpretation(file_path):
    with open(file_path, "r") as input_file:
        ifc_model = input_file.read()
    interpreter = Interpreter()
    return interpreter.parse(ifc_model)


def load_context(model_name, context_path=None):
    if context_path is None:

        context = dict(**METAMODEL)
    else:
        context = load_json(context_path)

    context["@context"]["ifc-model"] = (
        FPM_MODEL_BASE_URI + model_name.replace(" ", "-") + "/ifc/data#"
    )
    return context


def transform_ifc_to_jsonld(model_path, output_dir, file_name=None, save_prov=False):
    model_name = os.path.basename(model_path).lower().replace(".ifc", "")
    ifc_model, prov = get_jsonld_interpretation(model_path)

    model_iri = FPM_MODEL_BASE_URI + model_name + "/"

    context = load_context(model_name)

    # ifc_model.pop(0)
    ifc_model_compact = jsonld.compact(
        ifc_model,
        context.get("@context"),
        {
            "expandContext": context.get("@context"),
        },
    )

    model = ifc_model_compact.get("@graph")
    ctx = ifc_model_compact.get("@context")

    if file_name is None:
        file_name = "{}.ifc.json".format(model_name)

    save_jsonld_file(
        os.path.join(output_dir, file_name),
        model,
        context=ctx,
        # graph_id="model:ifc",
    )

    if save_prov:
        prov_context = dict(**PROV_METAMODEL)
        prov_context["@context"]["fpm-model"] = model_iri

        file_name = "{}.ifc.prov.json".format(model_name)
        save_jsonld_file(
            os.path.join(output_dir, file_name),
            prov,
            context=prov_context,
            graph_id="fpm-model:prov",
        )
    return model_name
