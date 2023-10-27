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

class CustomRectangleWithSpacer(VGroup):

    def __init__(self, scene, first_event, width=1, height=1, **kwargs):
        super().__init__(**kwargs)
        self.scene = scene
        self.id = first_event

        # Create a outline rectangle
        self.rectangle = Rectangle(width=width, height=height)
        self.add(self.rectangle)

        self.label = DecimalNumber(number=self.id + 1, color=COLORS[self.id], num_decimal_places=0)
        self.label.next_to(self.rectangle, UP)
        self.add(self.label)

        # Setup representation of event probabilities inside rectangle
        self.fe_rect = Rectangle(width=width, height=height)
        self.fe_rect.set_fill(color=COLORS[self.id], opacity=0.5)
        self.fe_rect.move_to(self.rectangle.get_center())
        self.add(self.fe_rect)
        self.se_rect = Rectangle(
            width=0,
            height=self.rectangle.height,
        ).move_to(self.rectangle.get_edge_center(RIGHT))
        self.add(self.se_rect)

        self.numbers = VGroup(
                DecimalNumber(number=0.25, color=COLORS[self.id], num_decimal_places=3),
                DecimalNumber(number=0.0, color=WHITE, num_decimal_places=3)
            )
        self.numbers.arrange(DOWN, buff=0.4).next_to(self.rectangle, DOWN, buff=0.4)
        self.add(self.numbers)

    def resize_events(self, new_value, second_event_id):

        old_fe_rect = self.fe_rect
        self.fe_rect = Rectangle(
            width=self.rectangle.width * new_value / 0.25,
            height=self.rectangle.height,
        ).set_fill(color=COLORS[self.id], opacity=0.5)
        self.fe_rect.move_to(self.rectangle.get_edge_center(LEFT) + [self.rectangle.width * new_value / (0.25 * 2), 0, 0])

        prev_width = self.se_rect.width
        old_se_rect = self.se_rect
        self.scene.remove(self.se_rect)
        self.se_rect = Rectangle(
            width=self.rectangle.width * (0.25 - new_value) / 0.25,
            height=self.rectangle.height,
        ).set_fill(color=COLORS[second_event_id], opacity=0.5)
        self.se_rect.move_to(self.rectangle.get_edge_center(RIGHT) - [self.rectangle.width * (0.25 - new_value) / (0.25 * 2), 0, 0])

        return (
            self.numbers[self.id].animate.set_value(new_value),
            self.numbers[second_event_id].animate.set_fill(color=COLORS[second_event_id])
                .set_value(0.25 - new_value),
            ReplacementTransform(old_fe_rect, self.fe_rect),
            ReplacementTransform(old_se_rect, self.se_rect),
        )
        
        

class SpacerMovement(Scene):
    def construct(self):
        # Create custom rectangle with spacer
        custom_rectangles = [CustomRectangleWithSpacer(scene=self, first_event=i, width=3, height=1) for i in range (4)]
        rectangle_group = VGroup(*custom_rectangles).arrange(buff=0)
        rectangle_group.move_to(ORIGIN).shift(UP)

        # Show the custom rectangle with spacer
        self.add(rectangle_group)

        self.wait(1)
        self.play(*rectangle_group[0].resize_events(0.05, 1))

        self.wait(3)

        self.play(*rectangle_group[0].resize_events(0.125, 1))

        self.wait(3)
