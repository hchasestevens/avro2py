"""Tests for avro2py/avro_types.py"""

import avro2py.avro_types as avro_types


def test_parsing_permits_metadata_attributes():
    """
    https://avro.apache.org/docs/1.10.2/spec.html#schemas states: "Attributes
    not defined in this document are permitted as metadata, but must not
    affect the format of serialized data". Ensure that metadata keys are
    permitted during avro2py schema parsing, and do not affect output (modulo
    original_schema field).
    """
    def schema(embedded_type):
        return dict(
            type="record",
            name="ExampleRecord",
            namespace="messages.example",
            doc="Example record",
            fields=[
                dict(
                    name="foo",
                    type=[
                        "null",
                        embedded_type
                    ],
                    doc="Foo field",
                    default=None,
                ),
            ]
        )

    metadata_schema = schema(
        embedded_type={
            "type": "map",
            "values": {
                "type": "string",
                "avro.java.string": "String"
            },
            "avro.java.string": "String"
        }
    )
    non_metadata_schema = schema(
        embedded_type={
            "type": "map",
            "values": {
                "type": "string",
            }
        }
    )
    parsed_metadata_schema = avro_types.parse_into_types(metadata_schema)._replace(original_schema=None)
    parsed_non_metadata_schema = avro_types.parse_into_types(non_metadata_schema)._replace(original_schema=None)

    assert parsed_metadata_schema == parsed_non_metadata_schema
