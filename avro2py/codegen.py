""" Avro codegen for Python 3. """

import ast
import itertools
import json
import re
from collections import defaultdict
from contextlib import contextmanager
from textwrap import wrap
from typing import NamedTuple, List, Union, Generator, Tuple, Optional, Dict

from avro2py.avro_types import (
    Primitives, LogicalTypes, Record, AvroPrimitives, DefinedType, Enum, Array,
    Map, Fixed, LogicalType,
)
from avro2py.utils import VERSION

PRIMITIVE_TYPE_MAPPINGS = {
    Primitives.NULL: 'None',
    Primitives.BOOLEAN: 'bool',
    Primitives.INT: 'int',
    Primitives.LONG: 'int',  # *
    Primitives.FLOAT: 'float',
    Primitives.DOUBLE: 'float',  # *
    Primitives.BYTES: 'bytes',
    Primitives.STRING: 'str',
}

LOGICAL_TYPE_MAPPINGS = {
    LogicalTypes.DECIMAL: ['decimal', 'decimal.Decimal'],
    LogicalTypes.DATE: ['datetime', 'datetime.date'],
    LogicalTypes.TIME_MILLIS: ['datetime', 'datetime.time'],
    LogicalTypes.TIME_MICROS: ['datetime', 'datetime.time'],
    LogicalTypes.TIMESTAMP_MILLIS: ['datetime', 'datetime.datetime'],
    LogicalTypes.TIMESTAMP_MICROS: ['datetime', 'datetime.datetime'],
    LogicalTypes.DURATION: ['datetime', 'datetime.timedelta'],
    LogicalTypes.UUID: ['uuid', 'uuid.UUID'],
}


NODE_CLASS_CONVERTERS = {}


def node_converter(fn):
    avro_type, = {v for k, v in fn.__annotations__.items() if k != 'return'}
    NODE_CLASS_CONVERTERS[avro_type] = fn
    return fn


class ResolvedClassResult(NamedTuple):
    resolved_class: ast.ClassDef
    imports: List[Union[ast.Import, ast.ImportFrom]]
    new_frontier: List[Union[Record, Enum]]


class Namespace(NamedTuple):
    node: ast.AST  # could be protocol - needs `.body`
    imports: List[Union[ast.Import, ast.ImportFrom]]


def consolidate_imports(imports: List[Union[ast.Import, ast.ImportFrom]]) -> List[ast.Expr]:
    """Deduplicate and combine imports, leaving smallest possible set."""
    deduped_imports = [
        node
        for repr_, node in sorted({
            ast.dump(node): node
            for node in imports
        }.items())
    ]

    def group_key(node):
        module = getattr(node, 'module', None)
        level = getattr(node, 'level', None)
        return module, level

    consolidated_imports = []
    for (module, level), group in itertools.groupby(deduped_imports, key=group_key):
        if module is None:  # ast.Import
            consolidated_imports.extend(group)
            continue

        # ast.ImportFrom
        all_names = sorted(
            name.name
            for node in group
            for name in node.names
        )
        combined_import = ast.ImportFrom(
            module=module,
            names=[
                ast.alias(name=name, asname=None)
                for name in all_names
            ],
            level=level if level is not None else 0
        )
        consolidated_imports.append(combined_import)

    return [ast.Expr(value=import_node) for import_node in consolidated_imports]


def docstring_declaration(doc: str) -> ast.Expr:
    """Sensibly format docstring into AST node."""
    formatted_doc = '\n'.join(wrap(
        doc,
        width=80,
        break_on_hyphens=False,
    ))
    return ast.Expr(value=ast.Str(s=f'\n{formatted_doc}\n\n'))


def locate_new_class_definitions(field_type: Union[AvroPrimitives, DefinedType, Record, Enum, Array, Map, Fixed]) \
        -> Generator[Union[Record, Enum], None, None]:
    """Locate next level of class definitions (do not recur through Records)."""

    if isinstance(field_type, (Record, Enum)):
        # these need to be rendered as classes
        yield field_type
        return

    if isinstance(field_type, Array):
        yield from locate_new_class_definitions(field_type.items)
        return

    if isinstance(field_type, Map):
        yield from locate_new_class_definitions(field_type.values)

    if isinstance(field_type, list):
        for item in field_type:
            yield from locate_new_class_definitions(item)
        return

    return  # not a nested type


