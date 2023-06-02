from manim import *
import numpy as np

def system(point, t, a, b):
    x, y = point
    dx_dt = x * (3 - a * x - b * y)
    dy_dt = y * (2 - x - y)
    return np.array([dx_dt, dy_dt])

class PhaseDiagramAnimation(Scene):
    def construct(self):
        a_tracker = ValueTracker(1)
        b_tracker = ValueTracker(1)

        def update_phase_diagram(mob):
            # Remove all submobjects from the VGroup
            for submob in mob.submobjects[:]:
                mob.remove(submob)

            phase_diagram = StreamLines(
                lambda p, t: system(p, t, a_tracker.get_value(), b_tracker.get_value()),
                xrange=(1, 3, 0.5),
                yrange=(1, 3, 0.5),
            )
            # Add the new phase_diagram to the VGroup
            mob.add(phase_diagram)

        phase_diagram_mob = VGroup()
        phase_diagram_mob.add_updater(update_phase_diagram)
        self.add(phase_diagram_mob)

        self.play(
            a_tracker.animate.set_value(3),
            b_tracker.animate.set_value(3),
            run_time=5,
            rate_func=linear,
        )
        self.wait()
