"""Tests for avro2py/utils.py"""
import datetime
import uuid

from hypothesis import strategies as st, given

from avro2py.utils import to_avro_dict
from example.marketprice.messages.wallyworld.bidder import (
    WallyworldAdGroupStructure, WallyworldAdItem
)


@given(st.integers(), st.text(), st.decimals())
def test_to_avro_dict_nested_named_tuples(random_int, item_id, bid):
    requested_at = datetime.datetime.utcnow()
    campaign_id = ad_group_id = advertiser_id = random_int
    users_lined = [uuid.uuid4() for _ in range(3)]
    payload = WallyworldAdGroupStructure(
        advertiserId=advertiser_id,
        campaignId=campaign_id,
        adGroupId=ad_group_id,
        state="Paused",
        users_linked=users_lined,
        adItems=[WallyworldAdItem(
            advertiserId=advertiser_id,
            campaignId=campaign_id,
            adGroupId=ad_group_id,
            adItemId=4,
            itemId=item_id,
            state="Enabled",
            bid=bid,
            requestedAt=requested_at
        )],
        requestedAt=requested_at
    )
    value = to_avro_dict(payload)
    assert value == {
        "advertiserId": advertiser_id,
        "campaignId": advertiser_id,
        "adGroupId": advertiser_id,
        "state": "Paused",
        "users_linked": users_lined,
        "adItems": [
            {
                "advertiserId": advertiser_id,
                "campaignId": advertiser_id,
                "adGroupId": advertiser_id,
                "adItemId": 4,
                "itemId": item_id,
                "state": "Enabled",
                "bid": bid,
                "requestedAt": requested_at
            }
        ],
        "requestedAt": requested_at
    }
