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

COLORS = [RED, GREEN, BLUE, YELLOW]

class RectangleWithNumber(VGroup):

    def __init__(self, scene, color, value, width=1, height=1, **kwargs):
        super().__init__(**kwargs)
        self.scene = scene

        rectangle = Rectangle(height=height, width=width)
        rectangle.set_fill(color, opacity=0.7)
        self.rectangle = rectangle
        self.add(rectangle)

        number = DecimalNumber(number=value, color=color)
        self.number = number
        number.align_to(rectangle.center)
        self.add(number)

    def horizontal_resize(self, k):
        return(self.rectangle.stretch_to_fit_width(k * self.rectangle.width), self.number.move_to(self.rectangle.center))




class CustomRectangleWithSpacer(VGroup):

    def __init__(self, scene, first_event, width=1, height=1, spacer_width=0.1, **kwargs):
        super().__init__(**kwargs)
        self.scene = scene

        # Create a outline rectangle
        rectangle = Rectangle()
        self.rectangle = rectangle
        rectangle.set_width(width)
        rectangle.set_height(height)
        self.add(rectangle)

        # Create a spacer inside the rectangle
        spacer = Line(UP, DOWN)
        spacer.set_length(spacer_width)
        spacer.set_color(WHITE)  # Customize spacer color if needed
        self.spacer_vertical_offset = [0, 0.05, 0]
        spacer.move_to(rectangle.get_right() + self.spacer_vertical_offset)
        self.add(spacer)
        self.spacer = spacer  # Save spacer as an attribute

        # Setup representation of event probabilities inside rectangle
        self.first_event_id = first_event
        self.first_event = RectangleWithNumber(scene, COLORS[self.first_event_id], value = 0.25)
        self.add(self.first_event)
        self.second_event_id = first_event
        self.second_event = RectangleWithNumber(scene, WHITE, value = 0)
        self.add(self.second_event)

    def resize_spacer(self, k):
        left_side = self.rectangle.get_left()
        right_side = self.rectangle.get_right()
        spacer_anim = self.spacer.animate.move_to(left_side + self.spacer_vertical_offset + (right_side - left_side) * k)
        first_event_anim = self.first_event.horizontal_resize(k)
        second_event_anim = self.second_event.horizontal_resize(1 + k)
        return (spacer_anim, first_event_anim, second_event_anim)
        
        

class SpacerMovement(Scene):
    def construct(self):
        # Create custom rectangle with spacer
        custom_rectangles = [CustomRectangleWithSpacer(scene=self, first_event=i, width=2, height=1, spacer_width=1.05) for i in range (4)]
        rectangle_group = VGroup(*custom_rectangles).arrange(buff=0)
        rectangle_group.move_to(ORIGIN)

        # Show the custom rectangle with spacer
        self.add(rectangle_group)

        self.wait(1)
        self.play(*rectangle_group[0].resize_spacer(0.5))

        self.wait(1)
