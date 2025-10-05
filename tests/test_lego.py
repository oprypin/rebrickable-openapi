import datetime
import re

import rebrickable_api


def test_list_colors(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_colors()
    assert resp.count > 0

    colors = resp.results
    assert len(colors) > 1

    assert any(color.id == -1 and color.name == "[Unknown]" for color in colors)

    black = next(color for color in colors if color.id == 0 and color.name == "Black")
    assert not black.is_trans
    brick_link = black.external_ids.brick_link
    assert brick_link
    assert brick_link.ext_ids == [11]
    assert brick_link.ext_descrs == [["Black"]]

    red = next(color for color in colors if color.id == 4 and color.name == "Red")
    _test_red(red)


def test_get_color(lego_api: rebrickable_api.LegoApi):
    red = lego_api.get_color(id=4)
    _test_red(red)


def _test_red(red: rebrickable_api.Color | rebrickable_api.ColorFull):
    assert red.id == 4
    assert red.name == "Red"
    assert red.rgb == "C91A09"
    assert not red.is_trans

    assert red.external_ids
    ids_lego = red.external_ids.lego
    assert ids_lego
    assert ids_lego.ext_ids == [21]
    assert "Bright red" in ids_lego.ext_descrs[0]


def test_get_element(lego_api: rebrickable_api.LegoApi):
    element = lego_api.get_element(element_id="4666579")
    assert element.element_id == "4666579"

    part = element.part
    assert part.part_num == "3749"
    assert "43093" in part.alternates
    ids_lego = part.external_ids.lego
    assert ids_lego
    assert "3749" in ids_lego
    assert part.print_of is None

    color = element.color
    assert color.id == 19
    assert color.name == "Tan"


def test_get_element_2(lego_api: rebrickable_api.LegoApi):
    element = lego_api.get_element(element_id="6522852")
    assert element.element_id == "6522852"

    part = element.part
    assert part.part_num == "3065pr0006"
    assert part.year_from == 2025
    assert part.part_img_url == "https://cdn.rebrickable.com/media/parts/elements/6522852.jpg"
    ids_lego = part.external_ids.lego
    assert ids_lego
    assert "110728" in ids_lego
    assert part.print_of == "3065"

    color = element.color
    assert color.id == 47
    assert color.name == "Trans-Clear"
    assert color.is_trans


def test_list_parts_search(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_parts(search="slope curved inverted double")
    assert resp.count >= 2
    assert resp.count == len(resp.results)

    parts = resp.results

    part = next(part for part in parts if part.part_num == "11301")
    assert re.search(r"(?i)curved.*\b2\b.+\b8\b", part.name)
    assert part.part_url
    ids_lego = part.external_ids.lego
    assert ids_lego
    assert "11301" in ids_lego


def test_get_part(lego_api: rebrickable_api.LegoApi):
    part = lego_api.get_part(part_num="3660")

    assert re.search(r"(?i)inverted.*\b45\b", part.name)
    assert part.part_url
    assert part.year_from == 1976
    assert part.part_img_url
    assert "3660pr0002" in part.prints
    assert "76959" in part.molds
    assert "3660b" in part.alternates
    assert part.print_of is None

    ids_lego = part.external_ids.lego
    assert ids_lego
    assert "3660" in ids_lego


def test_list_part_colors(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_part_colors(part_num="3660")
    assert resp.count >= 20
    assert resp.count == len(resp.results)

    colors = resp.results

    black = next(color for color in colors if color.color_id == 0 and color.color_name == "Black")
    assert black.num_sets >= 300
    assert "366026" in black.elements


def test_get_part_color(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.get_part_color(part_num="3660", color_id="1")

    assert resp.part_img_url
    assert resp.year_from == 1976
    assert resp.num_sets >= 100
    assert resp.num_set_parts >= 500
    assert "366023" in resp.elements


def test_list_part_color_sets(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_part_color_sets(part_num="3660", color_id="3")
    assert resp.count >= 3
    assert resp.count == len(resp.results)

    lset = next(lset for lset in resp.results if lset.set_num == "41433-1")
    assert lset.year == 2020
    assert lset.set_img_url
    assert "party" in lset.set_url.lower()


def test_list_sets_by_parts(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_sets(min_parts=1000, max_parts=1000)
    assert resp.count >= 16
    assert resp.count == len(resp.results)

    lset = next(lset for lset in resp.results if lset.set_num == "10705-1")
    assert "basket" in lset.name.lower()
    assert lset.year == 2016
    assert lset.num_parts == 1000
    assert lset.set_url
    assert lset.set_img_url


def test_get_set(lego_api: rebrickable_api.LegoApi):
    lset = lego_api.get_set(set_num="31124-1")
    assert lset.name == "Super Robot"
    assert lset.year == 2022
    assert lset.num_parts == 159
    assert lset.last_modified_dt > datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC)
    assert lset.last_modified_dt < datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
        days=100
    )
    assert lset.set_img_url


def test_list_set_alternates(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_set_alternates(set_num="11040-1")
    assert resp.count >= 5
    assert resp.count == len(resp.results)

    lset = next(lset for lset in resp.results if lset.set_num == "MOC-235303")
    assert lset.year == 2025
    assert 100 <= lset.num_parts <= 400
    assert lset.theme_id
    assert lset.moc_img_url
    assert "235303" in lset.moc_url
    assert lset.designer_name
    assert lset.designer_url


def test_list_set_parts(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_set_parts(set_num="60458-1", inc_minifig_parts=0)
    assert resp.count == len(resp.results) == 38
    parts = resp.results
    assert any(
        part.element_id == "6284574" and part.quantity == 2 and not part.is_spare for part in parts
    )
    assert any(
        part.element_id == "6284574" and part.quantity == 1 and part.is_spare for part in parts
    )
    assert all(part.set_num == "60458-1" for part in parts)

    resp = lego_api.list_set_parts(set_num="60458-1", inc_minifig_parts=1)
    assert resp.count == 47
    parts = resp.results
    assert any(part.set_num.startswith("fig-") for part in parts)


def test_list_set_minifigs(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_set_minifigs(set_num="60458-1")
    assert resp.count == len(resp.results) == 2

    assert any(
        "chef" in fig.set_name.lower()
        and fig.set_num == "fig-015987"
        and fig.id
        and fig.quantity == 1
        for fig in resp.results
    )


def test_list_minifigs(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_minifigs(in_set_num="60458-1")
    assert resp.count == len(resp.results) == 2

    assert any(
        "chef" in fig.name.lower() and "chef" in fig.set_url.lower() and fig.num_parts == 4
        for fig in resp.results
    )


def test_get_minifig(lego_api: rebrickable_api.LegoApi):
    fig = lego_api.get_minifig(set_num="fig-015987")

    assert fig.set_num == "fig-015987"
    assert "chef" in fig.name.lower()
    assert "chef" in fig.set_url.lower()
    assert fig.num_parts == 4


def test_list_minifig_parts(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_minifig_parts(set_num="fig-015987")

    assert resp.count == len(resp.results) == 4
    assert any(
        part.id
        and "chef" in part.part.name.lower()
        and "hat" in part.part.name.lower()
        and "hat" in part.part.part_url.lower()
        and part.part.part_img_url
        and part.part.external_ids.lego
        and part.color.id == 15
        and part.color.name == "White"
        and not part.color.is_trans
        and part.color.external_ids
        and part.color.external_ids.brick_link
        and part.set_num == "fig-015987"
        and part.quantity == 1
        and not part.is_spare
        and part.element_id == "6452529"
        and part.num_sets >= 50
        for part in resp.results
    )


def test_list_minifig_sets(lego_api: rebrickable_api.LegoApi):
    resp = lego_api.list_minifig_sets(set_num="fig-015987")

    assert resp.count >= 1
    assert len(resp.results) == resp.count
    assert any(
        lset.set_num == "60458-1"
        and "pizza" in lset.name.lower()
        and lset.num_parts >= 50
        and lset.set_img_url
        and lset.set_url
        for lset in resp.results
    )
