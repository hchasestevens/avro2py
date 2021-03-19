"""Schema definitions for `marketprice.messages.historical.replay` namespace. Generated by avro2py v.0.1.0."""
import datetime
from ...pubsub import S3FileDescriptor
from typing import Dict, NamedTuple


class S3DataAvailable(NamedTuple):
    """
    Represents a DataAvailable event with data stored in S3 (inline bytes are not
    supported); otherwise comparable to DataAvailable.
    """

    ownerId: str
    s3FileDescriptor: "S3FileDescriptor"
    mpContentType: str
    requestedAt: datetime.datetime
    receivedAt: datetime.datetime
    requestMetadata: Dict[str, str]
    responseMetadata: Dict[str, str]
    _schema = (
        '{"type": "record", "name": "S3DataAvailable", "namespace":'
        ' "marketprice.messages.historical.replay", "doc": "Represents a DataAvailable'
        " event with data stored in S3 (inline bytes are not supported); otherwise"
        ' comparable to DataAvailable.", "fields": [{"name": "ownerId", "type":'
        ' "string"}, {"name": "s3FileDescriptor", "type": {"type": "record", "name":'
        ' "S3FileDescriptor", "namespace": "marketprice.pubsub", "fields": [{"name":'
        ' "bucket", "type": "string"}, {"name": "key", "type": "string"}, {"name":'
        ' "contentType", "type": "string"}, {"name": "contentEncoding", "type":'
        ' "string"}, {"name": "metadata", "type": {"type": "map", "values":'
        ' "string"}}]}}, {"name": "mpContentType", "type": "string"}, {"name":'
        ' "requestedAt", "type": {"type": "long", "logicalType": "timestamp-millis"}},'
        ' {"name": "receivedAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}, {"name": "requestMetadata", "type": {"type": "map",'
        ' "values": "string"}}, {"name": "responseMetadata", "type": {"type": "map",'
        ' "values": "string"}}]}'
    )
