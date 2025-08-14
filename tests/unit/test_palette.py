from palette import load_color_palette


def test_full_palette():
    palette = load_color_palette()
    assert len(palette.palette.colors) == 256
