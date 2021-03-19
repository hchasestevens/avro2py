"""Schema definitions for `marketprice.messages.neo.wallyworld` namespace. Generated by avro2py v.0.1.0."""
import datetime
import decimal
import enum
import uuid
from typing import NamedTuple, Optional


class AdItemUpdateResponse(NamedTuple):
    """
    Response for an AdItemUpdateRequest message:
    wallyworld-sponsored-products-api/v1/response-update/ad-item
    """

    code: "AdItemUpdateResponse.ResponseCode"
    errorDetails: Optional[str]
    advertiserId: int
    bid: decimal.Decimal
    submissionId: uuid.UUID
    requestedAt: datetime.datetime
    receivedAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "AdItemUpdateResponse", "namespace":'
        ' "marketprice.messages.neo.wallyworld", "doc": "Response for an'
        " AdItemUpdateRequest message:"
        ' wallyworld-sponsored-products-api/v1/response-update/ad-item", "fields":'
        ' [{"name": "code", "type": {"type": "enum", "name": "ResponseCode",'
        ' "namespace": "marketprice.messages.neo.wallyworld.AdItemUpdateResponse",'
        ' "doc": "code returned by Wallyworld API", "symbols": ["success",'
        ' "failure"]}}, {"name": "errorDetails", "type": ["null", "string"]}, {"name":'
        ' "advertiserId", "type": "long"}, {"name": "bid", "type": {"type": "bytes",'
        ' "logicalType": "decimal", "precision": 12, "scale": 4}}, {"name":'
        ' "submissionId", "type": {"type": "string", "logicalType": "uuid"}}, {"name":'
        ' "requestedAt", "type": {"type": "long", "logicalType": "timestamp-millis"}},'
        ' {"name": "receivedAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}]}'
    )

    @enum.unique
    class ResponseCode(enum.Enum):
        """
        code returned by Wallyworld API
        """

        FAILURE = "failure"
        SUCCESS = "success"


class KeywordUpdateResponse(NamedTuple):
    """
    Response for a KeywordUpdateRequest message:
    wallyworld-sponsored-products-api/v1/response-update/keyword
    """

    code: "KeywordUpdateResponse.ResponseCode"
    errorDetails: Optional[str]
    advertiserId: int
    bid: decimal.Decimal
    submissionId: uuid.UUID
    requestedAt: datetime.datetime
    receivedAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "KeywordUpdateResponse", "namespace":'
        ' "marketprice.messages.neo.wallyworld", "doc": "Response for a'
        " KeywordUpdateRequest message:"
        ' wallyworld-sponsored-products-api/v1/response-update/keyword", "fields":'
        ' [{"name": "code", "type": {"type": "enum", "name": "ResponseCode",'
        ' "namespace": "marketprice.messages.neo.wallyworld.KeywordUpdateResponse",'
        ' "doc": "code returned by Wallyworld API", "symbols": ["success",'
        ' "failure"]}}, {"name": "errorDetails", "type": ["null", "string"]}, {"name":'
        ' "advertiserId", "type": "long"}, {"name": "bid", "type": {"type": "bytes",'
        ' "logicalType": "decimal", "precision": 12, "scale": 4}}, {"name":'
        ' "submissionId", "type": {"type": "string", "logicalType": "uuid"}}, {"name":'
        ' "requestedAt", "type": {"type": "long", "logicalType": "timestamp-millis"}},'
        ' {"name": "receivedAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}]}'
    )

    @enum.unique
    class ResponseCode(enum.Enum):
        """
        code returned by Wallyworld API
        """

        FAILURE = "failure"
        SUCCESS = "success"


class AdItemUpdateRequest(NamedTuple):
    """
    AdItem update request:
    wallyworld-sponsored-products-api/v1/request-update/ad-item
    """

    advertiserId: int
    campaignId: int
    adGroupId: int
    itemId: str
    bid: decimal.Decimal
    status: str
    submissionId: uuid.UUID
    publishedAt: datetime.datetime
    expiresAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "AdItemUpdateRequest", "namespace":'
        ' "marketprice.messages.neo.wallyworld", "doc": "AdItem update request:'
        ' wallyworld-sponsored-products-api/v1/request-update/ad-item", "fields":'
        ' [{"name": "advertiserId", "type": "long"}, {"name": "campaignId", "type":'
        ' "long"}, {"name": "adGroupId", "type": "long"}, {"name": "itemId", "type":'
        ' "string"}, {"name": "bid", "type": {"type": "bytes", "logicalType":'
        ' "decimal", "precision": 12, "scale": 4}}, {"name": "status", "type":'
        ' "string"}, {"name": "submissionId", "type": {"type": "string", "logicalType":'
        ' "uuid"}}, {"name": "publishedAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}, {"name": "expiresAt", "type": {"type": "long",'
        ' "logicalType": "timestamp-millis"}}]}'
    )


class KeywordUpdateRequest(NamedTuple):
    """
    Keyword update request:
    wallyworld-sponsored-products-api/v1/request-update/keyword
    """

    keywordId: int
    bid: decimal.Decimal
    status: str
    advertiserId: int
    submissionId: uuid.UUID
    publishedAt: datetime.datetime
    expiresAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "KeywordUpdateRequest", "namespace":'
        ' "marketprice.messages.neo.wallyworld", "doc": "Keyword update request:'
        ' wallyworld-sponsored-products-api/v1/request-update/keyword", "fields":'
        ' [{"name": "keywordId", "type": "long"}, {"name": "bid", "type": {"type":'
        ' "bytes", "logicalType": "decimal", "precision": 12, "scale": 4}}, {"name":'
        ' "status", "type": "string"}, {"name": "advertiserId", "type": "long"},'
        ' {"name": "submissionId", "type": {"type": "string", "logicalType": "uuid"}},'
        ' {"name": "publishedAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}, {"name": "expiresAt", "type": {"type": "long",'
        ' "logicalType": "timestamp-millis"}}]}'
    )
