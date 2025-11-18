import json


def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def save_json(file_path, data):
    with open(file_path, "w") as outfile:
        json.dump(
            data,
            outfile,
            indent=2,
        )


def get_graph_dict(graph, graph_id=None, context=None):
    if context is None:
        context = {"@context": {}}
    contents = dict(**context)

    if graph_id:
        contents["@id"] = graph_id
    contents["@graph"] = graph
    return contents


def save_jsonld_file(file_path, graph, context=None, graph_id=None, **kwargs):
    contents = get_graph_dict(graph, graph_id=graph_id, context=context)
    save_json(file_path, contents)


def get_jsonld_frame(model_path, frame_path, output_path=None):
    from pyld import jsonld

    model = load_json(model_path)
    frame = load_json(frame_path)

    framed_doc = jsonld.frame(model, frame, options={"omitGraph": False})

    if output_path:
        save_json(output_path, framed_doc)
    else:
        print(framed_doc)

    return framed_doc
