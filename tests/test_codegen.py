"""Tests for avro2py/codegen.py"""
import ast
import json
import os
from pathlib import Path

import astor
import pytest

import avro2py.codegen as codegen
from avro2py.avro_types import parse_into_types

TEST_PATH = Path(os.path.dirname(__file__))
TEST_SCHEMAS = json.load((TEST_PATH / 'sample_schema.avsc').open('r'))


@pytest.mark.parametrize('from_namespace, to_namespace, name, expected', [
    ('marketprice.messages.nile.mws', 'marketprice.messages.nile.mws', 'GetMatchingProductForId.ImageData', ('GetMatchingProductForId.ImageData', None)),
    ('marketprice.messages.historical.replay', 'marketprice.pubsub', 'S3FileDescriptor', ('S3FileDescriptor', ast.ImportFrom(module='pubsub', names=[ast.alias(name='S3FileDescriptor', asname=None)], level=3))),
    ('marketprice.messages.targeting_recommendation_engine', 'marketprice.messages.targeting_recommendation_engine', 'TargetingRecommendation.Predicate', ('TargetingRecommendation.Predicate', None))
])
def test_bridge_namespaces(from_namespace, to_namespace, name, expected):
    expected_name, expected_import = expected

    str_node, actual_import = codegen.RewriteCrossReferenceStrings.bridge_namespaces(
        from_namespace=from_namespace.split('.'),
        to_namespace=to_namespace.split('.'),
        target_name=name.split('.'),
    )
    actual_name = str_node.s

    both_imports_are_none = expected_import is None and actual_import is None
    assert actual_name == expected_name and (
        both_imports_are_none
        or ast.dump(expected_import) == ast.dump(actual_import)  # equality doesn't work for AST nodes
    )


def test_populate_namespaces_produces_roundtrippable_modules():
    populated_schemas = codegen.populate_namespaces(
        parse_into_types(schema)
        for schema in TEST_SCHEMAS
    )

    for _, module in populated_schemas:
        source = astor.to_source(module)
        assert isinstance(ast.parse(source), ast.Module)


def test_inline_avro_schema_of_nested_record():
    populated_schemas = codegen.populate_namespaces(
        parse_into_types(schema)
        for schema in TEST_SCHEMAS
    )
    adgroup_created_class_def, = (
        element
        for schema in populated_schemas
        for element in schema[1].body
        if hasattr(element, 'name') and element.name.endswith('AdgroupCreated')
    )

    # get the variable definition of _original_schema 
    t, = (obj for obj in adgroup_created_class_def.body if isinstance(obj, ast.Assign))
    _original_schema = t.value.s
    # verify that the avro schema of AdGroupCreated should not have not reference.
    schema_dict = json.loads(_original_schema)
    advertising_type = schema_dict['fields'][0]
    assert isinstance(advertising_type['type'], dict)
