#!/usr/bin/env manim -p -qk

from manim import *


class VectorFieldExample(Scene):
    def construct(self):
        a = ValueTracker(1)
        b = ValueTracker(1)

        # Define a number plane
        plane = NumberPlane(
            # axes values
            x_range=[-0.5, 4],
            y_range=[-0.5, 3],
            # size of the graph
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
            faded_line_ratio=4,
        )

        # Define the function
        diff_eq = lambda pos: np.array(
            [
                plane.p2c(pos)[0]
                * (
                    3
                    - a.get_value() * plane.p2c(pos)[0]
                    - b.get_value() * plane.p2c(pos)[1]
                ),
                plane.p2c(pos)[1] * (2 - plane.p2c(pos)[0] - plane.p2c(pos)[1]),
                0,
            ]
        )

        # Define colors
        colors = [PINK, BLUE_E, PURPLE_D]

        # Define the sliders
        a_slider = VGroup(
            NumberLine(x_range=[1, 3, 0.25], length=5, rotation=90 * DEGREES).to_edge(
                LEFT
            )
        )

        b_slider = VGroup(
            NumberLine(x_range=[1, 3, 0.25], length=5, rotation=90 * DEGREES).to_edge(
                RIGHT
            )
        )

        # Add the dot and the text near the sliders
        a_dot = Dot().set_color(RED_E).move_to(a_slider[0].n2p(a.get_value()))
        a_slider += a_dot
        a_slider += Text("a").next_to(a_slider[0], UP)

        b_dot = Dot().set_color(BLUE_E).move_to(b_slider[0].n2p(b.get_value()))
        b_slider += b_dot
        b_slider += Text("b").next_to(b_slider[0], UP)

        # Create DecimalNumber objects for a and b
        a_dot_text = DecimalNumber(a.get_value(), num_decimal_places=2).scale(0.75)
        b_dot_text = DecimalNumber(b.get_value(), num_decimal_places=2).scale(0.75)

        # Add next to the dots
        a_dot_text.add_updater(lambda m: m.next_to(a_dot, RIGHT, buff=0.1))
        b_dot_text.add_updater(lambda m: m.next_to(b_dot, LEFT, buff=0.1))

        # Define the updates
        def a_sliderUpdater(mobj):
            mobj[1].move_to(mobj[0].n2p(a.get_value()))
            a_dot_text.set_value(a.get_value())

        def b_sliderUpdater(mobj):
            mobj[1].move_to(mobj[0].n2p(b.get_value()))
            b_dot_text.set_value(b.get_value())

        # Add the updates
        a_slider.add_updater(a_sliderUpdater)
        b_slider.add_updater(b_sliderUpdater)

        # define a vector field
        field = always_redraw(
            lambda: ArrowVectorField(
                diff_eq,
                min_color_scheme_value=2,
                max_color_scheme_value=10,
                colors=colors,
                x_range=[plane.c2p(0, 0)[0], plane.c2p(4, 0)[0]],
                y_range=[plane.c2p(0, 0)[1], plane.c2p(0, 3)[1]],
            )
        )

        # define streamlines
        stream_lines = always_redraw(
            lambda: StreamLines(
                diff_eq,
                stroke_width=2,
                max_anchors_per_line=30,
                colors=colors,
                x_range=[plane.c2p(0, 0)[0], plane.c2p(4, 0)[0]],
                y_range=[plane.c2p(0, 0)[1], plane.c2p(0, 3)[1]],
            )
        )

        # add the plane
        self.add(plane)

        # Draw the vector field
        self.play(*[GrowArrow(vec) for vec in field])

        # Add the vector field and streamlines
        self.add(field)

        # Add the sliders
        self.play(Write(a_slider), run_time=1)
        self.play(Write(b_slider), run_time=1)

        self.play(Write(a_dot_text))
        self.play(Write(b_dot_text))

        # Add text for the updater
        self.add(a_dot_text)
        self.add(b_dot_text)

        # Create the ranges where to show a and b
        a_range = [1.5, 2, 2.5, 3]
        b_range = [1.5, 2, 2.5, 3]

        # Show in different ranges
        for a_val, b_val in zip(a_range, b_range):
            self.play(stream_lines.create())  # uses virtual_time as run_time
            self.add(stream_lines)
            self.play(a.animate.set_value(a_val), b.animate.set_value(b_val))
            self.play(Uncreate(stream_lines), run_time=0.5)

        a_range = [1, 3]
        b_range = [3, 1]

        self.wait(2)

        # Show in different ranges
        for a_val, b_val in zip(a_range, b_range):
            self.play(stream_lines.create())
            self.add(stream_lines)
            self.play(a.animate.set_value(a_val), b.animate.set_value(b_val))
            self.play(Uncreate(stream_lines), run_time=0.5)

        self.play(stream_lines.create())
        self.play(FadeOut(stream_lines), run_time=1.5)

        self.wait(2)
