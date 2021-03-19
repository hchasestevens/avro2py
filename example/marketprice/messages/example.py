"""Schema definitions for `marketprice.messages.example` namespace. Generated by avro2py v.0.1.0."""
import datetime
import decimal
import enum
import uuid
from typing import Dict, NamedTuple, Optional, Union


class ExampleAvroModel(NamedTuple):
    """
    Example Avro Model
    """

    id: uuid.UUID
    encryptedData: str
    timestamp: datetime.datetime
    date: datetime.date
    maybeInt: Optional[int]
    decimal: decimal.Decimal
    maybeDecimal: Optional[decimal.Decimal]
    stringMap: Dict[str, str]
    sampleEnum: "ExampleAvroModel.Cheese"
    sampleUnion: Union[
        "ExampleAvroModel.RecordWithInt", "ExampleAvroModel.RecordWithString"
    ]
    sampleInner: "ExampleAvroModel.ExampleInnerModel"
    _schema = (
        '{"type": "record", "name": "ExampleAvroModel", "namespace":'
        ' "marketprice.messages.example", "doc": "Example Avro Model", "fields":'
        ' [{"name": "id", "type": {"type": "string", "logicalType": "uuid"}}, {"name":'
        ' "encryptedData", "type": "string"}, {"name": "timestamp", "type": {"type":'
        ' "long", "logicalType": "timestamp-millis"}}, {"name": "date", "type":'
        ' {"type": "int", "logicalType": "date"}}, {"name": "maybeInt", "type":'
        ' ["null", "int"]}, {"name": "decimal", "type": {"type": "bytes",'
        ' "logicalType": "decimal", "precision": 21, "scale": 2}}, {"name":'
        ' "maybeDecimal", "type": ["null", {"type": "bytes", "logicalType": "decimal",'
        ' "precision": 21, "scale": 2}]}, {"name": "stringMap", "type": {"type": "map",'
        ' "values": "string"}}, {"name": "sampleEnum", "type": {"type": "enum", "name":'
        ' "Cheese", "namespace": "marketprice.messages.example.ExampleAvroModel",'
        ' "doc": "Example enum", "symbols": ["wensleydale", "havarti", "cheddar"]}},'
        ' {"name": "sampleUnion", "type": [{"type": "record", "name": "RecordWithInt",'
        ' "namespace": "marketprice.messages.example.ExampleAvroModel", "fields":'
        ' [{"name": "id", "type": {"type": "string", "logicalType": "uuid"}}, {"name":'
        ' "value", "type": "int"}]}, {"type": "record", "name": "RecordWithString",'
        ' "namespace": "marketprice.messages.example.ExampleAvroModel", "fields":'
        ' [{"name": "id", "type": {"type": "string", "logicalType": "uuid"}}, {"name":'
        ' "value", "type": "string"}]}]}, {"name": "sampleInner", "type": {"type":'
        ' "record", "name": "ExampleInnerModel", "namespace":'
        ' "marketprice.messages.example.ExampleAvroModel", "doc": "Example Inner'
        ' Model", "fields": [{"name": "foo", "type": "long"}, {"name": "bar", "type":'
        ' "string"}]}}]}'
    )

    class ExampleInnerModel(NamedTuple):
        """
        Example Inner Model
        """

        foo: int
        bar: str
        _schema = (
            '{"type": "record", "name": "ExampleInnerModel", "namespace":'
            ' "marketprice.messages.example.ExampleAvroModel", "doc": "Example Inner'
            ' Model", "fields": [{"name": "foo", "type": "long"}, {"name": "bar",'
            ' "type": "string"}]}'
        )

    class RecordWithString(NamedTuple):
        id: uuid.UUID
        value: str
        _schema = (
            '{"type": "record", "name": "RecordWithString", "namespace":'
            ' "marketprice.messages.example.ExampleAvroModel", "fields": [{"name":'
            ' "id", "type": {"type": "string", "logicalType": "uuid"}}, {"name":'
            ' "value", "type": "string"}]}'
        )

    class RecordWithInt(NamedTuple):
        id: uuid.UUID
        value: int
        _schema = (
            '{"type": "record", "name": "RecordWithInt", "namespace":'
            ' "marketprice.messages.example.ExampleAvroModel", "fields": [{"name":'
            ' "id", "type": {"type": "string", "logicalType": "uuid"}}, {"name":'
            ' "value", "type": "int"}]}'
        )

    @enum.unique
    class Cheese(enum.Enum):
        """
        Example enum
        """

        CHEDDAR = "cheddar"
        HAVARTI = "havarti"
        WENSLEYDALE = "wensleydale"


