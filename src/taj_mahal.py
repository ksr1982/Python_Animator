#!/usr/bin/env python3
"""
Cinematic 3D-Style Taj Mahal Architectural Animation for YouTube Shorts (1080x1920, 30 FPS).
Preserves the exact bilateral symmetry, Mughal onion-dome silhouette, four perspective-scaled
minarets, central Iwan entrance, converging reflecting pool, and cypress-lined gardens of the
reference photograph, re-lit in a dramatic midnight-blue nocturnal atmosphere.
"""

from manim import *
import numpy as np

# Configure Manim directly for vertical 9:16 YouTube Shorts (1080x1920 @ 30 FPS)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9.0
config.frame_height = 16.0
config.frame_rate = 30

# Cinematic Midnight Palette
COL_BG = "#080F1C"
COL_GLOW = "#142B42"
COL_GLOW_INNER = "#1E4266"
COL_MARBLE = "#FFF4E6"
COL_MARBLE_MID = "#EFE0CC"
COL_MARBLE_SHADOW = "#D9C7B2"
COL_RECESS = "#243447"
COL_RECESS_DEEP = "#162231"
COL_GOLD = "#D9AE62"
COL_GOLD_BRIGHT = "#F4D08A"
COL_WATER = "#19384A"
COL_WATER_DEEP = "#0E2330"
COL_WATER_HIGHLIGHT = "#7197A5"
COL_PATHWAY = "#B89B82"
COL_PATH_EDGE = "#8C7058"
COL_GRASS = "#183C32"
COL_CYPRESS = "#071F1C"
COL_CYPRESS_EDGE = "#123832"


# ==============================================================================
# ARCHITECTURAL HELPER FUNCTIONS
# ==============================================================================

def create_finial(scale: float = 1.0) -> VGroup:
    """Create a golden Mughal lotus-and-crescent finial."""
    finial = VGroup()
    stem = Line(ORIGIN, UP * 0.42 * scale, color=COL_GOLD_BRIGHT, stroke_width=2.6 * scale)
    orb1 = Circle(radius=0.045 * scale, color=COL_GOLD_BRIGHT, fill_color=COL_GOLD, fill_opacity=1.0, stroke_width=1.0)
    orb1.move_to(UP * 0.14 * scale)
    orb2 = Circle(radius=0.032 * scale, color=COL_GOLD_BRIGHT, fill_color=COL_GOLD, fill_opacity=1.0, stroke_width=1.0)
    orb2.move_to(UP * 0.27 * scale)
    crescent = Arc(
        radius=0.055 * scale, start_angle=-0.2 * PI, angle=1.4 * PI,
        color=COL_GOLD_BRIGHT, stroke_width=2.2 * scale
    ).move_to(UP * 0.38 * scale)
    finial.add(stem, orb1, orb2, crescent)
    return finial


