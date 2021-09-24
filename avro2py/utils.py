"""Common utilities."""
import decimal
import datetime
from enum import EnumMeta, Enum
from functools import reduce
from pathlib import Path
from typing import NamedTuple, Dict, Union, Any, Callable, get_type_hints, List
from uuid import UUID

import avro.io
import avro.schema


PACKAGE_DIR = Path(__file__).parent
VERSION_PATH = PACKAGE_DIR / 'VERSION'
with VERSION_PATH.open('r') as f:
    VERSION = f.read().strip()


AvroDictType = Dict[
    str,
    Union[str, int, float, decimal.Decimal, datetime.datetime, datetime.date, datetime.time, Dict[str, Any]]
]


_CONVERTERS_TO_AVRO = []


def compose(*fns: Callable) -> Callable:
    return reduce(lambda f, g: lambda x: f(g(x)), fns)


@_CONVERTERS_TO_AVRO.append
def _safe_convert_enum(v: Union[Enum, Any]) -> Union[str, any]:
    if isinstance(getattr(v, '__class__', None), EnumMeta):
        return v.value
    return v


@_CONVERTERS_TO_AVRO.append
def _safe_convert_uuid(v: Union[UUID, Any]) -> Union[bytes, any]:
    if isinstance(v, UUID):
        return str(v)
    return v


@_CONVERTERS_TO_AVRO.append
def _safe_convert_namedtuple(v: Union[NamedTuple, Any]) -> Union[AvroDictType, Any]:
    if hasattr(v, '_asdict'):
        return to_avro_dict(v)
    return v


@_CONVERTERS_TO_AVRO.append
def _safe_convert_list(v: Union[List, Any]) -> Union[AvroDictType, Any]:
    if isinstance(v, list) and len(v) and hasattr(v[0], '_asdict'):
        return [to_avro_dict(ele) for ele in v]
    return v


_convert_types_to_avro = compose(*_CONVERTERS_TO_AVRO)


def to_avro_dict(record: NamedTuple) -> AvroDictType:
    """Convert record to Avro dict representation."""
    return {
        k: _convert_types_to_avro(v)
        for k, v in record._asdict().items()
    }


def from_avro_dict(avro_dict: AvroDictType, record_type: type) -> NamedTuple:
    """Convert Avro dict representation to specified type."""
    annotations = get_type_hints(record_type)
    conversions = {}
    for field_name, value in avro_dict.items():
        annotation = annotations[field_name]

        if is_type_union(annotation):
            annotation_record_types = (
                t
                for t in annotation.__args__
                if hasattr(t, '_asdict')
            )
            for annotation_record_type in annotation_record_types:
                parsed_schema = avro.schema.parse(annotation_record_type._original_schema)
                if avro.io.validate(parsed_schema, value):
                    annotation = annotation_record_type

        if hasattr(annotation, '_asdict'):
            conversions[field_name] = from_avro_dict(value, record_type=annotation)

        elif annotation is UUID:
            conversions[field_name] = UUID(value) if not isinstance(value, UUID) else value

        elif isinstance(annotation, EnumMeta):
            values_to_members = {
                member.value: member
                for member in annotation.__members__.values()
            }
            conversions[field_name] = values_to_members[value]

    new_dict = {**avro_dict, **conversions}
    return record_type(**new_dict)


def is_type_union(type):
    """Return True if the type annotation is Union"""
    # every type annotation has __origin__ attribute
    return hasattr(type, '__origin__') and type.__origin__ is Union
