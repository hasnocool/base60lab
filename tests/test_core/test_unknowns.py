"""Tests for the core unknowns registry (updatable in place by experiments)."""

from base60lab.core.unknowns import UnknownEntry, UnknownsRegistry


def test_add_and_get_entry():
    reg = UnknownsRegistry()
    entry = UnknownEntry(
        id="base60.test.unknown",
        base=60,
        category="fractions",
        statement="test unknown",
        status="open",
    )
    reg.add(entry)
    assert reg.get("base60.test.unknown") is entry
    assert len(reg) == 1


def test_update_status_in_place():
    reg = UnknownsRegistry()
    reg.add(UnknownEntry(id="u1", base=12, category="geometry", statement="x", status="open"))
    reg.update_status("u1", "proven", evidence_id="exp_01", version="1.0.0")
    entry = reg.get("u1")
    assert entry.status == "proven"
    assert entry.version == "1.0.0"
    assert "exp_01" in entry.evidence


def test_update_nonexistent_raises():
    reg = UnknownsRegistry()
    try:
        reg.update_status("missing", "proven")
        assert False, "should have raised KeyError"
    except KeyError:
        pass


def test_list_by_base_and_status():
    reg = UnknownsRegistry()
    reg.add(UnknownEntry(id="a", base=10, category="f", statement="x", status="proven"))
    reg.add(UnknownEntry(id="b", base=60, category="f", statement="x", status="open"))
    reg.add(UnknownEntry(id="c", base=60, category="g", statement="x", status="conjecture"))
    assert len(reg.list_by_base(60)) == 2
    assert len(reg.list_by_status("open")) == 1
    assert len(reg.list_by_category("f")) == 2


def test_invalid_base_rejected():
    try:
        UnknownEntry(id="x", base=7, category="c", statement="s")
        assert False, "should have raised ValueError"
    except ValueError:
        pass


def test_invalid_status_rejected():
    try:
        UnknownEntry(id="x", base=10, category="c", statement="s", status="bogus")
        assert False, "should have raised ValueError"
    except ValueError:
        pass


def test_amend_in_place_overwrites():
    reg = UnknownsRegistry()
    reg.add(UnknownEntry(id="u", base=10, category="c", statement="v1", status="open", version="0.1.0"))
    reg.add(UnknownEntry(id="u", base=10, category="c", statement="v2", status="proven", version="1.0.0"))
    entry = reg.get("u")
    assert entry.statement == "v2"
    assert entry.status == "proven"
    assert entry.version == "1.0.0"
    assert len(reg) == 1
