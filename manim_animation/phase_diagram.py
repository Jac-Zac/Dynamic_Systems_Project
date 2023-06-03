#!/usr/bin/env manim -p -ql

from manim import *

class ContinuousMotion(Scene):
    def construct(self):
        def func(pos):
            x, y = pos[0], pos[1]
            dxdt = x * (3 - a.get_value()*x - b.get_value()*y)
            dydt = y * (2 - x - y)
            return np.array([dxdt, dydt, 0])

        a = ValueTracker(1)
        b = ValueTracker(1)

        stream_lines = StreamLines(
            func,
            stroke_width=1,
            max_anchors_per_line=10,
            x_range=[0, 4, 0.1],
            y_range=[0, 3, 0.1],
        )
        stream_lines.scale(2.5)
        stream_lines.to_corner(DR)  # move to bottom left corner
        self.add(stream_lines)

        stream_lines.start_animation(warm_up=True, flow_speed=1)

        a_decimal = DecimalNumber(a.get_value(), num_decimal_places=1).next_to(stream_lines, UP, buff=0.5)
        b_decimal = DecimalNumber(b.get_value(), num_decimal_places=1).next_to(a_decimal, RIGHT, buff=0.5)

        self.play(
            Write(a_decimal),
            Write(b_decimal),
        )

        self.wait()

        self.play(
            ChangingDecimal(a_decimal, 3, rate_func=linear, run_time=3),
            ChangingDecimal(b_decimal, 3, rate_func=linear, run_time=3),
            UpdateFromFunc(
                stream_lines,
                lambda sl: sl.func == func,
            ),
            rate_func=linear,
            run_time=3,
        )

        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)