def create_dome(width: float = 2.0, height: float = 1.65, with_drum: bool = True) -> VGroup:
    """
    Construct a Mughal onion-shaped dome using smooth Bezier curves,
    a cylindrical marble drum, lotus necking, and golden finial.
    """
    dome_group = VGroup()
    w = width / 2.0
    h = height

    if with_drum:
        drum_h = h * 0.26
        drum = Rectangle(
            width=width * 0.94, height=drum_h,
            fill_color=COL_MARBLE_MID, fill_opacity=1.0,
            stroke_color=COL_GOLD, stroke_width=1.4
        )
        drum.move_to(UP * (drum_h / 2.0))
        band = Line(
            LEFT * (w * 0.94) + UP * (drum_h * 0.85),
            RIGHT * (w * 0.94) + UP * (drum_h * 0.85),
            color=COL_GOLD, stroke_width=1.8
        )
        dome_group.add(drum, band)
        base_y = drum_h
    else:
        base_y = 0.0

    # Onion-dome profile: slight inward pinch at neck, swelling outward, tapering to pointed apex
    pts = [
        np.array([-w * 0.88, base_y, 0.0]),
        np.array([-w * 1.04, base_y + h * 0.28, 0.0]),
        np.array([-w * 0.96, base_y + h * 0.56, 0.0]),
        np.array([-w * 0.42, base_y + h * 0.84, 0.0]),
        np.array([0.0, base_y + h * 1.02, 0.0]),
        np.array([w * 0.42, base_y + h * 0.84, 0.0]),
        np.array([w * 0.96, base_y + h * 0.56, 0.0]),
        np.array([w * 1.04, base_y + h * 0.28, 0.0]),
        np.array([w * 0.88, base_y, 0.0]),
    ]
    bulb = VMobject(
        fill_color=COL_MARBLE, fill_opacity=1.0,
        stroke_color=COL_MARBLE_SHADOW, stroke_width=1.6
    )
    bulb.set_points_as_corners(pts)
    bulb.make_smooth()
    bulb.add_line_to(pts[0])

    # Subtle right-side shading crescent for 3D spherical volume
    shade_pts = [
        np.array([w * 0.15, base_y, 0.0]),
        np.array([w * 0.52, base_y + h * 0.35, 0.0]),
        np.array([w * 0.42, base_y + h * 0.72, 0.0]),
        np.array([0.0, base_y + h * 1.01, 0.0]),
        np.array([w * 0.42, base_y + h * 0.84, 0.0]),
        np.array([w * 0.96, base_y + h * 0.56, 0.0]),
        np.array([w * 1.04, base_y + h * 0.28, 0.0]),
        np.array([w * 0.88, base_y, 0.0]),
    ]
    shade = VMobject(fill_color=COL_MARBLE_SHADOW, fill_opacity=0.45, stroke_width=0)
    shade.set_points_as_corners(shade_pts)
    shade.make_smooth()
    shade.add_line_to(shade_pts[0])

    finial = create_finial(scale=max(0.55, width * 0.52))
    finial.move_to(np.array([0.0, base_y + h * 1.01, 0.0]), aligned_edge=DOWN)

    dome_group.add(bulb, shade, finial)
    return dome_group


def create_arch(width: float = 1.1, height: float = 1.65, is_main_iwan: bool = False) -> VGroup:
    """Create a pointed Mughal arch with rectangular framing and recessed interior."""
    arch_grp = VGroup()
    w = width / 2.0
    h = height

    # Outer rectangular spandrel frame
    frame = Rectangle(
        width=width * 1.18, height=height * 1.12,
        fill_color=COL_MARBLE_MID if is_main_iwan else COL_MARBLE,
        fill_opacity=1.0,
        stroke_color=COL_GOLD if is_main_iwan else COL_MARBLE_SHADOW,
        stroke_width=2.0 if is_main_iwan else 1.2
    )

    # Pointed Islamic arch silhouette
    spring_y = -h * 0.5 + h * 0.56
    arch_pts = [
        np.array([-w, -h * 0.5, 0.0]),
        np.array([-w, spring_y, 0.0]),
        np.array([-w * 0.72, spring_y + h * 0.26, 0.0]),
        np.array([0.0, h * 0.5, 0.0]),
        np.array([w * 0.72, spring_y + h * 0.26, 0.0]),
        np.array([w, spring_y, 0.0]),
        np.array([w, -h * 0.5, 0.0]),
    ]
    niche = VMobject(
        fill_color=COL_RECESS if is_main_iwan else COL_RECESS_DEEP,
        fill_opacity=0.95,
        stroke_color=COL_GOLD,
        stroke_width=1.8 if is_main_iwan else 1.1
    )
    niche.set_points_as_corners(arch_pts)
    niche.make_smooth()
    niche.add_line_to(arch_pts[0])

    arch_grp.add(frame, niche)

    # Inner doorway & upper window detail inside the central Iwan
    if is_main_iwan:
        inner_door = RoundedRectangle(
            width=width * 0.42, height=height * 0.34, corner_radius=0.08,
            fill_color="#0F1824", fill_opacity=1.0,
            stroke_color=COL_GOLD, stroke_width=1.2
        ).move_to(DOWN * (height * 0.31))
        upper_win = RoundedRectangle(
            width=width * 0.38, height=height * 0.22, corner_radius=0.06,
            fill_color="#121E2D", fill_opacity=1.0,
            stroke_color=COL_GOLD, stroke_width=1.0
        ).move_to(UP * (height * 0.04))
        arch_grp.add(inner_door, upper_win)

    return arch_grp


