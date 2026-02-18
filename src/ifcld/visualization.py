import os
import subprocess

from jinja2 import Environment, BaseLoader
from rdflib import Graph

from ifcld.query import full_project_spatial_decomposition, spatial_containment

TEMPLATE = """
digraph G {
compound=true;
splines=polyline;
fontsize="10";
node[shape=box, style=rounded];
{% for k, c in model.items() -%}
  {{ c.child }} [label="{{ c.child }}\\nType: {{c.child_type}}\\nComp.: {{c.get("comp_type")}}{% if c.get("elevation") %}\\nElevation: {{ c.get("elevation") |replace("_","-") }}{% endif %}", group="{{c.parent}}"];
  {% if c.parent %}
  {{ c.parent }} -> {{ c.child }} [weight=8, headport="n", tailport="s"];
  {% endif %}
  {% if c.child_contains %}
  subgraph cluster_{{ c.child }} {
  label="{{ c.child }}";
  fontsize="8";
  {% for p, t in c.child_contains %}
  {{ p }} [label="{{ p }}\\nType: {{ t }}", fontsize="8", group="{{c.child}}"];
  {% endfor %}
  };
  {{ c.child }} -> {{ c.child_contains[0][0] }} [weight=8, lhead=cluster_{{ c.child}}, headport="n", tailport="s" ];
  {% endif %}
{% endfor %}
};
"""
# { rank=same; {% for p, t in c.child_contains %}{{ p }} {% endfor %} };

SD_TEMPLATE = """
digraph G {
node[shape=box];
splines=line;
{% for k, c in model.items() -%}
  {{ c.child }} [label="{{ c.child }}\nType: {{c.child_type}}\nComposition: {{c.get("comp_type")}}"]
{% endfor %}
};
"""


def load_template(template_string):
    rtemplate = Environment(loader=BaseLoader).from_string(template_string)
    return rtemplate


def visualize_spatial_decomposition(model_path, **kwargs):
    def simplify_node_name(node_name):
        return os.path.basename(node_name).replace("-", "_").replace("#", "_")

    g = Graph()
    g.parse(model_path, format="json-ld")

    output_path = kwargs.get("output_path")
    template = load_template(TEMPLATE)
    file_name = "spatial_decomposition"

    file_gv = "{:s}.gv".format(file_name)
    file_pdf = "{:s}.pdf".format(file_name)
    dot_file_path = os.path.join(output_path, file_gv)
    pdf_file_path = os.path.join(output_path, file_pdf)

    spatial_decomposition = {}
    qres = g.query(full_project_spatial_decomposition)
    spatial_elements = [
        "IFCPROJECT",
        "IFCSITE",
        "IFCBUILDING",
        "IFCBUILDINGSTOREY",
        "IFCSPACE",
    ]
    for r in qres:
        d = r.asdict()
        cont_res = g.query(spatial_containment, initBindings={"element": d["child"]})
        if len(cont_res) == 0:
            contains = []
        else:
            contains = [
                (simplify_node_name(c), simplify_node_name(t)) for c, t in cont_res
            ]
        d = {k: simplify_node_name(v) for k, v in d.items()}
        if d.get("child_type") not in spatial_elements:
            continue
        spatial_decomposition[d["child"]] = d

    # Since we are looping over child nodes, we need to add  the nodes that don't have a parent as children
    # E.g., IFCPROJECT will show up as "parent" for some nodes,
    # but isn't a "child" in the query results
    orphans = {}
    for k, v in spatial_decomposition.items():
        if v["parent"] not in spatial_decomposition.keys():
            print(k, v)
            o = {
                "child": v["parent"],
                "child_type": v["parent_type"],
            }
            orphans[v["parent"]] = o

    spatial_decomposition.update(**orphans)
    contents = template.render(model=spatial_decomposition)
    with open(dot_file_path, "w") as f:
        f.write(contents)

    cmd = ["dot", "-Tpdf", dot_file_path, "-o", pdf_file_path]
    subprocess.Popen(cmd).communicate()
