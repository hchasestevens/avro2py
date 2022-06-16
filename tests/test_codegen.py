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


@pytest.mark.parametrize('from_namespace, to_namespace, other_namespaces, name, expected', [
    ('marketprice.messages.nile.mws', 'marketprice.messages.nile.mws', [], 'GetMatchingProductForId.ImageData', ('GetMatchingProductForId.ImageData', None)),
    ('marketprice.messages.historical.replay', 'marketprice.pubsub', [], 'S3FileDescriptor', ('S3FileDescriptor', ast.ImportFrom(module='pubsub', names=[ast.alias(name='S3FileDescriptor', asname=None)], level=3))),
    ('marketprice.messages.targeting_recommendation_engine', 'marketprice.messages.targeting_recommendation_engine', [], 'TargetingRecommendation.Predicate', ('TargetingRecommendation.Predicate', None)),
    ('foo.a', 'foo', ['foo.a.other'], 'Beta', ('Beta', ast.ImportFrom(module='', names=[ast.alias(name='Beta', asname=None)], level=2))),
    ('foo.a', 'foo', ['bar', 'bar.baz.a', 'bar.foo.a.s'], 'Beta', ('Beta', ast.ImportFrom(module='', names=[ast.alias(name='Beta', asname=None)], level=1))),
    ('foo.a', 'foo', ['bar', 'bar.baz.a', 'bar.foo.a.s', 'foo.a.other'], 'Beta', ('Beta', ast.ImportFrom(module='', names=[ast.alias(name='Beta', asname=None)], level=2)))
])
def test_bridge_namespaces(from_namespace, to_namespace, other_namespaces, name, expected):
    expected_name, expected_import = expected

    namespaces = {ns: () for ns in other_namespaces + [from_namespace, to_namespace]}

    rewriter = codegen.RewriteCrossReferenceStrings(namespaces=namespaces)

    str_node, actual_import = rewriter.bridge_namespaces(
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