def create_minaret(height: float = 3.55, base_width: float = 0.34, depth_scale: float = 1.0) -> VGroup:
    """
    Create a tapered cylindrical Taj Mahal minaret with 3 balcony rings,
    open chhatri cupola, and golden finial.
    """
    minaret = VGroup()
    h = height * depth_scale
    bw = base_width * depth_scale
    tw = bw * 0.68

    # Plinth base
    plinth = Rectangle(
        width=bw * 1.35, height=h * 0.06,
        fill_color=COL_MARBLE_MID, fill_opacity=1.0,
        stroke_color=COL_MARBLE_SHADOW, stroke_width=1.0
    ).move_to(UP * (h * 0.03))

    # Tapered main shaft
    shaft = Polygon(
        np.array([-bw / 2.0, h * 0.06, 0.0]),
        np.array([bw / 2.0, h * 0.06, 0.0]),
        np.array([tw / 2.0, h * 0.84, 0.0]),
        np.array([-tw / 2.0, h * 0.84, 0.0]),
        fill_color=COL_MARBLE, fill_opacity=1.0,
        stroke_color=COL_MARBLE_SHADOW, stroke_width=1.2
    )

    # Vertical shadow strip along right edge for cylindrical depth
    shadow_strip = Polygon(
        np.array([bw * 0.14, h * 0.06, 0.0]),
        np.array([bw / 2.0, h * 0.06, 0.0]),
        np.array([tw / 2.0, h * 0.84, 0.0]),
        np.array([tw * 0.14, h * 0.84, 0.0]),
        fill_color=COL_MARBLE_SHADOW, fill_opacity=0.5, stroke_width=0
    )

    minaret.add(plinth, shaft, shadow_strip)

    # Three projecting balcony rings
    for frac in (0.31, 0.57, 0.83):
        ring_w = bw * (1.0 - 0.30 * frac) * 1.38
        balcony = RoundedRectangle(
            width=ring_w, height=h * 0.026, corner_radius=0.015,
            fill_color=COL_MARBLE_MID, fill_opacity=1.0,
            stroke_color=COL_GOLD, stroke_width=1.3 * depth_scale
        ).move_to(UP * (h * frac))
        minaret.add(balcony)

    # Top open pavilion + cupola dome
    pavilion = Rectangle(
        width=tw * 0.82, height=h * 0.075,
        fill_color=COL_RECESS, fill_opacity=0.9,
        stroke_color=COL_MARBLE, stroke_width=1.2 * depth_scale
    ).move_to(UP * (h * 0.878))

    cupola = create_dome(width=tw * 1.15, height=h * 0.10, with_drum=False)
    cupola.move_to(UP * (h * 0.915), aligned_edge=DOWN)

    minaret.add(pavilion, cupola)
    return minaret


