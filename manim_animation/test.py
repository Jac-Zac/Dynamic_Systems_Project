#!/usr/bin/env manim -p -ql

from manim import *

class ScaleVectorFieldFunction(Scene):
    def construct(self):
        def diff_eq(pos, a=1, b=1):
            x, y, _ = pos
            dx_dt = x * (3 - a * x - b * y)
            dy_dt = y * (2 - x - y)
            return np.array([dx_dt, dy_dt, 0])

        plane = NumberPlane()
        self.add(plane)

        a_label = MathTex("a = 1")
        b_label = MathTex("b = 1")
        a_label.to_corner(UL)
        b_label.next_to(a_label, DOWN)
        self.add(a_label, b_label)

        vector_field = ArrowVectorField(diff_eq)
        self.add(vector_field)
        self.wait()

        for a in np.linspace(1, 3, 5):
            for b in np.linspace(1, 3, 5):
                new_diff_eq = lambda pos: diff_eq(pos, a=a, b=b)
                new_vector_field = ArrowVectorField(new_diff_eq)
                self.play(vector_field.animate.become(new_vector_field))
                a_label.animate.set_text(f"a = {a:.2f}")
                b_label.animate.set_text(f"b = {b:.2f}")
