import ast
from contextlib import suppress
from pathlib import Path
from typing import Iterable, Tuple, Dict

import astor
from black import Mode, TargetVersion, format_file_contents, NothingChanged

BLACK_MODE = Mode(
    target_versions={TargetVersion.PY36},
    line_length=88,  # default value
    is_pyi=False,  # for rendering type stubs
    string_normalization=True,
    experimental_string_processing=True,  # n.b. noted to occasionally cause crashes
)


def black_format(s: str):
    """Perform code formatting on unformatted source code."""
    return format_file_contents(
        s,
        fast=False,
        mode=BLACK_MODE,
    )


def render_module(module: ast.Module) -> str:
    """Transform AST module into source code."""
    source = astor.to_source(module)
    with suppress(NothingChanged):
        source = black_format(source)
    return source


def render_ipython(node):
    """Convenience method for rendering AST node in IPython environment."""
    from IPython.display import display, Code  # pylint: disable=import-error
    display(Code(render_module(node), language='python'))


def render_modules(modules: Iterable[Tuple[str, ast.Module]]) -> Dict[Path, str]:
    """Render populated modules into requisite file contents, paired with paths."""
    rendered = dict()
    discovered_directories = set()
    for module_name, module_node in modules:
        module_path = Path(f"{module_name.replace('.', '/')}.py")
        discovered_directories.update(
            parent_dir
            for parent_dir in module_path.parents
            if parent_dir.parts
        )
        rendered[module_path] = render_module(module_node)

    for discovered_directory in discovered_directories:
        contents = f'''"""`{'.'.join(discovered_directory.parts)}` namespace."""\n'''
        rendered[discovered_directory / '__init__.py'] = contents

    init_paths = [path for path in rendered if path.name == '__init__.py']
    for init_path in init_paths:
        conflicting_path = init_path.parent.with_suffix(".py")
        if conflicting_path not in rendered:
            continue
        rendered[init_path] = rendered[conflicting_path]
        del rendered[conflicting_path]

    return rendered
