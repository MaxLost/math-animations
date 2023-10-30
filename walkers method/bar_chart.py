from manim import *

class ProbabilitySchemeAsBarChart(Scene):
    def construct(self):
        probabilities = [0.18, 0.48, 0.31, 0.03]

        scheme = BarChart(
            values=probabilities,
            bar_names=["1", "2", "3", "4"],
            y_range = [0, 0.5, 0.1],
            y_length=4,
            x_length=8,
            bar_fill_opacity=0.75,
            bar_colors=[BLUE_A, RED, YELLOW, GREEN],
            x_axis_config = {"font_size": 32},
            y_axis_config = {"font_size": 32},
        )
        c_bar_lbls = scheme.get_bar_labels(font_size=36)

        self.play(Create(scheme), Create(c_bar_lbls))
        self.pause()