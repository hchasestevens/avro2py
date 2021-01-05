"""Tests for avro2py/rendering.py"""
import io
import sys
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import importlib.util as imp
from typing import Optional

import avro
from hypothesis import strategies as st, given, assume, note, settings, HealthCheck

from avro2py.avro_types import parse_into_types
from avro2py.codegen import populate_namespaces
from avro2py.utils import to_avro_dict, from_avro_dict
import avro2py.rendering as rendering

TEST_DIR = Path(__file__).parent
EXAMPLE_PATH = TEST_DIR / '..' / 'example'
EXAMPLE_SCHEMA = EXAMPLE_PATH / 'schema.avsc'
EXAMPLE_AVRO_MODEL_SCHEMA, = (x for x in json.load(open(EXAMPLE_SCHEMA)) if x['name'] == 'ExampleAvroModel')


@given(st.data())
@settings(suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow])  # because of exponent check below
def test_example_message_round_trippable(data):
    """Ensure generated classes can be round-tripped into avro and back."""
    # setup
    parsed_schema = parse_into_types(schema=EXAMPLE_AVRO_MODEL_SCHEMA)
    namespaces = populate_namespaces([parsed_schema])

    # the actual intrinsic thing we care to test
    module_contents, = (
        contents
        for path, contents in rendering.render_modules(namespaces).items()
        if path.stem != '__init__'
    )

    # write module contents out to file, then, load file and generate an example object
    tmp_path = Path('/tmp/example.py')
    with tmp_path.open('w') as f:
        f.write(module_contents)
    spec = imp.spec_from_file_location('example', tmp_path)
    example = imp.module_from_spec(spec)
    sys.modules['example'] = example
    spec.loader.exec_module(example)
    original_example_avro_model = data.draw(st.from_type(example.ExampleAvroModel))
    tmp_path.unlink()

    # clean up PBT-generated example model
    def check_decimal(d: Optional[Decimal]):
        if d is None:
            return
        assume(d.is_finite())
        assume(d.as_tuple().exponent == -2)  # bug in avro python implementation; exponent _must_ match scale

    check_decimal(original_example_avro_model.decimal)
    check_decimal(original_example_avro_model.maybeDecimal)
    assume(
        original_example_avro_model.maybeInt is None
        or -2_147_483_648 <= original_example_avro_model.maybeInt <= 2_147_483_647
    )  # 32-bit signed range is underspecified by python "int" type (which also supports longs)
    assume(
        -9_223_372_036_854_775_808 <= original_example_avro_model.sampleInner.foo <= 9_223_372_036_854_775_808
    )  # 64-bit signed range also underspecified
    if isinstance(original_example_avro_model.sampleUnion, example.ExampleAvroModel.RecordWithInt):
        assume(-2_147_483_648 <= original_example_avro_model.sampleUnion.value <= 2_147_483_647)
    original_example_avro_model = original_example_avro_model._replace(
        timestamp=datetime(2000, 1, 1, 0, 0, 0, 000000, tzinfo=avro.timezones.utc)
    )  # set this manually, since it's underspecified by the `datetime.datetime` type annotation

    # round trip through avro ser/deser
    avro_parsed_schema = avro.schema.parse(json.dumps(EXAMPLE_AVRO_MODEL_SCHEMA))
    example_model_dict = to_avro_dict(original_example_avro_model)
    note(example_model_dict)
    buffer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(buffer)
    datum_writer = avro.io.DatumWriter(avro_parsed_schema)
    datum_writer.write(example_model_dict, encoder)
    buffer.seek(0)
    decoder = avro.io.BinaryDecoder(buffer)
    datum_reader = avro.io.DatumReader(writers_schema=avro_parsed_schema, readers_schema=avro_parsed_schema)
    round_tripped_example_avro_model_dict = datum_reader.read(decoder)
    note(round_tripped_example_avro_model_dict)
    round_tripped_example_avro_model = from_avro_dict(
        round_tripped_example_avro_model_dict,
        record_type=example.ExampleAvroModel
    )

    assert round_tripped_example_avro_model == original_example_avro_model