def create_building() -> tuple[VGroup, VGroup, VGroup]:
    """
    Assemble the complete central Taj Mahal mausoleum:
    Returns (main_facade_group, domes_group, minarets_group) aligned to platform base y = 0.
    """
    # 1. Elevated marble plinth (Chabutra)
    plinth = Rectangle(
        width=6.8, height=0.42,
        fill_color=COL_MARBLE_MID, fill_opacity=1.0,
        stroke_color=COL_MARBLE_SHADOW, stroke_width=1.4
    ).move_to(UP * 0.21)

    plinth_trim = Line(LEFT * 3.4 + UP * 0.42, RIGHT * 3.4 + UP * 0.42, color=COL_GOLD, stroke_width=1.8)

    # Decorative blind niches along the plinth
    plinth_niches = VGroup(*[
        Rectangle(
            width=0.22, height=0.20,
            fill_color=COL_MARBLE_SHADOW, fill_opacity=0.45,
            stroke_color=COL_MARBLE_SHADOW, stroke_width=0.8
        ).move_to(np.array([x, 0.20, 0.0]))
        for x in np.linspace(-3.05, 3.05, 17)
    ])

    # 2. Central marble facade block + chamfered side wings
    wing_left = Rectangle(
        width=0.92, height=1.72,
        fill_color=COL_MARBLE_MID, fill_opacity=1.0,
        stroke_color=COL_MARBLE_SHADOW, stroke_width=1.2
    ).move_to(LEFT * 1.48 + UP * (0.42 + 0.86))

    wing_right = Rectangle(
        width=0.92, height=1.72,
        fill_color=COL_MARBLE_SHADOW, fill_opacity=0.92,
        stroke_color=COL_MARBLE_SHADOW, stroke_width=1.2
    ).move_to(RIGHT * 1.48 + UP * (0.42 + 0.86))

    center_block = Rectangle(
        width=2.16, height=1.96,
        fill_color=COL_MARBLE, fill_opacity=1.0,
        stroke_color=COL_GOLD, stroke_width=1.6
    ).move_to(UP * (0.42 + 0.98))

    # Central monumental Pishtaq (Iwan)
    main_iwan = create_arch(width=1.18, height=1.56, is_main_iwan=True)
    main_iwan.move_to(UP * (0.42 + 0.88))

    # Side two-story arched bays
    side_arches = VGroup()
    for sx in (-1.48, 1.48):
        top_arch = create_arch(width=0.46, height=0.58, is_main_iwan=False).move_to(np.array([sx, 0.42 + 1.24, 0.0]))
        bot_arch = create_arch(width=0.46, height=0.58, is_main_iwan=False).move_to(np.array([sx, 0.42 + 0.48, 0.0]))
        side_arches.add(top_arch, bot_arch)

    # Slim corner Guldasta pinnacles framing the central Pishtaq
    guldastas = VGroup()
    for gx in (-1.08, 1.08, -1.94, 1.94):
        pin = Rectangle(
            width=0.07, height=2.12 if abs(gx) < 1.5 else 1.84,
            fill_color=COL_MARBLE, fill_opacity=1.0, stroke_color=COL_GOLD, stroke_width=1.0
        )
        pin.move_to(np.array([gx, 0.42 + pin.height / 2.0, 0.0]))
        cap = create_finial(scale=0.35).move_to(pin.get_top(), aligned_edge=DOWN)
        guldastas.add(pin, cap)

    facade_group = VGroup(plinth, plinth_trim, plinth_niches, wing_left, wing_right, center_block, main_iwan, side_arches, guldastas)

    # 3. Central onion dome + flanking chhatri domes
    main_dome = create_dome(width=1.78, height=1.52, with_drum=True)
    main_dome.move_to(UP * (0.42 + 1.96), aligned_edge=DOWN)

    left_chhatri = create_dome(width=0.66, height=0.58, with_drum=True)
    left_chhatri.move_to(LEFT * 1.26 + UP * (0.42 + 1.72), aligned_edge=DOWN)

    right_chhatri = create_dome(width=0.66, height=0.58, with_drum=True)
    right_chhatri.move_to(RIGHT * 1.26 + UP * (0.42 + 1.72), aligned_edge=DOWN)

    domes_group = VGroup(left_chhatri, right_chhatri, main_dome)

    # 4. Four minarets: two rear (smaller, closer in) and two front (taller, outer corners)
    rear_left = create_minaret(height=2.95, base_width=0.28, depth_scale=0.88).move_to(LEFT * 2.38 + UP * 0.42, aligned_edge=DOWN)
    rear_right = create_minaret(height=2.95, base_width=0.28, depth_scale=0.88).move_to(RIGHT * 2.38 + UP * 0.42, aligned_edge=DOWN)
    front_left = create_minaret(height=3.45, base_width=0.34, depth_scale=1.0).move_to(LEFT * 3.22 + UP * 0.42, aligned_edge=DOWN)
    front_right = create_minaret(height=3.45, base_width=0.34, depth_scale=1.0).move_to(RIGHT * 3.22 + UP * 0.42, aligned_edge=DOWN)

    minarets_group = VGroup(rear_left, rear_right, front_left, front_right)
    return facade_group, domes_group, minarets_group


