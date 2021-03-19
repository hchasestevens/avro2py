"""Schema definitions for `marketprice.messages.wallyworld.bidder` namespace. Generated by avro2py v.0.1.0."""
import datetime
import decimal
from typing import NamedTuple


class WallyworldKeyword(NamedTuple):
    """
    Wallyworld Keyword Snapshot for bidder:
    wallyworld-sponsored-products-api/entity/v1/parsed-bidder/keyword
    """

    advertiserId: int
    campaignId: int
    adGroupId: int
    keywordId: int
    state: str
    matchType: str
    bid: decimal.Decimal
    requestedAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "WallyworldKeyword", "namespace":'
        ' "marketprice.messages.wallyworld.bidder", "doc": "Wallyworld Keyword Snapshot'
        " for bidder:"
        ' wallyworld-sponsored-products-api/entity/v1/parsed-bidder/keyword", "fields":'
        ' [{"name": "advertiserId", "type": "long"}, {"name": "campaignId", "type":'
        ' "long"}, {"name": "adGroupId", "type": "long"}, {"name": "keywordId", "type":'
        ' "long"}, {"name": "state", "type": "string"}, {"name": "matchType", "type":'
        ' "string"}, {"name": "bid", "type": {"type": "bytes", "logicalType":'
        ' "decimal", "precision": 12, "scale": 4}}, {"name": "requestedAt", "type":'
        ' {"type": "long", "logicalType": "timestamp-millis"}}]}'
    )


class WallyworldCampaign(NamedTuple):
    """
    Wallyworld Campaign Snapshot for bidder:
    wallyworld-sponsored-products-api/entity/v1/parsed-bidder/campaign
    """

    advertiserId: int
    campaignId: int
    targetingType: str
    state: str
    requestedAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "WallyworldCampaign", "namespace":'
        ' "marketprice.messages.wallyworld.bidder", "doc": "Wallyworld Campaign'
        " Snapshot for bidder:"
        ' wallyworld-sponsored-products-api/entity/v1/parsed-bidder/campaign",'
        ' "fields": [{"name": "advertiserId", "type": "long"}, {"name": "campaignId",'
        ' "type": "long"}, {"name": "targetingType", "type": "string"}, {"name":'
        ' "state", "type": "string"}, {"name": "requestedAt", "type": {"type": "long",'
        ' "logicalType": "timestamp-millis"}}]}'
    )


class WallyworldKeywordReport(NamedTuple):
    """
    Wallyworld Keyword Report for bidder:
    wallyworld-sponsored-products-api/reports/v1/parsed-bidder/keyword
    """

    advertiserId: int
    keywordId: int
    searchTerm: str
    impressions: int
    clicks: int
    unitsOrdered: int
    cost: decimal.Decimal
    sales: decimal.Decimal
    date: datetime.date
    requestedAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "WallyworldKeywordReport", "namespace":'
        ' "marketprice.messages.wallyworld.bidder", "doc": "Wallyworld Keyword Report'
        " for bidder:"
        ' wallyworld-sponsored-products-api/reports/v1/parsed-bidder/keyword",'
        ' "fields": [{"name": "advertiserId", "type": "long"}, {"name": "keywordId",'
        ' "type": "long"}, {"name": "searchTerm", "type": "string"}, {"name":'
        ' "impressions", "type": "int"}, {"name": "clicks", "type": "int"}, {"name":'
        ' "unitsOrdered", "type": "int"}, {"name": "cost", "type": {"type": "bytes",'
        ' "logicalType": "decimal", "precision": 21, "scale": 2}}, {"name": "sales",'
        ' "type": {"type": "bytes", "logicalType": "decimal", "precision": 21, "scale":'
        ' 2}}, {"name": "date", "type": {"type": "int", "logicalType": "date"}},'
        ' {"name": "requestedAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}]}'
    )


