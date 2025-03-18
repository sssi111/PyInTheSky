import pytest
from pylatex_sssi111.latex_generator import generate_table_latex, generate_image_latex


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            [["Header1", "Header2"], ["Data1", "Data2"]],
            "\\begin{tabular}{ll}\n"
            "    Header1 & Header2 \\\\\n"
            "    Data1 & Data2 \\\\\n"
            "\\end{tabular}",
        ),
        ([], ""),
        (
            [["&", "\\"]],
            "\\begin{tabular}{ll}\n"
            "    \\& & \\textbackslash{} \\\\\n"
            "\\end{tabular}",
        ),
        ([["A", "B", "C"], [1, 2, 3, 4]], ""),
        (
            [["Line\nBreak", "Tab\tTest"]],
            "\\begin{tabular}{ll}\n"
            "    Line\\newline Break & Tab\\texttabulartest Test \\\\\n"
            "\\end{tabular}",
        ),
    ],
)
def test_table_generation(data, expected):
    assert generate_table_latex(data) == expected


def test_invalid_input():
    with pytest.raises(ValueError):
        generate_table_latex("invalid")


def test_invalid_input():
    with pytest.raises(ValueError):
        generate_image_latex(image_path="invalid image path")

    with pytest.raises(TypeError):
        generate_image_latex(image_path="img.png", width=123)


def test_edge_cases():
    assert "width=0.1\\textwidth" in generate_image_latex(
        image_path="small.jpg", width="0.1\\textwidth"
    )

    assert "width=2\\textwidth" in generate_image_latex(
        image_path="large.png", width="2\\textwidth"
    )

    assert "special_file_v2" in generate_image_latex(image_path="special_file_v2.png")
