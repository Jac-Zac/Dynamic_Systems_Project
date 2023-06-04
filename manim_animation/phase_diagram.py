#!/usr/bin/env manim -p -ql

import numpy as np
from manim import *

class VectorFieldExample(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[0,4],
            y_range=[0,3],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
            faded_line_ratio=4
        )

        diff_eq = lambda pos, a=1, b=1: np.array([
            plane.p2c(pos)[0] * (3 - a*plane.p2c(pos)[0] - b*plane.p2c(pos)[1]),
            plane.p2c(pos)[1] * (2 - plane.p2c(pos)[0] - plane.p2c(pos)[1]),
            0
        ])
        colors = [PINK,BLUE_E,PURPLE_D]

        # Add vector field
        field = ArrowVectorField(
                diff_eq, min_color_scheme_value=2, max_color_scheme_value=10, colors=colors,
                x_range=[plane.c2p(0,0)[0], plane.c2p(4,0)[0]],
                y_range=[plane.c2p(0,0)[1], plane.c2p(0,3)[1]]
                )

        self.add(plane)
        self.play(*[GrowArrow(vec) for vec in field])

        # Add streamlines
        stream_lines = StreamLines(
                diff_eq, stroke_width=2.5, max_anchors_per_line=30, colors=colors,
                x_range=[plane.c2p(0,0)[0], plane.c2p(4,0)[0]],
                y_range=[plane.c2p(0,0)[1], plane.c2p(0,3)[1]]
                )

        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=1)

        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)