@node_converter
def record_to_class(record: Record) -> ResolvedClassResult:
    """Convert Record into AST class definition."""
    imports = [
        ast.ImportFrom(  # from typing import NamedTuple
            module='typing',
            names=[ast.alias(name='NamedTuple', asname=None)],
            level=0
        ),
    ]

    class_body = []

    if record.doc is not None:
        class_body.append(docstring_declaration(record.doc))

    new_frontier = []
    fields = []
    for field in record.fields:
        new_frontier.extend(locate_new_class_definitions(field.type))

        field_def = ast.AnnAssign(
            target=ast.Name(id=field.name),
            annotation=resolve_field_type(
                field.type,
                required_imports=imports,
            ),
            value=None,  # TODO - default value goes here
            simple=1,
        )
        fields.append(field_def)

    class_body.extend(fields)
    class_body.append(
        ast.Assign(  # _original_schema = "..."
            targets=[ast.Name(id='_original_schema')],
            value=ast.Str(s=json.dumps(record.original_schema))
        )
    )

    class_def = ast.ClassDef(
        name=record.name,
        bases=[ast.Name(id='NamedTuple')],
        keywords=[],
        body=class_body,
        decorator_list=[]
    )

    return ResolvedClassResult(
        resolved_class=class_def,
        imports=imports,
        new_frontier=new_frontier,
    )


def render_enum_name(symbol_name: str) -> ast.Name:
    """Render enum symbols into Pythonic equivalents."""
    formatted_name = re.sub('([A-Z]+)', r'_\1', symbol_name).upper().strip('_')
    return ast.Name(id=formatted_name)


@node_converter
def enum_to_class(enum: Enum) -> ResolvedClassResult:
    """Convert Enum into AST class definition."""
    enum_import = ast.Import(names=[ast.alias(name='enum', asname=None)])
    class_body = []

    if enum.doc:
        class_body.append(docstring_declaration(enum.doc))

    members = [
        ast.Expr(value=ast.Assign(
            targets=[render_enum_name(symbol)],
            value=ast.Str(s=symbol)
        ))
        for symbol in enum.symbols
    ]
    class_body.extend(sorted(members, key=lambda e: e.value.value.s))

    enum_class = ast.ClassDef(
        name=enum.name,
        bases=[ast.Attribute(value=ast.Name(id='enum'), attr='Enum')],
        keywords=[],
        body=class_body,
        decorator_list=[ast.Attribute(value=ast.Name(id='enum'), attr='unique')]  # just for signalling purposes
    )
    return ResolvedClassResult(
        resolved_class=enum_class,
        imports=[enum_import],
        new_frontier=[],
    )


def from_typing(name: str) -> ast.ImportFrom:
    """Import from the typing module."""
    return ast.ImportFrom(module='typing', names=[ast.alias(name=name, asname=None)], level=0)


def resolve_field_type(field_type: Union[AvroPrimitives, DefinedType, Record, Enum, Array, Map, Fixed],
                       required_imports: List[Union[ast.Import, ast.ImportFrom]]) -> ast.AST:
    """Resolve the requisite type annotation for a supplied field type."""
    if isinstance(field_type, Primitives):
        # http://avro.apache.org/docs/1.10.0/spec.html#schema_primitive
        return ast.Name(id=PRIMITIVE_TYPE_MAPPINGS[field_type])

    if isinstance(field_type, str):
        # DefinedType case
        return ast.Str(s=field_type)

    if isinstance(field_type, list):
        # http://avro.apache.org/docs/1.10.0/spec.html#Unions
        if len(field_type) == 2 and Primitives.NULL in field_type:
            # special case of 'optional'
            _, nested_type = field_type
            required_imports.append(from_typing('Optional'))
            return ast.Subscript(
                value=ast.Name(id='Optional'),
                slice=ast.Index(
                    value=resolve_field_type(
                        nested_type,
                        required_imports=required_imports,
                    )
                )
            )

        required_imports.append(from_typing('Union'))
        return ast.Subscript(
            value=ast.Name(id='Union'),
            slice=ast.Index(value=ast.Tuple(elts=[
                resolve_field_type(
                    nested_field,
                    required_imports=required_imports,
                )
                for nested_field in field_type
            ]))
        )

    if isinstance(field_type, Map):
        # http://avro.apache.org/docs/1.10.0/spec.html#Maps
        required_imports.append(from_typing('Dict'))
        return ast.Subscript(
            value=ast.Name(id='Dict'),
            slice=ast.Index(value=ast.Tuple(elts=[
                ast.Name(id='str'),
                resolve_field_type(
                    field_type.values,
                    required_imports=required_imports,
                ),
            ]))
        )

    if isinstance(field_type, Array):
        # http://avro.apache.org/docs/1.10.0/spec.html#Arrays
        required_imports.append(from_typing('List'))
        return ast.Subscript(
            value=ast.Name(id='List'),
            slice=ast.Index(
                value=resolve_field_type(
                    field_type.items,
                    required_imports=required_imports,
                )
            )
        )

    if isinstance(field_type, Fixed):
        # http://avro.apache.org/docs/1.10.0/spec.html#Fixed
        return ast.Name(id='bytes')

    if isinstance(field_type, LogicalType):
        import_module, type_ = LOGICAL_TYPE_MAPPINGS[field_type.logical_type]
        required_imports.append(
            ast.Import(names=[ast.alias(name=import_module, asname=None)])
        )
        return ast.Name(id=type_)

    if isinstance(field_type, (Record, Enum)):
        if field_type.namespace:
            return ast.Str(s="{0.namespace}.{0.name}".format(field_type))  # this is mutated/imported at a later date
        # TODO - is this case legal/reachable...?
        return ast.Str(s=field_type.name)

    raise ValueError(f"Didn't know how to handle field type `{field_type}`")


