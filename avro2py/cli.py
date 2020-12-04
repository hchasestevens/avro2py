"""Command-line interface for avro2py."""
import argparse
import json
import sys
import traceback

from avro2py.avro_types import parse_into_types
from avro2py.codegen import populate_namespaces
from avro2py.rendering import render_modules

PARSER = argparse.ArgumentParser()
PARSER.add_argument('schemas', nargs='+', help='Paths to AVSC schemas to generate code for.')


def generate_code(schema_paths) -> int:
    """Generate code, writing to file."""
    schemas = []
    for schema_path in schema_paths:
        with open(schema_path) as f:
            contents = json.load(f)
        if not isinstance(contents, list):
            raise Exception(
                f"Error when parsing schema file `{schema_path}`: expected list of schema definitions."
            )
        schemas.extend(contents)

    parsed_schemas = [parse_into_types(schema) for schema in schemas]
    namespaces = populate_namespaces(parsed_schemas)
    for path, module_contents in sorted(render_modules(namespaces).items()):
        print("Rendering:", path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as f:
            f.write(module_contents)

    return 0


def main():
    """Entrypoint for CLI."""
    args = PARSER.parse_args()
    try:
        exit_code = generate_code(schema_paths=args.schemas)
    except:
        print(traceback.format_exc())
        exit_code = 1
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
