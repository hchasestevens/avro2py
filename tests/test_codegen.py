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


@pytest.mark.parametrize('from_namespace, to_namespace, namespaces_with_children, name, expected', [
    ('marketprice.messages.nile.mws', 'marketprice.messages.nile.mws', frozenset(), 'GetMatchingProductForId.ImageData', ('GetMatchingProductForId.ImageData', None)),
    ('marketprice.messages.historical.replay', 'marketprice.pubsub', frozenset(), 'S3FileDescriptor', ('S3FileDescriptor', ast.ImportFrom(module='pubsub', names=[ast.alias(name='S3FileDescriptor', asname=None)], level=3))),
    ('marketprice.messages.targeting_recommendation_engine', 'marketprice.messages.targeting_recommendation_engine', frozenset(), 'TargetingRecommendation.Predicate', ('TargetingRecommendation.Predicate', None)),
    ('foo.a', 'foo', frozenset([('foo', 'a')]), 'Beta', ('Beta', ast.ImportFrom(module='', names=[ast.alias(name='Beta', asname=None)], level=2))),
    ('foo.a', 'foo', frozenset([('bar',), ('bar', 'baz'), ('bar', 'foo', 'a')]), 'Beta', ('Beta', ast.ImportFrom(module='', names=[ast.alias(name='Beta', asname=None)], level=1))),
    ('foo.a', 'foo', frozenset([('bar',), ('bar', 'baz'), ('bar', 'foo', 'a'), ('foo', 'a')]), 'Beta', ('Beta', ast.ImportFrom(module='', names=[ast.alias(name='Beta', asname=None)], level=2))),
    ('bar', 'foo', frozenset([('foo', 'a')]), 'Beta', ('Beta', ast.ImportFrom(module='foo', names=[ast.alias(name='Beta', asname=None)], level=1)))
])
def test_bridge_namespaces(from_namespace, to_namespace, namespaces_with_children, name, expected):
    expected_name, expected_import = expected
    str_node, actual_import = codegen.RewriteCrossReferenceStrings.bridge_namespaces(
        from_namespace=from_namespace.split('.'),
        to_namespace=to_namespace.split('.'),
        target_name=name.split('.'),
        namespaces_with_children=namespaces_with_children,
    )
    actual_name = str_node.s

    both_imports_are_none = expected_import is None and actual_import is None
    assert actual_name == expected_name and (
        both_imports_are_none
        or ast.dump(expected_import) == ast.dump(actual_import)  # equality doesn't work for AST nodes
    )


@pytest.mark.parametrize('potential_parent, potential_child, is_parent', [
    [['a', 'b'], ['ab'], False],
    [['a', 'b'], ['a', 'b'], False],
    [['a', 'b', 'c'], ['a', 'b'], False],
    [['a', 'b'], ['a', 'b', 'c'], True],
    [['a', 'b'], ['a', 'b', 'c', 'd'], True],
    [['z', 'a', 'b'], ['a', 'b', 'c'], False],
    [['a', 'b'], ['z', 'a', 'b', 'c'], False],
    [['b', 'a'], ['a', 'b', 'c'], False],
    [['a'], ['a'], False],
    [[], [], False],
    [[], ['a'], True],
])
def test_namespace_is_parent_of(potential_parent, potential_child, is_parent):
    actual = codegen.namespace_is_parent_of(potential_parent, potential_child)
    assert actual == is_parent


@pytest.mark.parametrize('namespaces, namespaces_that_should_have_children', [
    [['foo', 'foo.a', 'bar', 'foo.a.s', 'foo.s'], frozenset([('foo',), ('foo', 'a')])],
    [['foo', 'bar'], frozenset([])],
    [['foo.bar.baz', 'foo', 'foo.bar'], frozenset([('foo',), ('foo', 'bar')])]
])
def test_generates_all_parent_namespaces(namespaces, namespaces_that_should_have_children):
    namespaces_as_dict = {namespace: () for namespace in namespaces}
    rewriter = codegen.RewriteCrossReferenceStrings(namespaces=namespaces_as_dict)
    assert rewriter.namespaces_with_children == namespaces_that_should_have_children


def test_populate_namespaces_produces_roundtrippable_modules():
    populated_schemas = codegen.populate_namespaces(
        parse_into_types(schema)
        for schema in TEST_SCHEMAS
    )

    for _, module in populated_schemas:
        source = astor.to_source(module)
        assert isinstance(ast.parse(source), ast.Module)
