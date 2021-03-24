"""Representation of avro schema types."""
from contextlib import suppress
from enum import Enum as _Enum, auto, unique
from typing import NamedTuple, List, Union, Optional, Any, NewType, Dict


def case_insensitive(cls):
    """
    Add case-insensitive .get method to Enum. This is so we can conveniently
    resolve names like `time-micros` in the avro schema into their enum member.
    """
    @classmethod
    def get(cls_, value):
        return cls_[value.upper().replace('-', '_')]  # pylint: disable=unsubscriptable-object
    cls.get = get
    return cls


DefinedType = NewType('DefinedType', str)  # http://avro.apache.org/docs/1.10.0/spec.html#schemas


@case_insensitive
@unique
class Primitives(_Enum):
    """http://avro.apache.org/docs/1.10.0/spec.html#schema_primitive"""
    NULL = auto()
    BOOLEAN = auto()
    INT = auto()
    LONG = auto()
    FLOAT = auto()
    DOUBLE = auto()
    BYTES = auto()
    STRING = auto()


@case_insensitive
@unique
class LogicalTypes(_Enum):
    DECIMAL = auto()
    DATE = auto()
    TIME_MILLIS = auto()
    TIME_MICROS = auto()
    TIMESTAMP_MILLIS = auto()
    TIMESTAMP_MICROS = auto()
    DURATION = auto()
    UUID = auto()


class LogicalType(NamedTuple):
    type: Primitives
    logical_type: LogicalTypes
    precision: Optional[int] = None
    scale: Optional[int] = None


AvroPrimitives = Union[Primitives, LogicalType]
AvroType = Union[AvroPrimitives, NamedTuple, List, DefinedType]


class Record(NamedTuple):
    """http://avro.apache.org/docs/1.10.0/spec.html#Records"""
    original_schema: Dict
    name: str
    namespace: str
    fields: List['Field']
    doc: Optional[str] = None
    aliases: List[str] = []


class Field(NamedTuple):
    name: str
    type: AvroType


class Enum(NamedTuple):
    """http://avro.apache.org/docs/1.10.0/spec.html#Enums"""
    name: str
    namespace: str
    symbols: List[str]
    aliases: List[str] = []
    doc: Optional[str] = None
    default: Optional[str] = None


class Array(NamedTuple):
    """http://avro.apache.org/docs/1.10.0/spec.html#Arrays"""
    items: AvroType
    default: Optional[Any] = None


class Map(NamedTuple):
    """http://avro.apache.org/docs/1.10.0/spec.html#Maps"""
    values: AvroType
    default: Optional[Any] = None  # technically has to have the type specified by "items", but hard to capture


class Fixed(NamedTuple):
    """http://avro.apache.org/docs/1.10.0/spec.html#Fixed"""
    name: str
    namespace: str
    size: int
    aliases: List[str] = []


def parse_into_types(schema: Union[Dict[str, Any], str, List], parent_namespace: Optional[str] = None) \
        -> Union[Primitives, DefinedType, List, LogicalType, Fixed, Enum, Array, Map, Record]:
    """Parse JSON-represented avro schema into internal representation."""
    if isinstance(schema, str):
        with suppress(KeyError):
            return Primitives.get(schema)  # pylint: disable=no-member
        return DefinedType(
            schema
            if '.' in schema or not parent_namespace
            # "[...] if they do not contain a dot, the namespace is the namespace of the enclosing definition"
            # - http://avro.apache.org/docs/1.10.0/spec.html#names
            else f'{parent_namespace}.{schema}'
        )

    if isinstance(schema, list):
        return [
            parse_into_types(item, parent_namespace=parent_namespace)
            for item in schema
        ]

    if not isinstance(schema, dict):
        raise ValueError(f"Expected dict type, got `{type(schema)}` (in schema: `{schema}`)")

    type_name = schema['type']
    namespace = schema.get('namespace', parent_namespace)

    if 'logicalType' in schema:
        return LogicalType(
            type=Primitives.get(type_name),  # pylint: disable=no-member
            logical_type=LogicalTypes.get(schema['logicalType']),  # pylint: disable=no-member
            precision=schema.get('precision', None),
            scale=schema.get('scale', None),
        )

    if type_name == 'fixed':
        return Fixed(
            name=schema['name'],
            namespace=schema['namespace'],
            size=schema['size'],
            aliases=schema.get('aliases', [])
        )

    if type_name == 'enum':
        return Enum(
            name=schema['name'],
            namespace=namespace,
            symbols=schema['symbols'],
            aliases=schema.get('aliases', []),
            doc=schema.get('doc'),
            default=schema.get('default', None)
        )

    if type_name == 'array':
        return Array(
            items=parse_into_types(
                schema['items'],
                parent_namespace=namespace
            ),
            default=schema.get('default', None)
        )

    if type_name == 'map':
        return Map(
            values=parse_into_types(
                schema['values'],
                parent_namespace=namespace
            ),
            default=schema.get('default', None)
        )

    if type_name == 'record':
        return Record(
            original_schema=schema,
            name=schema['name'],
            namespace=namespace,
            fields=[
                Field(
                    name=field['name'],
                    type=parse_into_types(
                        field['type'],
                        parent_namespace=namespace
                    )
                )
                for field in schema.get('fields', ())
            ],
            doc=schema.get('doc'),
            aliases=schema.get('aliases', [])
        )

    with suppress(KeyError):
        # alternative representation permitted in http://avro.apache.org/docs/1.10.0/spec.html#schema_primitive
        return Primitives.get(type_name)  # pylint: disable=no-member

    return DefinedType(
        type_name
        if '.' in type_name or not parent_namespace  # same hack as above
        else f'{parent_namespace}.{type_name}'
    )
