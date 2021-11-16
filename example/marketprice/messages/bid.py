import enum
from typing import List, NamedTuple


class AdgroupCreated(NamedTuple):
    status: "Status"
    _original_schema = (
        '{"type": "record", "name": "AdgroupCreated", "namespace":'
        ' "marketprice.messages.bid", "fields": [{"name": "status", "type": {"type":'
        ' "enum", "name": "Status", "doc": "status can be one of Active, Paused",'
        ' "symbols": ["Active", "Paused"]}}]}'
    )


@enum.unique
class Status(enum.Enum):
    ACTIVE = "Active"
    PAUSED = "Paused"


class CampaignCreated(NamedTuple):
    status: "Status"
    adgroup: "AdgroupCreated"
    _original_schema = (
        '{"type": "record", "name": "CampaignCreated", "namespace":'
        ' "marketprice.messages.bid", "fields": [{"name": "status", "type": {"type":'
        ' "enum", "name": "Status", "doc": "status can be one of Active, Paused",'
        ' "symbols": ["Active", "Paused"]}}, {"name": "adgroup", "type": {"type":'
        ' "record", "name": "AdgroupCreated", "fields": [{"name": "status", "type":'
        ' "Status"}]}}]}'
    )


class WallyworldEntity(NamedTuple):
    tags: List["Status"]
    _original_schema = (
        '{"type": "record", "name": "WallyworldEntity", "namespace":'
        ' "marketprice.messages.bid", "fields": [{"name": "tags", "type": {"type":'
        ' "array", "items": {"type": "enum", "name": "Status", "doc": "advertising type'
        ' can be one of Active, Paused", "symbols": ["Active", "Paused"]}}}]}'
    )
