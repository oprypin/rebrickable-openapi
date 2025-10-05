import datetime
import os

import pytest

import rebrickable_api


@pytest.fixture(scope="session")
def users_api(api_client: rebrickable_api.ApiClient) -> rebrickable_api.UsersApi:
    return rebrickable_api.UsersApi(api_client)


@pytest.fixture(scope="session")
def user_token(users_api: rebrickable_api.UsersApi) -> str:
    return users_api.create_user_token(
        os.environ["REBRICKABLE_USERNAME"], os.environ["REBRICKABLE_PASSWORD"]
    ).user_token


@pytest.fixture(scope="session")
def testing_setlist(
    users_api: rebrickable_api.UsersApi, user_token: str
) -> rebrickable_api.SetList:
    setlists = users_api.list_setlists(user_token=user_token)
    try:
        return next(lst for lst in setlists.results if lst.name.startswith("Testing Set List"))
    except StopIteration:
        pass

    setlist = users_api.create_setlist(
        user_token=user_token, name="Testing Set List", is_buildable=True
    )
    users_api.create_setlist_set(
        user_token=user_token,
        list_id=setlist.id,
        set_num="31124-1",
        quantity=1,
        include_spares=True,
    )
    setlist.num_sets += 1
    return setlist


@pytest.fixture(scope="session")
def testing_partlist(
    users_api: rebrickable_api.UsersApi,
    user_token: str,
    lego_api: rebrickable_api.LegoApi,
) -> rebrickable_api.PartList:
    partlists = users_api.list_partlists(user_token=user_token)
    try:
        return next(lst for lst in partlists.results if lst.name.startswith("Testing Part List"))
    except StopIteration:
        pass

    partlist = users_api.create_partlist(
        user_token=user_token, name="Testing Part List", is_buildable=True
    )
    users_api.create_partlist_part(
        user_token=user_token,
        list_id=partlist.id,
        part_num="3020",
        quantity=1,
        color_id=0,
    )
    partlist.num_parts += 1

    set_parts = lego_api.list_set_parts(
        set_num="31124-1", inc_minifig_parts=0, inc_color_details=0
    ).results
    the_part = next(
        part
        for part in set_parts
        if part.part.part_num == "3005" and part.color.id == 321  # Dark Azure
    )
    users_api.create_lost_part(user_token=user_token, inv_part_id=the_part.inv_part_id)

    return partlist


def test_partlists(
    users_api: rebrickable_api.UsersApi,
    user_token: str,
    testing_partlist: rebrickable_api.PartList,
):
    assert testing_partlist.num_parts == 1
    assert testing_partlist.is_buildable

    lst2 = users_api.get_partlist(user_token=user_token, list_id=testing_partlist.id)
    assert lst2.id == testing_partlist.id
    assert lst2.is_buildable
    assert lst2.name == testing_partlist.name
    assert lst2.num_parts == 1

    resp2 = users_api.list_partlist_parts(
        user_token=user_token, list_id=testing_partlist.id, inc_color_details=0
    )
    assert resp2.count == len(resp2.results)
    assert any(
        part.list_id == testing_partlist.id
        and part.quantity == 1
        and part.part.part_num == "3020"
        and part.part.part_url
        and part.part.external_ids.brick_owl
        and part.color.id == 0
        and part.color.rgb
        for part in resp2.results
    )

    part = users_api.get_partlist_part(
        user_token=user_token, list_id=testing_partlist.id, part_num="3020", color_id=0
    )
    assert part.list_id == testing_partlist.id
    assert part.quantity == 1
    assert part.part.part_num == "3020"
    assert part.part.part_url
    assert part.part.external_ids.brick_owl
    assert part.color.id == 0
    assert part.color.rgb
    assert part.color.external_ids.lego
    assert part.color.external_ids.lego.ext_ids


