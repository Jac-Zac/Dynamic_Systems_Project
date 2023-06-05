#!/usr/bin/env manim -p -ql

from manim import *

class VectorFieldExample(Scene):
    def construct(self):

        a = ValueTracker(1)
        b = ValueTracker(1)

        plane = NumberPlane(
            x_range=[0,4],
            y_range=[0,3],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True},
            faded_line_ratio=4
        )

        diff_eq = lambda pos: np.array([
            plane.p2c(pos)[0] * (3 - a.get_value()*plane.p2c(pos)[0] - b.get_value()*plane.p2c(pos)[1]),
            plane.p2c(pos)[1] * (2 - plane.p2c(pos)[0] - plane.p2c(pos)[1]),
            0
        ])
        colors = [PINK,BLUE_E,PURPLE_D]


        aslider = VGroup(
            NumberLine(x_range=[1,3,0.5],length=5, rotation=90*DEGREES).to_edge(LEFT)
        )
        aslider += Dot().set_color(RED).move_to(aslider[0].n2p(a.get_value()))
        aslider += Text("a").next_to(aslider[0], UP)

        def asliderUpdater(mobj):
            mobj[1].move_to(mobj[0].n2p(a.get_value()))
        aslider.add_updater(asliderUpdater)
        self.add(aslider)

        bslider = VGroup(
            NumberLine(x_range=[1,3,0.5],length=5, rotation=90*DEGREES).to_edge(RIGHT)
        )
        bslider += Dot().set_color(BLUE).move_to(bslider[0].n2p(b.get_value()))
        bslider += Text("b").next_to(bslider[0], UP)

        def bsliderUpdater(mobj):
            mobj[1].move_to(mobj[0].n2p(b.get_value()))
        bslider.add_updater(bsliderUpdater)
        self.add(bslider)

        # Add vector field
        field = always_redraw(lambda:
            ArrowVectorField(
                diff_eq, min_color_scheme_value=2, max_color_scheme_value=10, colors=colors,
                x_range=[plane.c2p(0,0)[0], plane.c2p(4,0)[0]],
                y_range=[plane.c2p(0,0)[1], plane.c2p(0,3)[1]]
            )
        )
        self.add(plane)
        self.play(*[GrowArrow(vec) for vec in field])

        # Add streamlines
        stream_lines = always_redraw(lambda:
            StreamLines(
                diff_eq, stroke_width=2.5, max_anchors_per_line=30, colors=colors,
                x_range=[plane.c2p(0,0)[0], plane.c2p(4,0)[0]],
                y_range=[plane.c2p(0,0)[1], plane.c2p(0,3)[1]]
            )
        )

        self.add(stream_lines)

        stream_lines.start_animation(warm_up=True, flow_speed=1)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)

        self.play(a.animate.set_value(2))
        self.wait()
        self.play(b.animate.set_value(2))
        self.wait()
