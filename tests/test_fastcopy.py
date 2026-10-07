from fastcopy import sizeof_fmt


def test_sizeof_fmt_scales_by_thousands():
    assert sizeof_fmt(0) == "0.0B"
    assert sizeof_fmt(999) == "999.0B"
    assert sizeof_fmt(1000) == "1.0KB"
    assert sizeof_fmt(2_500_000) == "2.5MB"
    assert sizeof_fmt(3_000_000_000) == "3.0GB"


def test_sizeof_fmt_falls_through_to_terabytes():
    assert sizeof_fmt(5e12) == "5.0TB"


def test_sizeof_fmt_custom_suffix():
    assert sizeof_fmt(1500, suffix="iB") == "1.5KiB"
