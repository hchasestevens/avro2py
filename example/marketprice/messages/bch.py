"""Schema definitions for `marketprice.messages.bch` namespace. Generated by avro2py v.0.0.6."""
import datetime
from typing import NamedTuple


class ProductTrigger(NamedTuple):
    """
    BCH Product for Demand Forecast processing:
    MpDataType(mprice/bch/x/demand-forecast/product-trigger)
    """

    channel: str
    sellerId: str
    marketplaceId: str
    sku: str
    _original_schema = (
        '{"type": "record", "name": "ProductTrigger", "namespace":'
        ' "marketprice.messages.bch", "doc": "BCH Product for Demand Forecast'
        ' processing: MpDataType(mprice/bch/x/demand-forecast/product-trigger)",'
        ' "fields": [{"name": "channel", "type": "string"}, {"name": "sellerId",'
        ' "type": "string"}, {"name": "marketplaceId", "type": "string"}, {"name":'
        ' "sku", "type": "string"}]}'
    )


class ProductDemandEstimate(NamedTuple):
    """
    BCH Demand Forecast response record:
    MpDataType(mprice/bch/x/demand-forecast/deciles)
    """

    channel: str
    sellerId: str
    marketplaceId: str
    sku: str
    forecastDate: datetime.date
    requestedAt: datetime.date
    percentile: str
    estimate: int
    _original_schema = (
        '{"type": "record", "name": "ProductDemandEstimate", "namespace":'
        ' "marketprice.messages.bch", "doc": "BCH Demand Forecast response record:'
        ' MpDataType(mprice/bch/x/demand-forecast/deciles)", "fields": [{"name":'
        ' "channel", "type": "string"}, {"name": "sellerId", "type": "string"},'
        ' {"name": "marketplaceId", "type": "string"}, {"name": "sku", "type":'
        ' "string"}, {"name": "forecastDate", "type": {"type": "int", "logicalType":'
        ' "date"}}, {"name": "requestedAt", "type": {"type": "int", "logicalType":'
        ' "date"}}, {"name": "percentile", "type": "string"}, {"name": "estimate",'
        ' "type": "int"}]}'
    )
