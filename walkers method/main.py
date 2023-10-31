from manim import *
from functools import cmp_to_key

COLORS = [RED, GREEN, BLUE, YELLOW, WHITE]
N = 4
PROBABILITIES = [0.18, 0.48, 0.31, 0.03] 
RESIZE_TIME = 2

class CustomRectangleWithZones(VGroup):

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
                DecimalNumber(number=1/N, color=COLORS[self.id], num_decimal_places=3),
                DecimalNumber(number=0.0, color=WHITE, num_decimal_places=3)
            )
        self.numbers.arrange(DOWN, buff=0.4).next_to(self.rectangle, DOWN, buff=0.4)
        self.add(self.numbers)

    def resize_events(self, new_value, second_event_id):

        old_fe_rect = self.fe_rect
        self.fe_rect = Rectangle(
            width=self.rectangle.width * new_value / (1/N),
            height=self.rectangle.height,
        ).set_fill(color=COLORS[self.id], opacity=0.5)
        self.fe_rect.move_to(self.rectangle.get_edge_center(LEFT) + [self.rectangle.width * new_value / ((1/N) * 2), 0, 0])

        prev_width = self.se_rect.width
        old_se_rect = self.se_rect
        self.scene.remove(self.se_rect)
        self.se_rect = Rectangle(
            width=self.rectangle.width * ((1/N)- new_value) / (1/N),
            height=self.rectangle.height,
        ).set_fill(color=COLORS[second_event_id], opacity=0.5)
        self.se_rect.move_to(self.rectangle.get_edge_center(RIGHT) - [self.rectangle.width * ((1/N) - new_value) / ((1/N) * 2), 0, 0])

        return (
            self.numbers[0].animate(run_time=RESIZE_TIME).set_value(new_value),
            self.numbers[1].animate(run_time=RESIZE_TIME).set_fill(color=COLORS[second_event_id])
                .set_value((1/N) - new_value),
            ReplacementTransform(old_fe_rect, self.fe_rect, run_time=RESIZE_TIME),
            ReplacementTransform(old_se_rect, self.se_rect, run_time=RESIZE_TIME),
        )      

class AliasMethodAnimation(Scene):
    def construct(self):

        custom_rectangles = [CustomRectangleWithZones(scene=self, first_event=i, width=3, height=1) for i in range (N)]
        rectangle_group = VGroup(*custom_rectangles).arrange(buff=0)
        rectangle_group.move_to(ORIGIN).shift(UP)
        self.add(rectangle_group)
        
        labels = [f"P({i+1})" for i in range(N)]
        probs = [Variable(PROBABILITIES[i], MathTex(labels[i]), num_decimal_places=3) for i in range(N)]
        for i in range(N):
            probs[i].label.set_color(COLORS[i])
            probs[i].value.set_color(COLORS[i])

        probs = VGroup(*probs).arrange(buff=0.7)
        probs.move_to(ORIGIN).shift(3*DOWN)
        self.add(probs)

        self.wait(1)

        n = len(PROBABILITIES)
        self.alias = [0] * n
        self.prob = [0] * n

        scaled_probabilities = [prob * n for prob in PROBABILITIES]
        small = []
        large = []

        for i, prob in enumerate(scaled_probabilities):
            if prob < 1:
                small.append(i)
            else:
                large.append(i)

        # sorted(small, key=cmp_to_key(lambda x, y: PROBABILITIES[x] < PROBABILITIES[y]))
        # sorted(large, key=cmp_to_key(lambda x, y: PROBABILITIES[x] > PROBABILITIES[y]))

        while small and large:
            small_index = small.pop()
            large_index = large.pop()

            self.prob[small_index] = scaled_probabilities[small_index]
            self.alias[small_index] = large_index
            scaled_probabilities[large_index] = (scaled_probabilities[large_index] + scaled_probabilities[small_index]) - 1
            
            #Animate probability change for one block
            self.play(*custom_rectangles[small_index].resize_events(self.prob[small_index] / N, large_index), 
                      Indicate(probs[small_index], scale_factor=1.18, color=COLORS[small_index], run_time=RESIZE_TIME),
                      Indicate(probs[large_index], scale_factor=1.18, color=COLORS[large_index], run_time=RESIZE_TIME)
                      )
            self.wait(2)

            if scaled_probabilities[large_index] < 1:
                small.append(large_index)
            else:
                large.append(large_index)
        
        for remaining in small + large:
            self.prob[remaining] = 1
            self.play(*custom_rectangles[remaining].resize_events(self.prob[remaining] / N, -1))

        self.wait(3)