def create_tree(height: float = 1.0) -> VGroup:
    """Create a dark green tapered Mughal cypress tree with subtle rim highlight."""
    tree = VGroup()
    w = height * 0.25
    trunk = Rectangle(
        width=w * 0.26, height=height * 0.14,
        fill_color="#1B1612", fill_opacity=1.0, stroke_width=0
    ).move_to(UP * (height * 0.07))

    foliage_pts = [
        np.array([0.0, height, 0.0]),
        np.array([-w * 0.62, height * 0.68, 0.0]),
        np.array([-w, height * 0.32, 0.0]),
        np.array([-w * 0.72, height * 0.10, 0.0]),
        np.array([w * 0.72, height * 0.10, 0.0]),
        np.array([w, height * 0.32, 0.0]),
        np.array([w * 0.62, height * 0.68, 0.0]),
    ]
    canopy = VMobject(
        fill_color=COL_CYPRESS, fill_opacity=1.0,
        stroke_color=COL_CYPRESS_EDGE, stroke_width=1.4
    )
    canopy.set_points_as_corners(foliage_pts)
    canopy.make_smooth()
    canopy.add_line_to(foliage_pts[0])

    tree.add(trunk, canopy)
    return tree


def create_reflection(architecture: VGroup, horizon_y: float) -> VGroup:
    """
    Duplicate and vertically mirror the Taj Mahal across the waterline,
    applying low opacity and a cool blue-green water tint.
    """
    refl = architecture.copy()
    refl.stretch(-1, dim=1, about_point=np.array([0.0, horizon_y, 0.0]))
    refl.stretch(0.92, dim=1, about_point=np.array([0.0, horizon_y, 0.0]))
    refl.set_color(interpolate_color(ManimColor(COL_MARBLE), ManimColor(COL_WATER_HIGHLIGHT), 0.58))
    refl.set_opacity(0.32)
    return refl


def create_water_ripples(horizon_y: float, bottom_y: float) -> VGroup:
    """Create horizontal perspective-spaced water ripples across the reflecting pool."""
    ripples = VGroup()
    num_lines = 26
    for i in range(num_lines):
        t = (i + 1) / (num_lines + 1)
        # Non-linear perspective spacing (denser near horizon, wider in foreground)
        y = horizon_y - (horizon_y - bottom_y) * (t ** 1.35)
        half_w = 0.72 + 1.85 * (t ** 1.15)
        seg_w = half_w * (0.45 + 0.35 * np.sin(i * 2.1))
        offset_x = 0.25 * np.cos(i * 1.7)
        line = Line(
            np.array([offset_x - seg_w, y, 0.0]),
            np.array([offset_x + seg_w, y, 0.0]),
            color=COL_WATER_HIGHLIGHT,
            stroke_width=1.1 + 1.2 * t,
            stroke_opacity=0.16 + 0.22 * (1.0 - t)
        )
        ripples.add(line)
    return ripples


# ==============================================================================
# MAIN CINEMATIC SCENE
# ==============================================================================

