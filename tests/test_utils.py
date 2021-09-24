"""Tests for avro2py/utils.py"""
from hypothesis import given, strategies as st

from avro2py.utils import to_avro_dict
from example.marketprice.messages.wallyworld.bidder import (
    WallyworldAdGroupStructure, WallyworldAdItem
)


@given(
    random_int=st.integers(),
    item_id=st.text(),
    bid=st.decimals(),
    requested_at=st.datetimes(),
    users_linked=st.lists(st.uuids(), min_size=0, max_size=33)
)
def test_to_avro_dict_nested_named_tuples(random_int, item_id, bid, requested_at, users_linked):
    campaign_id = ad_group_id = advertiser_id = random_int
    payload = WallyworldAdGroupStructure(
        advertiserId=advertiser_id,
        campaignId=campaign_id,
        adGroupId=ad_group_id,
        state="Paused",
        users_linked=users_linked,
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
        "users_linked": users_linked,
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


@given(
    random_int=st.integers(),
    requested_at=st.datetimes(),
    users_linked=st.lists(st.uuids(), min_size=0, max_size=13),
    ad_items=st.lists(st.builds(WallyworldAdItem), min_size=0, max_size=3)
)
def test_to_avro_dict_nested_named_tuples(random_int, requested_at, users_linked, ad_items):
    campaign_id = ad_group_id = advertiser_id = random_int
    payload = WallyworldAdGroupStructure(
        advertiserId=advertiser_id,
        campaignId=campaign_id,
        adGroupId=ad_group_id,
        state="Paused",
        users_linked=users_linked,
        adItems=ad_items,
        requestedAt=requested_at
    )
    value = to_avro_dict(payload)
    if ad_items:
        ad_items_dict = value["adItems"]
        assert len(ad_items_dict) == len(ad_items)
        for idx, d in enumerate(ad_items_dict):
            assert d["advertiserId"] == ad_items[idx].advertiserId
            assert d["adItemId"] == ad_items[idx].adItemId

    assert value["advertiserId"] == advertiser_id
    assert value["campaignId"] == campaign_id
    assert value["users_linked"] == users_linked