class ModuleAwareNodeTransformer(ast.NodeTransformer):
    """Base class for NodeTransformers which need module/global context."""
    def __init__(self, namespaces: Dict[str, Tuple[ast.AST, List[Union[ast.Import, ast.ImportFrom]]]]):
        super(ModuleAwareNodeTransformer, self).__init__()
        self.namespaces = namespaces
        self.module_namespace: Optional[str] = None
        self.module_imports: Optional[List[Union[ast.Import, ast.ImportFrom]]] = None

    @contextmanager
    def rewriter(self, module_namespace: str, module_imports: List[Union[ast.Import, ast.ImportFrom]]):
        self.module_namespace = module_namespace
        self.module_imports = module_imports
        try:
            yield self
        finally:
            self.module_namespace = None
            self.module_imports = None


class RewriteCrossReferenceStrings(ModuleAwareNodeTransformer):
    """Used to rewrite deferred type annotations within an AnnAssign node."""

    @staticmethod
    def bridge_namespaces(from_namespace: List[str], to_namespace: List[str], target_name: List[str]) \
            -> Tuple[ast.Str, Optional[ast.ImportFrom]]:
        """
        Given two module namespaces and a desired annotation, find the path to
        import the required object from its module.
        """
        paired_components = itertools.zip_longest(from_namespace, to_namespace)
        for from_component, to_component in paired_components:
            if from_component != to_component:
                break
        else:
            return ast.Str(s='.'.join(target_name)), None
        paired_components = list(paired_components)
        try:
            partial_remaining_from_components, partial_remaining_to_components = zip(*paired_components)
        except ValueError:
            partial_remaining_from_components = ()
            partial_remaining_to_components = ()
        paired_remaining_from_components = from_component, *partial_remaining_from_components
        paired_remaining_to_components = to_component, *partial_remaining_to_components
        remaining_from_components = [c for c in paired_remaining_from_components if c is not None]
        remaining_to_components = [c for c in paired_remaining_to_components if c is not None]

        if remaining_from_components:
            import_node = ast.ImportFrom(
                module='.'.join(remaining_to_components),
                names=[ast.alias(name=target_name[0], asname=None)],
                level=len(remaining_from_components)
            )
            name = ast.Str(s='.'.join(target_name))
        else:
            import_node = None
            name = ast.Str(
                s='.'.join(itertools.chain(remaining_to_components, target_name))
            )

        return name, import_node

    def visit_Str(self, node: ast.Str) -> ast.Str:
        if '.' not in node.s:
            return node

        remaining_components = node.s.split('.')
        desired_name_components = []
        while remaining_components and not isinstance(self.namespaces['.'.join(remaining_components)][0], ast.Module):
            desired_name_components.insert(0, remaining_components.pop())
        if not remaining_components:
            raise RuntimeError("Unexpected case.")

        new_node, possible_import = self.bridge_namespaces(
            from_namespace=self.module_namespace.split('.'),
            to_namespace=remaining_components,
            target_name=desired_name_components,
        )
        if possible_import is not None:
            self.module_imports.append(possible_import)

        return new_node


