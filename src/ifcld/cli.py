import os
import click

from ifcld.transformations import transform_ifc_to_jsonld


@click.command()
@click.option(
    "-f",
    "--from",
    "model_path",
    type=click.Path(exists=True, resolve_path=True),
    required=True,
    # multiple=True,
    help="Path for the input model",
)
@click.option(
    "-o",
    "--output-path",
    type=click.Path(exists=True, resolve_path=True),
    default=os.path.join("."),
    help="Output path for generated model",
)
def ifcld(model_path, output_path):
    """CLI for the ifcld transformations"""

    transform_ifc_to_jsonld(model_path, output_path)


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]

    ifcld.main(args=args)