def test_setlists(
    users_api: rebrickable_api.UsersApi,
    user_token: str,
    testing_setlist: rebrickable_api.SetList,
):
    assert testing_setlist.num_sets == 1
    assert testing_setlist.is_buildable

    lst2 = users_api.get_setlist(user_token=user_token, list_id=testing_setlist.id)
    assert lst2.id == testing_setlist.id
    assert lst2.is_buildable
    assert lst2.name == testing_setlist.name
    assert lst2.num_sets == 1

    resp2 = users_api.list_setlist_sets(user_token=user_token, list_id=testing_setlist.id)
    assert resp2.count == len(resp2.results)
    assert any(
        lset.list_id == testing_setlist.id
        and lset.quantity == 1
        and lset.include_spares
        and lset.set.set_num == "31124-1"
        and lset.set.year == 2022
        and lset.set.num_parts == 159
        and lset.set.set_url
        and lset.set.last_modified_dt > datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC)
        for lset in resp2.results
    )

    lset = users_api.get_setlist_set(
        user_token=user_token, list_id=testing_setlist.id, set_num="31124-1"
    )
    assert lset.list_id == testing_setlist.id
    assert lset.quantity == 1
    assert lset.include_spares
    assert lset.set.set_num == "31124-1"
    assert lset.set.year == 2022
    assert lset.set.num_parts == 159
    assert lset.set.set_url
    assert lset.set.last_modified_dt > datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC)


@pytest.mark.usefixtures("testing_partlist")
def test_list_parts(users_api: rebrickable_api.UsersApi, user_token: str):
    resp = users_api.list_parts(user_token=user_token, color_id=0)

    assert resp.count == 1
    part = next(part for part in resp.results if part.part.part_num == "3020")
    assert part.quantity == 1
    assert part.part.part_url

    part_ids_lego = part.part.external_ids.lego
    assert part_ids_lego
    assert "3020" in part_ids_lego

    assert part.color.id == 0
    assert part.color.name == "Black"
    assert not part.color.is_trans

    color_ids_lego = part.color.external_ids.lego
    assert color_ids_lego
    assert 26 in color_ids_lego.ext_ids
    assert any("Black" in group for group in color_ids_lego.ext_descrs)


@pytest.mark.usefixtures("testing_setlist", "testing_partlist")
def test_list_all_parts(users_api: rebrickable_api.UsersApi, user_token: str):
    resp = users_api.list_all_parts(user_token=user_token, color_id=0)

    assert 10 <= resp.count <= 20
    part = next(part for part in resp.results if part.part.part_num == "3020")
    assert part.quantity == 7
    assert part.part.part_url

    part_ids_lego = part.part.external_ids.lego
    assert part_ids_lego
    assert "3020" in part_ids_lego

    assert part.color.id == 0
    assert part.color.name == "Black"
    assert not part.color.is_trans

    color_ids_lego = part.color.external_ids.lego
    assert color_ids_lego
    assert 26 in color_ids_lego.ext_ids
    assert any("Black" in group for group in color_ids_lego.ext_descrs)


@pytest.mark.usefixtures("testing_setlist", "testing_partlist")
def test_build_set(users_api: rebrickable_api.UsersApi, user_token: str):
    resp = users_api.build_set(user_token=user_token, set_num="31100-1")
    assert resp.num_missing == 125
    assert resp.total_parts == 134


@pytest.mark.usefixtures("testing_setlist")
def test_list_lost_parts(users_api: rebrickable_api.UsersApi, user_token: str):
    resp = users_api.list_lost_parts(user_token=user_token)
    assert resp.count == len(resp.results)
    assert any(
        part.lost_part_id
        and part.lost_quantity == 1
        and part.inv_part.id
        and part.inv_part.part.part_num == "3005"
        and "brick" in part.inv_part.part.name.lower()
        and part.inv_part.color.name == "Dark Azure"
        and not part.inv_part.color.is_trans
        and part.inv_part.set_num == "31124-1"
        and part.inv_part.element_id == "6225538"
        for part in resp.results
    )