class TajMahalCartoon(MovingCameraScene):
    def construct(self):
        self.camera.background_color = COL_BG
        horizon_y = 0.45
        bottom_y = -8.0

        # ----------------------------------------------------------------------
        # SCENE 1: Cinematic Introduction (0–3s)
        # ----------------------------------------------------------------------
        glow_outer = Circle(radius=4.6, fill_color=COL_GLOW, fill_opacity=0.42, stroke_width=0).move_to(UP * 2.2)
        glow_inner = Circle(radius=2.7, fill_color=COL_GLOW_INNER, fill_opacity=0.38, stroke_width=0).move_to(UP * 2.4)

        # Subtle nocturnal starfield above the horizon
        rng = np.random.default_rng(27)
        stars = VGroup(*[
            Dot(
                point=np.array([rng.uniform(-4.3, 4.3), rng.uniform(1.2, 7.6), 0.0]),
                radius=rng.uniform(0.012, 0.028),
                color=COL_MARBLE,
                fill_opacity=rng.uniform(0.25, 0.75)
            )
            for _ in range(42)
        ])

        facade, domes, minarets = create_building()
        full_building = VGroup(facade, domes, minarets)
        full_building.move_to(UP * horizon_y, aligned_edge=DOWN)

        silhouette = full_building.copy().set_fill("#0D1B2E", opacity=0.95).set_stroke("#1D3554", width=1.2)

        self.camera.frame.save_state()
        self.camera.frame.scale(1.12).move_to(UP * 0.4)

        self.play(
            FadeIn(glow_outer, run_time=1.4),
            FadeIn(glow_inner, run_time=1.6),
            FadeIn(stars, run_time=1.6),
            FadeIn(silhouette, run_time=1.8),
            self.camera.frame.animate.scale(1.0 / 1.12).move_to(ORIGIN),
            run_time=3.0,
            rate_func=smooth
        )

        # ----------------------------------------------------------------------
        # SCENE 2: Architectural Construction (3–8s)
        # ----------------------------------------------------------------------
        self.play(
            FadeOut(silhouette, run_time=0.9),
            DrawBorderThenFill(facade, run_time=2.4),
        )
        # Central onion dome & flanking chhatri cupolas rise into position
        domes_start = domes.copy().shift(DOWN * 0.35).set_opacity(0.0)
        self.add(domes)
        domes.save_state()
        domes.become(domes_start)
        self.play(
            Restore(domes),
            run_time=2.0,
            rate_func=smooth
        )

        # ----------------------------------------------------------------------
        # SCENE 3: Minaret Reveal (8–12s)
        # ----------------------------------------------------------------------
        # Rear minarets first, then outer foreground minarets
        ordered_minarets = [minarets[0], minarets[1], minarets[2], minarets[3]]
        self.play(
            LaggedStart(
                *[GrowFromEdge(m, DOWN) for m in ordered_minarets],
                lag_ratio=0.25
            ),
            run_time=3.2,
            rate_func=smooth
        )
        self.play(
            Indicate(domes[2], color=COL_GOLD_BRIGHT, scale_factor=1.03),
            run_time=0.8
        )

        # ----------------------------------------------------------------------
        # SCENE 4: Gardens and Cypress Trees (12–16s)
        # ----------------------------------------------------------------------
        # Ground plane & symmetrical lawns
        ground = Polygon(
            np.array([-4.5, horizon_y, 0.0]),
            np.array([4.5, horizon_y, 0.0]),
            np.array([4.5, bottom_y, 0.0]),
            np.array([-4.5, bottom_y, 0.0]),
            fill_color=COL_GRASS, fill_opacity=1.0, stroke_width=0
        )

        # Converging sandstone walkways flanking the central reflecting pool
        left_walk = Polygon(
            np.array([-1.05, horizon_y, 0.0]),
            np.array([-0.68, horizon_y, 0.0]),
            np.array([-2.55, bottom_y, 0.0]),
            np.array([-3.75, bottom_y, 0.0]),
            fill_color=COL_PATHWAY, fill_opacity=0.95,
            stroke_color=COL_PATH_EDGE, stroke_width=1.4
        )
        right_walk = Polygon(
            np.array([0.68, horizon_y, 0.0]),
            np.array([1.05, horizon_y, 0.0]),
            np.array([3.75, bottom_y, 0.0]),
            np.array([2.55, bottom_y, 0.0]),
            fill_color=COL_PATHWAY, fill_opacity=0.95,
            stroke_color=COL_PATH_EDGE, stroke_width=1.4
        )

        # Perspective-scaled cypress trees lining both pathways (background -> foreground)
        trees = VGroup()
        tree_specs = [
            (0.10, 0.58),
            (0.24, 0.82),
            (0.42, 1.15),
            (0.64, 1.58),
            (0.88, 2.15),
        ]
        for t, h in tree_specs:
            y = horizon_y - (horizon_y - bottom_y) * (t ** 1.18)
            x_offset = 1.18 + 2.65 * (t ** 1.12)
            t_left = create_tree(height=h).move_to(np.array([-x_offset, y, 0.0]), aligned_edge=DOWN)
            t_right = create_tree(height=h).move_to(np.array([x_offset, y, 0.0]), aligned_edge=DOWN)
            trees.add(t_left, t_right)

        self.play(
            FadeIn(ground, run_time=1.0),
            FadeIn(left_walk, run_time=1.2),
            FadeIn(right_walk, run_time=1.2),
        )
        self.play(
            LaggedStart(
                *[GrowFromEdge(tr, DOWN) for tr in trees],
                lag_ratio=0.12
            ),
            run_time=2.8,
            rate_func=smooth
        )

        # ----------------------------------------------------------------------
        # SCENE 5: Reflection Pool & Animated Ripples (16–21s)
        # ----------------------------------------------------------------------
        pool = Polygon(
            np.array([-0.68, horizon_y, 0.0]),
            np.array([0.68, horizon_y, 0.0]),
            np.array([2.55, bottom_y, 0.0]),
            np.array([-2.55, bottom_y, 0.0]),
            fill_color=COL_WATER, fill_opacity=1.0,
            stroke_color=COL_MARBLE_SHADOW, stroke_width=1.8
        )

        # Central fountain spine & nozzles matching reference photograph
        fountains = VGroup()
        for t in np.linspace(0.08, 0.94, 11):
            fy = horizon_y - (horizon_y - bottom_y) * (t ** 1.25)
            f_rad = 0.025 + 0.085 * t
            nozzle = Ellipse(
                width=f_rad * 1.4, height=f_rad * 2.1,
                fill_color="#3A2820", fill_opacity=0.9,
                stroke_color=COL_GOLD, stroke_width=0.9
            ).move_to(np.array([0.0, fy, 0.0]))
            fountains.add(nozzle)

        # Subtle depth gradient fade over the lower half of the pool
        pool_fade = Polygon(
            np.array([-1.55, -3.5, 0.0]),
            np.array([1.55, -3.5, 0.0]),
            np.array([2.55, bottom_y, 0.0]),
            np.array([-2.55, bottom_y, 0.0]),
            fill_color=COL_WATER_DEEP, fill_opacity=0.62, stroke_width=0
        )

        reflection = create_reflection(full_building, horizon_y)
        ripples = create_water_ripples(horizon_y, bottom_y)

        # Bring foreground framing elements above the reflection so nothing overlaps improperly
        self.play(FadeIn(pool, run_time=1.0))
        self.add(reflection, pool_fade, ripples, fountains, left_walk, right_walk, trees)

        self.play(
            FadeIn(reflection, shift=DOWN * 0.15, run_time=1.8),
            Create(ripples, run_time=1.8),
            FadeIn(fountains, run_time=1.4),
        )

        # Gentle horizontal water shimmer animation
        self.play(
            ripples.animate.shift(RIGHT * 0.06),
            reflection.animate.shift(LEFT * 0.02),
            run_time=1.1,
            rate_func=there_and_back
        )
        self.play(
            ripples.animate.shift(LEFT * 0.06),
            reflection.animate.shift(RIGHT * 0.02),
            run_time=1.1,
            rate_func=there_and_back
        )

        # ----------------------------------------------------------------------
        # SCENE 6: Cinematic Final Reveal & Hold (21–26s)
        # ----------------------------------------------------------------------
        dome_halo = Circle(
            radius=1.35, fill_color=COL_GOLD_BRIGHT, fill_opacity=0.14, stroke_width=0
        ).move_to(domes[2].get_center())

        self.play(
            FadeIn(dome_halo, run_time=1.4),
            self.camera.frame.animate.scale(1.04).move_to(DOWN * 0.15),
            ripples.animate.shift(RIGHT * 0.04),
            run_time=3.2,
            rate_func=smooth
        )
        self.wait(1.8)