class WallyworldAdItemReport(NamedTuple):
    """
    Wallyworld Ad Item Report for bidder:
    wallyworld-sponsored-products-api/reports/v1/parsed-bidder/ad-item
    """

    advertiserId: int
    adGroupId: int
    itemId: str
    date: datetime.date
    cost: decimal.Decimal
    sales: decimal.Decimal
    impressions: int
    clicks: int
    unitsOrdered: int
    requestedAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "WallyworldAdItemReport", "namespace":'
        ' "marketprice.messages.wallyworld.bidder", "doc": "Wallyworld Ad Item Report'
        " for bidder:"
        ' wallyworld-sponsored-products-api/reports/v1/parsed-bidder/ad-item",'
        ' "fields": [{"name": "advertiserId", "type": "long"}, {"name": "adGroupId",'
        ' "type": "long"}, {"name": "itemId", "type": "string"}, {"name": "date",'
        ' "type": {"type": "int", "logicalType": "date"}}, {"name": "cost", "type":'
        ' {"type": "bytes", "logicalType": "decimal", "precision": 21, "scale": 2}},'
        ' {"name": "sales", "type": {"type": "bytes", "logicalType": "decimal",'
        ' "precision": 21, "scale": 2}}, {"name": "impressions", "type": "int"},'
        ' {"name": "clicks", "type": "int"}, {"name": "unitsOrdered", "type": "int"},'
        ' {"name": "requestedAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}]}'
    )


class WallyworldAdGroupReport(NamedTuple):
    """
    Wallyworld Ad Group Report for bidder:
    wallyworld-sponsored-products-api/reports/v1/parsed-bidder/ad-group
    """

    advertiserId: int
    campaignId: int
    adGroupId: int
    date: datetime.date
    cost: decimal.Decimal
    sales: decimal.Decimal
    impressions: int
    clicks: int
    unitsOrdered: int
    requestedAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "WallyworldAdGroupReport", "namespace":'
        ' "marketprice.messages.wallyworld.bidder", "doc": "Wallyworld Ad Group Report'
        " for bidder:"
        ' wallyworld-sponsored-products-api/reports/v1/parsed-bidder/ad-group",'
        ' "fields": [{"name": "advertiserId", "type": "long"}, {"name": "campaignId",'
        ' "type": "long"}, {"name": "adGroupId", "type": "long"}, {"name": "date",'
        ' "type": {"type": "int", "logicalType": "date"}}, {"name": "cost", "type":'
        ' {"type": "bytes", "logicalType": "decimal", "precision": 21, "scale": 2}},'
        ' {"name": "sales", "type": {"type": "bytes", "logicalType": "decimal",'
        ' "precision": 21, "scale": 2}}, {"name": "impressions", "type": "int"},'
        ' {"name": "clicks", "type": "int"}, {"name": "unitsOrdered", "type": "int"},'
        ' {"name": "requestedAt", "type": {"type": "long", "logicalType":'
        ' "timestamp-millis"}}]}'
    )


class WallyworldAdGroup(NamedTuple):
    """
    Wallyworld Ad Group Snapshot for bidder:
    wallyworld-sponsored-products-api/entity/v1/parsed-bidder/ad-group
    """

    advertiserId: int
    campaignId: int
    adGroupId: int
    state: str
    requestedAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "WallyworldAdGroup", "namespace":'
        ' "marketprice.messages.wallyworld.bidder", "doc": "Wallyworld Ad Group'
        " Snapshot for bidder:"
        ' wallyworld-sponsored-products-api/entity/v1/parsed-bidder/ad-group",'
        ' "fields": [{"name": "advertiserId", "type": "long"}, {"name": "campaignId",'
        ' "type": "long"}, {"name": "adGroupId", "type": "long"}, {"name": "state",'
        ' "type": "string"}, {"name": "requestedAt", "type": {"type": "long",'
        ' "logicalType": "timestamp-millis"}}]}'
    )


class WallyworldAdItem(NamedTuple):
    """
    Wallyworld Ad Item Snapshot for bidder:
    wallyworld-sponsored-products-api/entity/v1/parsed-bidder/ad-item
    """

    advertiserId: int
    campaignId: int
    adGroupId: int
    adItemId: int
    itemId: str
    state: str
    bid: decimal.Decimal
    requestedAt: datetime.datetime
    _schema = (
        '{"type": "record", "name": "WallyworldAdItem", "namespace":'
        ' "marketprice.messages.wallyworld.bidder", "doc": "Wallyworld Ad Item Snapshot'
        " for bidder:"
        ' wallyworld-sponsored-products-api/entity/v1/parsed-bidder/ad-item", "fields":'
        ' [{"name": "advertiserId", "type": "long"}, {"name": "campaignId", "type":'
        ' "long"}, {"name": "adGroupId", "type": "long"}, {"name": "adItemId", "type":'
        ' "long"}, {"name": "itemId", "type": "string"}, {"name": "state", "type":'
        ' "string"}, {"name": "bid", "type": {"type": "bytes", "logicalType":'
        ' "decimal", "precision": 12, "scale": 4}}, {"name": "requestedAt", "type":'
        ' {"type": "long", "logicalType": "timestamp-millis"}}]}'
    )
