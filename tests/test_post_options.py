import pytest

from opencaxpy import PlotOptions, ViewerOptions


def test_plot_options_colors():
    options = PlotOptions(
        node_label_color=(1.0, 0.0, 0.0),
        edge_label_color=(0.0, 0.0, 1.0),
        cell_label_color=(0.0, 1.0, 0.0),
    )
    assert options.node_label_color == (1.0, 0.0, 0.0)


def test_viewer_options_visibility():
    options = ViewerOptions(
        show_node_ids=True,
        show_edge_ids=True,
        show_cell_ids=True,
        show_boundary=True,
    )
    assert options.show_node_ids
    assert options.show_edge_ids
    assert options.show_cell_ids
    assert options.show_boundary


def test_invalid_color_rejected():
    with pytest.raises(ValueError):
        ViewerOptions(node_color=(1.5, 0.0, 0.0))
