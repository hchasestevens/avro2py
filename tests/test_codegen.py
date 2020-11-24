"""Tests for avro2py/codegen.py"""
import ast

import pytest

import avro2py.codegen as codegen


@pytest.mark.parametrize('from_namespace, to_namespace, expected', [
    ('teikametrics.messages.amazon.mws', 'teikametrics.messages.amazon.mws.GetMatchingProductForId.ImageData', ('GetMatchingProductForId.ImageData', None)),
    ('teikametrics.messages.historical.replay', 'teikametrics.pubsub.S3FileDescriptor', ('S3FileDescriptor', ast.ImportFrom(module='pubsub', names=[ast.alias(name='S3FileDescriptor', asname=None)], level=3))),
    pytest.param('teikametrics.messages.targeting_recommendation_engine.TargetingRecommendation', 'teikametrics.messages.targeting_recommendation_engine.TargetingRecommendation.Predicate', ('TargetingRecommendation.Predicate', None), marks=pytest.mark.skip(reason='TODO - Namespace/record differentiation bug'))
])
def test_bridge_namespaces(from_namespace, to_namespace, expected):
    expected_name, expected_import = expected

    actual_name, actual_import = codegen.bridge_namespaces(
        from_namespace=from_namespace, to_namespace=to_namespace
    )

    both_imports_are_none = expected_import is None and actual_import is None
    assert actual_name == expected_name and (
        both_imports_are_none
        or ast.dump(expected_import) == ast.dump(actual_import)  # equality doesn't work for AST nodes
    )

