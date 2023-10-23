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

class WalkersSchemeDemo(Scene):
    def construct(self):
        EVENT_NUMBER = 4
        BLOCK_WIDTH = 10 / EVENT_NUMBER
        
        blocks = VGroup(*[Rectangle(width=BLOCK_WIDTH) for _ in range(0, 4)])
        #blocks.arrange_in_grid(buff=0, rows=1, cols=EVENT_NUMBER)
        self.add(blocks)

        spacers = VGroup()
        for i in range(0, 4):
            RL = blocks[0].get_right() + blocks[0].get_bottom()
            RU = blocks[0].get_right() + blocks[0].get_top()
            self.add(Dot(RL, color=GREEN), Dot(RU, color=GREEN))
            spacers.add(Line(blocks[i].get_right() + blocks[i].get_bottom(), blocks[i].get_right() + blocks[i].get_top(), color=RED).scale(1.2))
        self.add(spacers)

        labels=VGroup()
        for i in range(1, 5):
            labels.add(Text(str(i)).next_to(blocks[i - 1], DOWN, buff=0.4))
        self.add(labels)



class CustomRectangleWithSpacer(VGroup):

    def __init__(self, scene, width=1, height=1, spacer_width=0.1, **kwargs):
        super().__init__(**kwargs)
        self.scene = scene

        # Create a rectangle
        rectangle = Rectangle()
        self.rectangle = rectangle
        rectangle.set_width(width)
        rectangle.set_height(height)
        self.add(rectangle)

        # Create a spacer inside the rectangle
        spacer = Line(UP, DOWN)
        spacer.set_width(spacer_width)
        spacer.set_color(BLUE)  # Customize spacer color if needed
        spacer.move_to(rectangle.get_right())
        self.add(spacer)
        self.spacer = spacer  # Save spacer as an attribute

    def move_spacer(self, position):
        return self.spacer.animate.move_to(self.rectangle.get_left() + (self.rectangle.get_right() - self.rectangle.get_left()) * position)
        

class SpacerMovement(Scene):
    def construct(self):
        # Create custom rectangle with spacer
        custom_rectangles = [CustomRectangleWithSpacer(scene=self, width=2, height=1, spacer_width=0.05) for _ in range (4)]
        rectangle_group = VGroup(*custom_rectangles).arrange(buff=0)
        rectangle_group.move_to(ORIGIN)

        # Show the custom rectangle with spacer
        self.add(rectangle_group)

        self.wait(1)
        self.play(rectangle_group[0].move_spacer(0.5))

        self.wait(1)