class SimpleExampleMessageStringData(NamedTuple):
    """
    Simple example message format with string data, for use in examples and testing
    """

    id: uuid.UUID
    name: str
    data: str
    timestamp: datetime.datetime
    _schema = (
        '{"type": "record", "name": "SimpleExampleMessageStringData", "namespace":'
        ' "marketprice.messages.example", "doc": "Simple example message format with'
        ' string data, for use in examples and testing", "fields": [{"name": "id",'
        ' "type": {"type": "string", "logicalType": "uuid"}}, {"name": "name", "type":'
        ' "string"}, {"name": "data", "type": "string"}, {"name": "timestamp", "type":'
        ' {"type": "long", "logicalType": "timestamp-millis"}}]}'
    )


class SimpleExampleDecimalMessage(NamedTuple):
    """
    Simple example message format with decimals, for use in examples and testing
    """

    id: uuid.UUID
    name: str
    decimal21P2S: decimal.Decimal
    decimal21P6S: decimal.Decimal
    timestamp: datetime.datetime
    _schema = (
        '{"type": "record", "name": "SimpleExampleDecimalMessage", "namespace":'
        ' "marketprice.messages.example", "doc": "Simple example message format with'
        ' decimals, for use in examples and testing", "fields": [{"name": "id", "type":'
        ' {"type": "string", "logicalType": "uuid"}}, {"name": "name", "type":'
        ' "string"}, {"name": "decimal21P2S", "type": {"type": "bytes", "logicalType":'
        ' "decimal", "precision": 21, "scale": 2}}, {"name": "decimal21P6S", "type":'
        ' {"type": "bytes", "logicalType": "decimal", "precision": 21, "scale": 6}},'
        ' {"name": "timestamp", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}]}'
    )


class SimpleExampleMessage(NamedTuple):
    """
    Simple example message format, for use in examples and testing
    """

    id: uuid.UUID
    name: str
    dataMap: Dict[str, str]
    timestamp: datetime.datetime
    _schema = (
        '{"type": "record", "name": "SimpleExampleMessage", "namespace":'
        ' "marketprice.messages.example", "doc": "Simple example message format, for'
        ' use in examples and testing", "fields": [{"name": "id", "type": {"type":'
        ' "string", "logicalType": "uuid"}}, {"name": "name", "type": "string"},'
        ' {"name": "dataMap", "type": {"type": "map", "values": "string"}}, {"name":'
        ' "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}}]}'
    )


class ExampleModelWithMpContentType(NamedTuple):
    """
    Simple example model for testing MpContentType (not used outside of tests)
    """

    id: uuid.UUID
    name: str
    contentType: str
    separateMpDataType: str
    separateMpContentFormat: str
    timestamp: datetime.datetime
    _schema = (
        '{"type": "record", "name": "ExampleModelWithMpContentType", "namespace":'
        ' "marketprice.messages.example", "doc": "Simple example model for testing'
        ' MpContentType (not used outside of tests)", "fields": [{"name": "id", "type":'
        ' {"type": "string", "logicalType": "uuid"}}, {"name": "name", "type":'
        ' "string"}, {"name": "contentType", "type": "string"}, {"name":'
        ' "separateMpDataType", "type": "string"}, {"name": "separateMpContentFormat",'
        ' "type": "string"}, {"name": "timestamp", "type": {"type": "long",'
        ' "logicalType": "timestamp-millis"}}]}'
    )