class RewriteCrossReferenceAnnotations(ModuleAwareNodeTransformer):
    """Used to rewrite type deferred type annotations, from the module-level."""

    def visit_AnnAssign(self, node: ast.AnnAssign) -> ast.AnnAssign:
        transformer = RewriteCrossReferenceStrings(namespaces=self.namespaces)
        with transformer.rewriter(module_namespace=self.module_namespace, module_imports=self.module_imports) as rewriter:
            return rewriter.visit(node)


def populate_namespaces(schemas: List[Record]) -> Generator[Tuple[str, ast.Module], None, None]:
    """Convert internal Record representations into renderable AST module nodes."""
    namespace_nodes = defaultdict(lambda: Namespace(
        node=ast.Module(body=[]),
        imports=[],
    ))

    def frontier_sorting_key(s):
        return s.namespace not in namespace_nodes, s.namespace

    frontier = sorted(schemas, key=frontier_sorting_key)
    while frontier:
        schema = frontier.pop()
        schema_fully_qualified_name = f'{schema.namespace}.{schema.name}'
        if schema_fully_qualified_name in namespace_nodes:
            continue

        parent_namespace = namespace_nodes[schema.namespace]

        converter = NODE_CLASS_CONVERTERS.get(schema.__class__)
        if converter is None:
            raise ValueError(f"Unknown schema type: `{type(schema)}` (in schema `{schema}`)")

        result = converter(schema)
        resolved_class = result.resolved_class
        parent_namespace.node.body.append(resolved_class)
        parent_namespace.imports.extend(result.imports)
        frontier.extend(result.new_frontier)
        namespace_nodes[schema_fully_qualified_name] = Namespace(
            node=resolved_class,
            imports=parent_namespace.imports  # n.b. multiple pointers to same object
        )

        frontier = sorted(frontier, key=frontier_sorting_key)

    # Sometimes there are implicit namespaces that are children of classes, and
    # hence themselves need to be classes - but have been instantiated as
    # modules. The below loop fixes this.
    while True:
        modules_to_convert = [
            (namespace_name, namespace)
            for namespace_name, namespace in namespace_nodes.items()
            if isinstance(namespace.node, ast.Module)
            if any(
                parent_namespace in namespace_nodes
                and isinstance(namespace_nodes[parent_namespace].node, ast.ClassDef)
                for parent_namespace in itertools.accumulate(
                    namespace_name.split('.')[:-1],
                    func='{}.{}'.format
                )
            )
        ]
        if not modules_to_convert:
            break

        for namespace_name, namespace in modules_to_convert:
            *parent_namespace_components, name = namespace_name.split('.')

            new_class = ast.ClassDef(
                name=name,
                bases=[],
                keywords=[],
                body=namespace.node.body,
                decorator_list=[]
            )

            parent_namespace_name = '.'.join(parent_namespace_components)
            if parent_namespace_name not in namespace_nodes:
                namespace_nodes[parent_namespace_name] = Namespace(
                    node=ast.Module(body=[]),
                    imports=namespace.imports,  # need this to be the same referent, so can't rely on defaultdict
                )
            parent_namespace = namespace_nodes[parent_namespace_name]
            parent_namespace.node.body.append(new_class)

            namespace_nodes[namespace_name] = Namespace(
                node=new_class,
                imports=namespace.imports,
            )

    node_transformer = RewriteCrossReferenceAnnotations(namespaces=namespace_nodes)
    for namespace_name, namespace in namespace_nodes.items():
        if not isinstance(namespace.node, ast.Module):
            continue

        # transform fully-qualified internal cross-reference forward annotations
        # to relative (resolvable) forward annotations, adding any necessary imports
        with node_transformer.rewriter(module_namespace=namespace_name, module_imports=namespace.imports) as rewriter:
            node = rewriter.visit(namespace.node)

        module_docstring = ast.Expr(value=ast.Str(
            s=f'Schema definitions for `{namespace_name}` namespace. Generated by avro2py v.{VERSION}.'
        ))
        yield namespace_name, ast.Module(
            body=[module_docstring] + consolidate_imports(namespace.imports) + node.body,
        )
