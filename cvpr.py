"""
=============================================================================
  Manim + manim-slides  —  Reusable Presentation Template
=============================================================================
"""

from __future__ import annotations

from manim import (
    # core
    Scene, VMobject, VGroup, Mobject, AnimationGroup,
    # shapes
    Rectangle, Polygon, Ellipse, Square, RoundedRectangle, Arrow, Line, Dot, Circle, CurvedArrow, CubicBezier,
    # text
    Text, MathTex, Tex,
    # animations
    Write, FadeIn, FadeOut, GrowArrow, Create, DrawBorderThenFill,
    Transform, ReplacementTransform, TransformFromCopy, MoveToTarget, GrowFromCenter,
    Indicate,
    # utilities
    ORIGIN, UP, DOWN, LEFT, RIGHT, DR, DL, UR, UL,
    config, WHITE, BLACK, GRAY, DARK_GRAY, LIGHT_GRAY, BLUE, RED, GREEN, YELLOW,
    ManimColor, color_gradient,
    smooth, linear,
    PI, TAU,
    rate_functions,
)
from manim_slides import Slide

# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 1 — THEME  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Theme:
    """
    Centralised design-token store.
    """

    # ── Canvas ────────────────────────────────────────────────────────────────
    BG          = ManimColor("#0A0A0A")       
    SLIDE_W     = 14.22                       
    SLIDE_H     = 8.0

    # ── Palette ───────────────────────────────────────────────────────────────
    PRIMARY     = ManimColor("#4FC3F7")       # sky-blue  → "Neural Networks"
    ACCENT_RED  = ManimColor("#EF5350")       # coral-red → "Data"
    ACCENT_GOLD = ManimColor("#FFD54F")       # amber     → highlight / goal
    NEUTRAL     = ManimColor("#ECEFF1")       # near-white text
    DIM         = ManimColor("#546E7A")       # muted border / secondary
    SUCCESS     = ManimColor("#66BB6A")       # green 

    # ── Box styling ───────────────────────────────────────────────────────────
    BOX_BORDER      = NEUTRAL
    BOX_FILL        = ManimColor("#111111")   
    BOX_FILL_ALT    = ManimColor("#1A1F2C")   
    BOX_STROKE_W    = 3
    BOX_SIDE        = 2.2                     

    # ── Arrow ─────────────────────────────────────────────────────────────────
    ARROW_COLOR     = NEUTRAL
    ARROW_STROKE_W  = 4
    ARROW_TIP_LEN   = 0.28

    # ── Typography ────────────────────────────────────────────────────────────
    FONT_TITLE      = "sans-serif"                  
    FONT_BODY       = "sans-serif"               

    SIZE_TITLE      = 46                      
    SIZE_LABEL      = 32                      
    SIZE_BODY       = 28                      
    SIZE_MATH       = 64                      

    # ── Layout ────────────────────────────────────────────────────────────────
    DIAGRAM_Y       = 0.8                    
    BOX_GAP         = 2.4                     


# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 2 — COMPONENT FACTORIES  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class BoxNode(VGroup):
    def __init__(
        self,
        symbol: str,
        caption: str,
        caption_color: ManimColor = Theme.NEUTRAL,
        box_fill: ManimColor = Theme.BOX_FILL,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.rect = Square(
            side_length=Theme.BOX_SIDE,
            stroke_color=Theme.BOX_BORDER,
            stroke_width=Theme.BOX_STROKE_W,
            fill_color=box_fill,
            fill_opacity=1,
        )

        self.symbol = MathTex(
            symbol,
            font_size=Theme.SIZE_MATH,
            color=Theme.NEUTRAL,
        ).move_to(self.rect.get_center())

        self.caption = Text(
            caption,
            font=Theme.FONT_BODY,
            font_size=Theme.SIZE_LABEL,
            color=caption_color,
            weight="BOLD",
        ).next_to(self.rect, DOWN, buff=0.35)

        self.add(self.rect, self.symbol, self.caption)


class ConnectArrow(VMobject):
    def __init__(self, start_mob: Mobject, end_mob: Mobject, **kwargs):
        super().__init__(**kwargs)
        arrow = Arrow(
            start=start_mob.get_right(),
            end=end_mob.get_left(),
            buff=0.12,
            stroke_width=Theme.ARROW_STROKE_W,
            color=Theme.ARROW_COLOR,
            tip_length=Theme.ARROW_TIP_LEN,
            max_stroke_width_to_length_ratio=999,
        )
        self.add(arrow)
        self._arrow = arrow


def build_flow_diagram(
    left_sym: str,  left_cap: str,  left_color: ManimColor,
    mid_sym: str,   mid_cap: str,   mid_color: ManimColor,
    right_sym: str, right_cap: str, right_color: ManimColor,
    y_center: float = Theme.DIAGRAM_Y,
    left_box_fill: ManimColor  = Theme.BOX_FILL,
    right_box_fill: ManimColor = Theme.BOX_FILL,
) -> tuple[BoxNode, ConnectArrow, BoxNode, ConnectArrow, BoxNode]:
    
    spacing = Theme.BOX_SIDE + Theme.BOX_GAP   

    node_L = BoxNode(left_sym,  left_cap,  left_color,  left_box_fill)
    node_M = BoxNode(mid_sym,   mid_cap,   mid_color,   Theme.BOX_FILL)
    node_R = BoxNode(right_sym, right_cap, right_color, right_box_fill)

    node_L.move_to([-spacing,  y_center, 0])
    node_M.move_to([0,         y_center, 0])
    node_R.move_to([ spacing,  y_center, 0])

    arrow_LM = ConnectArrow(node_L, node_M)
    arrow_MR = ConnectArrow(node_M, node_R)

    return node_L, arrow_LM, node_M, arrow_MR, node_R


def slide_title(text: str) -> Text:
    return (
        Text(
            text,
            font=Theme.FONT_TITLE,
            font_size=Theme.SIZE_TITLE,
            color=Theme.NEUTRAL,
        )
        .to_corner(UL, buff=0.6)
    )


def goal_text(heading: str, body: str) -> VGroup:
    h = Text(
        f"{heading}:",
        font=Theme.FONT_BODY,
        font_size=Theme.SIZE_BODY,
        color=Theme.NEUTRAL,
        weight="BOLD",
    )
    b = Text(
        body,
        font=Theme.FONT_BODY,
        font_size=Theme.SIZE_BODY,
        color=Theme.NEUTRAL,
    )
    b.next_to(h, DOWN, aligned_edge=LEFT, buff=0.18)
    group = VGroup(h, b)
    
    return group

# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 26 — SESSION TRANSITION CARD CLASS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class SessionIntroBase(Slide):
    """
    Lớp cơ sở để tạo slide chuyển cảnh giữa các Session.
    Đã lược bỏ thông tin về thời gian (time_slot).
    """
    session_num: str = "SESSION 01"
    presenter: str = "Presenter Name"
    title_text: str = "Title of the Talk"
    theme_color: ManimColor = Theme.PRIMARY

    def construct(self):
        self.camera.background_color = Theme.BG
        
        # 1. Dòng tiêu đề trên: Số Session (Accent Gold)
        session_label = Text(
            self.session_num, 
            font=Theme.FONT_TITLE, font_size=20, 
            color=Theme.ACCENT_GOLD, weight="BOLD"
        )
        
        # 2. Tên diễn giả chính (Cỡ chữ lớn, nổi bật)
        presenter_label = Text(
            self.presenter, 
            font=Theme.FONT_TITLE, font_size=36, 
            color=Theme.NEUTRAL, weight="BOLD"
        )
        
        # 3. Tiêu đề bài thuyết trình (Gióng hàng ngang, ngắt dòng thủ công)
        title_label = Text(
            self.title_text, 
            font=Theme.FONT_BODY, font_size=22, 
            color=self.theme_color, line_spacing=0.8,
            weight="BOLD"
        )
        
        # Chốt chặn chống tràn viền ngang: Ép tiêu đề dài luôn nằm gọn trong khung 9.0 đơn vị
        if title_label.width > 9.0:
            title_label.scale_to_fit_width(9.0)
            
        # 4. Đóng gói các dòng nội dung
        card_content = VGroup(session_label, presenter_label, title_label).arrange(DOWN, buff=0.45)
        
        # Tạo Thẻ (Card) bao ngoài tự động ôm sát nội dung văn bản cộng thêm đệm (Padding)
        card_width = max(card_content.width + 1.2, 9.5) # Giữ độ rộng tối thiểu 9.5 để đồng bộ
        card_height = card_content.height + 1.0
        
        card_border = RoundedRectangle(
            width=card_width,
            height=card_height,
            corner_radius=0.25,
            stroke_color=self.theme_color,
            stroke_width=2.5,
            fill_color=Theme.BOX_FILL_ALT,
            fill_opacity=1
        )
        card_content.move_to(card_border.get_center())
        
        # Hiệu ứng viền phát quang (glow border) mờ bao ngoài thẻ để tăng tính thẩm mỹ
        glow_border = RoundedRectangle(
            width=card_width + 0.1,
            height=card_height + 0.1,
            corner_radius=0.25,
            stroke_color=self.theme_color,
            stroke_width=1.0,
            stroke_opacity=0.3,
            fill_opacity=0
        )
        
        # Đóng gói và căn giữa tuyệt đối trên màn hình (An toàn tuyệt đối, tránh Lỗi 5)
        full_card = VGroup(glow_border, card_border, card_content)
        full_card.center()
        
        # 5. Kịch bản xuất hiện mượt mà
        self.play(
            DrawBorderThenFill(card_border),
            FadeIn(glow_border),
            run_time=0.8
        )
        self.play(
            FadeIn(session_label, shift=DOWN*0.1),
            run_time=0.3
        )
        self.play(Write(presenter_label), run_time=0.5)
        self.play(FadeIn(title_label, scale=0.9), run_time=0.5)
        
        self.next_slide()
        
# Session 1: Saining Xie
class Session1_Xie(SessionIntroBase):
    session_num = "SESSION 01"
    presenter = "Saining Xie"
    title_text = "Generating More with Less:\nA Representation Learning Perspective"
    theme_color = Theme.PRIMARY

# Session 2: Deepti Ghadiyaram
class Session2_Deepti(SessionIntroBase):
    session_num = "SESSION 02"
    presenter = "Deepti Ghadiyaram"
    title_text = "Advancing Safety, Alignment, and\nInterpretability in Generative Media"
    theme_color = Theme.ACCENT_GOLD

# Session 3: Jiatao Gu
class Session3_Gu(SessionIntroBase):
    session_num = "SESSION 03"
    presenter = "Jiatao Gu"
    title_text = "Scalable Normalizing Flows\nfor Visual Generation"
    theme_color = Theme.SUCCESS

# Session 4: Kaiming He
class Session4_He(SessionIntroBase):
    session_num = "SESSION 04"
    presenter = "Kaiming He"
    title_text = "Towards End-to-End\nGenerative Modeling"
    theme_color = Theme.PRIMARY

# Session 5: Sherry Yang
class Session5_Yang(SessionIntroBase):
    session_num = "SESSION 05"
    presenter = "Sherry Yang"
    title_text = "Scaling World Models for Agents"
    theme_color = Theme.ACCENT_RED

# Session 6: Arash Vahdat
class Session6_Vahdat(SessionIntroBase):
    session_num = "SESSION 06"
    presenter = "Arash Vahdat"
    title_text = "From Hundreds to One:\nOn Accelerated Sampling from Diffusion Models"
    theme_color = Theme.ACCENT_GOLD

# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 3 — MODULE 1: INTRO SLIDE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module1_Intro(Slide):

    def _setup_canvas(self):
        self.camera.background_color = Theme.BG

    def _build_slide1(self):
        title1 = slide_title("Supervised Learning")

        node_X1, arrow_Xf1, node_f1, arrow_fY1, node_Y1 = build_flow_diagram(
            left_sym  ="X",    left_cap  ="Data",           left_color  =Theme.ACCENT_RED,
            mid_sym   ="f",    mid_cap   ="Neural Networks", mid_color   =Theme.PRIMARY,
            right_sym ="Y",    right_cap ="Labels",          right_color =Theme.NEUTRAL,
        )

        return title1, node_X1, arrow_Xf1, node_f1, arrow_fY1, node_Y1

    def _build_slide2(self):
        title2 = slide_title("Self-Supervised Learning")

        node_X2, arrow_Xf2, node_f2, arrow_fXp2, node_Xp2 = build_flow_diagram(
            left_sym  ="X",   left_cap  ="Data",           left_color  =Theme.ACCENT_RED,
            mid_sym   ="f",   mid_cap   ="Neural Networks", mid_color   =Theme.PRIMARY,
            right_sym ="X'",  right_cap ="Data",            right_color =Theme.ACCENT_RED,
            right_box_fill=Theme.BOX_FILL_ALT,
        )

        goal_group = goal_text(
            "Goal",
            "To build background knowledge and approximate a form\n"
            "of common sense in AI systems.",
        )
        goal_group.next_to(node_X2, DOWN, buff=1.0, aligned_edge=LEFT)

        return title2, node_X2, arrow_Xf2, node_f2, arrow_fXp2, node_Xp2, goal_group

    def construct(self):
        self._setup_canvas()

        # ══════════════════════════════════════════════════════════════════════
        # SLIDE 1
        # ══════════════════════════════════════════════════════════════════════
        title1, node_X1, arrow_Xf1, node_f1, arrow_fY1, node_Y1 = self._build_slide1()

        self.play(Write(title1), run_time=0.8)
        self.play(DrawBorderThenFill(node_X1.rect), FadeIn(node_X1.symbol, scale=0.6), run_time=0.55)
        self.play(FadeIn(node_X1.caption, shift=DOWN * 0.2), run_time=0.35)
        self.play(GrowArrow(arrow_Xf1._arrow), run_time=0.4)

        self.play(DrawBorderThenFill(node_f1.rect), FadeIn(node_f1.symbol, scale=0.6), run_time=0.55)
        self.play(FadeIn(node_f1.caption, shift=DOWN * 0.2), run_time=0.35)
        self.play(GrowArrow(arrow_fY1._arrow), run_time=0.4)

        self.play(DrawBorderThenFill(node_Y1.rect), FadeIn(node_Y1.symbol, scale=0.6), run_time=0.55)
        self.play(FadeIn(node_Y1.caption, shift=DOWN * 0.2), run_time=0.35)

        self.next_slide()

        # ══════════════════════════════════════════════════════════════════════
        # SLIDE 2
        # ══════════════════════════════════════════════════════════════════════
        title2, node_X2, arrow_Xf2, node_f2, arrow_fXp2, node_Xp2, goal_grp = self._build_slide2()

        self.play(ReplacementTransform(title1, title2), run_time=0.8, rate_func=smooth)

        self.play(
            ReplacementTransform(node_X1.rect,    node_X2.rect),
            ReplacementTransform(node_X1.symbol,  node_X2.symbol),
            ReplacementTransform(node_X1.caption, node_X2.caption),
            ReplacementTransform(arrow_Xf1._arrow, arrow_Xf2._arrow),
            ReplacementTransform(node_f1.rect,    node_f2.rect),
            ReplacementTransform(node_f1.symbol,  node_f2.symbol),
            ReplacementTransform(node_f1.caption, node_f2.caption),
            ReplacementTransform(arrow_fY1._arrow, arrow_fXp2._arrow),
            run_time=0.9,
            rate_func=smooth,
        )

        self.play(
            ReplacementTransform(node_Y1.rect,    node_Xp2.rect),
            ReplacementTransform(node_Y1.symbol,  node_Xp2.symbol),
            ReplacementTransform(node_Y1.caption, node_Xp2.caption),
            run_time=0.75,
            rate_func=smooth,
        )

        self.play(FadeIn(goal_grp, shift=UP * 0.35), run_time=0.8)

        self.next_slide()
        self.wait(0.5)
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 4 — EXTRA COMPONENTS (DiT diagram)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────
 
class RoundedBox(VGroup):
    def __init__(
        self,
        lines: list[str],
        width: float = 1.5,
        height: float = 1.1,
        corner_radius: float = 0.15,
        fill_color: ManimColor = ManimColor("#2A2A2A"),
        stroke_color: ManimColor = ManimColor("#AAAAAA"),
        stroke_width: float = 2.0,
        font_size: int = 22,
        text_color: ManimColor = Theme.NEUTRAL,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.rect = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=corner_radius,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=1,
        )
        label_mobs = VGroup(*[
            Text(ln, font=Theme.FONT_BODY, font_size=font_size, color=text_color)
            for ln in lines
        ]).arrange(DOWN, buff=0.08)
        label_mobs.move_to(self.rect.get_center())
        self.label = label_mobs
        self.add(self.rect, self.label)
 
 
class SmallSquareNode(VGroup):
    def __init__(
        self,
        symbol: str,
        caption_lines: list[str],
        side: float = 0.9,
        font_size_sym: int = 40,
        font_size_cap: int = 24,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.rect = Square(
            side_length=side,
            stroke_color=Theme.NEUTRAL,
            stroke_width=2.0,
            fill_color=Theme.BOX_FILL,
            fill_opacity=1,
        )
        self.symbol = Text(
            symbol,
            font=Theme.FONT_BODY,
            font_size=font_size_sym,
            color=Theme.NEUTRAL,
            slant="ITALIC",
        ).move_to(self.rect.get_center())
 
        cap_mobs = VGroup(*[
            Text(ln, font=Theme.FONT_BODY, font_size=font_size_cap, color=Theme.NEUTRAL)
            for ln in caption_lines
        ]).arrange(DOWN, buff=0.06)
        cap_mobs.next_to(self.rect, DOWN, buff=0.2)
        self.caption = cap_mobs
 
        self.add(self.rect, self.symbol, self.caption)
 
 
def connect_arrow(box1, box2, buff=0.05, tip_length=0.15):
    """Hàm tạo mũi tên nối tự động giữa 2 hộp"""
    return Arrow(
        start=box1.get_right(),
        end=box2.get_left(),
        buff=buff, 
        stroke_width=3, 
        color=Theme.NEUTRAL, 
        tip_length=tip_length,
        max_stroke_width_to_length_ratio=999
    )

def curved_arrow(start_point, end_point, angle: float = -0.5) -> "CurvedArrow":
    from manim import CurvedArrow as _CA
    return _CA(
        start_point=start_point,
        end_point=end_point,
        angle=angle,
        color=Theme.NEUTRAL,
        stroke_width=2.5,
        tip_length=0.15,
    )
 
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 5 — MODULE 2: DiT / SiT SLIDE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────
 
class Module2_DiT(Slide):

    def _setup_canvas(self):
        self.camera.background_color = Theme.BG
 
    def construct(self):
        self._setup_canvas()
 
        # ══════════════════════════════════════════════════════════════════════
        # 1. TITLE
        # ══════════════════════════════════════════════════════════════════════
        title = slide_title("DiT/SiT: Scalable Diffusion Transformers")
        self.play(Write(title), run_time=0.7)
 
        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 1: KHỞI TẠO TẤT CẢ CÁC KHỐI (CHƯA VẼ MŨI TÊN)
        # ══════════════════════════════════════════════════════════════════════
        # Top Row
        img_rect = RoundedRectangle(width=1.2, height=1.0, corner_radius=0.1, stroke_color=Theme.NEUTRAL, stroke_width=2, fill_color=ManimColor("#4E3B2A"), fill_opacity=1)
        img_label = Text("Input image", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL).next_to(img_rect, DOWN, buff=0.15)
        img_group = VGroup(img_rect, img_label)
 
        vae_box = RoundedBox(["VAE Encoder", "(8x ↓)"], width=1.4, height=1.0, font_size=18)
        lock = Text("🔒", font_size=20).next_to(vae_box.rect, UP, buff=0.05)
        vae_group = VGroup(vae_box, lock)

        sl_box = RoundedBox(["Spatial", "Latent"], width=1.1, height=1.0, font_size=18)
        fp_box = RoundedBox(["Forward", "Process"], width=1.1, height=1.0, stroke_width=3.0, font_size=18)
        nl_box = RoundedBox(["Noised", "Latent"], width=1.1, height=1.0, font_size=18)
        dit_box = RoundedBox(["DiT"], width=2.0, height=1.8, corner_radius=0.2, font_size=42, fill_color=ManimColor("#0D0D0D"))
 
        top_row = VGroup(img_group, vae_group, sl_box, fp_box, nl_box, dit_box)
        top_row.arrange(RIGHT, buff=0.25) # Đã thu hẹp khoảng cách giữa các khối

        # Right Column (Losses)
        np_box = RoundedBox(["Noise", "Prediction"], width=1.5, height=0.7, font_size=16)
        cov_box = RoundedBox(["Covariance"], width=1.5, height=0.7, font_size=16)
        right_col = VGroup(np_box, cov_box).arrange(DOWN, buff=0.2).next_to(dit_box, RIGHT, buff=0.4)

        loss_box = RoundedBox(["Training losses"], width=1.5, height=0.9, font_size=18)
        loss_box.next_to(right_col, RIGHT, buff=0.4)

        # Bottom Nodes (t, c)
        t_node = SmallSquareNode("t", ["Forward process", "timestep"], side=0.7, font_size_sym=30, font_size_cap=18)
        c_node = SmallSquareNode("c", ["Conditional info", "(label, text)"], side=0.7, font_size_sym=30, font_size_cap=18)
        bottom_nodes = VGroup(t_node, c_node).arrange(DOWN, buff=0.4)
        
        # Căn khối t,c nằm ngay dưới VAE box
        bottom_nodes.next_to(top_row, DOWN, buff=0.8).align_to(vae_group, LEFT)

        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 2: GOM TẤT CẢ VÀ ÉP KHUNG SIZE CHUẨN (BÍ QUYẾT)
        # ══════════════════════════════════════════════════════════════════════
        master_diagram = VGroup(top_row, right_col, loss_box, bottom_nodes)
        
        # Chiều rộng màn hình là 14.22. Ép toàn bộ cụm này rộng tối đa 13.5
        master_diagram.set_width(13.5)
        
        # Đặt nó vào chính giữa màn hình, nhích xuống 0.3 để nhường chỗ cho Title
        master_diagram.center().shift(DOWN * 0.3)

        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 3: SAU KHI FIX VỊ TRÍ, BÂY GIỜ MỚI VẼ MŨI TÊN NỐI
        # ══════════════════════════════════════════════════════════════════════
        arr1 = connect_arrow(img_rect, vae_box.rect)
        arr2 = connect_arrow(vae_box.rect, sl_box.rect)
        arr3 = connect_arrow(sl_box.rect, fp_box.rect)
        arr4 = connect_arrow(fp_box.rect, nl_box.rect)
        arr5 = connect_arrow(nl_box.rect, dit_box.rect)

        # Nhánh rẽ từ DiT ra 2 hộp NP/Covariance
        stem_start = dit_box.rect.get_right()
        stem_end = stem_start + RIGHT * 0.2
        line_stem = Line(stem_start, stem_end, stroke_width=2.5)
        line_up = Line(stem_end, [stem_end[0], np_box.rect.get_left()[1], 0], stroke_width=2.5)
        line_down = Line(stem_end, [stem_end[0], cov_box.rect.get_left()[1], 0], stroke_width=2.5)
        arr_to_np = connect_arrow(line_up, np_box.rect, buff=0)
        arr_to_cov = connect_arrow(line_down, cov_box.rect, buff=0)

        # Nhánh chụm từ NP/Covariance vào Loss
        m_up = Line(np_box.rect.get_right(), [np_box.rect.get_right()[0] + 0.2, np_box.rect.get_right()[1], 0], stroke_width=2.5)
        m_down = Line(cov_box.rect.get_right(), [cov_box.rect.get_right()[0] + 0.2, cov_box.rect.get_right()[1], 0], stroke_width=2.5)
        m_vert = Line(m_up.get_end(), m_down.get_end(), stroke_width=2.5)
        arr_to_loss = Arrow(start=m_vert.get_center(), end=loss_box.rect.get_left(), buff=0.05, stroke_width=3, tip_length=0.15)

        # Mũi tên cong từ t và c
        c_arr_t_fp = curved_arrow(t_node.rect.get_right(), fp_box.rect.get_bottom(), angle=-0.5)
        c_arr_t_dit = curved_arrow(t_node.rect.get_right(), dit_box.rect.get_bottom() + LEFT*0.3, angle=-0.4)
        c_arr_c_dit = curved_arrow(c_node.rect.get_right(), dit_box.rect.get_bottom() + RIGHT*0.3, angle=-0.3)

        # ══════════════════════════════════════════════════════════════════════
        # CHẠY ANIMATION
        # ══════════════════════════════════════════════════════════════════════
        self.play(FadeIn(img_group), run_time=0.5)
        self.play(GrowArrow(arr1), DrawBorderThenFill(vae_box.rect), FadeIn(vae_box.label, lock), run_time=0.6)
        
        self.play(
            GrowArrow(arr2), DrawBorderThenFill(sl_box.rect), FadeIn(sl_box.label),
            GrowArrow(arr3), DrawBorderThenFill(fp_box.rect), FadeIn(fp_box.label),
            GrowArrow(arr4), DrawBorderThenFill(nl_box.rect), FadeIn(nl_box.label),
            run_time=1.0, lag_ratio=0.3
        )
        
        self.play(GrowArrow(arr5), DrawBorderThenFill(dit_box.rect), FadeIn(dit_box.label), run_time=0.6)

        self.play(
            Create(line_stem), Create(line_up), Create(line_down),
            GrowArrow(arr_to_np), GrowArrow(arr_to_cov),
            DrawBorderThenFill(np_box.rect), FadeIn(np_box.label),
            DrawBorderThenFill(cov_box.rect), FadeIn(cov_box.label),
            run_time=0.8
        )

        self.play(
            Create(m_up), Create(m_down), Create(m_vert), GrowArrow(arr_to_loss),
            DrawBorderThenFill(loss_box.rect), FadeIn(loss_box.label),
            run_time=0.6
        )

        self.play(
            FadeIn(t_node),
            Create(c_arr_t_fp), Create(c_arr_t_dit),
            run_time=0.8
        )
        self.play(
            FadeIn(c_node),
            Create(c_arr_c_dit),
            run_time=0.8
        )

        self.next_slide()
        self.wait(0.5)
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 6 — MODULE 3: GPT-3 / Chinchilla SLIDE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────
 
TEAL_FILL   = ManimColor("#3DAA88")    
TEAL_DARK   = ManimColor("#2C7A62")    
TEAL_STROKE = ManimColor("#55CCAA")    
 
class StackBar(VGroup):
    def __init__(
        self,
        label: str,
        width: float        = 5.8,
        height: float       = 0.72,
        fill_color: ManimColor = TEAL_FILL, 
        font_size: int      = 28,  # Giảm font chữ để an toàn
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.rect = Rectangle(
            width=width,
            height=height,
            stroke_color=Theme.NEUTRAL,
            stroke_width=2.2,
            fill_color=fill_color,
            fill_opacity=1,
        )
        self.label_mob = Text(
            label,
            font=Theme.FONT_BODY,
            font_size=font_size,
            color=Theme.NEUTRAL,
        ).move_to(self.rect.get_center())
        self.add(self.rect, self.label_mob)
 
 
class Module3_GPT(Slide):

    def _setup_canvas(self):
        self.camera.background_color = Theme.BG
 
    def construct(self):
        self._setup_canvas()
 
        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 1: TẠO TẤT CẢ CÁC COMPONENT (Chưa quan tâm vị trí)
        # ══════════════════════════════════════════════════════════════════════
        
        # 1. Các khối Stack
        decoder_bar = StackBar("Linear Decoder", fill_color=TEAL_DARK)
        
        dots = VGroup(*[Dot(radius=0.06, color=Theme.NEUTRAL) for _ in range(3)])
        dots.arrange(DOWN, buff=0.15)
        
        transformer_bars = [StackBar("Transformer Block") for _ in range(4)]
        tok_bar = StackBar("Tokenize")

        # 2. Text bên dưới
        quote = Text('"A dog walked over to the barn..."', font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        model_name = Text("GPT-3 / Chinchilla / ...", font=Theme.FONT_TITLE, font_size=42, weight="BOLD", color=Theme.NEUTRAL)

        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 2: AUTO LAYOUT ENGINGE (BÍ QUYẾT)
        # ══════════════════════════════════════════════════════════════════════
        
        # Nhóm toàn bộ cột stack (Xếp từ trên xuống dưới)
        stack_group = VGroup(decoder_bar, dots, *transformer_bars, tok_bar)
        stack_group.arrange(DOWN, buff=0.1)

        # Nhóm tổng toàn bộ slide
        master_group = VGroup(stack_group, quote, model_name)
        master_group.arrange(DOWN, buff=0.5)

        # ÉP CHIỀU CAO TỐI ĐA! Chiều cao màn hình là 8.0, ta ép khối này chỉ cao 7.0
        # Nó sẽ tự động thu nhỏ (scale) tỷ lệ tất cả mọi thứ để vừa vặn, không bao giờ bị cắt viền
        master_group.set_height(7.0)
        master_group.center()

        # ══════════════════════════════════════════════════════════════════════
        # BƯỚC 3: ANIMATION (Trình tự từ dưới lên trên)
        # ══════════════════════════════════════════════════════════════════════
        
        self.play(FadeIn(quote, shift=UP * 0.25), run_time=0.55)
        
        self.play(FadeIn(tok_bar, shift=UP * 0.30), run_time=0.40)
        
        # Chạy vòng lặp ngược (reversed) để Transformer xếp từ dưới lên trên
        for bar in reversed(transformer_bars):
            self.play(FadeIn(bar, shift=UP * 0.28), run_time=0.35)
 
        self.play(FadeIn(dots, shift=UP * 0.2), run_time=0.35)
        self.play(Indicate(dots, color=TEAL_STROKE, scale_factor=1.5), run_time=0.40)
 
        self.play(
            DrawBorderThenFill(decoder_bar.rect),
            FadeIn(decoder_bar.label_mob, scale=0.8),
            run_time=0.55,
        )
 
        self.play(Write(model_name), run_time=0.75)
 
        self.play(
            Indicate(stack_group, color=TEAL_STROKE, scale_factor=1.02),
            run_time=0.55,
        )
 
        self.next_slide() 
        self.wait(0.5)
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 7 — MODULE 4: LATENT DIFFUSION MODELS SLIDE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module4_LDM(Slide):
    def construct(self):
        # 1. Thiết lập màu nền slide thống nhất với Theme
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề Slide (Ghim sát góc trên bên trái tránh bị lệch chữ)
        title = slide_title("Latent Diffusion Models (LDM)")
        
        # 3. Tạo các Panel bao ngoài (Frames) và nhãn tiêu đề tương ứng
        
        # --- PANEL 1: PIXEL SPACE (Màu đỏ san hô - Coral Red) ---
        pixel_frame = RoundedRectangle(
            width=3.2, 
            height=5.2, 
            corner_radius=0.2, 
            stroke_color=Theme.ACCENT_RED, 
            stroke_width=2, 
            fill_color=Theme.BG, 
            fill_opacity=0.3
        )
        
        x_box = RoundedBox(
            lines=["Input Image", "(x)"], 
            width=2.5, 
            height=0.9, 
            fill_color=Theme.BOX_FILL, 
            stroke_color=Theme.ACCENT_RED
        )
        enc_box = RoundedBox(
            lines=["Encoder", "(E)"], 
            width=2.5, 
            height=0.9, 
            fill_color=Theme.BOX_FILL_ALT, 
            stroke_color=Theme.PRIMARY
        )
        dec_box = RoundedBox(
            lines=["Decoder", "(D)"], 
            width=2.5, 
            height=0.9, 
            fill_color=Theme.BOX_FILL_ALT, 
            stroke_color=Theme.PRIMARY
        )
        x_tilde_box = RoundedBox(
            lines=["Output Image", "(x_recon)"], 
            width=2.5, 
            height=0.9, 
            fill_color=Theme.BOX_FILL, 
            stroke_color=Theme.ACCENT_RED
        )
        
        pixel_contents = VGroup(x_box, enc_box, dec_box, x_tilde_box).arrange(DOWN, buff=0.22)
        pixel_contents.move_to(pixel_frame.get_center())
        
        pixel_label = Text("Pixel Space", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED, weight="BOLD")
        pixel_label.next_to(pixel_frame, UP, buff=0.15)
        pixel_group = VGroup(pixel_frame, pixel_contents, pixel_label)
        
        # --- PANEL 2: LATENT SPACE (Màu xanh lá - Success Green) ---
        latent_z = RoundedBox(
            lines=["Latent Code", "(z)"], 
            width=1.6, 
            height=0.9, 
            fill_color=Theme.BOX_FILL, 
            stroke_color=Theme.SUCCESS
        )
        latent_zT = RoundedBox(
            lines=["Noisy Latent", "(z_T)"], 
            width=1.6, 
            height=0.9, 
            fill_color=Theme.BOX_FILL, 
            stroke_color=Theme.SUCCESS
        )
        
        diff_box = RoundedBox(
            lines=["Diffusion Process", "Forward (Noise)"], 
            width=2.8, 
            height=0.9, 
            fill_color=Theme.BOX_FILL, 
            stroke_color=Theme.DIM
        )
        unet_box = RoundedBox(
            lines=["Denoising U-Net", "Backward (Predictor)"], 
            width=2.8, 
            height=1.2, 
            fill_color=Theme.BOX_FILL_ALT, 
            stroke_color=Theme.PRIMARY
        )
        
        # Sắp xếp các thành phần bên trong Latent Space
        mid_col = VGroup(diff_box, unet_box).arrange(DOWN, buff=0.5)
        latent_contents = VGroup(latent_z, mid_col, latent_zT).arrange(RIGHT, buff=0.35)
        
        latent_frame = RoundedRectangle(
            width=latent_contents.get_width() + 0.5,
            height=pixel_frame.get_height(),  # Đồng bộ chiều cao với Pixel Space để tạo sự cân bằng trực quan
            corner_radius=0.2,
            stroke_color=Theme.SUCCESS,
            stroke_width=2,
            fill_color=Theme.BG,
            fill_opacity=0.3
        )
        latent_contents.move_to(latent_frame.get_center())
        
        latent_label = Text("Latent Space", font=Theme.FONT_BODY, font_size=20, color=Theme.SUCCESS, weight="BOLD")
        latent_label.next_to(latent_frame, UP, buff=0.15)
        latent_group = VGroup(latent_frame, latent_contents, latent_label)
        
        # --- PANEL 3: CONDITIONING (Màu vàng hổ phách - Accent Gold) ---
        cond_prompt = RoundedBox(
            lines=["Prompt (y)", "(Text / Image)"], 
            width=2.4, 
            height=0.9, 
            fill_color=Theme.BOX_FILL, 
            stroke_color=Theme.ACCENT_GOLD
        )
        cond_enc = RoundedBox(
            lines=["Conditioning", "Encoder (tau)"], 
            width=2.4, 
            height=0.9, 
            fill_color=Theme.BOX_FILL_ALT, 
            stroke_color=Theme.PRIMARY
        )
        
        cond_contents = VGroup(cond_prompt, cond_enc).arrange(DOWN, buff=0.5)
        
        cond_frame = RoundedRectangle(
            width=cond_contents.get_width() + 0.5,
            height=pixel_frame.get_height(),  # Đồng bộ chiều cao
            corner_radius=0.2,
            stroke_color=Theme.ACCENT_GOLD,
            stroke_width=2,
            fill_color=Theme.BG,
            fill_opacity=0.3
        )
        cond_contents.move_to(cond_frame.get_center())
        
        cond_label = Text("Conditioning", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_GOLD, weight="BOLD")
        cond_label.next_to(cond_frame, UP, buff=0.15)
        cond_group = VGroup(cond_frame, cond_contents, cond_label)
        
        # 4. Gom cụm, căn chỉnh tỷ lệ và định vị an toàn trên khung hình
        all_panels = VGroup(pixel_group, latent_group, cond_group).arrange(RIGHT, buff=0.4)
        all_panels.set_width(13.2) # Giới hạn chiều rộng an toàn tránh tràn viền ngang (Slide Rộng 14.22)
        all_panels.center()
        all_panels.shift(UP * 0.2) # Dịch nhẹ lên trên để chừa không gian trống cho dòng giải thích ở dưới cùng
        
        # 5. Khởi tạo các mũi tên kết nối (Sau khi định vị xong để tránh lệch tọa độ)
        
        # Mũi tên nội bộ Pixel Space
        arrow_x_enc = Arrow(x_box.get_bottom(), enc_box.get_top(), buff=0.08, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        arrow_dec_x_tilde = Arrow(dec_box.get_bottom(), x_tilde_box.get_top(), buff=0.08, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        
        # Mũi tên nội bộ Latent Space (Chu trình Forward & Backward)
        arrow_z_diff = Arrow(latent_z.get_top(), diff_box.get_left(), buff=0.06, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        arrow_diff_zT = Arrow(diff_box.get_right(), latent_zT.get_top(), buff=0.06, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        arrow_zT_unet = Arrow(latent_zT.get_bottom(), unet_box.get_right(), buff=0.06, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        arrow_unet_z = Arrow(unet_box.get_left(), latent_z.get_bottom(), buff=0.06, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        
        # Mũi tên kết nối liên không gian (Cross-space)
        arrow_enc_z = Arrow(enc_box.get_right(), latent_z.get_left(), buff=0.08, color=Theme.PRIMARY, stroke_width=2.5, tip_length=0.12)
        arrow_z_dec = Arrow(latent_z.get_left(), dec_box.get_right(), buff=0.08, color=Theme.PRIMARY, stroke_width=2.5, tip_length=0.12)
        
        # Mũi tên Conditioning
        arrow_prompt_enc = Arrow(cond_prompt.get_bottom(), cond_enc.get_top(), buff=0.08, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        arrow_cond_unet = Arrow(cond_enc.get_left(), unet_box.get_right(), buff=0.08, color=Theme.ACCENT_GOLD, stroke_width=2.5, tip_length=0.12)
        
        # 6. Dòng văn bản chú thích dưới cùng (Sử dụng neo tuyệt đối to_edge để không bị tràn biên dọc)
        summary_text = Text(
            "LDM performs diffusion in a low-dimensional Latent Space, significantly reducing compute.",
            font=Theme.FONT_BODY,
            font_size=20,
            color=Theme.NEUTRAL,
        ).to_edge(DOWN, buff=0.4)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        # Bước 1: Hiển thị tiêu đề slide và 3 khung không gian trống
        self.play(Write(title))
        self.play(
            FadeIn(pixel_frame), FadeIn(pixel_label),
            FadeIn(latent_frame), FadeIn(latent_label),
            FadeIn(cond_frame), FadeIn(cond_label)
        )
        self.next_slide()
        
        # Bước 2: Biểu diễn Pixel Space (Nén ảnh gốc & Giải nén ảnh tái tạo)
        self.play(
            FadeIn(x_box), FadeIn(enc_box), Create(arrow_x_enc),
            FadeIn(dec_box), FadeIn(x_tilde_box), Create(arrow_dec_x_tilde)
        )
        self.next_slide()
        
        # Bước 3: Ánh xạ từ Pixel Space sang Latent Space (Z) thông qua Encoder
        self.play(
            FadeIn(latent_z),
            Create(arrow_enc_z)
        )
        self.next_slide()
        
        # Bước 4: Chu trình khuếch tán thuận (Forward Diffusion) trong không gian ẩn
        self.play(
            FadeIn(diff_box), FadeIn(latent_zT),
            Create(arrow_z_diff), Create(arrow_diff_zT)
        )
        self.next_slide()
        
        # Bước 5: Quá trình khử nhiễu ngược (Denoising U-Net) phục hồi không gian ẩn ban đầu
        self.play(
            FadeIn(unet_box),
            Create(arrow_zT_unet), Create(arrow_unet_z)
        )
        self.next_slide()
        
        # Bước 6: Đưa các thông tin điều kiện (Text/Image Conditioning) bổ trợ cho U-Net
        self.play(
            FadeIn(cond_prompt), FadeIn(cond_enc), Create(arrow_prompt_enc)
        )
        self.play(
            Create(arrow_cond_unet)
        )
        self.next_slide()
        
        # Bước 7: Kết nối từ Z đã khử nhiễu quay lại Decoder để tái tạo ảnh và hiện chú thích cuối slide
        self.play(
            Create(arrow_z_dec)
        )
        self.play(
            FadeIn(summary_text)
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 8 — MODULE 5: DiT CONDITIONING MECHANISMS (FIXED) ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module5_Conditioning(Slide):
    def construct(self):
        # 1. Thiết lập nền và tiêu đề
        self.camera.background_color = Theme.BG
        title = slide_title("DiT Conditioning Mechanisms")
        
        # ─────────────────────────────────────────────────────────────────────
        # KHỞI TẠO 3 PHIÊN BẢN CONDITIONING (Tinh chỉnh kích thước chuẩn)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- PANEL A: (a) In-Context Conditioning ---
        tok_a = RoundedBox(["Image Tokens"], width=1.5, height=0.7, font_size=20)
        cond_a = RoundedBox(["Conditioning"], width=1.5, height=0.7, stroke_color=Theme.ACCENT_GOLD, font_size=20)
        bot_a = VGroup(tok_a, cond_a).arrange(RIGHT, buff=0.2)
        
        # Giảm width xuống 3.2 để tiết kiệm không gian ngang
        concat_a = RoundedBox(["Concatenate", "on Sequence"], width=3.2, height=0.8, font_size=18)
        sa_a = RoundedBox(["Self-Attention"], width=3.2, height=0.8, stroke_color=Theme.PRIMARY)
        ffn_a = RoundedBox(["Pointwise FFN"], width=3.2, height=0.8, stroke_color=Theme.PRIMARY)
        
        col_a = VGroup(bot_a, concat_a, sa_a, ffn_a).arrange(UP, buff=0.4)
        
        # --- PANEL B: (b) Cross-Attention ---
        tok_b = RoundedBox(["Image Tokens"], width=2.2, height=0.7, font_size=20)
        sa_b = RoundedBox(["Self-Attention"], width=2.2, height=0.8, stroke_color=Theme.PRIMARY)
        ca_b = RoundedBox(["Cross-Attention"], width=2.2, height=0.8, fill_color=ManimColor("#8E24AA"), stroke_color=Theme.NEUTRAL)
        ffn_b = RoundedBox(["Pointwise FFN"], width=2.2, height=0.8, stroke_color=Theme.PRIMARY)
        
        col_b_main = VGroup(tok_b, sa_b, ca_b, ffn_b).arrange(UP, buff=0.4)
        
        cond_b = RoundedBox(["Conditioning"], width=1.4, height=0.7, stroke_color=Theme.ACCENT_GOLD, font_size=20)
        # Neo Cond vào bên phải Cross-Attention
        cond_b.next_to(ca_b, RIGHT, buff=0.2)
        
        panel_b = VGroup(col_b_main, cond_b)
        
        # --- PANEL C: (d) Adaptive Layer Norm (adaLN-Zero) ---
        tok_c = RoundedBox(["Image Tokens"], width=2.2, height=0.7, font_size=20)
        adaln_sa = RoundedBox(["Scale, Shift"], width=2.2, height=0.45, fill_color=Theme.DIM, font_size=18)
        sa_c = RoundedBox(["Self-Attention"], width=2.2, height=0.8, stroke_color=Theme.PRIMARY)
        adaln_ffn = RoundedBox(["Scale, Shift"], width=2.2, height=0.45, fill_color=Theme.DIM, font_size=18)
        ffn_c = RoundedBox(["Pointwise FFN"], width=2.2, height=0.8, stroke_color=Theme.PRIMARY)
        
        col_c_main = VGroup(tok_c, adaln_sa, sa_c, adaln_ffn, ffn_c).arrange(UP, buff=0.25)
        
        cond_c = RoundedBox(["Conditioning"], width=1.4, height=0.7, stroke_color=Theme.ACCENT_GOLD, font_size=20)
        mlp_c = RoundedBox(["MLP"], width=1.4, height=0.7, stroke_color=Theme.ACCENT_RED, font_size=20)
        
        # Neo vào bên phải cột chính
        cond_c.next_to(tok_c, RIGHT, buff=0.3) 
        mlp_c.next_to(cond_c, UP, buff=0.6) 
        
        panel_c = VGroup(col_c_main, cond_c, mlp_c)
        
        # ─────────────────────────────────────────────────────────────────────
        # GOM NHÓM TỔNG THỂ & KHẮC PHỤC LỖI 2 TRÀN BIÊN NGANG
        # ─────────────────────────────────────────────────────────────────────
        
        # Vẫn dùng aligned_edge=DOWN để chống LỖI 4 (đảm bảo đáy bằng nhau)
        all_panels = VGroup(col_a, panel_b, panel_c).arrange(RIGHT, buff=0.6, aligned_edge=DOWN)
        
        # FIX LỖI 2: Dùng .set_width(13.2) để KHÓA chặt vào biên an toàn. 
        # Chiều cao sẽ tự động bóp lại theo tỷ lệ mà không lo tràn màn hình.
        all_panels.set_width(13.2)
        all_panels.center()
        all_panels.shift(UP * 0.1)
        
        # ─────────────────────────────────────────────────────────────────────
        # VẼ MŨI TÊN (CHỈ VẼ SAU KHI ĐÃ CỐ ĐỊNH TỌA ĐỘ)
        # ─────────────────────────────────────────────────────────────────────
        
        arrows = VGroup()
        def make_arrow(start, end, color=Theme.NEUTRAL):
            return Arrow(start, end, buff=0.08, color=color, stroke_width=2.5, tip_length=0.12)
            
        # Panel A Arrows
        arrows.add(make_arrow(tok_a.get_top(), concat_a.get_bottom()))
        arrows.add(make_arrow(cond_a.get_top(), concat_a.get_bottom()))
        arrows.add(make_arrow(concat_a.get_top(), sa_a.get_bottom()))
        arrows.add(make_arrow(sa_a.get_top(), ffn_a.get_bottom()))
        arrows.add(make_arrow(ffn_a.get_top(), ffn_a.get_top() + UP * 0.4))
        
        # Panel B Arrows
        arrows.add(make_arrow(tok_b.get_top(), sa_b.get_bottom()))
        arrows.add(make_arrow(sa_b.get_top(), ca_b.get_bottom()))
        arrows.add(make_arrow(cond_b.get_left(), ca_b.get_right(), Theme.ACCENT_GOLD))
        arrows.add(make_arrow(ca_b.get_top(), ffn_b.get_bottom()))
        arrows.add(make_arrow(ffn_b.get_top(), ffn_b.get_top() + UP * 0.4))
        
        # Panel C Arrows
        arrows.add(make_arrow(tok_c.get_top(), adaln_sa.get_bottom()))
        arrows.add(make_arrow(adaln_sa.get_top(), sa_c.get_bottom()))
        arrows.add(make_arrow(sa_c.get_top(), adaln_ffn.get_bottom()))
        arrows.add(make_arrow(adaln_ffn.get_top(), ffn_c.get_bottom()))
        arrows.add(make_arrow(ffn_c.get_top(), ffn_c.get_top() + UP * 0.4))
        arrows.add(make_arrow(cond_c.get_top(), mlp_c.get_bottom(), Theme.ACCENT_GOLD))
        
        # Dashed Lines của Panel C
        path_to_sa = DashedLine(mlp_c.get_left(), adaln_sa.get_right(), buff=0.1, color=Theme.ACCENT_RED, stroke_width=2.5).add_tip(tip_length=0.12)
        path_to_ffn = DashedLine(mlp_c.get_left(), adaln_ffn.get_right(), buff=0.1, color=Theme.ACCENT_RED, stroke_width=2.5).add_tip(tip_length=0.12)
        arrows.add(path_to_sa, path_to_ffn)
        
        # ─────────────────────────────────────────────────────────────────────
        # THÊM NHÃN CHÚ THÍCH (Gắn tương đối vào các khối đã cố định)
        # ─────────────────────────────────────────────────────────────────────
        
        lbl_a = Text("(a) In-Context", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL).next_to(col_a, DOWN, buff=0.3)
        lbl_b = Text("(b) Cross-Attention", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL).next_to(col_b_main, DOWN, buff=0.3)
        lbl_c = Text("(d) Adaptive Layer Norm", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL).next_to(col_c_main, DOWN, buff=0.3)
        
        summary = Text(
            "DiT explores multiple conditioning methods. adaLN-Zero proves most efficient and scalable.",
            font=Theme.FONT_BODY, font_size=20, color=Theme.DIM
        ).to_edge(DOWN, buff=0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATIONS)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.next_slide()
        
        # Hiển thị (a)
        self.play(FadeIn(col_a), FadeIn(lbl_a))
        self.play(FadeIn(VGroup(arrows[0:5])))
        self.next_slide()
        
        # Hiển thị (b)
        self.play(FadeIn(panel_b), FadeIn(lbl_b))
        self.play(FadeIn(VGroup(arrows[5:10])))
        self.next_slide()
        
        # Hiển thị (d)
        self.play(FadeIn(panel_c), FadeIn(lbl_c))
        self.play(FadeIn(VGroup(arrows[10:])))
        self.next_slide()
        
        self.play(FadeIn(summary))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 9 — MODULE 6: DiT DESIGN SPACE - PATCH SIZE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module6_DiT_PatchSize(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề chính & Tiêu đề phụ (Ghim sát góc trên bên trái an toàn)
        title = slide_title("DiT Design Space — Patch Size")
        subtitle = Text(
            "Design space: p = 2, 4, 8", 
            font=Theme.FONT_BODY, 
            font_size=20, 
            color=Theme.ACCENT_GOLD, 
            weight="BOLD"
        )
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        
        # ─────────────────────────────────────────────────────────────────────
        # PHẦN LƯU ĐỒ ĐỒ HỌA (FLOW DIAGRAM)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- KHỐI BÊN TRÁI: Noised Latent 2D Grid ---
        # Tạo lưới đại diện cho các patch (màu vàng Accent Gold)
        grid = VGroup(*[
            VGroup(*[
                Square(
                    side_length=0.4, 
                    fill_color=Theme.ACCENT_GOLD, 
                    fill_opacity=0.8, 
                    stroke_color=Theme.NEUTRAL, 
                    stroke_width=1
                ) for _ in range(4)
            ]).arrange(RIGHT, buff=0.04)
            for _ in range(4)
        ]).arrange(DOWN, buff=0.04)
        
        # Thêm các mũi tên kích thước tổng thể I x I
        arrow_I_y = DoubleArrow(
            grid.get_corner(DL) + LEFT * 0.25, 
            grid.get_corner(UL) + LEFT * 0.25, 
            buff=0, stroke_width=2, color=Theme.NEUTRAL, tip_length=0.1
        )
        label_I_y = MathTex("I", font_size=24, color=Theme.NEUTRAL).next_to(arrow_I_y, LEFT, buff=0.1)
        
        arrow_I_x = DoubleArrow(
            grid.get_corner(DL) + DOWN * 0.25, 
            grid.get_corner(DR) + DOWN * 0.25, 
            buff=0, stroke_width=2, color=Theme.NEUTRAL, tip_length=0.1
        )
        label_I_x = MathTex("I", font_size=24, color=Theme.NEUTRAL).next_to(arrow_I_x, DOWN, buff=0.1)
        
        # Thêm kích thước của một patch đơn lẻ p x p
        target_patch = grid[0][-1]
        arrow_p_x = DoubleArrow(
            target_patch.get_corner(UL) + UP * 0.15, 
            target_patch.get_corner(UR) + UP * 0.15, 
            buff=0, stroke_width=1.5, color=Theme.NEUTRAL, tip_length=0.06
        )
        label_p_x = MathTex("p", font_size=18, color=Theme.NEUTRAL).next_to(arrow_p_x, UP, buff=0.05)
        
        arrow_p_y = DoubleArrow(
            target_patch.get_corner(UR) + RIGHT * 0.15, 
            target_patch.get_corner(DR) + RIGHT * 0.15, 
            buff=0, stroke_width=1.5, color=Theme.NEUTRAL, tip_length=0.06
        )
        label_p_y = MathTex("p", font_size=18, color=Theme.NEUTRAL).next_to(arrow_p_y, RIGHT, buff=0.05)
        
        latent_grid_group = VGroup(
            grid, arrow_I_y, label_I_y, arrow_I_x, label_I_x, 
            arrow_p_x, label_p_x, arrow_p_y, label_p_y
        )
        
        # Khung bao ngoài của Noised Latent
        latent_label = Text("Noised Latent", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL, weight="BOLD")
        latent_sub = Text("I x I x C", font=Theme.FONT_BODY, font_size=14, color=Theme.DIM)
        latent_title_group = VGroup(latent_label, latent_sub).arrange(DOWN, buff=0.05)
        
        latent_bg = RoundedRectangle(
            width=latent_grid_group.get_width() + 0.8,
            height=latent_grid_group.get_height() + 1.2,
            corner_radius=0.2,
            stroke_color=Theme.DIM,
            stroke_width=2,
            fill_color=Theme.BG,
            fill_opacity=0.3
        )
        
        latent_grid_group.move_to(latent_bg.get_center())
        latent_grid_group.shift(DOWN * 0.2)
        latent_title_group.next_to(latent_bg.get_top(), DOWN, buff=0.15)
        latent_panel = VGroup(latent_bg, latent_grid_group, latent_title_group)
        
        # --- KHỐI BÊN PHẢI: Input Tokens (Chuỗi phẳng 1D) ---
        token_squares = VGroup(*[
            Square(
                side_length=0.4, 
                fill_color=Theme.ACCENT_GOLD, 
                fill_opacity=0.8, 
                stroke_color=Theme.NEUTRAL, 
                stroke_width=1
            ) for _ in range(12)
        ]).arrange(RIGHT, buff=0.04)
        
        arrow_L = DoubleArrow(
            token_squares.get_corner(DL) + DOWN * 0.2, 
            token_squares.get_corner(DR) + DOWN * 0.2, 
            buff=0, stroke_width=2, color=Theme.NEUTRAL, tip_length=0.1
        )
        label_L = MathTex("L = (I/p)^2", font_size=22, color=Theme.NEUTRAL).next_to(arrow_L, DOWN, buff=0.15)
        token_group = VGroup(token_squares, arrow_L, label_L)
        
        tokens_label = Text("Input Tokens", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL, weight="BOLD")
        tokens_sub = Text("L x C", font=Theme.FONT_BODY, font_size=14, color=Theme.DIM)
        tokens_title_group = VGroup(tokens_label, tokens_sub).arrange(DOWN, buff=0.05)
        
        tokens_bg = RoundedRectangle(
            width=token_squares.get_width() + 0.8,
            height=latent_bg.get_height(), # Cố định chiều cao cân bằng tuyệt đối với cột trái
            corner_radius=0.2,
            stroke_color=Theme.DIM,
            stroke_width=2,
            fill_color=Theme.BG,
            fill_opacity=0.3
        )
        
        token_group.move_to(tokens_bg.get_center())
        token_group.shift(DOWN * 0.2)
        tokens_title_group.next_to(tokens_bg.get_top(), DOWN, buff=0.15)
        tokens_panel = VGroup(tokens_bg, token_group, tokens_title_group)
        
        # --- KHỐI TRÊN CÙNG: DiT Block ---
        dit_block = RoundedBox(
            lines=["DiT Block"],
            width=2.5,
            height=0.9,
            fill_color=Theme.BOX_FILL_ALT,
            stroke_color=Theme.PRIMARY,
            stroke_width=3.0,
            font_size=22,
            text_color=Theme.NEUTRAL
        )
        
        # ─────────────────────────────────────────────────────────────────────
        # SẮP XẾP VÀ CĂN CHỈNH TOÀN CỤC CHỐNG OVERLAY
        # ─────────────────────────────────────────────────────────────────────
        
        # Bước 1: Ghép song song hàng dưới (Noised Latent & Input Tokens nằm cùng trục ngang)
        lower_flow = VGroup(latent_panel, tokens_panel).arrange(RIGHT, buff=0.8)
        
        # Bước 2: Đặt DiT Block trực tiếp lên trên Tokens Panel theo khoảng cách tuyệt đối
        dit_block.next_to(tokens_panel, UP, buff=0.5)
        
        # Bước 3: Tạo nhóm tổng thể
        all_flow = VGroup(lower_flow, dit_block)
        
        # Bước 4: Khống chế chiều cao tối đa cực kỳ an toàn để không đè lên tiêu đề và chú thích dưới cùng
        all_flow.set_height(4.8) 
        all_flow.center()
        all_flow.shift(DOWN * 0.2) # Hạ thấp sơ đồ một chút tạo độ thoáng cho phần Header
        
        # Bước 5: Khởi tạo các mũi tên nối (Tọa độ chính xác tuyệt đối sau khi co giãn)
        arrow_flatten = Arrow(
            latent_panel.get_right(), 
            tokens_panel.get_left(), 
            buff=0.12, 
            color=Theme.PRIMARY, 
            stroke_width=3, 
            tip_length=0.12
        )
        arrow_to_dit = Arrow(
            tokens_panel.get_top(), 
            dit_block.get_bottom(), 
            buff=0.12, 
            color=Theme.PRIMARY, 
            stroke_width=3, 
            tip_length=0.12
        )
        
        # --- DÒNG CHÚ THÍCH DƯỚI CHÂN SLIDE ---
        summary_text = Text(
            "Smaller patch sizes (p) create longer token sequences (L), increasing computational complexity.",
            font=Theme.FONT_BODY,
            font_size=18,
            color=Theme.NEUTRAL,
        ).to_edge(DOWN, buff=0.35)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        # Bước 1: Hiển thị tiêu đề chính và phụ
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.next_slide()
        
        # Bước 2: Hiển thị khung "Noised Latent" và lưới 2D đại diện
        self.play(FadeIn(latent_bg), FadeIn(latent_title_group))
        self.play(
            FadeIn(grid),
            Create(arrow_I_x), Create(arrow_I_y),
            Write(label_I_x), Write(label_I_y)
        )
        self.play(
            Create(arrow_p_x), Create(arrow_p_y),
            Write(label_p_x), Write(label_p_y)
        )
        self.next_slide()
        
        # Bước 3: Xuất hiện mũi tên chuyển đổi và khung "Input Tokens" trống nằm ngang đối xứng
        self.play(
            FadeIn(tokens_bg), FadeIn(tokens_title_group),
            Create(arrow_flatten)
        )
        self.next_slide()
        
        # Bước 4: Làm phẳng lưới 2D thành chuỗi Token 1D nằm ngang cùng công thức tính L
        self.play(
            FadeIn(token_squares),
            Create(arrow_L),
            Write(label_L)
        )
        self.next_slide()
        
        # Bước 5: Truyền chuỗi Token đi thẳng lên trên vào DiT Block
        self.play(
            FadeIn(dit_block),
            Create(arrow_to_dit)
        )
        self.next_slide()
        
        # Bước 6: Hiện dòng đúc kết ở chân slide
        self.play(FadeIn(summary_text))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 10 — MODULE 7: CONDITIONED DiT BLOCK ARCHITECTURE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import DashedLine

class Module7_Architecture(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề slide (Ghim góc trái trên, tránh Lỗi 1)
        title = slide_title("Conditioned DiT Block")
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG TRỤC TRUNG TÂM (CORE SPINE)
        # ─────────────────────────────────────────────────────────────────────
        
        zt_box = RoundedBox(
            lines=["Noised Latent", "(z_t)"], 
            width=2.5, height=0.8, fill_color=Theme.SUCCESS
        )
        
        self_attn = RoundedBox(
            lines=["Self-Attention", "+ AdaLN (Scale/Shift)"], 
            width=3.2, height=1.0, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY
        )
        
        cross_attn = RoundedBox(
            lines=["Multi-Head", "Cross-Attention"], 
            width=3.2, height=1.0, fill_color=ManimColor("#8E24AA"), stroke_color=Theme.NEUTRAL # Màu tím phân biệt Text Cond
        )
        
        ffn = RoundedBox(
            lines=["Pointwise FFN", "+ AdaLN (Scale/Shift)"], 
            width=3.2, height=1.0, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY
        )
        
        # Xếp chồng trục trung tâm
        core_spine = VGroup(zt_box, self_attn, cross_attn, ffn).arrange(UP, buff=0.7)
        
        # Tạo khung bao ngoài cho "i-th Block" (chỉ bao quanh Attention và FFN)
        block_group = VGroup(self_attn, cross_attn, ffn)
        block_frame = RoundedRectangle(
            width=block_group.width + 0.8,
            height=block_group.height + 0.6,
            corner_radius=0.2,
            stroke_color=Theme.DIM,
            stroke_width=2,
            fill_color=Theme.BG,
            fill_opacity=0.4
        ).move_to(block_group.get_center())
        
        block_label = Text("i-th Block (Tunable)", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_RED, weight="BOLD")
        block_label.next_to(block_frame, UP, buff=0.15)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: NEO CÁC KHỐI PHỤ THEO TRỤC TRUNG TÂM (TRÁNH LỖI 4)
        # ─────────────────────────────────────────────────────────────────────
        
        # Cột trái: Đầu vào Image & Text
        vae_enc = RoundedBox(
            lines=["VAE Encoder", "[Frozen]"], 
            width=2.2, height=0.9, fill_color=Theme.DIM, stroke_color=Theme.PRIMARY
        )
        vae_enc.next_to(zt_box, LEFT, buff=1.8) # Neo ngang hàng với z_t
        
        t5_enc = RoundedBox(
            lines=["T5 Text Encoder", "[Frozen]"], 
            width=2.5, height=0.9, fill_color=Theme.DIM, stroke_color=Theme.PRIMARY
        )
        t5_enc.next_to(cross_attn, LEFT, buff=1.5) # Neo ngang hàng với Cross-Attention
        
        # Cột phải: Conditioning (Thời gian)
        time_mlp = RoundedBox(
            lines=["Time MLP (t)", "Shared by N blocks", "[Tunable]"], 
            width=2.6, height=1.2, fill_color=Theme.BOX_FILL, stroke_color=Theme.ACCENT_RED
        )
        
        # FIX LỖI OVERLAP: Chỉ dùng 1 lệnh next_to neo vào bên phải khung block_frame
        time_mlp.next_to(block_frame, RIGHT, buff=0.8)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM NHÓM & SCALE TỔNG THỂ 
        # ─────────────────────────────────────────────────────────────────────
        
        all_elements = VGroup(
            block_frame, block_label, core_spine, 
            vae_enc, t5_enc, time_mlp
        )
        
        all_elements.set_height(5.5)
        all_elements.center()
        
        # FIX LỖI ĐÈ TIÊU ĐỀ: Đẩy sơ đồ xuống dưới một chút để chừa không gian cho title
        all_elements.shift(DOWN * 0.2)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: VẼ MŨI TÊN KẾT NỐI (TRÁNH LỖI 2)
        # ─────────────────────────────────────────────────────────────────────
        # Mũi tên trục chính
        arr_vae_zt = Arrow(vae_enc.get_right(), zt_box.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15)
        noise_text = Text("+ noise_t", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM).next_to(arr_vae_zt, UP, buff=0.05)
        
        arr_zt_sa = Arrow(zt_box.get_top(), self_attn.get_bottom(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15)
        arr_sa_ca = Arrow(self_attn.get_top(), cross_attn.get_bottom(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15)
        arr_ca_ffn = Arrow(cross_attn.get_top(), ffn.get_bottom(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15)
        
        arr_out = Arrow(ffn.get_top(), ffn.get_top() + UP * 0.5, buff=0, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15)
        
        # Mũi tên Text Conditioning
        arr_t5_ca = Arrow(t5_enc.get_right(), cross_attn.get_left(), buff=0.1, color=ManimColor("#8E24AA"), stroke_width=3, tip_length=0.15)
        
        # Mũi tên Time Conditioning (Đường đứt nét để phân biệt luồng parameter)
        path_time_ffn = DashedLine(time_mlp.get_top(), ffn.get_right(), buff=0.15, color=Theme.ACCENT_RED, stroke_width=2.5)
        path_time_ffn.add_tip(tip_length=0.15)
        
        path_time_sa = DashedLine(time_mlp.get_bottom(), self_attn.get_right(), buff=0.15, color=Theme.ACCENT_RED, stroke_width=2.5)
        path_time_sa.add_tip(tip_length=0.15)
        
        arrows_group = VGroup(
            arr_vae_zt, noise_text, arr_zt_sa, arr_sa_ca, arr_ca_ffn, arr_out, 
            arr_t5_ca, path_time_ffn, path_time_sa
        )
        
        # Caption dưới cùng
        summary_text = Text(
            "Text modifies latent via Cross-Attention. Time (t) modifies parameters via AdaLN (Scale/Shift).",
            font=Theme.FONT_BODY,
            font_size=20,
            color=Theme.NEUTRAL,
        ).to_edge(DOWN, buff=0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.next_slide()
        
        # Hiển thị đầu vào: Image -> VAE -> Latent
        self.play(FadeIn(vae_enc))
        self.play(Create(arr_vae_zt), FadeIn(noise_text), FadeIn(zt_box))
        self.next_slide()
        
        # Hiển thị khung của i-th block
        self.play(FadeIn(block_frame), FadeIn(block_label))
        self.next_slide()
        
        # Hiển thị luồng dữ liệu chính và các layer bên trong block
        self.play(Create(arr_zt_sa), FadeIn(self_attn))
        self.play(Create(arr_sa_ca), FadeIn(cross_attn))
        self.play(Create(arr_ca_ffn), FadeIn(ffn))
        self.play(Create(arr_out))
        self.next_slide()
        
        # Điều kiện 1: Đưa Text qua T5 vào Cross-Attention
        self.play(FadeIn(t5_enc))
        self.play(Create(arr_t5_ca))
        self.next_slide()
        
        # Điều kiện 2: Đưa Time qua MLP vào AdaLN
        self.play(FadeIn(time_mlp))
        self.play(Create(path_time_sa), Create(path_time_ffn))
        self.next_slide()
        
        # Hiện kết luận
        self.play(FadeIn(summary_text))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 11 — MODULE 8: INTERPOLANT FRAMEWORK  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module8_Interpolant(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề slide (Ghim sát góc trên bên trái)
        title = slide_title("Interpolant Framework")
        
        # ─────────────────────────────────────────────────────────────────────
        # KHỞI TẠO CÁC KHỐI NỘI DUNG (CHƯA ĐỊNH VỊ)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- Khối 1: Giới thiệu (Tóm tắt lại chữ để dễ đọc hơn) ---
        intro_line = Text(
            "Flow and diffusion models gradually turn:", 
            font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL
        )
        
        noise_math = MathTex(r"\text{Noise } \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})", color=Theme.DIM, font_size=36)
        arrow_transform = Arrow(LEFT, RIGHT, color=Theme.NEUTRAL, buff=0.2, stroke_width=3)
        data_math = MathTex(r"\text{Data } \mathbf{x}_* \sim p(\mathbf{x})", color=Theme.SUCCESS, font_size=36)
        
        transform_group = VGroup(noise_math, arrow_transform, data_math).arrange(RIGHT, buff=0.4)
        intro_group = VGroup(intro_line, transform_group).arrange(DOWN, buff=0.3)
        
        # --- Khối 2: Phương trình chính ---
        eq_label = Text(
            "The time-dependent process can be summarized as:", 
            font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL
        )
        
        eq_math = MathTex(
            r"\mathbf{x}_t = ", 
            r"\alpha_t", 
            r"\mathbf{x}_*", 
            r"+", 
            r"\sigma_t", 
            r"\epsilon",
            font_size=64
        )
        # Phân rã màu sắc tương ứng với ý nghĩa của từng biến
        eq_math[0].set_color(Theme.ACCENT_GOLD) # x_t
        eq_math[1].set_color(Theme.SUCCESS)     # alpha_t (Gắn với Data)
        eq_math[2].set_color(Theme.SUCCESS)     # x_*
        eq_math[4].set_color(Theme.DIM)         # sigma_t (Gắn với Noise)
        eq_math[5].set_color(Theme.DIM)         # epsilon
        
        eq_box = RoundedRectangle(
            width=eq_math.width + 1.5,
            height=eq_math.height + 0.8,
            corner_radius=0.2,
            stroke_color=Theme.ACCENT_GOLD,
            stroke_width=2,
            fill_color=Theme.BOX_FILL_ALT,
            fill_opacity=1
        )
        eq_math.move_to(eq_box.get_center()) # Căn giữa phương trình vào trong hộp
        eq_group = VGroup(eq_box, eq_math)
        
        full_eq_group = VGroup(eq_label, eq_group).arrange(DOWN, buff=0.4)
        
        # --- Khối 3: Giải thích tham số ---
        exp_alpha = VGroup(
            MathTex(r"\alpha_t", font_size=36, color=Theme.SUCCESS),
            Text(": decreasing function of t", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        ).arrange(RIGHT, buff=0.2)
        
        exp_sigma = VGroup(
            MathTex(r"\sigma_t", font_size=36, color=Theme.DIM),
            Text(": increasing function of t", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        ).arrange(RIGHT, buff=0.2)
        
        # Xếp dọc 2 dòng giải thích và căn lề trái (aligned_edge)
        exp_group = VGroup(exp_alpha, exp_sigma).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        # --- Khối 4: Hình ảnh minh họa (Mô phỏng chuỗi ảnh mờ dần trong video) ---
        timeline_squares = VGroup()
        # Tạo mảng màu nội suy từ Xám (Nhiễu) sang Xanh lá (Dữ liệu)
        colors = color_gradient([Theme.DIM, Theme.SUCCESS], 5)
        for i in range(5):
            sq = RoundedRectangle(
                corner_radius=0.1, width=1.0, height=1.0, 
                fill_color=colors[i], fill_opacity=0.9, 
                stroke_width=1.5, stroke_color=Theme.NEUTRAL
            )
            timeline_squares.add(sq)
        timeline_squares.arrange(RIGHT, buff=0.2)
        
        # Mũi tên chỉ chiều thời gian ở dưới các ô
        timeline_arrow = Arrow(
            timeline_squares.get_left() + LEFT*0.2, 
            timeline_squares.get_right() + RIGHT*0.2, 
            color=Theme.NEUTRAL, stroke_width=2, tip_length=0.15
        )
        timeline_arrow.next_to(timeline_squares, DOWN, buff=0.15)
        
        t_start = MathTex("t = 1", font_size=22, color=Theme.NEUTRAL).next_to(timeline_arrow.get_start(), DOWN, buff=0.1)
        t_end = MathTex("t = 0", font_size=22, color=Theme.NEUTRAL).next_to(timeline_arrow.get_end(), DOWN, buff=0.1)
        t_label = Text("Time", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL).next_to(timeline_arrow, DOWN, buff=0.1)
        
        visual_group = VGroup(timeline_squares, timeline_arrow, t_start, t_end, t_label)
        
        # ─────────────────────────────────────────────────────────────────────
        # GOM NHÓM & CĂN CHỈNH TỔNG THỂ (TRÁNH LỖI 3, 4, 5)
        # ─────────────────────────────────────────────────────────────────────
        # Sử dụng một trục dọc (DOWN) duy nhất, tuyệt đối không dùng align_to hay shift trên từng khối lẻ.
        content_group = VGroup(
            intro_group,
            full_eq_group,
            exp_group,
            visual_group
        ).arrange(DOWN, buff=0.5) 
        
        # Giới hạn chiều cao an toàn để tránh chạm trần/đáy và đưa vào chính giữa màn hình
        content_group.set_height(6.0)
        content_group.center()
        content_group.shift(DOWN * 0.1) # Dịch nhẹ tổng thể xuống một lần duy nhất để nhường không gian cho Title
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.next_slide()
        
        # Ý 1: Biến đổi Noise -> Data
        self.play(FadeIn(intro_line))
        self.play(
            FadeIn(noise_math),
            GrowArrow(arrow_transform),
            FadeIn(data_math)
        )
        self.next_slide()
        
        # Ý 2: Xuất hiện Phương trình tổng quát
        self.play(FadeIn(eq_label))
        self.play(
            Create(eq_box),
            Write(eq_math)
        )
        self.next_slide()
        
        # Ý 3: Giải thích tham số Alpha và Sigma
        self.play(FadeIn(exp_alpha))
        self.play(FadeIn(exp_sigma))
        self.next_slide()
        
        # Ý 4: Minh họa trực quan quá trình nội suy (Hình thay cho cụm ảnh của video)
        self.play(
            AnimationGroup(
                *[FadeIn(sq) for sq in timeline_squares],
                lag_ratio=0.15
            )
        )
        self.play(
            GrowArrow(timeline_arrow),
            FadeIn(t_start), FadeIn(t_end), FadeIn(t_label)
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 12 — MODULE 9: CONCURRENT WORK (FLOW MATCHING)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Axes, ValueTracker, always_redraw, DoubleArrow, there_and_back
import numpy as np

class Module9_ConcurrentWork(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: TIÊU ĐỀ & TRÍCH DẪN (Ghim độc lập ở góc trên)
        # ─────────────────────────────────────────────────────────────────────
        
        # Tiêu đề bên trái (3 tên gọi khác nhau của cùng một khái niệm)
        title_lines = VGroup(
            Text("Stochastic Interpolants", font=Theme.FONT_TITLE, font_size=28, color=Theme.NEUTRAL, weight="BOLD"),
            Text("Rectified Flow", font=Theme.FONT_TITLE, font_size=28, color=Theme.NEUTRAL, weight="BOLD"),
            Text("Flow Matching", font=Theme.FONT_TITLE, font_size=28, color=Theme.NEUTRAL, weight="BOLD")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        title_lines.to_corner(UL, buff=0.5)
        
        # Nguồn trích dẫn bên phải
        ref_lines = VGroup(
            Text("Albergo & Vanden-Eijnden arXiv:2209.15571 (2022);", font=Theme.FONT_BODY, font_size=18, color=Theme.DIM),
            Text("Liu et al. arXiv:2209.03003 (2022);", font=Theme.FONT_BODY, font_size=18, color=Theme.DIM),
            Text("Lipman et al. arXiv:2210.02747 (2022)", font=Theme.FONT_BODY, font_size=18, color=Theme.DIM)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        ref_lines.to_corner(UR, buff=0.5)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: CỘT BÊN TRÁI (Phương trình + Biểu đồ Flow)
        # ─────────────────────────────────────────────────────────────────────
        
        # Phương trình cốt lõi
        eq_math = MathTex(
            r"\mathbf{x}_t = \alpha_t\mathbf{x}_* + \sigma_t\mathbf{z}",
            font_size=64, color=Theme.NEUTRAL
        )
        
        # Trục biểu đồ (Ẩn số để nhìn giống Heatmap Flow)
        flow_ax = Axes(
            x_range=[-3, 3], y_range=[0, 1.2],
            x_length=5, y_length=2.5,
            axis_config={"color": Theme.DIM, "include_ticks": False, "include_tip": False}
        )
        
        label_x0 = MathTex("X_0", color=Theme.PRIMARY).next_to(flow_ax, LEFT, buff=0.2)
        label_x1 = MathTex("X_1", color=Theme.ACCENT_GOLD).next_to(flow_ax, RIGHT, buff=0.2)
        
        flow_container = VGroup(label_x0, flow_ax, label_x1)
        
        left_col = VGroup(eq_math, flow_container).arrange(DOWN, buff=1.0)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: CỘT BÊN PHẢI (Mô phỏng Spiderman Meme bằng Manim Mobjects)
        # ─────────────────────────────────────────────────────────────────────
        
        # Khởi tạo 3 hộp độc lập
        node_si = RoundedBox(["Stochastic", "Interpolants"], width=2.4, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS)
        node_fm = RoundedBox(["Flow", "Matching"], width=2.0, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY)
        node_rf = RoundedBox(["Rectified", "Flow"], width=2.0, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_RED)
        
        # Xếp vị trí tương đối thành hình tam giác
        node_si.move_to(UP * 1.5)
        node_fm.move_to(DOWN * 0.8 + LEFT * 1.8)
        node_rf.move_to(DOWN * 0.8 + RIGHT * 1.8)
        
        # Tạo mũi tên trỏ vào nhau (Spiderman pointing meme)
        arr1 = DoubleArrow(node_si.get_corner(DL), node_fm.get_corner(UR), buff=0.2, color=Theme.DIM)
        arr2 = DoubleArrow(node_fm.get_right(), node_rf.get_left(), buff=0.2, color=Theme.DIM)
        arr3 = DoubleArrow(node_rf.get_corner(UL), node_si.get_corner(DR), buff=0.2, color=Theme.DIM)
        
        meme_group = VGroup(node_si, node_fm, node_rf, arr1, arr2, arr3)
        right_col = VGroup(meme_group)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: GOM NHÓM TỔNG VÀ CĂN CHỈNH AN TOÀN (TRÁNH LỖI 4 & 5)
        # ─────────────────────────────────────────────────────────────────────
        
        main_content = VGroup(left_col, right_col).arrange(RIGHT, buff=1.0)
        main_content.set_height(4.5)  # Khống chế chiều cao an toàn
        main_content.center()         # Căn giữa tổng thể
        main_content.shift(DOWN * 0.5) # Hạ nhẹ khối trung tâm xuống để chừa chỗ cho Title
        
        # Đảm bảo chiều rộng không bị Lỗi 2 (Tràn viền)
        if main_content.width > 13.5:
            main_content.set_width(13.5)
            main_content.center()
            main_content.shift(DOWN * 0.5)
            
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 5: XÂY DỰNG LOGIC HOẠT HỌA VÒNG LẶP (GIF-LIKE ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        
        # ValueTracker quản lý thời gian t từ 0 -> 1
        t_tracker = ValueTracker(0)
        
        def get_flow_curve():
            t = t_tracker.get_value()
            def pdf(x):
                # t=0: Một đỉnh duy nhất (Gaussian cơ bản)
                g0 = np.exp(-x**2 / 1.0)
                # t=1: Hai đỉnh (Phân phối bimodal đích)
                g1 = 0.8 * np.exp(-(x-1.5)**2 / 0.5) + 0.8 * np.exp(-(x+1.5)**2 / 0.5)
                # Nội suy mượt mà
                return (1-t)*g0 + t*g1
            
            # Đổi màu động dọc theo trục thời gian (Primary -> Accent Gold)
            c = color_gradient([Theme.PRIMARY, Theme.ACCENT_GOLD], 100)[int(t*99)]
            
            curve = flow_ax.plot(pdf, color=c, stroke_width=3)
            area = flow_ax.get_area(curve, color=c, opacity=0.3)
            return VGroup(curve, area)
        
        # Luôn redraw lại đường cong dựa trên sự thay đổi của t_tracker
        animated_flow = always_redraw(get_flow_curve)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(FadeIn(title_lines), FadeIn(ref_lines))
        self.next_slide()
        
        self.play(FadeIn(eq_math))
        self.play(FadeIn(label_x0), FadeIn(flow_ax), FadeIn(label_x1))
        self.add(animated_flow)
        self.play(FadeIn(meme_group))
        
        self.next_slide()
        
        # CHẠY ANIMATION DẠNG GIF LẶP LẠI (Vòng lặp tiến/lùi liên tục)
        # Biến đổi đồ thị từ Single (X_0) sang Bimodal (X_1) và ngược lại
        for _ in range(3): 
            self.play(
                t_tracker.animate.set_value(1),
                run_time=2.0,
                rate_func=there_and_back
            )
            
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 13 — MODULE 10: RELAXING SBDM DEFINITIONS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module10_SBDM_Interpolant(Slide):
    def construct(self):
        # 1. Thiết lập màu nền slide
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề slide (Ghim cứng góc trên bên trái - Tránh Lỗi 1)
        title = slide_title("Relax the rigid definitions of SBDM")
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: KHỐI NỘI DUNG TRÊN CÙNG (Noising Process & Generative Model)
        # ─────────────────────────────────────────────────────────────────────
        
        noising_label = Text("SBDM introduces a noising process:", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, slant="ITALIC")
        
        # Trục hình ảnh minh họa quá trình thêm nhiễu (Chuyển từ Primary sang Xám)
        colors = color_gradient([Theme.PRIMARY, Theme.BOX_FILL_ALT], 5)
        timeline_squares = VGroup(*[
            RoundedRectangle(
                corner_radius=0.1, width=1.2, height=1.2, 
                fill_color=c, fill_opacity=1, 
                stroke_color=Theme.DIM, stroke_width=1.5
            ) for c in colors
        ]).arrange(RIGHT, buff=0.1)
        
        # Phương trình Generative Model
        gen_label = Text("Generative model", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL)
        gen_math = MathTex(r"\hat{s}(t,x) \approx \nabla \log p(t,x)", font_size=32, color=Theme.NEUTRAL)
        gen_group = VGroup(gen_label, gen_math).arrange(DOWN, buff=0.15)
        
        top_row = VGroup(timeline_squares, gen_group).arrange(RIGHT, buff=1.5)
        top_block = VGroup(noising_label, top_row).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: KHỐI TRUNG TÂM (Phương trình Interpolant & Chú thích)
        # ─────────────────────────────────────────────────────────────────────
        
        recast_label = Text("When recasted as an interpolant:", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        
        # Cắt nhỏ phương trình để dễ dàng trỏ mũi tên vào đúng hệ số
        eq_math = MathTex(
            r"x(t) = ",                        # [0]
            r"x_0 e^{-t}",                     # [1] Coeff 1
            r" + ",                            # [2] Center of Coeffs
            r"\sqrt{1 - e^{-2t}} z",           # [3] Coeff 2
            r", \quad x_0 \sim p_0, \quad ",   # [4]
            r"z \sim \mathcal{N}(0, I_d)",     # [5] Gaussian mapping
            r", \quad ",                       # [6] Center of Params
            r"t \in [0, \infty)"               # [7] Infinite time
        )
        eq_math.set_color(Theme.NEUTRAL)
        eq_math[1].set_color(Theme.ACCENT_GOLD)
        eq_math[3].set_color(Theme.ACCENT_GOLD)
        eq_math[5].set_color(Theme.PRIMARY)
        eq_math[7].set_color(Theme.PRIMARY)
        
        # Tạo hai khối ghi chú (Notes)
        note_left = Text("Coefficients fixed by\nnoising process", font=Theme.FONT_BODY, font_size=20, color=Theme.DIM)
        note_left.next_to(eq_math[2], DOWN, buff=1.2) # Neo ngay dưới dấu "+"
        
        note_right = Text("Maps to a Gaussian\nin infinite time", font=Theme.FONT_BODY, font_size=20, color=Theme.DIM)
        note_right.next_to(eq_math[6], DOWN, buff=1.2) # Neo ngay dưới dấu phẩy ","
        
        # Đóng gói Khối Trung Tâm (chưa có mũi tên)
        mid_block = VGroup(recast_label, eq_math, note_left, note_right)
        
        # Căn chỉnh tiêu đề của khối trung tâm lề trái so với phương trình
        recast_label.next_to(eq_math, UP, buff=0.6, aligned_edge=LEFT)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: KHỐI KẾT LUẬN & GOM NHÓM TỔNG THỂ (Tránh Lỗi 2, 3, 4)
        # ─────────────────────────────────────────────────────────────────────
        
        bottom_box = RoundedBox(
            lines=["SBDM is just one possible interpolant"],
            width=8.0, height=1.0, 
            fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.DIM
        )
        
        # Dùng một trục dọc duy nhất để kết dính toàn bộ nội dung
        main_layout = VGroup(top_block, mid_block, bottom_box).arrange(DOWN, buff=0.8)
        
        # Giới hạn kích thước an toàn
        main_layout.set_height(5.8)
        main_layout.center()
        main_layout.shift(DOWN * 0.1) # Dịch tổng thể nhường khoảng trống cho title
        
        if main_layout.width > 13.5:
            main_layout.set_width(13.5)
            main_layout.center()
            main_layout.shift(DOWN * 0.1)
            
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: VẼ MŨI TÊN (Sử dụng hàm helper `curved_arrow` của cv.py)
        # ─────────────────────────────────────────────────────────────────────
        
        # Mũi tên từ note_left trỏ lên 2 hệ số
        arr_left1 = curved_arrow(note_left.get_top(), eq_math[1].get_bottom(), angle=0.4)
        arr_left2 = curved_arrow(note_left.get_top(), eq_math[3].get_bottom(), angle=-0.4)
        
        # Mũi tên từ note_right trỏ lên phân phối chuẩn và thời gian
        arr_right1 = curved_arrow(note_right.get_top(), eq_math[5].get_bottom(), angle=0.4)
        arr_right2 = curved_arrow(note_right.get_top(), eq_math[7].get_bottom(), angle=-0.4)
        
        arrows_group = VGroup(arr_left1, arr_left2, arr_right1, arr_right2)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.next_slide()
        
        # Hiển thị Khối 1: Noising process
        self.play(FadeIn(noising_label))
        self.play(
            AnimationGroup(*[FadeIn(sq) for sq in timeline_squares], lag_ratio=0.15)
        )
        self.play(FadeIn(gen_group))
        self.next_slide()
        
        # Hiển thị Khối 2: Phương trình Interpolant
        self.play(FadeIn(recast_label))
        self.play(Write(eq_math))
        self.next_slide()
        
        # Hiển thị Chú thích trái (Fixed Coefficients)
        self.play(FadeIn(note_left))
        self.play(Create(arr_left1), Create(arr_left2))
        self.next_slide()
        
        # Hiển thị Chú thích phải (Gaussian limit)
        self.play(FadeIn(note_right))
        self.play(Create(arr_right1), Create(arr_right2))
        self.next_slide()
        
        # Hiển thị Khối 3: Kết luận cuối cùng
        self.play(FadeIn(bottom_box))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 14 — MODULE 11: UNDER THE INTERPOLANT FRAMEWORK  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module11_InterpolantFramework(Slide):
    def construct(self):
        # 1. Thiết lập màu nền slide
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề slide (Ghim sát góc trên bên trái)
        title = slide_title("Under the Interpolant Framework")
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: KHỐI TÓM TẮT PHÍA TRÊN (Summarized Text Blocks)
        # ─────────────────────────────────────────────────────────────────────
        
        fm_summary = VGroup(
            Text("Flow Matching / Interpolants", font=Theme.FONT_BODY, font_size=24, color=Theme.PRIMARY, weight="BOLD"),
            Text("Restrict process on time  t ∈ [0, 1].", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL),
            Text("Interpolates exactly between data and noise.", font=Theme.FONT_BODY, font_size=20, color=Theme.DIM)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        diff_summary = VGroup(
            Text("Score-Based Diffusion", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_RED, weight="BOLD"),
            Text("Forward-time SDE with N(0, I) equilibrium.", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL),
            Text("Converges to noise only if  t → ∞.", font=Theme.FONT_BODY, font_size=20, color=Theme.DIM)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        # Đóng gói thành 2 cột ngang
        top_summaries = VGroup(fm_summary, diff_summary).arrange(RIGHT, buff=1.0)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: KHỞI TẠO BẢNG SO SÁNH (Custom Table Construction)
        # ─────────────────────────────────────────────────────────────────────
        
        # Hàm tiện ích để tạo một hàng với các tọa độ X cố định, tránh Lỗi 4 & 5
        def create_row(m_left, m_mid, m_right):
            # Tạo nhóm và neo tâm Y bằng 0 để các phần tử thẳng hàng ngang
            for m in [m_left, m_mid, m_right]:
                m.set_y(0)
            
            # Neo tọa độ X tuyệt đối (nhưng chỉ mang tính cục bộ bên trong hàng này)
            m_left.move_to(LEFT * 5.0)
            m_mid.move_to(LEFT * 1.0)
            m_right.move_to(RIGHT * 4.0)
            
            return VGroup(m_left, m_mid, m_right)
            
        def make_line():
            return Line(LEFT * 6.5, RIGHT * 6.5, color=Theme.DIM, stroke_width=1.5)

        # Hàng 1: Header (Đã thay thế Text rỗng bằng Square vô hình có đầy đủ điểm tọa độ)
        row_header = create_row(
            Square(side_length=0.1, stroke_opacity=0, fill_opacity=0),
            Text("Diffusion", font=Theme.FONT_BODY, font_size=28, color=Theme.ACCENT_RED),
            Text("Flow Matching", font=Theme.FONT_BODY, font_size=28, color=Theme.PRIMARY)
        )
        
        # Hàng 2: x_t
        row_xt = create_row(
            MathTex(r"x_t", font_size=32, color=Theme.ACCENT_GOLD),
            MathTex(r"\alpha_t x + \sigma_t \epsilon", font_size=32, color=Theme.NEUTRAL),
            MathTex(r"\alpha_t x + \sigma_t z", font_size=32, color=Theme.NEUTRAL)
        )
        
        # Hàng 3: Loss L(theta)
        row_loss = create_row(
            MathTex(r"\mathcal{L}(\theta)", font_size=32, color=Theme.ACCENT_GOLD),
            MathTex(r"\mathcal{L}_S \sim \left\| s_\theta(x_t, t) + \frac{\epsilon}{\sigma_t} \right\|_2^2", font_size=30, color=Theme.NEUTRAL),
            MathTex(r"\mathcal{L}_V \sim \left\| v_\theta(X_t, t) - \tilde{v}(X_t, t) \right\|_2^2", font_size=30, color=Theme.NEUTRAL)
        )
        
        # Hàng 4: ODE
        row_ode = create_row(
            Text("ODE", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD),
            MathTex(r"dX_t = \left[-\frac{1}{2}\beta_t X_t - \frac{1}{2}\beta_t \nabla_x \log p(x)\right]dt", font_size=26, color=Theme.NEUTRAL),
            MathTex(r"dX_t = v(X_t, t)", font_size=26, color=Theme.NEUTRAL)
        )
        
        # Hàng 5: SDE
        row_sde = create_row(
            Text("SDE", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD),
            MathTex(r"dX_t = \left[-\frac{1}{2}\beta_t X_t - \beta_t \nabla_x \log p(x)\right]dt + \sqrt{\beta_t}d\bar{W}_t", font_size=26, color=Theme.NEUTRAL),
            MathTex(r"?", font_size=36, color=Theme.DIM)
        )
        
        # Xếp các hàng và các đường kẻ dọc theo trục Y
        table_group = VGroup(
            row_header,
            make_line(),
            row_xt,
            make_line(),
            row_loss,
            make_line(),
            row_ode,
            make_line(),
            row_sde,
            make_line()
        ).arrange(DOWN, buff=0.35)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: KẾT LUẬN CUỐI SLIDE
        # ─────────────────────────────────────────────────────────────────────
        
        conclusion = MathTex(
            r"\text{With same set of } \alpha_t \text{ and } \sigma_t \text{, their } x_t \text{ is the same.}",
            font_size=36, color=Theme.NEUTRAL
        )
        conclusion[0][14:16].set_color(Theme.ACCENT_GOLD) # highlight alpha_t
        conclusion[0][19:21].set_color(Theme.ACCENT_GOLD) # highlight sigma_t
        conclusion[0][28:30].set_color(Theme.ACCENT_GOLD) # highlight x_t
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: GOM NHÓM TỔNG THỂ & ÉP KÍCH THƯỚC AN TOÀN (Tránh Lỗi 2, 3)
        # ─────────────────────────────────────────────────────────────────────
        
        main_layout = VGroup(top_summaries, table_group, conclusion).arrange(DOWN, buff=0.6)
        
        # Khống chế toàn bộ slide ở độ cao an toàn (5.8/8.0) và căn giữa màn hình
        main_layout.set_height(5.8)
        main_layout.center()
        main_layout.shift(DOWN * 0.1) # Dịch xuống 1 chút để nhường không gian cho Title
        
        # Chốt chặn kiểm tra chiều rộng an toàn (Tránh lỗi tràn viền)
        if main_layout.width > 13.5:
            main_layout.set_width(13.5)
            main_layout.center()
            main_layout.shift(DOWN * 0.1)
            
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.next_slide()
        
        # 1. Hiện đoạn văn tóm tắt
        self.play(FadeIn(fm_summary))
        self.play(FadeIn(diff_summary))
        self.next_slide()
        
        # 2. Hiện Header bảng và đường kẻ đầu tiên
        self.play(FadeIn(table_group[0]), Create(table_group[1]))
        self.next_slide()
        
        # 3. Hiện lần lượt các hàng so sánh
        row_indices = [2, 4, 6, 8]
        for idx in row_indices:
            self.play(FadeIn(table_group[idx]))
            self.play(Create(table_group[idx+1]), run_time=0.5)
            self.next_slide()
            
        # 4. Hiện kết luận cuối cùng
        self.play(Write(conclusion))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 15 — MODULE 12: MMDIT ARCHITECTURE (STABLE DIFFUSION 3)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module12_MMDiT_Architecture(Slide):
    def construct(self):
        # 1. Nền & Tiêu đề (Đã bỏ chữ "Module")
        self.camera.background_color = Theme.BG
        title = slide_title("MMDiT Architecture")
        
        # ─────────────────────────────────────────────────────────────────────
        # PANEL (A): OVERVIEW (VĨ MÔ)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- Cột 1: Text Conditioning ---
        t_in = RoundedBox(["Caption"], width=1.6, height=0.6, fill_color=Theme.BOX_FILL)
        t_enc = RoundedBox(["Text", "Encoders"], width=1.6, height=0.8, fill_color=Theme.DIM)
        c_tok = RoundedBox(["c"], width=0.8, height=0.6, stroke_color=Theme.ACCENT_GOLD)
        col_t = VGroup(t_in, t_enc, c_tok).arrange(DOWN, buff=0.3)
        
        # --- Cột 2: Time Modulation ---
        time_in = RoundedBox(["Timestep"], width=1.6, height=0.6, fill_color=Theme.BOX_FILL)
        time_enc = RoundedBox(["MLP"], width=1.6, height=0.8, fill_color=Theme.DIM)
        y_tok = RoundedBox(["y"], width=0.8, height=0.6, stroke_color=Theme.ACCENT_RED)
        col_y = VGroup(time_in, time_enc, y_tok).arrange(DOWN, buff=0.3)
        
        # --- Cột 3: Image / Latent ---
        i_in = RoundedBox(["Noised", "Latent"], width=1.6, height=0.6, fill_color=Theme.BOX_FILL)
        i_enc = RoundedBox(["Patching"], width=1.6, height=0.8, fill_color=Theme.DIM)
        x_tok = RoundedBox(["x"], width=0.8, height=0.6, stroke_color=Theme.SUCCESS)
        col_i = VGroup(i_in, i_enc, x_tok).arrange(DOWN, buff=0.3)
        
        # Gom 3 cột lại (căn bằng đầu trên để không bị Lỗi 4)
        top_macro = VGroup(col_t, col_y, col_i).arrange(RIGHT, buff=0.4, aligned_edge=UP)
        
        # --- Khối MM-DiT cốt lõi ---
        core_blocks = RoundedBox(
            ["MM-DiT Blocks (x N)"], 
            width=top_macro.width, height=1.0, 
            fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY
        )
        core_blocks.next_to(top_macro, DOWN, buff=0.5)
        
        out_box = RoundedBox(["Output"], width=2.0, height=0.6, fill_color=Theme.BOX_FILL)
        out_box.next_to(core_blocks, DOWN, buff=0.4)
        
        panel_a_group = VGroup(top_macro, core_blocks, out_box)
        lbl_a = Text("(a) Overview", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL).next_to(panel_a_group, DOWN, buff=0.4)
        panel_a = VGroup(panel_a_group, lbl_a)
        
        # ─────────────────────────────────────────────────────────────────────
        # PANEL (B): ONE MM-DiT BLOCK (VI MÔ)
        # ─────────────────────────────────────────────────────────────────────
        
        # Cấu trúc luồng kép (Parallel Streams) - Căn giữa, khoảng cách đều
        c_stream = RoundedBox(["c (Text)"], width=1.6, height=0.6, stroke_color=Theme.ACCENT_GOLD)
        x_stream = RoundedBox(["x (Image)"], width=1.6, height=0.6, stroke_color=Theme.SUCCESS)
        row0 = VGroup(c_stream, x_stream).arrange(RIGHT, buff=1.2)
        
        ln_c1 = RoundedBox(["AdaLN"], width=1.6, height=0.5, fill_color=Theme.DIM)
        ln_x1 = RoundedBox(["AdaLN"], width=1.6, height=0.5, fill_color=Theme.DIM)
        row1 = VGroup(ln_c1, ln_x1).arrange(RIGHT, buff=1.2)
        row1.next_to(row0, DOWN, buff=0.8) # Chừa chỗ cho biến y
        
        joint_attn = RoundedBox(["Joint QKV Attention"], width=4.4, height=0.8, fill_color=ManimColor("#8E24AA"), stroke_color=Theme.NEUTRAL)
        joint_attn.next_to(row1, DOWN, buff=0.4)
        
        ln_c2 = RoundedBox(["AdaLN"], width=1.6, height=0.5, fill_color=Theme.DIM)
        ln_x2 = RoundedBox(["AdaLN"], width=1.6, height=0.5, fill_color=Theme.DIM)
        row3 = VGroup(ln_c2, ln_x2).arrange(RIGHT, buff=1.2)
        row3.next_to(joint_attn, DOWN, buff=0.8)
        
        mlp_c = RoundedBox(["Text MLP"], width=1.6, height=0.6, stroke_color=Theme.PRIMARY)
        mlp_x = RoundedBox(["Image MLP"], width=1.6, height=0.6, stroke_color=Theme.PRIMARY)
        row4 = VGroup(mlp_c, mlp_x).arrange(RIGHT, buff=1.2)
        row4.next_to(row3, DOWN, buff=0.4)
        
        # Biến điều kiện Y (Modulation) chen vào giữa các block AdaLN
        y_mod1 = RoundedBox(["y"], width=0.8, height=0.4, stroke_color=Theme.ACCENT_RED)
        y_mod1.next_to(row1, UP, buff=0.2)
        
        y_mod2 = RoundedBox(["y"], width=0.8, height=0.4, stroke_color=Theme.ACCENT_RED)
        y_mod2.next_to(row3, UP, buff=0.2)
        
        panel_b_group = VGroup(row0, y_mod1, row1, joint_attn, y_mod2, row3, row4)
        
        # Đóng khung khối MM-DiT Block
        block_frame = RoundedRectangle(
            width=panel_b_group.width + 0.6, height=panel_b_group.height + 0.6,
            corner_radius=0.2, stroke_color=Theme.DIM, stroke_width=2,
            fill_color=Theme.BG, fill_opacity=0.3
        ).move_to(panel_b_group.get_center())
        
        lbl_b = Text("(b) One MM-DiT Block", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL).next_to(block_frame, DOWN, buff=0.4)
        panel_b = VGroup(block_frame, panel_b_group, lbl_b)
        
        # ─────────────────────────────────────────────────────────────────────
        # GOM NHÓM TỔNG THỂ & CHỐNG TRÀN BIÊN LỖI 2 & 3
        # ─────────────────────────────────────────────────────────────────────
        
        all_panels = VGroup(panel_a, panel_b).arrange(RIGHT, buff=1.2)
        all_panels.set_height(5.2) # Ép chiều cao an toàn
        all_panels.center()
        all_panels.shift(UP * 0.1) # Dịch lên một chút cho caption
        
        # ─────────────────────────────────────────────────────────────────────
        # VẼ MŨI TÊN (SAU KHI ĐÃ CỐ ĐỊNH TỌA ĐỘ)
        # ─────────────────────────────────────────────────────────────────────
        
        def make_arrow(start, end, color=Theme.NEUTRAL):
            return Arrow(start, end, buff=0.08, color=color, stroke_width=2.5, tip_length=0.12)
            
        arrows = VGroup()
        
        # Arrows (a)
        for col in [col_t, col_y, col_i]:
            arrows.add(make_arrow(col[0].get_bottom(), col[1].get_top()))
            arrows.add(make_arrow(col[1].get_bottom(), col[2].get_top()))
            
        # Nối c, y, x thẳng xuống core_blocks (Sử dụng vector numpy chiếu tọa độ Y chuẩn xác)
        arrows.add(make_arrow(c_tok.get_bottom(), np.array([c_tok.get_x(), core_blocks.get_top()[1], 0]), Theme.ACCENT_GOLD))
        arrows.add(make_arrow(y_tok.get_bottom(), np.array([y_tok.get_x(), core_blocks.get_top()[1], 0]), Theme.ACCENT_RED))
        arrows.add(make_arrow(x_tok.get_bottom(), np.array([x_tok.get_x(), core_blocks.get_top()[1], 0]), Theme.SUCCESS))
        arrows.add(make_arrow(core_blocks.get_bottom(), out_box.get_top()))
        
        # Arrows (b) - Text Stream
        arrows.add(make_arrow(c_stream.get_bottom(), ln_c1.get_top()))
        arrows.add(make_arrow(ln_c1.get_bottom(), np.array([ln_c1.get_x(), joint_attn.get_top()[1], 0])))
        arrows.add(make_arrow(np.array([ln_c2.get_x(), joint_attn.get_bottom()[1], 0]), ln_c2.get_top()))
        arrows.add(make_arrow(ln_c2.get_bottom(), mlp_c.get_top()))
        arrows.add(make_arrow(mlp_c.get_bottom(), mlp_c.get_bottom() + DOWN*0.4))
        
        # Arrows (b) - Image Stream
        arrows.add(make_arrow(x_stream.get_bottom(), ln_x1.get_top()))
        arrows.add(make_arrow(ln_x1.get_bottom(), np.array([ln_x1.get_x(), joint_attn.get_top()[1], 0])))
        arrows.add(make_arrow(np.array([ln_x2.get_x(), joint_attn.get_bottom()[1], 0]), ln_x2.get_top()))
        arrows.add(make_arrow(ln_x2.get_bottom(), mlp_x.get_top()))
        arrows.add(make_arrow(mlp_x.get_bottom(), mlp_x.get_bottom() + DOWN*0.4))
        
        # Arrows (b) - Modulation (Dashed)
        def make_dash(start, end):
            return DashedLine(start, end, buff=0.1, color=Theme.ACCENT_RED, stroke_width=2.5).add_tip(tip_length=0.1)
            
        arrows.add(make_dash(y_mod1.get_left(), ln_c1.get_top() + RIGHT*0.2))
        arrows.add(make_dash(y_mod1.get_right(), ln_x1.get_top() + LEFT*0.2))
        arrows.add(make_dash(y_mod2.get_left(), ln_c2.get_top() + RIGHT*0.2))
        arrows.add(make_dash(y_mod2.get_right(), ln_x2.get_top() + LEFT*0.2))

        # Dòng kết luận dưới cùng
        summary = Text(
            "MMDiT uses parallel streams for Text and Image, fusing them only inside the Joint Attention layer.",
            font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL
        ).to_edge(DOWN, buff=0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.next_slide()
        
        # (1) Hiển thị tổng quan Macro
        self.play(FadeIn(panel_a), FadeIn(arrows[:11]))
        self.next_slide()
        
        # (2) Hiển thị khung của khối Micro
        self.play(FadeIn(block_frame), FadeIn(lbl_b))
        self.play(FadeIn(c_stream), FadeIn(x_stream))
        self.next_slide()
        
        # (3) Quá trình điều kiện hóa thứ nhất (AdaLN 1)
        self.play(FadeIn(ln_c1), FadeIn(ln_x1), FadeIn(arrows[11]), FadeIn(arrows[16])) # Mũi tên thẳng xuống
        self.play(FadeIn(y_mod1), FadeIn(arrows[-4]), FadeIn(arrows[-3])) # Mũi tên đứt nét từ y
        self.next_slide()
        
        # (4) Lớp Joint Attention hợp nhất hai luồng
        self.play(FadeIn(joint_attn), FadeIn(arrows[12]), FadeIn(arrows[17]))
        self.next_slide()
        
        # (5) Tách luồng và điều kiện hóa thứ hai, đưa qua MLP
        self.play(FadeIn(ln_c2), FadeIn(ln_x2), FadeIn(arrows[13]), FadeIn(arrows[18]))
        self.play(FadeIn(y_mod2), FadeIn(arrows[-2]), FadeIn(arrows[-1]))
        self.play(FadeIn(mlp_c), FadeIn(mlp_x), FadeIn(arrows[14]), FadeIn(arrows[15]), FadeIn(arrows[19]), FadeIn(arrows[20]))
        self.next_slide()
        
        # (6) Kết luận
        self.play(FadeIn(summary))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 16 — MODULE 13: GENERATION FOR REPRESENTATION LEARNING  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Brace

class Module13_Representation(Slide):
    def construct(self):
        # 1. Nền & Tiêu đề (Đã bỏ chữ "Module" theo yêu cầu)
        self.camera.background_color = Theme.BG
        title = slide_title("Generation for Representation Learning")
        
        # 2. Text Bullets (Tóm tắt ý chính, ghim sát lề trái dưới Title)
        bullet_1 = Text(
            "• Diffusion models can learn acceptable discriminative representations.",
            font=Theme.FONT_BODY, font_size=24, color=Theme.SUCCESS
        )
        bullet_2 = Text(
            "• However, quality still lags behind state-of-the-art self-supervised methods.",
            font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_RED
        )
        bullets = VGroup(bullet_1, bullet_2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bullets.next_to(title, DOWN, aligned_edge=LEFT, buff=0.4)
        
        # ─────────────────────────────────────────────────────────────────────
        # XÂY DỰNG 3 LUỒNG SƠ ĐỒ (PIPELINES) ĐƯỢC TỐI GIẢN
        # ─────────────────────────────────────────────────────────────────────
        
        # Màu sắc chủ đạo đại diện cho Encoder (Cam) và Decoder (Xanh)
        COLOR_ENC = ManimColor("#E67E22") # Cam
        COLOR_DEC = ManimColor("#3498DB") # Xanh lam
        
        # --- PIPELINE 1: Pixel-Space Diffusion (U-Net) ---
        p1_in = RoundedBox(["Noised Image", "+ timestep t"], width=2.0, height=0.8, fill_color=Theme.BOX_FILL)
        p1_enc = RoundedBox(["Down/Mid Layers"], width=2.6, height=0.8, fill_color=COLOR_ENC)
        p1_dec = RoundedBox(["Up Layers"], width=2.6, height=0.8, fill_color=COLOR_DEC)
        p1_out = RoundedBox(["Predicted", "Noise"], width=1.6, height=0.8, fill_color=Theme.BOX_FILL)
        
        pipe1_boxes = VGroup(p1_in, p1_enc, p1_dec, p1_out).arrange(RIGHT, buff=0.6)
        
        # Nhãn Brace (Dấu ngoặc ôm lấy phần Encoder / Decoder)
        brace_enc1 = Brace(p1_enc, UP, buff=0.1)
        lbl_enc1 = Text('"encoder"', font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL).next_to(brace_enc1, UP, buff=0.1)
        brace_dec1 = Brace(p1_dec, UP, buff=0.1)
        lbl_dec1 = Text('"decoder"', font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL).next_to(brace_dec1, UP, buff=0.1)
        
        pipe1_full = VGroup(pipe1_boxes, brace_enc1, lbl_enc1, brace_dec1, lbl_dec1)
        
        # --- PIPELINE 2: Latent-Space Diffusion (DiT) ---
        p2_in = RoundedBox(["Image"], width=1.2, height=0.8, fill_color=Theme.BOX_FILL)
        p2_vae = RoundedBox(["VAE", "Encoder"], width=1.4, height=0.8, fill_color=Theme.DIM)
        p2_latent = RoundedBox(["Noised Latent", "+ timestep t"], width=2.0, height=0.8, fill_color=Theme.BOX_FILL)
        p2_enc = RoundedBox(["ViT Layers"], width=2.0, height=0.8, fill_color=COLOR_ENC)
        p2_dec = RoundedBox(["ViT Layers"], width=2.0, height=0.8, fill_color=COLOR_DEC)
        p2_out = RoundedBox(["Predicted", "Noise"], width=1.6, height=0.8, fill_color=Theme.BOX_FILL)
        
        pipe2_boxes = VGroup(p2_in, p2_vae, p2_latent, p2_enc, p2_dec, p2_out).arrange(RIGHT, buff=0.4)
        pipe2_full = VGroup(pipe2_boxes) # Chừa chỗ thêm nhãn nếu cần
        
        # --- PIPELINE 3: Representation Extraction (DDAE / Linear Probe) ---
        p3_in = RoundedBox(["Image"], width=1.2, height=0.8, fill_color=Theme.BOX_FILL)
        p3_enc = RoundedBox(["DDAE", '"Encoder"'], width=2.0, height=0.8, fill_color=COLOR_ENC)
        p3_pool = RoundedBox(["Global Avg", "Pooling"], width=2.0, height=0.8, fill_color=ManimColor("#5DADE2"))
        p3_cls = RoundedBox(["Linear", "Classifier"], width=2.0, height=0.8, fill_color=ManimColor("#5DADE2"))
        p3_out = RoundedBox(["Linear probe", "Accuracy"], width=2.2, height=0.8, fill_color=Theme.BOX_FILL, stroke_color=Theme.SUCCESS)
        
        pipe3_boxes = VGroup(p3_in, p3_enc, p3_pool, p3_cls, p3_out).arrange(RIGHT, buff=0.4)
        pipe3_full = VGroup(pipe3_boxes)
        
        # ─────────────────────────────────────────────────────────────────────
        # GOM NHÓM VÀ CĂN CHỈNH TỔNG THỂ (CHỐNG LỖI TRÀN VIỀN)
        # ─────────────────────────────────────────────────────────────────────
        
        # Đưa 3 luồng vào 1 cụm, xếp chồng dọc
        all_pipelines = VGroup(pipe1_full, pipe2_full, pipe3_full).arrange(DOWN, buff=0.8)
        
        # Ép chiều rộng và chiều cao để đảm bảo an toàn tuyệt đối
        all_pipelines.set_width(13.0)
        all_pipelines.set_height(4.2)
        
        # Neo cụm sơ đồ ngay dưới phần Text Bullets, cách một khoảng an toàn
        all_pipelines.next_to(bullets, DOWN, buff=0.6)
        # Căn giữa theo trục X để đẹp mắt
        all_pipelines.set_x(0)
        
        # Thêm nhãn phụ nhỏ dưới các cụm
        lbl_p12 = Text("(a) Denoising networks in pixel-space and latent-space.", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM).next_to(pipe2_full, DOWN, buff=0.2)
        lbl_p3 = Text("(b) Extracting representation for linear probing.", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM).next_to(pipe3_full, DOWN, buff=0.2)
        
        # ─────────────────────────────────────────────────────────────────────
        # VẼ MŨI TÊN KẾT NỐI (LÀM SAU KHI ĐÃ CỐ ĐỊNH LAYOUT)
        # ─────────────────────────────────────────────────────────────────────
        
        def make_arrow(start, end, color=Theme.NEUTRAL):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=3, tip_length=0.15)
        
        arr_p1 = VGroup(*[make_arrow(pipe1_boxes[i].get_right(), pipe1_boxes[i+1].get_left()) for i in range(len(pipe1_boxes)-1)])
        arr_p2 = VGroup(*[make_arrow(pipe2_boxes[i].get_right(), pipe2_boxes[i+1].get_left()) for i in range(len(pipe2_boxes)-1)])
        arr_p3 = VGroup(*[make_arrow(pipe3_boxes[i].get_right(), pipe3_boxes[i+1].get_left()) for i in range(len(pipe3_boxes)-1)])
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATIONS)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.play(FadeIn(bullet_1))
        self.play(FadeIn(bullet_2))
        self.next_slide()
        
        # Hiển thị Pipeline 1 (U-Net)
        self.play(FadeIn(pipe1_boxes[0]))
        for i in range(1, len(pipe1_boxes)):
            self.play(Create(arr_p1[i-1]), FadeIn(pipe1_boxes[i]), run_time=0.4)
        self.play(FadeIn(brace_enc1), FadeIn(lbl_enc1), FadeIn(brace_dec1), FadeIn(lbl_dec1))
        self.next_slide()
        
        # Hiển thị Pipeline 2 (DiT / Latent)
        self.play(FadeIn(pipe2_boxes[0]))
        for i in range(1, len(pipe2_boxes)):
            self.play(Create(arr_p2[i-1]), FadeIn(pipe2_boxes[i]), run_time=0.4)
        self.play(FadeIn(lbl_p12))
        self.next_slide()
        
        # Hiển thị Pipeline 3 (Representation Extraction) - Đổi màu mũi tên cuối để nhấn mạnh
        arr_p3[-1].set_color(Theme.SUCCESS)
        self.play(FadeIn(pipe3_boxes[0]))
        for i in range(1, len(pipe3_boxes)):
            self.play(Create(arr_p3[i-1]), FadeIn(pipe3_boxes[i]), run_time=0.4)
        self.play(FadeIn(lbl_p3))
        
        # Nhấn mạnh việc Encoder được tái sử dụng để làm Linear Probing
        self.play(Indicate(p1_enc, color=Theme.ACCENT_GOLD), Indicate(p2_enc, color=Theme.ACCENT_GOLD), Indicate(p3_enc, color=Theme.ACCENT_GOLD))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 17 — MODULE 14: REPA REGULARIZATION  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Line

class Module14_REPA(Slide):
    def construct(self):
        # 1. Nền & Tiêu đề (Đã lược bỏ "Module*")
        self.camera.background_color = Theme.BG
        title = slide_title("REPA: A Simple Regularization")
        
        # 2. Text Bullets (Ghim sát lề trái dưới Title)
        bullet_1 = Text(
            "• We guide representation learning via a simple regularization.",
            font=Theme.FONT_BODY, font_size=24, color=Theme.SUCCESS
        )
        bullet_2 = Text(
            "• REPA: Distills pretrained SSL representations into diffusion representations.",
            font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL
        )
        bullets = VGroup(bullet_1, bullet_2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        bullets.next_to(title, DOWN, aligned_edge=LEFT, buff=0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # SƠ ĐỒ BÊN TRÁI: TEACHER & STUDENT ARCHITECTURE
        # ─────────────────────────────────────────────────────────────────────
        
        # --- Cột Teacher (Bên trái) ---
        clean_img = RoundedBox(["Clean", "Image"], width=2.0, height=0.8, fill_color=Theme.BOX_FILL)
        pre_enc = RoundedBox(["Pretrained", "Visual Encoders"], width=2.4, height=1.6, fill_color=Theme.DIM)
        rep_align = RoundedBox(["Representation", "Alignment"], width=2.4, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS)
        
        teacher_col = VGroup(clean_img, pre_enc, rep_align).arrange(UP, buff=0.5)
        
        # --- Cột Student (Bên phải) ---
        noised_img = RoundedBox(["Noised", "Image"], width=2.0, height=0.8, fill_color=Theme.BOX_FILL)
        dit_blocks = VGroup(*[
            RoundedBox(["DiT/SiT Block"], width=2.8, height=0.45, fill_color=Theme.SUCCESS, stroke_color=Theme.PRIMARY)
            for _ in range(5) # Tạo stack 5 khối để tượng trưng
        ]).arrange(UP, buff=0.1) 
        denoise_obj = RoundedBox(["Denoising", "Objective"], width=2.8, height=0.8, fill_color=Theme.BOX_FILL)
        
        student_col = VGroup(noised_img, dit_blocks, denoise_obj).arrange(UP, buff=0.5)
        
        # Căn chỉnh đáy của 2 cột ngang nhau
        diagram_cols = VGroup(teacher_col, student_col).arrange(RIGHT, buff=2.5, aligned_edge=DOWN)
        
        # --- Khối MLP kết nối ở giữa ---
        mlp = RoundedBox(["MLP"], width=1.2, height=0.6, fill_color=Theme.ACCENT_GOLD, stroke_color=Theme.NEUTRAL)
        
        # Neo MLP thẳng hàng với DiT Block giữa (index 2)
        mlp.set_y(dit_blocks[2].get_y())
        mlp.set_x((teacher_col.get_right()[0] + student_col.get_left()[0]) / 2)
        
        # QUAN TRỌNG: Điều chỉnh lại trục ngang của cột Teacher để Representation Alignment thẳng hàng với MLP
        rep_align.set_y(mlp.get_y())
        pre_enc.next_to(rep_align, DOWN, buff=0.5)
        clean_img.next_to(pre_enc, DOWN, buff=0.5)
        
        diagram = VGroup(clean_img, pre_enc, rep_align, noised_img, dit_blocks, denoise_obj, mlp)
        
        # ─────────────────────────────────────────────────────────────────────
        # PHƯƠNG TRÌNH TOÁN HỌC BÊN PHẢI (MÃ HÓA MÀU SẮC)
        # ─────────────────────────────────────────────────────────────────────
        
        eq_text = Text(
            "Alignment between the target representation\nand the projected hidden state",
            font=Theme.FONT_BODY, font_size=20, color=Theme.SUCCESS
        )
        
        # Cắt chuỗi công thức để có thể tô màu từng thành phần độc lập
        eq_math = MathTex(
            r"-\mathbb{E}_{x, \epsilon, t} \left[ \frac{1}{N} \sum_{n=1}^N \mathrm{sim} \left(",
            r"y^{[n]}",      # 1: Target (Đích)
            r",", 
            r"h_\phi",       # 3: MLP (Chiếu)
            r"(", 
            r"h_t^{[n]}",    # 5: Hidden state (Trạng thái ẩn)
            r") \right) \right]",
            font_size=40,
            color=Theme.NEUTRAL
        )
        eq_math[1].set_color(Theme.SUCCESS)
        eq_math[3].set_color(Theme.ACCENT_GOLD)
        eq_math[5].set_color(Theme.ACCENT_RED)
        
        # Nhãn chú thích
        lbl_target = Text("Target", font=Theme.FONT_BODY, font_size=16, color=Theme.SUCCESS).next_to(eq_math[1], DOWN, buff=0.4)
        lbl_mlp = Text("MLP", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_GOLD).next_to(eq_math[3], UP, buff=0.4)
        lbl_hidden = Text("Hidden state", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_RED).next_to(eq_math[5], DOWN, buff=0.4)
        
        # Đường kẻ nối nhãn với công thức
        line_t = Line(lbl_target.get_top(), eq_math[1].get_bottom(), stroke_width=2, color=Theme.SUCCESS)
        line_m = Line(lbl_mlp.get_bottom(), eq_math[3].get_top(), stroke_width=2, color=Theme.ACCENT_GOLD)
        line_h = Line(lbl_hidden.get_top(), eq_math[5].get_bottom(), stroke_width=2, color=Theme.ACCENT_RED)
        
        eq_math_full = VGroup(eq_math, lbl_target, lbl_mlp, lbl_hidden, line_t, line_m, line_h)
        eq_group = VGroup(eq_text, eq_math_full).arrange(DOWN, buff=0.8)
        
        # ─────────────────────────────────────────────────────────────────────
        # ĐÓNG GÓI, ÉP KHUNG VÀ VẼ MŨI TÊN (CHỐNG LỖI 2, 3, 4)
        # ─────────────────────────────────────────────────────────────────────
        
        main_content = VGroup(diagram, eq_group).arrange(RIGHT, buff=1.0)
        main_content.set_width(13.5)
        main_content.set_height(4.8) # Đảm bảo nằm lọt khe giữa text và viền dưới
        main_content.next_to(bullets, DOWN, buff=0.5)
        main_content.set_x(0)
        
        # Chỉ tạo mũi tên SAU KHI kích thước của main_content đã bị khóa
        def make_arrow(start, end, color=Theme.NEUTRAL):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=2.5, tip_length=0.15)
            
        arrows = VGroup(
            make_arrow(clean_img.get_top(), pre_enc.get_bottom()),
            make_arrow(pre_enc.get_top(), rep_align.get_bottom()),
            make_arrow(noised_img.get_top(), dit_blocks.get_bottom()),
            make_arrow(dit_blocks.get_top(), denoise_obj.get_bottom()),
            
            # Luồng trích xuất (Extraction path) từ phải sang trái
            make_arrow(dit_blocks[2].get_left(), mlp.get_right(), Theme.ACCENT_RED),
            make_arrow(mlp.get_left(), rep_align.get_right(), Theme.ACCENT_GOLD)
        )
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATIONS)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.play(FadeIn(bullets))
        self.next_slide()
        
        # 1. Hiển thị cột Student (Mô hình Diffusion cần train)
        self.play(FadeIn(noised_img))
        self.play(FadeIn(arrows[2]), FadeIn(dit_blocks))
        self.play(FadeIn(arrows[3]), FadeIn(denoise_obj))
        self.next_slide()
        
        # 2. Hiển thị cột Teacher (Model Pretrained dùng để tham chiếu)
        self.play(FadeIn(clean_img))
        self.play(FadeIn(arrows[0]), FadeIn(pre_enc))
        self.play(FadeIn(arrows[1]), FadeIn(rep_align))
        self.next_slide()
        
        # 3. Kết nối luồng học (Regularization) qua MLP
        self.play(FadeIn(arrows[4]), FadeIn(mlp))
        self.play(FadeIn(arrows[5]))
        self.next_slide()
        
        # 4. Hiện phương trình mô tả toán học của quá trình trên
        self.play(FadeIn(eq_text))
        self.play(Write(eq_math))
        self.next_slide()
        
        # 5. Phân tích màu sắc từng thành phần của phương trình
        self.play(FadeIn(lbl_target), Create(line_t))
        self.play(FadeIn(lbl_mlp), Create(line_m))
        self.play(FadeIn(lbl_hidden), Create(line_h))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 18 — MODULE 15: ELEPHANT IN THE ROOM (LDM FLOPs)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import SurroundingRectangle

class Module15_ElephantInLDM(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG
        title = slide_title('The "Elephant in the room" in LDM')
        
        # 1. TEXT INFO: Phân tích FLOPs (Tối ưu hóa chiều cao gọn gàng hơn)
        info_box = RoundedRectangle(
            width=12.0, height=1.1, corner_radius=0.15,
            stroke_color=Theme.DIM, stroke_width=2, fill_color=Theme.BG, fill_opacity=0.5
        )
        t1 = Text("SD-VAE Total FLOPs: 895.17 GFLOPs (!!!)", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_RED, weight="BOLD")
        t2 = Text("SiT-XL/2 (4, 32, 32) FLOPs: 228.84 GFLOPs", font=Theme.FONT_BODY, font_size=20, color=Theme.PRIMARY)
        t3 = Text("=> VAE takes ~4x more compute than the diffusion backbone!", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_GOLD)
        
        texts = VGroup(t1, t2, t3).arrange(DOWN, buff=0.12)
        texts.move_to(info_box.get_center())
        
        top_group = VGroup(info_box, texts)
        top_group.next_to(title, DOWN, buff=0.15, aligned_edge=LEFT)
        
        # ─────────────────────────────────────────────────────────────────────
        # 2. SƠ ĐỒ LDM ĐƯỢC TỐI ƯU HÓA KHÔNG GIAN DỌC (CHIỀU CAO = 3.0)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- PANEL 1: PIXEL SPACE ---
        pixel_frame = RoundedRectangle(width=2.4, height=3.0, corner_radius=0.15, stroke_color=Theme.ACCENT_RED, stroke_width=3, fill_color=Theme.ACCENT_RED, fill_opacity=0.08)
        x_box = RoundedBox(["Input Image"], width=1.8, height=0.45, font_size=16)
        enc_box = RoundedBox(["Encoder (E)"], width=1.8, height=0.45, font_size=16, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY)
        dec_box = RoundedBox(["Decoder (D)"], width=1.8, height=0.45, font_size=16, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY)
        x_tilde_box = RoundedBox(["Output Image"], width=1.8, height=0.45, font_size=16)
        
        pixel_contents = VGroup(x_box, enc_box, dec_box, x_tilde_box).arrange(DOWN, buff=0.12)
        pixel_contents.move_to(pixel_frame.get_center())
        pixel_label = Text("Pixel Space", font=Theme.FONT_BODY, font_size=14, color=Theme.ACCENT_RED, weight="BOLD").next_to(pixel_frame, UP, buff=0.1)
        pixel_group = VGroup(pixel_frame, pixel_contents, pixel_label)
        
        # --- PANEL 2: LATENT SPACE ---
        latent_z = RoundedBox(["Latent (z)"], width=1.1, height=0.45, font_size=14, stroke_color=Theme.SUCCESS)
        latent_zT = RoundedBox(["Noisy (z_T)"], width=1.1, height=0.45, font_size=14, stroke_color=Theme.SUCCESS)
        diff_box = RoundedBox(["Diffusion Process"], width=2.0, height=0.45, font_size=14, fill_color=Theme.DIM)
        unet_box = RoundedBox(["Denoising SiT"], width=2.0, height=0.6, font_size=14, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY)
        
        mid_col = VGroup(diff_box, unet_box).arrange(DOWN, buff=0.2)
        latent_contents = VGroup(latent_z, mid_col, latent_zT).arrange(RIGHT, buff=0.15)
        
        latent_frame = RoundedRectangle(width=latent_contents.width + 0.3, height=pixel_frame.height, corner_radius=0.15, stroke_color=Theme.SUCCESS, stroke_width=2, fill_color=Theme.BG, fill_opacity=0.3)
        latent_contents.move_to(latent_frame.get_center())
        latent_label = Text("Latent Space", font=Theme.FONT_BODY, font_size=14, color=Theme.SUCCESS, weight="BOLD").next_to(latent_frame, UP, buff=0.1)
        latent_group = VGroup(latent_frame, latent_contents, latent_label)
        
        # --- PANEL 3: CONDITIONING ---
        cond_prompt = RoundedBox(["Prompt"], width=1.4, height=0.45, font_size=14, stroke_color=Theme.ACCENT_GOLD)
        cond_enc = RoundedBox(["Cond Encoder"], width=1.4, height=0.45, font_size=14, stroke_color=Theme.PRIMARY)
        cond_contents = VGroup(cond_prompt, cond_enc).arrange(DOWN, buff=0.2)
        
        cond_frame = RoundedRectangle(width=cond_contents.width + 0.3, height=pixel_frame.height, corner_radius=0.15, stroke_color=Theme.ACCENT_GOLD, stroke_width=2, fill_color=Theme.BG, fill_opacity=0.3)
        cond_contents.move_to(cond_frame.get_center())
        cond_label = Text("Conditioning", font=Theme.FONT_BODY, font_size=14, color=Theme.ACCENT_GOLD, weight="BOLD").next_to(cond_frame, UP, buff=0.1)
        cond_group = VGroup(cond_frame, cond_contents, cond_label)
        
        # Gom cụm sơ đồ
        all_panels = VGroup(pixel_group, latent_group, cond_group).arrange(RIGHT, buff=0.3)
        all_panels.set_width(11.5)
        all_panels.next_to(top_group, DOWN, buff=0.3)
        all_panels.set_x(0)
        
        # Vẽ các mũi tên liên kết tương đối chuẩn xác
        arr_x_enc = Arrow(x_box.get_bottom(), enc_box.get_top(), buff=0.06, color=Theme.NEUTRAL, stroke_width=2, tip_length=0.08)
        arr_dec_x_tilde = Arrow(dec_box.get_bottom(), x_tilde_box.get_top(), buff=0.06, color=Theme.NEUTRAL, stroke_width=2, tip_length=0.08)
        arr_enc_z = Arrow(enc_box.get_right(), latent_z.get_left(), buff=0.06, color=Theme.PRIMARY, stroke_width=2, tip_length=0.08)
        arr_z_dec = Arrow(latent_z.get_left(), dec_box.get_right(), buff=0.06, color=Theme.PRIMARY, stroke_width=2, tip_length=0.08)
        
        # Highlight Box cho VAE
        hl_box = SurroundingRectangle(pixel_group, color=Theme.ACCENT_RED, buff=0.04, stroke_width=4)
        hl_text = Text("~80% Compute Bottleneck!", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_RED, weight="BOLD").next_to(hl_box, DOWN, buff=0.1)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        self.play(FadeIn(info_box), FadeIn(t1))
        self.play(FadeIn(t2), FadeIn(t3))
        self.next_slide()
        
        self.play(FadeIn(all_panels))
        self.play(FadeIn(arr_x_enc), FadeIn(arr_dec_x_tilde), FadeIn(arr_enc_z), FadeIn(arr_z_dec))
        self.next_slide()
        
        self.play(Create(hl_box), Write(hl_text))
        self.next_slide()


# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 19 — MODULE 16: OPTIMIZATION DILEMMA  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module16_OptimizationDilemma(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG
        title = slide_title("Optimization Dilemma in LDM")
        
        subtitle = Text("Reconstruction vs. Generation", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.2)
        
        # ─────────────────────────────────────────────────────────────────────
        # DIAGRAM: TRUYỀN THỐNG VS. VF LOSS
        # ─────────────────────────────────────────────────────────────────────
        
        # --- Luồng Trái: VAE Truyền thống ---
        enc = RoundedBox(["Encoder"], width=2.4, height=0.6, fill_color=Theme.DIM)
        tok = RoundedBox(["High-dimensional", "Visual Tokens"], width=2.6, height=1.0, fill_color=Theme.BOX_FILL, stroke_color=Theme.ACCENT_GOLD)
        dec = RoundedBox(["Decoder"], width=2.4, height=0.6, fill_color=Theme.DIM)
        
        vae_col = VGroup(dec, tok, enc).arrange(DOWN, buff=0.6)
        
        loss_recon = Text("Reconstruction\n+ GAN Loss", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_RED).next_to(dec, UP, buff=0.3)
        loss_kl = Text("KL Loss", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL).next_to(tok, LEFT, buff=0.4)
        
        # --- Luồng Phải: VF Loss (Ours) ---
        vf_model = RoundedBox(["Vision Foundation", "Models (DINOv2, MAE)"], width=3.4, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_GOLD)
        vf_loss = RoundedBox(["VF Loss (Ours)"], width=2.4, height=0.6, fill_color=Theme.BOX_FILL, stroke_color=Theme.SUCCESS)
        
        # Gióng hàng ngang với Visual Tokens
        vf_loss.set_y(tok.get_y())
        vf_loss.next_to(tok, RIGHT, buff=2.5)
        
        vf_model.set_x(vf_loss.get_x())
        vf_model.next_to(vf_loss, UP, buff=0.9)
        
        diagram = VGroup(vae_col, loss_recon, loss_kl, vf_model, vf_loss)
        diagram.set_height(4.0) # Khống chế chiều cao an toàn (Lỗi 3)
        diagram.next_to(subtitle, DOWN, buff=0.6)
        diagram.center()
        
        # --- Vẽ mũi tên kết nối ---
        def make_arrow(start, end, color=Theme.NEUTRAL):
            return Arrow(start, end, buff=0.1, color=color, stroke_width=3, tip_length=0.15)
            
        arrows = VGroup(
            make_arrow(enc.get_top(), tok.get_bottom()),
            make_arrow(tok.get_top(), dec.get_bottom()),
            make_arrow(dec.get_top(), loss_recon.get_bottom(), Theme.ACCENT_RED),
            make_arrow(tok.get_left(), loss_kl.get_right()),
            
            # VF Loss connections
            make_arrow(tok.get_right(), vf_loss.get_left(), Theme.SUCCESS),
            make_arrow(vf_model.get_bottom(), vf_loss.get_top(), Theme.ACCENT_GOLD)
        )
        
        # ─────────────────────────────────────────────────────────────────────
        # TEXT ĐỐI CHIẾU ĐẶC ĐIỂM Ở CHÂN SLIDE
        # ─────────────────────────────────────────────────────────────────────
        
        col1_t1 = Text("• High reconstruction quality", font=Theme.FONT_BODY, font_size=20, color=Theme.SUCCESS)
        col1_t2 = Text("• Generation inhibitive", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED)
        col1 = VGroup(col1_t1, col1_t2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        col2_t1 = Text("• Semantic-rich representations", font=Theme.FONT_BODY, font_size=20, color=Theme.SUCCESS)
        col2_t2 = Text("• Generation friendly", font=Theme.FONT_BODY, font_size=20, color=Theme.SUCCESS)
        col2 = VGroup(col2_t1, col2_t2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Căn chỉnh 2 cột text vào 2 bên luồng
        col1.next_to(enc, DOWN, buff=0.6)
        col2.next_to(vf_loss, DOWN, buff=0.6)
        col2.set_y(col1.get_y()) # Ép thẳng hàng ngang đáy
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.next_slide()
        
        # Hiển thị luồng VAE truyền thống
        self.play(FadeIn(vae_col), FadeIn(loss_recon), FadeIn(loss_kl))
        self.play(FadeIn(arrows[:4]))
        self.play(FadeIn(col1))
        self.next_slide()
        
        # Hiển thị giải pháp VF Loss
        self.play(FadeIn(vf_model), FadeIn(vf_loss))
        self.play(Create(arrows[4]), Create(arrows[5]))
        self.play(FadeIn(col2))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 20 — MODULE 17: E2E REPA  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module17_E2ERepa(Slide):
    def construct(self):
        # 1. Nền & Tiêu đề
        self.camera.background_color = Theme.BG
        title = slide_title("E2E REPA")
        
        subtitle = Text(
            "REPA-E: Unlocking VAE for End-to-End Tuning with Latent Diffusion Transformers",
            font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD
        )
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.3)
        
        # Hàm tạo nhanh một chồng các block SiT (5 block)
        def make_sit_stack(color, n=5):
            return VGroup(*[
                RoundedBox(["SiT Block"], width=2.4, height=0.4, fill_color=Theme.BOX_FILL_ALT, stroke_color=color, font_size=18)
                for _ in range(n)
            ]).arrange(DOWN, buff=0.1)

        # ─────────────────────────────────────────────────────────────────────
        # COL A: Traditional LDM
        # ─────────────────────────────────────────────────────────────────────
        sit_a = make_sit_stack(Theme.SUCCESS)
        vae_a = RoundedBox(["VAE", "[Frozen]"], width=2.4, height=0.8, fill_color=Theme.DIM)
        col_a_boxes = VGroup(sit_a, vae_a).arrange(DOWN, buff=0.6)

        # ─────────────────────────────────────────────────────────────────────
        # COL B: Naive E2E LDM
        # ─────────────────────────────────────────────────────────────────────
        sit_b = make_sit_stack(Theme.ACCENT_RED)
        vae_b = RoundedBox(["VAE"], width=2.4, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_RED)
        col_b_boxes = VGroup(sit_b, vae_b).arrange(DOWN, buff=0.6)

        # ─────────────────────────────────────────────────────────────────────
        # COL C: REPA-E (Ours)
        # ─────────────────────────────────────────────────────────────────────
        sit_c = make_sit_stack(Theme.PRIMARY)
        bn_c = RoundedBox(["BatchNorm"], width=2.4, height=0.45, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY, font_size=18)
        top_c = VGroup(sit_c, bn_c).arrange(DOWN, buff=0.1)
        
        vae_c = RoundedBox(["VAE"], width=2.4, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY)
        col_c_boxes = VGroup(top_c, vae_c).arrange(DOWN, buff=0.4)

        # ─────────────────────────────────────────────────────────────────────
        # SẮP XẾP 3 CỘT (Khóa đáy VAE ngang hàng để tránh Lỗi 4)
        # ─────────────────────────────────────────────────────────────────────
        diagrams = VGroup(col_a_boxes, col_b_boxes, col_c_boxes).arrange(RIGHT, buff=2.5, aligned_edge=DOWN)

        # Nhãn text bên dưới mỗi cột
        lbl_a = Text("a) Traditional\nLDM Training", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL).next_to(vae_a, DOWN, buff=0.4)
        lbl_b = Text("b) Naïve End-to-End\nLDM Training", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL).next_to(vae_b, DOWN, buff=0.4)
        lbl_c = Text("c) REPA-E\n(Ours)", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL).next_to(vae_c, DOWN, buff=0.4)

        # ─────────────────────────────────────────────────────────────────────
        # VẼ MŨI TÊN (SAU KHI CỐ ĐỊNH TỌA ĐỘ)
        # ─────────────────────────────────────────────────────────────────────
        def make_bracket_arrow(sit_group, color, is_left=True):
            direction = LEFT if is_left else RIGHT
            shift_x = 1.2 * direction
            arrow_x = 1.4 * direction
            
            p1 = sit_group.get_top() + shift_x
            p2 = sit_group.get_top() + arrow_x
            p3 = sit_group.get_bottom() + shift_x
            p4 = sit_group.get_bottom() + arrow_x
            
            l1 = Line(p1, p2, color=color, stroke_width=2)
            l2 = Line(p3, p4, color=color, stroke_width=2)
            arr = Arrow(p2, p4, buff=0, color=color, stroke_width=2, tip_length=0.15)
            
            rot = PI/2 if is_left else -PI/2
            lbl = Text("Diffusion Loss", font_size=18, color=color).rotate(rot).next_to(arr, direction, buff=0.15)
            
            return VGroup(l1, l2, arr, lbl)

        arrow_a = make_bracket_arrow(sit_a, Theme.SUCCESS)
        arrow_b = make_bracket_arrow(sit_b, Theme.ACCENT_RED)
        arrow_c = make_bracket_arrow(sit_c, Theme.PRIMARY)

        # Mũi tên Stop-Grad (Dọc từ khối SiT cuối cùng xuống VAE)
        arr_stop = Arrow(sit_c.get_bottom() + LEFT*0.8, vae_c.get_top() + LEFT*0.8, buff=0.05, color=Theme.NEUTRAL, stroke_width=2, tip_length=0.12)
        cross = Text("X", font_size=16, color=Theme.ACCENT_RED, weight="BOLD").move_to(arr_stop.get_center())
        lbl_stop = Text("Stop-Grad", font_size=14, color=Theme.NEUTRAL).next_to(cross, LEFT, buff=0.1)
        vg_stop = VGroup(arr_stop, cross, lbl_stop)

        # Mũi tên Alignment Loss (Bên phải khối SiT cuối cùng và BatchNorm)
        p1 = sit_c[-1].get_top() + RIGHT*1.2
        p2 = sit_c[-1].get_top() + RIGHT*1.4
        p3 = bn_c.get_bottom() + RIGHT*1.2
        p4 = bn_c.get_bottom() + RIGHT*1.4
        l1 = Line(p1, p2, color=Theme.PRIMARY, stroke_width=2)
        l2 = Line(p3, p4, color=Theme.PRIMARY, stroke_width=2)
        arr_align = Arrow(p2, p4, buff=0, color=Theme.PRIMARY, stroke_width=2, tip_length=0.15)
        lbl_align = Text("Alignment Loss", font_size=18, color=Theme.PRIMARY).rotate(-PI/2).next_to(arr_align, RIGHT, buff=0.15)
        vg_align = VGroup(l1, l2, arr_align, lbl_align)

        # ─────────────────────────────────────────────────────────────────────
        # GOM NHÓM & ÉP KHUNG CHỐNG TRÀN LỖI 2, 3
        # ─────────────────────────────────────────────────────────────────────
        all_content = VGroup(
            diagrams, lbl_a, lbl_b, lbl_c,
            arrow_a, arrow_b, arrow_c,
            vg_stop, vg_align
        )
        all_content.set_height(5.2)  # Giới hạn chiều cao an toàn
        all_content.next_to(subtitle, DOWN, buff=0.5)
        all_content.set_x(0)  # Căn giữa hoàn hảo
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATIONS)
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.next_slide()
        
        # Hiển thị cột A
        self.play(FadeIn(col_a_boxes), FadeIn(lbl_a))
        self.play(FadeIn(arrow_a))
        self.next_slide()
        
        # Hiển thị cột B
        self.play(FadeIn(col_b_boxes), FadeIn(lbl_b))
        self.play(FadeIn(arrow_b))
        self.next_slide()
        
        # Hiển thị cột C
        self.play(FadeIn(col_c_boxes), FadeIn(lbl_c))
        self.play(FadeIn(arrow_c))
        
        # Xuất hiện các cải tiến của mô hình (Stop-Grad & Alignment Loss)
        self.play(FadeIn(vg_stop))
        self.play(FadeIn(vg_align))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 21 — MODULE 18: SELF-GUIDED REPA (FIXED OVERLAP)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module18_SelfGuidedREPA(Slide):
    def construct(self):
        # 1. Nền & Tiêu đề
        self.camera.background_color = Theme.BG
        title = slide_title("Self-guided REPA")
        
        # ─────────────────────────────────────────────────────────────────────
        # CỘT TRÁI: THÔNG ĐIỆP
        # ─────────────────────────────────────────────────────────────────────
        
        t1 = Text("No Other Representation", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD")
        t2 = Text("Component Is Needed:", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD")
        t3 = Text("Diffusion Transformers", font=Theme.FONT_BODY, font_size=28, color=Theme.PRIMARY, weight="BOLD")
        t4 = Text("Can Provide Representation", font=Theme.FONT_BODY, font_size=28, color=Theme.SUCCESS, weight="BOLD")
        t5 = Text("Guidance by Themselves", font=Theme.FONT_BODY, font_size=28, color=Theme.SUCCESS, weight="BOLD")
        
        quote_text = VGroup(t1, t2, t3, t4, t5).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        link_text = Text(
            "Code available at:\nhttps://github.com/vvvvvjdy/SRA", 
            font=Theme.FONT_BODY, font_size=16, color=Theme.DIM, line_spacing=0.8
        )
        
        left_col = VGroup(quote_text, link_text).arrange(DOWN, aligned_edge=LEFT, buff=0.8)

        # ─────────────────────────────────────────────────────────────────────
        # CỘT PHẢI: KHỞI TẠO HÌNH HỌC (TẠO KHOẢNG TRỐNG CỰC LỚN)
        # ─────────────────────────────────────────────────────────────────────
        
        def make_stack(color):
            return VGroup(*[
                RoundedBox(["DiT/SiT Block"], width=2.0, height=0.45, fill_color=Theme.BOX_FILL_ALT, stroke_color=color, font_size=16)
                for _ in range(5)
            ]).arrange(DOWN, buff=0.15)

        # 1. Hai trụ cột chính
        stack_L = make_stack(Theme.SUCCESS)
        img_L = RoundedBox(["Input Image"], width=1.8, height=0.5, fill_color=Theme.BOX_FILL)
        l_gen = MathTex(r"\mathcal{L}_{gen}", font_size=32, color=Theme.NEUTRAL)
        
        stack_R = make_stack(Theme.PRIMARY)
        img_R = RoundedBox(["Input Image"], width=1.8, height=0.5, fill_color=Theme.BOX_FILL)

        # Nới rộng khoảng cách giữa 2 trụ lên tận buff=5.0 để tạo vùng giữa rộng rãi
        stacks_group = VGroup(stack_L, stack_R).arrange(RIGHT, buff=5.0)
        
        img_L.next_to(stack_L, DOWN, buff=0.5)
        img_R.next_to(stack_R, DOWN, buff=0.5)
        l_gen.next_to(stack_L, UP, buff=0.3)

        # 2. Khối MLPs và Loss (Đẩy ra xa khỏi trụ cột bằng buff=1.8)
        # Điều này đảm bảo mũi tên sinh ra sẽ đủ dài để chứa text
        mlp_box = RoundedBox(["MLPs"], width=1.2, height=0.5, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_RED)
        mlp_box.next_to(stack_L[3], RIGHT, buff=1.8) 

        l_sa = MathTex(r"\mathcal{L}_{sa}", font_size=32, color=Theme.NEUTRAL)
        l_sa.next_to(stack_R[1], LEFT, buff=1.8)

        core_diagram = VGroup(stacks_group, img_L, img_R, l_gen, mlp_box, l_sa)

        # ─────────────────────────────────────────────────────────────────────
        # GOM NHÓM TỔNG VÀ ÉP SCALE THEO CHIỀU RỘNG
        # ─────────────────────────────────────────────────────────────────────
        
        content = VGroup(left_col, core_diagram).arrange(RIGHT, buff=0.6)
        content.set_width(13.6) # Khóa an toàn chiều ngang màn hình
        content.next_to(title, DOWN, buff=0.5)
        content.set_x(0)
        
        # ─────────────────────────────────────────────────────────────────────
        # VẼ MŨI TÊN VÀ TEXT (Sau khi mọi thứ đã được Scale chuẩn tỷ lệ)
        # ─────────────────────────────────────────────────────────────────────
        
        def make_arrow(start, end, color=Theme.NEUTRAL, dashed=False):
            if dashed:
                return DashedLine(start, end, color=color, stroke_width=2.5, buff=0.1).add_tip(tip_length=0.12)
            return Arrow(start, end, color=color, stroke_width=2.5, buff=0.08, tip_length=0.15)

        arr_in_L = make_arrow(img_L.get_top(), stack_L.get_bottom())
        arr_in_R = make_arrow(img_R.get_top(), stack_R.get_bottom())
        arr_out_L = make_arrow(stack_L.get_top(), l_gen.get_bottom())

        ema_arrow = make_arrow(img_L.get_right(), img_R.get_left(), color=Theme.DIM, dashed=True)
        ema_lbl = Text("ema", font_size=16, color=Theme.DIM).next_to(ema_arrow, DOWN, buff=0.1)

        # --- Đường dẫn Student -> MLP ---
        arr_feat_L = make_arrow(stack_L[3].get_right(), mlp_box.get_left(), color=Theme.SUCCESS)
        # Sử dụng line_spacing=0.8 để text gọn lại theo chiều dọc
        lbl_feat_L = Text("Earlier Layer\nHigher Noise", font_size=14, color=Theme.SUCCESS, line_spacing=0.8)
        lbl_feat_L.next_to(arr_feat_L, UP, buff=0.1)

        # --- Đường dẫn MLP -> Loss ---
        arr_mlp_lsa = make_arrow(mlp_box.get_top(), l_sa.get_bottom(), color=Theme.ACCENT_RED)

        # --- Đường dẫn Teacher -> Loss ---
        arr_feat_R = make_arrow(stack_R[1].get_left(), l_sa.get_right(), color=Theme.PRIMARY)
        lbl_feat_R = Text("Later Layer\nLower Noise", font_size=14, color=Theme.PRIMARY, line_spacing=0.8)
        lbl_feat_R.next_to(arr_feat_R, UP, buff=0.1)
        
        # --- Ký hiệu Stop Gradient (X đỏ) ---
        c_pt = arr_feat_R.get_center()
        sg_l1 = Line(c_pt + UL*0.1, c_pt + DR*0.1, color=Theme.ACCENT_RED, stroke_width=3)
        sg_l2 = Line(c_pt + UR*0.1, c_pt + DL*0.1, color=Theme.ACCENT_RED, stroke_width=3)
        sg_mark = VGroup(sg_l1, sg_l2)
        lbl_sg = Text("sg", font_size=14, color=Theme.ACCENT_RED).next_to(sg_mark, DOWN, buff=0.1)

        # Gom toàn bộ mũi tên và nhãn
        dynamic_elements = VGroup(
            arr_in_L, arr_in_R, arr_out_L, ema_arrow, ema_lbl,
            arr_feat_L, lbl_feat_L, arr_mlp_lsa, arr_feat_R, lbl_feat_R,
            sg_mark, lbl_sg
        )

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.play(FadeIn(left_col))
        self.next_slide()
        
        self.play(FadeIn(img_L), FadeIn(stack_L), Create(arr_in_L))
        self.play(Create(arr_out_L), FadeIn(l_gen))
        self.next_slide()
        
        self.play(FadeIn(img_R), FadeIn(stack_R), Create(arr_in_R))
        self.play(Create(ema_arrow), FadeIn(ema_lbl))
        self.next_slide()
        
        self.play(
            Create(arr_feat_L), FadeIn(lbl_feat_L),
            Create(arr_feat_R), FadeIn(lbl_feat_R), FadeIn(sg_mark), FadeIn(lbl_sg)
        )
        self.next_slide()
        
        self.play(FadeIn(mlp_box))
        self.play(Create(arr_mlp_lsa), FadeIn(l_sa))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 22 — MODULE 19: LLM OUTPUTS FOR IMAGE GENERATION  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module19_LLM_ImageGen(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG
        
        # 1. Tiêu đề cố định (Neo góc UL tránh Lỗi 1)
        title = slide_title("LLM outputs for image generation")
        self.play(Write(title))
        
        # Hàm tạo khối văn bản nằm độc quyền ở cột TRÁI
        def get_text_block(subtitle_str, bullet_lines):
            group = VGroup()
            sub = Text(subtitle_str, font=Theme.FONT_BODY, font_size=28, color=Theme.ACCENT_GOLD, weight="BOLD")
            group.add(sub)
            
            for line in bullet_lines:
                b_text = Text(line, font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL)
                group.add(b_text)
            
            group.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            group.next_to(title, DOWN, aligned_edge=LEFT, buff=0.5)
            group.to_edge(LEFT, buff=0.8) # Ghim chặt lề trái
            group.shift(UP * 0.2)
            return group

        # Hàm tạo Pipeline nằm độc quyền ở cột PHẢI (Thu gọn size để cân đối)
        def get_pipeline(llm_name, rep_name, gen_name, rep_color):
            llm_box = RoundedBox(lines=[llm_name], width=5.2, height=1.0, fill_color=Theme.BOX_FILL_ALT, font_size=18)
            rep_box = RoundedBox(lines=[rep_name], width=4.2, height=0.9, fill_color=Theme.BOX_FILL, stroke_color=rep_color, font_size=16)
            gen_box = RoundedBox(lines=[gen_name], width=4.2, height=0.9, fill_color=Theme.DIM, font_size=16)
            
            # Xếp dọc trục trung tâm cột phải
            boxes = VGroup(llm_box, rep_box, gen_box).arrange(UP, buff=0.6)
            
            arr1 = Arrow(llm_box.get_top(), rep_box.get_bottom(), buff=0.08, color=rep_color, stroke_width=3, tip_length=0.12)
            arr2 = Arrow(rep_box.get_top(), gen_box.get_bottom(), buff=0.08, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.12)
            
            pipeline = VGroup(boxes, arr1, arr2)
            pipeline.set_height(4.2)
            pipeline.to_edge(RIGHT, buff=1.0) # Ghim chặt lề phải
            pipeline.shift(DOWN * 0.4)
            return pipeline

        # =====================================================================
        # GIAI ĐOẠN 1: DISCRETE TOKENS (Chameleon)
        # =====================================================================
        text_1 = get_text_block(
            "Discrete image tokens: Chameleon",
            [
                "- Train the LLM to directly",
                "  predict image tokens",
                "- Decoded with VAE decoder",
                "- Limitation: Hard discretization",
                "  can harm image understanding" # Đã ngắt dòng thủ công để tránh tràn ngang
            ]
        )
        
        pipe_1 = get_pipeline(
            "Mixed Modal Auto-Regressive LM",
            "Discrete Image Tokens [IMG]",
            "Image De-Tokenizer (VAE)",
            Theme.SUCCESS
        )

        self.play(FadeIn(text_1), FadeIn(pipe_1))
        self.next_slide()

        # =====================================================================
        # GIAI ĐOẠN 2: CONTINUOUS IMAGE FEATURES (Emu2 / MetaMorph)
        # =====================================================================
        text_2 = get_text_block(
            "CLIP image feature: Emu2 / MetaMorph",
            [
                "- Use MSE loss to push the LLM",
                "  to output target image features",
                "- Outputs continuous representations",
                "  instead of discrete tokens"
            ]
        )
        
        pipe_2 = get_pipeline(
            "Generative Multimodal Model",
            "Continuous Image Features",
            "Regression Decoder",
            Theme.PRIMARY
        )

        self.play(
            ReplacementTransform(text_1, text_2),
            ReplacementTransform(pipe_1, pipe_2)
        )
        self.next_slide()

        # =====================================================================
        # GIAI ĐOẠN 3: CONTINUOUS TEXT FEATURES (DreamLLM)
        # =====================================================================
        text_3 = get_text_block(
            "CLIP text feature: DreamLLM",
            [
                "- Force the LLM output to align",
                "  with T2I models input space",
                "- Outputs 'Dream Queries'",
                "  (Continuous Text Features)"
            ]
        )
        
        pipe_3 = get_pipeline(
            "Causal Multimodal LLM",
            "Dream Queries (Text Feature)",
            "U-Net (Score Distillation)",
            ManimColor("#8E24AA")
        )

        self.play(
            ReplacementTransform(text_2, text_3),
            ReplacementTransform(pipe_2, pipe_3)
        )
        self.next_slide()

        # =====================================================================
        # GIAI ĐOẠN 4: DENOISED VAE FEATURES (Transfusion)
        # =====================================================================
        text_4 = get_text_block(
            "Denoised VAE features: Transfusion",
            [
                "- Train the LLM to also",
                "  perform image denoising",
                "- Noisy VAE features are not",
                "  good for image understanding"
            ]
        )
        
        transfusion_box = RoundedBox(
            lines=["Transformer", "(Predict + Denoise)"], 
            width=5.5, height=1.0, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_RED, font_size=18
        )
        
        # Tạo chuỗi dữ liệu mini nằm gọn bên cột phải
        in_t1 = Text("cute cat", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL)
        in_img = Square(side_length=0.4, fill_color=Theme.DIM, fill_opacity=0.8, stroke_color=Theme.ACCENT_RED)
        in_t2 = Text("what color?", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL)
        inputs = VGroup(in_t1, in_img, in_t2).arrange(RIGHT, buff=0.4)
        
        out_t1 = Text("<BOI>", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL)
        out_img = Square(side_length=0.4, fill_color=Theme.ACCENT_GOLD, fill_opacity=0.8, stroke_color=Theme.ACCENT_GOLD)
        out_t2 = Text("...", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL)
        outputs = VGroup(out_t1, out_img, out_t2).arrange(RIGHT, buff=0.4)
        
        transfusion_group = VGroup(outputs, transfusion_box, inputs).arrange(DOWN, buff=0.6)
        
        arrs_in = VGroup(*[Arrow(inputs[i].get_top(), transfusion_box.get_bottom(), buff=0.08, stroke_width=2.5, tip_length=0.1) for i in range(3)])
        arrs_out = VGroup(*[Arrow(transfusion_box.get_top(), outputs[i].get_bottom(), buff=0.08, stroke_width=2.5, tip_length=0.1) for i in range(3)])
        
        pipe_4 = VGroup(transfusion_group, arrs_in, arrs_out)
        pipe_4.set_width(5.8)
        pipe_4.to_edge(RIGHT, buff=1.0)
        pipe_4.shift(DOWN * 0.4)

        self.play(
            ReplacementTransform(text_3, text_4),
            FadeOut(pipe_3), FadeIn(pipe_4)
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 23 — MODULE 20: JOINTLY MODELING P(text, pixels)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────
        
class Module20_JointModeling(Slide):
    def construct(self):
        # 1. Cài đặt nền và Tiêu đề an toàn (Tránh Lỗi 1 và khắc phục lỗi tràn viền)
        self.camera.background_color = Theme.BG
        title = slide_title("Jointly modeling P(text, pixels) in one transformer")
        
        # Tự động phát hiện và co nhỏ tiêu đề nếu chiều rộng vượt quá mức an toàn (13.0)
        if title.get_width() > 13.0:
            title.scale_to_fit_width(13.0)
            title.to_corner(UL, buff=0.6) # Căn lề lại về góc sau khi co nhỏ
            
        self.play(Write(title))
        
        # =====================================================================
        # PHÂN CẢNH 1: KIẾN TRÚC TỔNG QUAN (CONCEPT)
        # =====================================================================
        vision_enc = RoundedBox(lines=["Vision Encoder"], width=6.0, height=0.8, fill_color=Theme.PRIMARY)
        unified_tf = RoundedBox(lines=["Unified Transformer (Text & Pixels)"], width=7.5, height=0.9, fill_color=ManimColor("#8E24AA")) # Màu Tím
        gen_head = RoundedBox(lines=["Generation Head"], width=5.0, height=0.8, fill_color=Theme.ACCENT_RED)
        pixel_out = Text("Pixel Output", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        
        boxes_group = VGroup(vision_enc, unified_tf, gen_head, pixel_out).arrange(UP, buff=0.6)
        
        b1 = Text("• Input: ViT features, discrete tokens, or noisy VAE latents.", font=Theme.FONT_BODY, font_size=24)
        b2 = Text("• Generation Head: LM head or Diffusion models.", font=Theme.FONT_BODY, font_size=24)
        b3 = Text("• Aim: Train a unified transformer to model both modalities.", font=Theme.FONT_BODY, font_size=24, color=Theme.SUCCESS)
        bullets_group = VGroup(b1, b2, b3).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        
        # Gói tổng thể và định vị trục duy nhất
        master_group_1 = VGroup(boxes_group, bullets_group).arrange(DOWN, buff=0.8)
        master_group_1.set_height(5.2) 
        master_group_1.next_to(title, DOWN, buff=0.5) 
        
        arr1 = Arrow(vision_enc.get_top(), unified_tf.get_bottom(), buff=0.1)
        arr2 = Arrow(unified_tf.get_top(), gen_head.get_bottom(), buff=0.1)
        arr3 = Arrow(gen_head.get_top(), pixel_out.get_bottom(), buff=0.1)
        arrows_1 = VGroup(arr1, arr2, arr3)
        
        self.play(FadeIn(master_group_1), Create(arrows_1))
        self.next_slide()
        
        # =====================================================================
        # PHÂN CẢNH 2: VPiT vs INFERENCE (CHUYỂN CẢNH)
        # =====================================================================
        self.play(FadeOut(master_group_1), FadeOut(arrows_1))
        
        # --- Helper function tạo các block chuẩn hóa ---
        def make_head(text, color): return RoundedBox(lines=[text, "Head"], width=2.0, height=0.8, fill_color=color)
        def make_enc(text, color): return RoundedBox(lines=[text], width=2.0, height=0.6, fill_color=color)
        
        # --- CỘT TRÁI: VPiT (TRAINING) ---
        vpit_title = Text("VPiT (Training)", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL, weight="BOLD")
        
        t_icon_v = make_enc("Text Input", Theme.ACCENT_RED)
        v_enc_v = make_enc("Vision Enc", Theme.PRIMARY)
        v_adap_v = make_enc("Adapter", Theme.PRIMARY)
        v_stack_v = VGroup(v_adap_v, v_enc_v).arrange(DOWN, buff=0.1)
        inputs_v = VGroup(t_icon_v, v_stack_v).arrange(RIGHT, aligned_edge=DOWN, buff=0.4)
        
        ar_model_v = RoundedBox(lines=["Autoregressive Model"], width=4.5, height=1.0, fill_color=ManimColor("#8E24AA"))
        heads_v = VGroup(make_head("Text", Theme.ACCENT_RED), make_head("Vision", Theme.PRIMARY)).arrange(RIGHT, buff=0.2)
        
        vpit_core = VGroup(inputs_v, ar_model_v, heads_v).arrange(UP, buff=0.5)
        vpit_col = VGroup(vpit_title, vpit_core).arrange(DOWN, buff=0.5)
        
        # --- CỘT PHẢI: INFERENCE ---
        inf_title = Text("Inference", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL, weight="BOLD")
        
        t_icon_i = make_enc("Text Input", Theme.ACCENT_RED)
        v_enc_i = make_enc("Vision Enc", Theme.PRIMARY)
        v_adap_i = make_enc("Adapter", Theme.PRIMARY)
        v_stack_i = VGroup(v_adap_i, v_enc_i).arrange(DOWN, buff=0.1)
        inputs_i = VGroup(t_icon_i, v_stack_i).arrange(RIGHT, aligned_edge=DOWN, buff=0.4)
        
        ar_model_i = RoundedBox(lines=["Autoregressive Model"], width=4.5, height=1.0, fill_color=ManimColor("#8E24AA"))
        t_head_i = make_head("Text", Theme.ACCENT_RED)
        v_head_i = make_head("Vision", Theme.PRIMARY)
        heads_i = VGroup(t_head_i, v_head_i).arrange(RIGHT, buff=0.2)
        
        inf_core = VGroup(inputs_i, ar_model_i, heads_i).arrange(UP, buff=0.5)
        
        # Các khối bổ sung cho Inference (Projector + Diffusion)
        proj = RoundedBox(lines=["Projector"], width=2.4, height=0.6, fill_color=ManimColor("#673AB7"))
        diff = RoundedBox(lines=["Adapted", "Diffusion Model"], width=2.4, height=1.2, fill_color=ManimColor("#673AB7"))
        extra_inf = VGroup(diff, proj).arrange(DOWN, buff=0.3)
        extra_inf.next_to(heads_i, RIGHT, buff=0.6) # Neo an toàn bên phải cụm Heads
        
        inf_content = VGroup(inf_core, extra_inf) # Gói ngang
        inf_col = VGroup(inf_title, inf_content).arrange(DOWN, buff=0.5) # Gói dọc
        
        # --- GÓI TỔNG THỂ & CĂN CHỈNH ---
        separator = DashedLine(UP*3, DOWN*3, color=Theme.DIM)
        master_group_2 = VGroup(vpit_col, separator, inf_col).arrange(RIGHT, buff=0.8)
        
        # Ép kích thước an toàn và neo dưới Title (Tránh Lỗi 3 & Lỗi 5)
        master_group_2.set_height(5.5)
        master_group_2.set_max_width(13.5)
        master_group_2.next_to(title, DOWN, buff=0.4)
        
        # --- VẼ MŨI TÊN (Chỉ vẽ sau khi tọa độ đã chốt) ---
        arrs_2 = VGroup()
        
        # Mũi tên VPiT
        arrs_2.add(Arrow(t_icon_v.get_top(), ar_model_v.get_bottom(), buff=0.1, color=Theme.ACCENT_RED))
        arrs_2.add(Arrow(v_stack_v.get_top(), ar_model_v.get_bottom(), buff=0.1, color=Theme.PRIMARY))
        arrs_2.add(Arrow(ar_model_v.get_top(), heads_v[0].get_bottom(), buff=0.1, color=Theme.ACCENT_RED))
        arrs_2.add(Arrow(ar_model_v.get_top(), heads_v[1].get_bottom(), buff=0.1, color=Theme.PRIMARY))
        
        # Mũi tên Inference
        arrs_2.add(Arrow(t_icon_i.get_top(), ar_model_i.get_bottom(), buff=0.1, color=Theme.ACCENT_RED))
        arrs_2.add(Arrow(v_stack_i.get_top(), ar_model_i.get_bottom(), buff=0.1, color=Theme.PRIMARY))
        arrs_2.add(Arrow(ar_model_i.get_top(), t_head_i.get_bottom(), buff=0.1, color=Theme.ACCENT_RED))
        arrs_2.add(Arrow(ar_model_i.get_top(), v_head_i.get_bottom(), buff=0.1, color=Theme.PRIMARY))
        
        # Mũi tên đặc biệt (Dashed line) từ Vision Head sang Projector
        path_proj = DashedLine(v_head_i.get_right(), proj.get_left(), buff=0.1, color=Theme.NEUTRAL).add_tip(tip_length=0.15)
        path_diff = Arrow(proj.get_top(), diff.get_bottom(), buff=0.1, color=Theme.NEUTRAL)
        arrs_2.add(path_proj, path_diff)
        
        # Render
        self.play(FadeIn(master_group_2))
        self.play(Create(arrs_2))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 24 — MODULE 21: TRAINING RECIPE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import DashedVMobject, DashedLine

class Module21_TrainingRecipe(Slide):
    def construct(self):
        # 1. Cài đặt nền và Tiêu đề (Đã bỏ "Module21: " và thêm bảo vệ tràn viền)
        self.camera.background_color = Theme.BG
        title = slide_title("Training Recipe (Joint Understanding & Generation)")
        if title.width > 13.0:
            title.set_width(13.0)
        title.to_corner(UL, buff=0.6)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG 3 CỘT CHỨC NĂNG CHÍNH
        # ─────────────────────────────────────────────────────────────────────
        
        # --- CỘT 1: UNDERSTANDING ---
        und_in = RoundedBox(lines=["Multimodal Input", "(Image/Text)"], width=3.2, height=0.8, fill_color=Theme.BOX_FILL)
        und_mllm = RoundedBox(lines=["Shared MLLM", "[Frozen]"], width=3.2, height=1.0, fill_color=Theme.DIM, stroke_color=Theme.PRIMARY)
        und_out = RoundedBox(lines=["Understanding", "Output Tokens"], width=3.2, height=0.8, fill_color=Theme.BOX_FILL, stroke_color=Theme.PRIMARY)
        
        col_und = VGroup(und_in, und_mllm, und_out).arrange(UP, buff=0.8)
        
        # --- CỘT 2: GENERATION (Lõi MLLM) ---
        gen_in = RoundedBox(lines=["MetaQueries", "[Tunable]"], width=3.2, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_RED)
        gen_mllm = RoundedBox(lines=["Shared MLLM", "[Frozen]"], width=3.2, height=1.0, fill_color=Theme.DIM, stroke_color=Theme.PRIMARY)
        gen_conn = RoundedBox(lines=["Connector", "[Tunable]"], width=3.2, height=0.8, fill_color=Theme.ACCENT_RED)
        
        col_gen = VGroup(gen_in, gen_mllm, gen_conn).arrange(UP, buff=0.8)
        
        # --- CỘT 3: GENERATION (Luồng Diffusion) ---
        diff_in = RoundedBox(lines=["Noisy Input"], width=3.2, height=0.8, fill_color=Theme.BOX_FILL)
        
        diff_b1 = RoundedBox(lines=["Diffusion Block", "[Tunable]"], width=3.2, height=0.5, fill_color=ManimColor("#4A148C"))
        diff_b2 = RoundedBox(lines=["Diffusion Block", "[Tunable]"], width=3.2, height=0.5, fill_color=ManimColor("#4A148C"))
        diff_stack = VGroup(diff_b1, diff_b2).arrange(UP, buff=0.15)
        
        diff_out = RoundedBox(lines=["Denoising", "Objective"], width=3.2, height=0.8, fill_color=Theme.BOX_FILL, stroke_color=Theme.SUCCESS)
        
        col_diff = VGroup(diff_in, diff_stack, diff_out).arrange(UP, buff=0.65)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM NHÓM, CĂN CHỈNH VÀ ĐÓNG GÓI TOÀN CỤC (TRÁNH LỖI 5)
        # ─────────────────────────────────────────────────────────────────────
        # Gom các cột nằm ngang, neo bằng cạnh đáy (DOWN)
        all_cols = VGroup(col_und, col_gen, col_diff).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)
        all_cols.set_height(4.2)
        
        # Hợp nhất khối Shared MLLM bằng một background mờ chạy ngang 2 cột
        mllm_bg = RoundedRectangle(
            width=und_mllm.width + gen_mllm.width + 0.9, 
            height=und_mllm.height + 0.2,
            corner_radius=0.1,
            fill_color=Theme.DIM,
            fill_opacity=0.3,
            stroke_width=0
        ).move_to(VGroup(und_mllm, gen_mllm).get_center())
        
        mllm_label = Text("Single Unified Transformer Architecture", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL)
        mllm_label.move_to(mllm_bg.get_center())
        
        # Ẩn nhãn chữ thừa bên trong
        und_mllm[1].set_opacity(0)
        gen_mllm[1].set_opacity(0)
        
        # Khung Dashed bao quanh Understanding & Generation Zone
        frame_und = DashedVMobject(
            Rectangle(
                width=col_und.width + 0.6,
                height=col_und.height + 0.8,
                color=Theme.PRIMARY,
                stroke_width=2
            ),
            num_dashes=24
        ).move_to(col_und.get_center())
        title_und = Text("Understanding", font=Theme.FONT_BODY, font_size=20, color=Theme.PRIMARY).next_to(frame_und, UP, buff=0.15)
        
        frame_gen = DashedVMobject(
            Rectangle(
                width=col_gen.width + col_diff.width + 1.5,
                height=col_gen.height + 0.8,
                color=Theme.ACCENT_RED,
                stroke_width=2
            ),
            num_dashes=40
        ).move_to(VGroup(col_gen, col_diff).get_center())
        title_gen = Text("Generation", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED).next_to(frame_gen, UP, buff=0.15)
        
        # Gói toàn bộ sơ đồ thành một thực thể duy nhất
        master_diagram = VGroup(
            all_cols, mllm_bg, mllm_label, 
            frame_und, title_und, 
            frame_gen, title_gen
        )
        
        # Căn giữa sơ đồ tuyệt đối trên màn hình theo trục ngang, dịch nhẹ trục dọc để chừa chỗ cho Title và Footer
        master_diagram.center()
        master_diagram.shift(DOWN * 0.1)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: VẼ MŨI TÊN KẾT NỐI (Chỉ vẽ sau khi sơ đồ đã cố định vị trí)
        # ─────────────────────────────────────────────────────────────────────
        arrs = VGroup()
        arrs.add(Arrow(und_in.get_top(), und_mllm.get_bottom(), buff=0.1, color=Theme.NEUTRAL))
        arrs.add(Arrow(und_mllm.get_top(), und_out.get_bottom(), buff=0.1, color=Theme.PRIMARY))
        
        arrs.add(Arrow(gen_in.get_top(), gen_mllm.get_bottom(), buff=0.1, color=Theme.ACCENT_RED))
        arrs.add(Arrow(gen_mllm.get_top(), gen_conn.get_bottom(), buff=0.1, color=Theme.ACCENT_RED))
        
        arrs.add(Arrow(diff_in.get_top(), diff_stack.get_bottom(), buff=0.1, color=Theme.NEUTRAL))
        arrs.add(Arrow(diff_stack.get_top(), diff_out.get_bottom(), buff=0.1, color=Theme.SUCCESS))
        
        arr_cond_1 = Arrow(gen_conn.get_right(), diff_b1.get_left(), buff=0.1, color=Theme.ACCENT_RED, stroke_width=3, tip_length=0.15)
        arr_cond_2 = Arrow(gen_conn.get_right(), diff_b2.get_left(), buff=0.1, color=Theme.ACCENT_RED, stroke_width=3, tip_length=0.15)
        arrs.add(arr_cond_1, arr_cond_2)
        
        summary = Text(
            "Frozen MLLM processes all inputs. Tunable MetaQueries & Connector adapt it specifically for generation.",
            font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL
        ).to_edge(DOWN, buff=0.4)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        self.next_slide()
        
        self.play(FadeIn(mllm_bg), FadeIn(und_mllm[0]), FadeIn(gen_mllm[0]), Write(mllm_label))
        self.next_slide()
        
        self.play(Create(frame_und), Write(title_und))
        self.play(FadeIn(und_in))
        self.play(Create(arrs[0]), Create(arrs[1]), FadeIn(und_out))
        self.next_slide()
        
        self.play(Create(frame_gen), Write(title_gen))
        self.play(FadeIn(gen_in))
        self.play(Create(arrs[2]), Create(arrs[3]), FadeIn(gen_conn))
        self.next_slide()
        
        self.play(FadeIn(diff_in))
        self.play(Create(arrs[4]), FadeIn(diff_stack))
        self.next_slide()
        
        self.play(Create(arr_cond_1), Create(arr_cond_2))
        self.next_slide()
        
        self.play(Create(arrs[5]), FadeIn(diff_out))
        self.play(FadeIn(summary))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 25 — MODULE 22: VISUAL FEATURE GENERATION PARADIGMS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module22_FeatureGeneration(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG
        
        # 1. TIÊU ĐỀ (Chuẩn bị 3 state cho 3 slide)
        title1 = slide_title("Regress CLIP feature (MetaMorph)")
        title2 = slide_title("Denoise VAE Feature (MetaQuery)")
        title3 = slide_title("Denoise CLIP Feature (BLIP3-o)")
        
        # 2. CHÚ GIẢI (LEGEND) TỪ KHÓA
        # Dùng mã màu Cam sáng cho Prompt (Input) và Đỏ Cam cho Visual Feature (Output) giống ảnh gốc
        leg_pill1 = RoundedRectangle(width=0.9, height=0.25, corner_radius=0.12, fill_color=ManimColor("#F57C00"), stroke_width=0)
        leg_text1 = Text("Prompt", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        leg1 = VGroup(leg_pill1, leg_text1).arrange(RIGHT, buff=0.2)

        leg_pill2 = RoundedRectangle(width=0.9, height=0.25, corner_radius=0.12, fill_color=ManimColor("#D84315"), stroke_width=0)
        leg_text2 = Text("Visual Feature", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        leg2 = VGroup(leg_pill2, leg_text2).arrange(RIGHT, buff=0.2)

        legend = VGroup(leg1, leg2).arrange(RIGHT, buff=1.0)
        legend.next_to(title1, DOWN, buff=0.3)
        legend.set_x(0) # Khắc phục triệt để lỗi lệch tâm X (Căn giữa ngang màn hình)
        
        # 3. BUILDER: HÀM TẠO LÕI AR MODEL
        def make_ar_base():
            ar = RoundedBox(
                lines=["Autoregressive", "Model"], 
                width=3.4, height=1.0, 
                fill_color=ManimColor("#1565C0"), # Màu xanh dương
                stroke_color=Theme.PRIMARY
            )
            # Hai pill (Token) trên đỉnh khối AR
            pill1 = RoundedRectangle(width=0.9, height=0.25, corner_radius=0.12, fill_color=ManimColor("#F57C00"), stroke_width=0)
            pill2 = RoundedRectangle(width=0.9, height=0.25, corner_radius=0.12, fill_color=ManimColor("#D84315"), stroke_width=0)
            pills = VGroup(pill1, pill2).arrange(RIGHT, buff=0.3)
            pills.next_to(ar, UP, buff=-0.1) # Cố ý cho lẹm một chút xuống viền AR
            return VGroup(ar, pills)
            
        base_a = make_ar_base()
        base_c = make_ar_base()
        base_b = make_ar_base()
        
        # Arrange các base theo đúng thứ tự bản vẽ: (a) trái, (c) giữa, (b) phải
        bases = VGroup(base_a, base_c, base_b).arrange(RIGHT, buff=0.9)
        
        # 4. BUILDER: HÀM TẠO CỘT KIẾN TRÚC THEO TRỤC DỌC TỰ ĐỘNG
        def build_upper(base, target_name, loss_name, has_diffusion, label_name):
            # Nhãn phụ dưới cùng
            label = Text(label_name, font=Theme.FONT_BODY, font_size=20, color=Theme.DIM)
            label.next_to(base, DOWN, buff=0.4)
            
            # ĐIỂM NEO QUAN TRỌNG: Mọi luồng dữ liệu đều bắn thẳng lên từ pill thứ 2 (Visual Feature)
            arr_start = base[1][1] 
            
            # Hàm mất mát (Loss Text)
            loss = Text(loss_name, font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
            # Dùng next_to với UP buff lớn để đẩy hàm mất mát tít lên cao (Tạo thành 1 đường lưới ngang vô hình)
            loss.next_to(arr_start, UP, buff=2.6) 
            loss.set_x(arr_start.get_x()) # Căn thẳng tắp theo tọa độ X của pill 2
            
            # Khối Target Input (CLIP/VAE)
            target = RoundedBox(
                lines=[target_name], width=1.5, height=0.6, 
                fill_color=ManimColor("#311B92"), # Tím đậm
                stroke_color=ManimColor("#6A1B9A")
            )
            target.next_to(loss, LEFT, buff=0.6)
            
            # Mũi tên từ Target đâm ngang vào Loss
            arr_top = Arrow(target.get_right(), loss.get_left(), buff=0.1, color=Theme.DIM, tip_length=0.15)
            
            col = VGroup(base, label, loss, target, arr_top)
            
            if has_diffusion:
                diff = RoundedBox(
                    lines=["Diffusion", "Transformer"], width=2.4, height=0.8, 
                    fill_color=ManimColor("#6A1B9A"), # Tím sáng
                    stroke_color=ManimColor("#8E24AA")
                )
                diff.next_to(arr_start, UP, buff=0.8)
                diff.set_x(arr_start.get_x()) # Căn thẳng tắp theo pill 2
                
                arr1 = Arrow(arr_start.get_top(), diff.get_bottom(), buff=0.1, color=Theme.DIM, tip_length=0.15)
                arr2 = Arrow(diff.get_top(), loss.get_bottom(), buff=0.1, color=Theme.DIM, tip_length=0.15)
                col.add(diff, arr1, arr2)
            else:
                arr1 = Arrow(arr_start.get_top(), loss.get_bottom(), buff=0.1, color=Theme.DIM, tip_length=0.15)
                col.add(arr1)
                
            return col

        # Khởi tạo 3 luồng
        col_a = build_upper(base_a, "CLIP", "MSE", False, "(a) CLIP + MSE")
        col_c = build_upper(base_c, "VAE", "Flow\nMatching", True, "(c) VAE + Flow Matching")
        col_b = build_upper(base_b, "CLIP", "Flow\nMatching", True, "(b) CLIP + Flow Matching")
        
        # Đóng gói và giới hạn an toàn
        master_group = VGroup(col_a, col_c, col_b)
        master_group.set_height(5.0) # Ép giới hạn Y-axis chống Lỗi 3 & Lỗi 4
        master_group.next_to(legend, DOWN, buff=0.5)
        master_group.set_x(0) # Tái căn ngang chống Lỗi lệch theo Title
        
        # 5. KỊCH BẢN HIỂN THỊ (ANIMATION)
        # Bắt đầu với Slide 1 (Làm nổi bật Cột A)
        col_c.set_opacity(0.3)
        col_b.set_opacity(0.3)
        
        self.play(Write(title1))
        self.play(FadeIn(legend), FadeIn(master_group))
        self.next_slide()
        
        # Slide 2: Chuyển focus sang Cột C
        self.play(
            Transform(title1, title2),
            col_a.animate.set_opacity(0.3),
            col_c.animate.set_opacity(1.0)
        )
        self.next_slide()
        
        # Slide 3: Chuyển focus sang Cột B
        self.play(
            Transform(title1, title3),
            col_c.animate.set_opacity(0.3),
            col_b.animate.set_opacity(1.0)
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 26 — MODULE 23: K-SPARSE AUTOENCODERS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module23_KSparseAutoencoders(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề slide (Góc trên bên trái)
        title = slide_title("K-sparse autoencoders")
        
        # 2. Bảng mục tiêu (Goal Banner) - Neo ngay dưới tiêu đề
        goal_bg = RoundedRectangle(
            corner_radius=0.1, 
            width=13.0, 
            height=0.8, 
            fill_color=ManimColor("#E5EED0"), # Màu xanh nhạt theo ảnh gốc
            fill_opacity=1, 
            stroke_width=0
        )
        goal_text = Text(
            "Goal: Study the semantic information captured in diffusion models.", 
            font=Theme.FONT_BODY, 
            font_size=26, 
            color=Theme.BOX_FILL_ALT, 
            slant="ITALIC",
            weight="BOLD"
        )
        goal_text.move_to(goal_bg.get_center())
        goal_banner = VGroup(goal_bg, goal_text)
        goal_banner.next_to(title, DOWN, buff=0.4, aligned_edge=LEFT)

        # ─────────────────────────────────────────────────────────────────────
        # HÀM HỖ TRỢ VẼ KIẾN TRÚC MẠNG
        # ─────────────────────────────────────────────────────────────────────
        
        def build_network_polygon(label_text: str, is_encoder: bool = True) -> VGroup:
            """Tạo hình thang đại diện cho Encoder/Decoder"""
            w = 1.0
            h_tall = 2.6
            h_short = 1.2
            
            if is_encoder:
                points = [[-w/2, h_tall/2, 0], [w/2, h_short/2, 0], [w/2, -h_short/2, 0], [-w/2, -h_tall/2, 0]]
                angle = PI/2 # Chữ dọc từ dưới lên
            else:
                points = [[-w/2, h_short/2, 0], [w/2, h_tall/2, 0], [w/2, -h_tall/2, 0], [-w/2, -h_short/2, 0]]
                angle = -PI/2 # Chữ dọc từ trên xuống
                
            poly = Polygon(
                *points, 
                fill_color=ManimColor("#A3C4ED"), 
                fill_opacity=0.9, 
                stroke_color=Theme.PRIMARY, 
                stroke_width=2
            )
            label = Text(
                label_text, font=Theme.FONT_BODY, font_size=22, color=Theme.BOX_FILL_ALT, weight="BOLD"
            ).rotate(angle)
            label.move_to(poly.get_center())
            
            return VGroup(poly, label)

        def build_latent_blocks(colors: list[str]) -> VGroup:
            """Tạo cột các khối vuông đại diện cho Feature Space"""
            blocks = VGroup(*[
                Square(
                    side_length=0.4, 
                    fill_color=ManimColor(c), 
                    fill_opacity=1, 
                    stroke_color=Theme.BOX_FILL_ALT, 
                    stroke_width=1.5
                ) for c in colors
            ]).arrange(DOWN, buff=0.04)
            return blocks

        # ─────────────────────────────────────────────────────────────────────
        # THIẾT LẬP HAI SƠ ĐỒ
        # ─────────────────────────────────────────────────────────────────────
        
        # --- BÊN TRÁI: Undercomplete (4 blocks) ---
        colors_under = ["#E07A5F", "#F4F1DE", "#3D405B", "#81B29A"]
        enc_L = build_network_polygon("Encoder", is_encoder=True)
        lat_L = build_latent_blocks(colors_under)
        dec_L = build_network_polygon("Decoder", is_encoder=False)
        
        diagram_L = VGroup(enc_L, lat_L, dec_L).arrange(RIGHT, buff=0.4)
        
        label_L = Text("Undercomplete feature space", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)

        # --- BÊN PHẢI: Overcomplete (8 blocks) ---
        colors_over = ["#0077B6", "#FFFFFF", "#F4A261", "#2A9D8F", "#E9C46A", "#00FF00", "#A44A3F", "#FFB5A7"]
        enc_R = build_network_polygon("Encoder", is_encoder=True)
        lat_R = build_latent_blocks(colors_over)
        dec_R = build_network_polygon("Decoder", is_encoder=False)
        
        diagram_R = VGroup(enc_R, lat_R, dec_R).arrange(RIGHT, buff=0.4)
        
        # Tách chữ Overcomplete để vẽ hình elip vòng quanh
        lbl_over_kw = Text("Overcomplete", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        lbl_over_rem = Text("feature space", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        label_R_group = VGroup(lbl_over_kw, lbl_over_rem).arrange(RIGHT, buff=0.15)
        
        # Ellipse đỏ khoanh vùng từ khóa
        highlight_ellipse = Ellipse(
            width=lbl_over_kw.width + 0.5, 
            height=lbl_over_kw.height + 0.4, 
            color=Theme.ACCENT_RED, 
            stroke_width=3
        )
        highlight_ellipse.move_to(lbl_over_kw.get_center())
        
        # ─────────────────────────────────────────────────────────────────────
        # BỐ CỤC VÀ ĐỊNH VỊ AN TOÀN (SAFE LAYOUT)
        # ─────────────────────────────────────────────────────────────────────
        
        # Xếp 2 mạng song song ngang
        diagrams_core = VGroup(diagram_L, diagram_R).arrange(RIGHT, buff=1.8)
        
        # Đặt Label cách đều lên trên sơ đồ
        label_R_group.next_to(diagram_R, UP, buff=0.4)
        label_L.next_to(diagram_L, UP, buff=0.4)
        # Bắt buộc 2 label thẳng hàng dọc ngang dẫu bên phải có cột latent cao hơn
        label_L.match_y(label_R_group)
        
        highlight_ellipse.move_to(lbl_over_kw.get_center()) # Cập nhật tọa độ elip sau match_y
        
        # Đóng gói TẤT CẢ vào 1 group để scale an toàn
        all_content = VGroup(diagrams_core, label_L, label_R_group, highlight_ellipse)
        all_content.set_height(4.8) # Giới hạn chống tràn Y-axis
        
        # Neo toàn bộ cục diện xuống dưới Goal banner (Tuyệt đối không dùng shift tự do)
        all_content.next_to(goal_banner, DOWN, buff=0.8)
        all_content.set_x(0) # Căn giữa hoàn hảo trên màn hình

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.play(FadeIn(goal_bg), Write(goal_text))
        self.next_slide()
        
        # Hiện sơ đồ Undercomplete
        self.play(FadeIn(label_L))
        self.play(FadeIn(enc_L), FadeIn(dec_L))
        self.play(Create(lat_L), run_time=1.5)
        self.next_slide()
        
        # Hiện sơ đồ Overcomplete
        self.play(FadeIn(label_R_group))
        self.play(FadeIn(enc_R), FadeIn(dec_R))
        self.play(Create(lat_R), run_time=2.0)
        self.next_slide()
        
        # Đóng khung làm nổi bật "Overcomplete"
        self.play(Create(highlight_ellipse), run_time=0.8)
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 27 — MODULE 24: FEATURE EXTRACTION IN SAE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module24_FeatureExtraction(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề slide (Ghi nhớ ghim sát góc UL)
        title = slide_title("Monosemantic Feature Extraction")
        
        # ─────────────────────────────────────────────────────────────────────
        # HÀM HỖ TRỢ VẼ KHỐI (BLOCKS & POLYGONS)
        # ─────────────────────────────────────────────────────────────────────
        
        def build_block_row(colors: list[str]) -> VGroup:
            """Tạo một hàng các khối vuông nhỏ đại diện cho vector"""
            blocks = VGroup(*[
                Square(
                    side_length=0.45, 
                    fill_color=ManimColor(c), 
                    fill_opacity=1, 
                    stroke_color=Theme.NEUTRAL, 
                    stroke_width=1.5
                ) for c in colors
            ]).arrange(RIGHT, buff=0.08)
            return blocks

        def build_trapezoid(label_text: str, is_encoder: bool = True) -> VGroup:
            """Tạo hình thang cho Encoder/Decoder"""
            w_wide, w_narrow = 4.0, 1.8
            h = 1.2
            
            if is_encoder:
                points = [[-w_wide/2, h/2, 0], [w_wide/2, h/2, 0], [w_narrow/2, -h/2, 0], [-w_narrow/2, -h/2, 0]]
            else:
                points = [[-w_narrow/2, h/2, 0], [w_narrow/2, h/2, 0], [w_wide/2, -h/2, 0], [-w_wide/2, -h/2, 0]]
                
            poly = Polygon(
                *points, 
                fill_color=ManimColor("#A3C4ED"), # Màu xanh lam nhạt
                fill_opacity=0.9, 
                stroke_color=Theme.PRIMARY, 
                stroke_width=2
            )
            label = Text(label_text, font=Theme.FONT_BODY, font_size=28, color=Theme.BOX_FILL_ALT, weight="BOLD")
            label.move_to(poly.get_center())
            return VGroup(poly, label)

        def build_concept_grid(concept_name: str, base_color: str, highlight_color: str) -> VGroup:
            """Lưới khái niệm (Concept Grid) sinh bằng code thay thế ảnh gốc"""
            grid = VGroup(*[
                Square(side_length=0.7, fill_color=ManimColor(c), fill_opacity=0.9, stroke_width=1)
                for c in [base_color, highlight_color, highlight_color, base_color]
            ]).arrange_in_grid(rows=2, cols=2, buff=0.02)
            
            lbl = Text(f"Concept: {concept_name}", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL, weight="BOLD")
            lbl.next_to(grid, UP, buff=0.15)
            
            frame = Rectangle(
                width=grid.width + 0.3, height=grid.height + 0.8, 
                color=ManimColor(highlight_color), stroke_width=3
            )
            frame.move_to(VGroup(grid, lbl).get_center())
            return VGroup(frame, grid, lbl)

        # ─────────────────────────────────────────────────────────────────────
        # XÂY DỰNG TRỤC CHÍNH (CENTRAL SPINE)
        # ─────────────────────────────────────────────────────────────────────
        
        # Bảng màu đại diện
        poly_colors = ["#E07A5F", "#3D405B", "#81B29A", "#F2CC8F", "#E07A5F"]
        latent_colors = [Theme.BOX_FILL_ALT]*8
        latent_colors[3] = "#81B29A" # Active block 1 (Green)
        latent_colors[7] = "#E07A5F" # Active block 2 (Red)

        # 1. Input Box
        input_blocks = build_block_row(poly_colors)
        input_frame = RoundedRectangle(width=input_blocks.width+0.5, height=input_blocks.height+0.4, corner_radius=0.1, color=Theme.NEUTRAL)
        input_grp = VGroup(input_frame, input_blocks.move_to(input_frame.get_center()))

        # 2. Encoder
        enc_grp = build_trapezoid("Encoder", is_encoder=True)

        # 3. Latent Box (Màu cam nổi bật)
        latent_blocks = build_block_row(latent_colors)
        latent_frame = RoundedRectangle(width=latent_blocks.width+0.5, height=latent_blocks.height+0.4, corner_radius=0.1, color=Theme.ACCENT_GOLD)
        latent_grp = VGroup(latent_frame, latent_blocks.move_to(latent_frame.get_center()))

        # 4. Decoder
        dec_grp = build_trapezoid("Decoder", is_encoder=False)

        # 5. Output Box
        output_blocks = build_block_row(poly_colors)
        output_frame = RoundedRectangle(width=output_blocks.width+0.5, height=output_blocks.height+0.4, corner_radius=0.1, color=Theme.NEUTRAL)
        output_grp = VGroup(output_frame, output_blocks.move_to(output_frame.get_center()))

        # Thu gọn buff từ 0.4 xuống 0.25 để sơ đồ cô đọng hơn
        spine = VGroup(input_grp, enc_grp, latent_grp, dec_grp, output_grp).arrange(DOWN, buff=0.25)

        # ─────────────────────────────────────────────────────────────────────
        # NHÃN VĂN BẢN VÀ CÁC KHÁI NIỆM BÊN LỀ (SIDE CONCEPTS)
        # ─────────────────────────────────────────────────────────────────────
        
        # Nhãn cho trục
        lbl_diff = Text("(diffusion features)", font=Theme.FONT_BODY, font_size=20, color=Theme.SUCCESS)
        lbl_in_poly = Text("Input (poly semantic)", font=Theme.FONT_BODY, font_size=20, t2c={"poly": Theme.PRIMARY})
        lbl_mono = Text("(mono semantic)", font=Theme.FONT_BODY, font_size=22, t2c={"mono": Theme.ACCENT_GOLD})
        lbl_out_poly = Text("Output (poly semantic)", font=Theme.FONT_BODY, font_size=20, t2c={"poly": Theme.PRIMARY})

        lbl_diff.next_to(input_grp, LEFT, buff=0.4)
        lbl_in_poly.next_to(input_grp, RIGHT, buff=0.4)
        lbl_mono.next_to(latent_grp, RIGHT, buff=0.4)
        lbl_out_poly.next_to(output_grp, RIGHT, buff=0.4)
        spine_labels = VGroup(lbl_diff, lbl_in_poly, lbl_mono, lbl_out_poly)

        # Hộp khái niệm thay cho ảnh Chó/Mèo
        concept_left = build_concept_grid("Forest", "#2D6A4F", "#74C69D") # Tone Xanh lá
        concept_right = build_concept_grid("Desert", "#D4A373", "#FAEDCD") # Tone Đất/Cát

        # Định vị an toàn bằng match_y
        concept_left.next_to(spine, LEFT, buff=0.8)
        concept_left.match_y(dec_grp) # Hạ hộp trái ngang hàng Decoder

        concept_right.next_to(spine, RIGHT, buff=0.8)
        concept_right.match_y(enc_grp) # Nâng hộp phải ngang hàng Encoder

        # ─────────────────────────────────────────────────────────────────────
        # GOM NHÓM VÀ CĂN CHỈNH TRỤC DỌC TRÁNH ĐÈ TIÊU ĐỀ
        # ─────────────────────────────────────────────────────────────────────
        
        all_layout = VGroup(spine, spine_labels, concept_left, concept_right)
        all_layout.set_height(4.4) # Thu nhỏ chiều cao tổng thể xuống 4.4 để tạo vùng đệm an toàn với tiêu đề
        
        # Đẩy sơ đồ xuống dưới tiêu đề 0.5 đơn vị, sau đó căn giữa trục ngang màn hình
        all_layout.next_to(title, DOWN, buff=0.5)
        all_layout.set_x(0)

        # ─────────────────────────────────────────────────────────────────────
        # VẼ MŨI TÊN (Chỉ vẽ SAU KHI toàn bộ tọa độ đã được scale cố định)
        # ─────────────────────────────────────────────────────────────────────
        
        spine_arrows = VGroup()
        for i in range(len(spine) - 1):
            arrow = Arrow(
                spine[i].get_bottom(), 
                spine[i+1].get_top(), 
                buff=0.06, stroke_width=4, tip_length=0.15, color=Theme.NEUTRAL
            )
            spine_arrows.add(arrow)

        # Mũi tên trích xuất đặc trưng
        source_green = latent_blocks[3]
        arrow_to_forest = Arrow(
            source_green.get_bottom(), 
            concept_left.get_top() + RIGHT * 0.4, 
            buff=0.08, color="#74C69D", stroke_width=3, tip_length=0.15
        )

        source_orange = latent_blocks[7]
        arrow_to_desert = Arrow(
            source_orange.get_top(), 
            concept_right.get_bottom() + LEFT * 0.4, 
            buff=0.08, color="#E07A5F", stroke_width=3, tip_length=0.15
        )

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        
        # 1. Hiện khối Input và nhãn
        self.play(FadeIn(input_grp), FadeIn(lbl_diff), FadeIn(lbl_in_poly))
        self.next_slide()

        # 2. Hiện toàn bộ trục chính xuống tới Output
        self.play(
            FadeIn(enc_grp), FadeIn(spine_arrows[0]),
            FadeIn(latent_grp), FadeIn(spine_arrows[1]), FadeIn(lbl_mono)
        )
        self.play(
            FadeIn(dec_grp), FadeIn(spine_arrows[2]),
            FadeIn(output_grp), FadeIn(spine_arrows[3]), FadeIn(lbl_out_poly)
        )
        self.next_slide()

        # 3. Trích xuất đặc trưng 1 (Forest)
        self.play(Indicate(source_green, color=WHITE, scale_factor=1.5))
        self.play(Create(arrow_to_forest))
        self.play(FadeIn(concept_left))
        self.next_slide()

        # 4. Trích xuất đặc trưng 2 (Desert)
        self.play(Indicate(source_orange, color=WHITE, scale_factor=1.5))
        self.play(Create(arrow_to_desert))
        self.play(FadeIn(concept_right))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 28 — MODULE 25: IMPROVING DOMAIN GENERALIZATION  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import DashedVMobject

class Module25_DomainGen(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề slide
        title = slide_title("Improving Domain Generalization")
        
        # 2. BANNER DỌC (Sửa lỗi overlap bằng sơ đồ khối dọc: Interpretability -> Better Algorithms)
        v_top_text = Text("Interpretability", font=Theme.FONT_BODY, font_size=16, color=ManimColor("#224DBA"), weight="BOLD")
        v_arrow = Arrow(UP * 0.15, DOWN * 0.15, buff=0, stroke_width=3, color=ManimColor("#224DBA"), tip_length=0.1)
        v_bot_text = Text("Better Algorithms", font=Theme.FONT_BODY, font_size=16, color=ManimColor("#224DBA"), weight="BOLD")
        
        # Sắp xếp các thành phần của banner theo chiều dọc
        v_flow = VGroup(v_top_text, v_arrow, v_bot_text).arrange(DOWN, buff=0.1)
        
        # Hộp nền bo góc dọc gọn gàng
        v_banner_bg = RoundedRectangle(
            width=v_flow.width + 0.4,
            height=v_flow.height + 0.3,
            corner_radius=0.15,
            fill_color=ManimColor("#E6EDFD"),
            fill_opacity=1,
            stroke_width=0
        )
        v_flow.move_to(v_banner_bg.get_center())
        v_banner = VGroup(v_banner_bg, v_flow).to_corner(UR, buff=0.4)

        # ─────────────────────────────────────────────────────────────────────
        # HÀM HỖ TRỢ VẼ CLUSTER (KHÔNG GIAN ĐẶC TRƯNG)
        # ─────────────────────────────────────────────────────────────────────
        def build_cluster(label_str: str, base_color: str, offset_dots: list) -> VGroup:
            ellipse = Ellipse(width=1.4, height=1.0, fill_color=ManimColor(base_color), fill_opacity=0.7, stroke_color=WHITE, stroke_width=1)
            label = MathTex(label_str, color=BLACK, font_size=26).move_to(ellipse.get_center())
            
            cluster_grp = VGroup(ellipse, label)
            for dx, dy in offset_dots:
                dot = Dot(radius=0.05, color=ManimColor(base_color))
                dot.move_to(ellipse.get_center() + RIGHT * dx + UP * dy)
                cluster_grp.add(dot)
                
            return cluster_grp

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG CÁC KHỐI THÀNH PHẦN
        # ─────────────────────────────────────────────────────────────────────

        # --- Khối 1: Training Data (X) ---
        x_rect = RoundedRectangle(
            width=1.6, height=1.6, corner_radius=0.3, 
            fill_color=ManimColor("#F3E1D4"), fill_opacity=1, stroke_color=WHITE, stroke_width=2
        )
        x_sym = MathTex(r"X", color=BLACK, font_size=48).move_to(x_rect.get_center())
        x_lbl = Text("Training Data", font=Theme.FONT_BODY, font_size=22, color=Theme.NEUTRAL)
        x_lbl.next_to(x_rect, UP, buff=0.15)
        box_X = VGroup(x_rect, x_sym, x_lbl)

        # --- Khối 2: Generative Feature Space (\Psi) ---
        psi_lbl_top = Text("Generative\nfeature space", font=Theme.FONT_BODY, font_size=20, color=ManimColor("#295A39"), weight="BOLD")
        psi_sym = MathTex(r"\Psi", color=BLACK, font_size=42)
        psi_title_grp = VGroup(psi_lbl_top, psi_sym).arrange(DOWN, buff=0.3)

        c1 = build_cluster(r"\hat{\Psi}_1", "#E9A8C5", [(0.8, 0.2), (-0.8, -0.1), (0.2, 0.7), (0.4, -0.6)])
        c2 = build_cluster(r"\hat{\Psi}_2", "#A1B9F1", [(0.7, -0.3), (-0.6, 0.4), (-0.2, -0.6)])
        c3 = build_cluster(r"\hat{\Psi}_3", "#F3A1A1", [(0.6, 0.4), (-0.7, -0.2), (0.1, 0.6), (-0.4, -0.5)])

        cluster_label_box = RoundedRectangle(width=2.0, height=0.5, corner_radius=0.1, fill_color=WHITE, fill_opacity=1, stroke_color=GRAY)
        cluster_lbl = Text("Clustering", color=BLACK, font_size=18).move_to(cluster_label_box.get_center())
        cluster_center = VGroup(cluster_label_box, cluster_lbl)

        c_top = VGroup(c1, c2).arrange(RIGHT, buff=0.4)
        c_all = VGroup(c_top, cluster_center, c3).arrange(DOWN, buff=0.2)
        
        psi_content = VGroup(psi_title_grp, c_all).arrange(RIGHT, buff=0.6)
        
        psi_bg_fill = RoundedRectangle(
            width=psi_content.width + 1.2, height=psi_content.height + 0.8, corner_radius=0.5, 
            fill_color=ManimColor("#E5ECD4"), fill_opacity=1, stroke_width=0
        )
        psi_bg_border = DashedVMobject(
            RoundedRectangle(
                width=psi_content.width + 1.2, height=psi_content.height + 0.8, corner_radius=0.5, 
                stroke_color=GRAY, stroke_width=4, fill_opacity=0
            ),
            num_dashes=30,
            dashed_ratio=0.5
        )
        psi_bg = VGroup(psi_bg_fill, psi_bg_border)
        
        psi_content.move_to(psi_bg_fill.get_center())
        box_Psi = VGroup(psi_bg, psi_content)

        # --- Khối 3: Cluster Centroids ---
        cent_rect = Rectangle(
            width=2.5, height=1.4, fill_color=ManimColor("#E5ECD4"), fill_opacity=1, stroke_color=GRAY, stroke_width=2
        )
        cent_lbl = Text("Cluster\nCentroids", color=ManimColor("#295A39"), font_size=24, line_spacing=1.2).move_to(cent_rect.get_center())
        box_Centroids = VGroup(cent_rect, cent_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: THIẾT LẬP TRỤC ĐẾ NẰM NGANG & TREO CÁC KHỐI PHỤ
        # ─────────────────────────────────────────────────────────────────────
        
        main_axis = VGroup(box_X, box_Psi, box_Centroids).arrange(RIGHT, buff=0.8)

        # --- Khối 4: Mô hình Phi (\Phi) ---
        phi_poly = Polygon(
            [-0.7, 0.7, 0], [0.7, 0.7, 0], [0.4, -0.7, 0], [-0.4, -0.7, 0],
            fill_color=ManimColor("#BDD5E9"), fill_opacity=0.9, stroke_color=WHITE, stroke_width=2
        )
        phi_sym = MathTex(r"\Phi", font_size=40, color=BLACK).move_to(phi_poly.get_center())
        box_Phi = VGroup(phi_poly, phi_sym)
        
        box_Phi.next_to(box_X, DOWN, buff=1.0)

        # --- Khối 5: Output Vectors ---
        out_blocks = VGroup(*[
            Square(
                side_length=0.7, 
                fill_color=ManimColor("#BDD5E9") if i < 3 else ManimColor("#E5ECD4"), 
                fill_opacity=1, stroke_color=GRAY, stroke_width=2
            ) for i in range(6)
        ]).arrange(RIGHT, buff=0)
        
        out_blocks.next_to(box_Centroids, DOWN, buff=1.0)
        out_blocks.match_y(box_Phi)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: ĐÓNG GÓI, GIỚI HẠN TỶ LỆ TRƯỚC KHI VẼ MŨI TÊN
        # ─────────────────────────────────────────────────────────────────────
        
        all_layout = VGroup(main_axis, box_Phi, out_blocks)
        
        all_layout.set_width(13.2)
        if all_layout.height > 5.5:
            all_layout.set_height(5.5)
            
        all_layout.center()
        all_layout.shift(DOWN * 0.2)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: KHỞI TẠO MŨI TÊN BÁM THEO TỌA ĐỘ ĐÃ ĐƯỢC CHỐT
        # ─────────────────────────────────────────────────────────────────────
        
        c_green = ManimColor("#85B57A")
        c_red   = Theme.ACCENT_RED

        arr_X_Psi = Arrow(box_X.get_right(), box_Psi.get_left(), buff=0.1, color=c_green, stroke_width=5)
        arr_Psi_Cent = Arrow(box_Psi.get_right(), box_Centroids.get_left(), buff=0.1, color=c_green, stroke_width=5)
        
        arr_X_Phi = Arrow(box_X.get_bottom(), box_Phi.get_top(), buff=0.1, color=c_red, stroke_width=6, tip_length=0.2)
        arr_Cent_Out = Arrow(box_Centroids.get_bottom(), out_blocks.get_top(), buff=0.1, color=c_red, stroke_width=6, tip_length=0.2)
        
        arr_Phi_Out = Arrow(box_Phi.get_right(), out_blocks.get_left(), buff=0.15, color=c_green, stroke_width=5)

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title), FadeIn(v_banner))
        self.next_slide()

        # 1. Trục chính phía trên
        self.play(FadeIn(box_X))
        self.play(Create(arr_X_Psi))
        self.play(FadeIn(psi_bg_fill), Create(psi_bg_border), FadeIn(psi_content))
        self.next_slide()

        self.play(Create(arr_Psi_Cent))
        self.play(FadeIn(box_Centroids))
        self.next_slide()

        # 2. Nhánh model bên dưới và kết hợp vector
        self.play(Create(arr_X_Phi), FadeIn(box_Phi))
        self.next_slide()

        self.play(Create(arr_Cent_Out), Create(arr_Phi_Out))
        self.play(FadeIn(out_blocks))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 29 — MODULE 26: TRACK4GEN  ██████╗
# ─────────────────────────────────────────────────────────────────────────────
from manim import DashedLine

class Module26_Track4Gen(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề slide
        title = slide_title("Track4Gen Architecture")
        
        # ─────────────────────────────────────────────────────────────────────
        # HÀM HỖ TRỢ XÂY DỰNG CÁC THÀNH PHẦN (COMPONENTS)
        # ─────────────────────────────────────────────────────────────────────
        
        def build_frame_stack(label_str: str, base_color: str) -> VGroup:
            stack = VGroup()
            for i in range(3):
                rect = Rectangle(
                    width=1.8, height=1.2, fill_color=ManimColor(base_color), 
                    fill_opacity=0.8, stroke_color=WHITE, stroke_width=1.5
                )
                rect.shift(RIGHT * (0.15 * i) + UP * (0.15 * i))
                stack.add(rect)
                
            label = MathTex(label_str, font_size=32, color=Theme.NEUTRAL).next_to(stack, UP, buff=0.1)
            return VGroup(stack, label)

        def build_feature_stack(label_str: str) -> VGroup:
            stack = VGroup()
            for i in range(3):
                rect = Rectangle(
                    width=1.2, height=0.6, fill_color=ManimColor("#D485B8"), 
                    fill_opacity=0.9, stroke_color=BLACK, stroke_width=1
                )
                rect.shift(RIGHT * (0.1 * i) + UP * (0.1 * i))
                stack.add(rect)
            label = Text(label_str, font=Theme.FONT_BODY, font_size=16, color=BLACK, weight="BOLD").move_to(stack.get_center())
            return VGroup(stack, label)

        def build_unet_block(label_str: str) -> VGroup:
            rect = Rectangle(width=0.8, height=2.5, fill_color=ManimColor("#A3281E"), fill_opacity=0.9, stroke_color=WHITE, stroke_width=1)
            label = Text(label_str, font=Theme.FONT_BODY, font_size=18, color=WHITE).rotate(PI/2).move_to(rect.get_center())
            return VGroup(rect, label)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG BẢNG BÊN PHẢI (VIDEO DENOISER)
        # ─────────────────────────────────────────────────────────────────────
        
        u_in = build_unet_block("U-Net Enc")
        raw_feat = build_feature_stack("Raw\nFeatures")
        
        plus_node = Circle(radius=0.25, color=Theme.NEUTRAL, fill_color=Theme.BOX_FILL, fill_opacity=1)
        plus_sym = MathTex("+", color=Theme.NEUTRAL).move_to(plus_node.get_center())
        plus_grp = VGroup(plus_node, plus_sym)
        
        u_out = build_unet_block("U-Net Dec")
        main_stream = VGroup(u_in, raw_feat, plus_grp, u_out).arrange(RIGHT, buff=0.6)

        refiner_box = Rectangle(width=1.5, height=1.0, fill_color=ManimColor("#2B5C30"), fill_opacity=0.9, stroke_color=WHITE)
        ref_lbl = Text("Refiner\nNetwork", font=Theme.FONT_BODY, font_size=16, color=WHITE).move_to(refiner_box.get_center())
        refiner = VGroup(refiner_box, ref_lbl)
        
        refined_feat = build_feature_stack("Refined\nFeatures")
        
        zero_conv = Rectangle(width=1.5, height=0.5, fill_color=Theme.ACCENT_RED, fill_opacity=0.9)
        zc_lbl = Text("Zero Conv", font_size=16, color=WHITE).move_to(zero_conv.get_center())
        z_conv_grp = VGroup(zero_conv, zc_lbl)

        # Treo nhánh phụ theo chiều dọc an toàn
        refiner.next_to(raw_feat, DOWN, buff=0.6)
        refined_feat.next_to(refiner, DOWN, buff=0.4)
        z_conv_grp.match_y(refined_feat).match_x(plus_grp)

        denoiser_content = VGroup(main_stream, refiner, refined_feat, z_conv_grp)
        denoiser_bg = RoundedRectangle(
            width=denoiser_content.width + 1.2, height=denoiser_content.height + 1.4, 
            corner_radius=0.4, fill_color=ManimColor("#2C364A"), fill_opacity=1, stroke_color=Theme.PRIMARY, stroke_width=2
        )
        
        # Sắp xếp và đặt Title an toàn vào LÕI của Denoiser Box thay vì treo bên ngoài
        denoiser_content.move_to(denoiser_bg.get_center()).shift(DOWN * 0.2)
        dn_title = Text("Video Denoiser f\u03B8", font_size=22, color=Theme.NEUTRAL, weight="BOLD")
        dn_title.next_to(denoiser_bg.get_top(), DOWN, buff=0.15)
        
        right_panel = VGroup(denoiser_bg, denoiser_content, dn_title)
        right_panel.move_to(ORIGIN)

        output_lbl = MathTex(r"f_\theta(z_t^{1:N}, t, c)", font_size=24, color=Theme.NEUTRAL).next_to(right_panel, RIGHT, buff=0.4)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG BẢNG BÊN TRÁI & NEO TRỤC ĐỂ CHỐNG LỆCH
        # ─────────────────────────────────────────────────────────────────────
        
        clean_vid = build_frame_stack(r"z_0^{1:N}", "#4A4A4A")
        # Khắc phục lỗi ô vuông bằng việc tách \epsilon thành MathTex riêng
        add_noise_lbl = VGroup(
            Text("Add Noise", font_size=16, color=Theme.NEUTRAL), 
            MathTex(r"\epsilon", font_size=20, color=Theme.NEUTRAL)
        ).arrange(RIGHT, buff=0.1)
        noisy_vid = build_frame_stack(r"z_t^{1:N}", "#2A2A2A")
        vid_flow = VGroup(clean_vid, add_noise_lbl, noisy_vid).arrange(RIGHT, buff=0.4)
        
        traj_bg = RoundedRectangle(width=4.5, height=1.6, fill_color=ManimColor("#4A5F45"), fill_opacity=0.8, stroke_color=ManimColor("#85B57A"))
        fi = Rectangle(width=1.0, height=0.6, fill_color=GRAY, fill_opacity=0.5, stroke_width=1).move_to(traj_bg.get_center() + LEFT*1.0 + DOWN*0.1)
        fj = Rectangle(width=1.0, height=0.6, fill_color=GRAY, fill_opacity=0.5, stroke_width=1).move_to(traj_bg.get_center() + RIGHT*1.0 + UP*0.1)
        d1 = DashedLine(fi.get_center()+LEFT*0.2+UP*0.1, fj.get_center()+LEFT*0.2+UP*0.1, color=Theme.ACCENT_RED, stroke_width=2)
        d2 = DashedLine(fi.get_center()+RIGHT*0.3+DOWN*0.1, fj.get_center()+RIGHT*0.3+DOWN*0.1, color=Theme.PRIMARY, stroke_width=2)
        
        traj_box = VGroup(traj_bg, fi, fj, d1, d2)
        t_lbl = Text("Compute Point Trajectories\nAcross Frames", font_size=16, color=Theme.NEUTRAL)

        # === QUY TẮC CĂN CHỈNH GIẢI QUYẾT LỖI TỌA ĐỘ ===
        # 1. Đặt Video Box ngang với luồng U-Net
        vid_flow.next_to(right_panel, LEFT, buff=2.0)
        vid_flow.match_y(main_stream)

        # 2. Đặt Trajectory Box ngang với nhánh Refined Features
        traj_box.align_to(vid_flow, LEFT) # Căn lề trái thẳng hàng
        traj_box.match_y(refined_feat)
        t_lbl.next_to(traj_box, UP, buff=0.1, aligned_edge=LEFT)
        
        traj_group = VGroup(traj_box, t_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM TỔNG THỂ, CĂN CHỈNH AN TOÀN TRƯỚC KHI VẼ MŨI TÊN
        # ─────────────────────────────────────────────────────────────────────
        
        all_elements = VGroup(vid_flow, traj_group, right_panel, output_lbl)
        all_elements.set_width(13.2)
        if all_elements.height > 4.5:
            all_elements.set_height(4.5)
            
        # Dời toàn bộ xuống cách Title một khoảng buff = 1.2 KHỔNG LỒ
        # Để đảm bảo không bao giờ có đường kẻ nào đè lên chữ Title!
        all_elements.next_to(title, DOWN, buff=1.2)
        all_elements.set_x(0) # Đưa vào trung tâm trục X

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: KHỞI TẠO MŨI TÊN BẰNG TỌA ĐỘ ĐÃ CHỐT
        # ─────────────────────────────────────────────────────────────────────
        
        c_line = Theme.NEUTRAL
        
        arr_add_noise = Arrow(clean_vid.get_right(), add_noise_lbl.get_left(), buff=0.1, color=c_line)
        arr_noise_out = Arrow(add_noise_lbl.get_right(), noisy_vid.get_left(), buff=0.1, color=c_line)
        arr_final = Arrow(denoiser_bg.get_right(), output_lbl.get_left(), buff=0.1, color=c_line)
        
        # Mũi tên từ Noisy Vid đi NGANG chuẩn 100% vào Denoiser
        arr_to_dn = Arrow(noisy_vid.get_right(), [denoiser_bg.get_left()[0], noisy_vid.get_right()[1], 0], buff=0.1, color=c_line)

        # Mũi tên ngoài cùng bên trái (Kéo thẳng dọc xuống dài và đẹp mắt)
        arr_to_traj = Arrow(clean_vid.get_bottom(), [clean_vid.get_bottom()[0], t_lbl.get_top()[1], 0], buff=0.1, color=c_line)

        # Nội bộ Denoiser
        a1 = Arrow(u_in.get_right(), raw_feat.get_left(), buff=0.1, color=c_line)
        a2 = Arrow(raw_feat.get_right(), plus_grp.get_left(), buff=0.1, color=c_line)
        a3 = Arrow(plus_grp.get_right(), u_out.get_left(), buff=0.1, color=c_line)
        a_ref1 = Arrow(raw_feat.get_bottom(), refiner.get_top(), buff=0.1, color=c_line)
        a_ref2 = Arrow(refiner.get_bottom(), refined_feat.get_top(), buff=0.1, color=c_line)
        a_ref3 = Arrow(refined_feat.get_right(), z_conv_grp.get_left(), buff=0.1, color=c_line)
        a_ref4 = Arrow(z_conv_grp.get_top(), plus_grp.get_bottom(), buff=0.1, color=c_line)

        # Xóa gradient bằng vạch chéo đỏ
        detach_cross = MathTex(r"\times", color=Theme.ACCENT_RED, font_size=36).move_to(a_ref3.get_center())
        detach_lbl = Text("Detach\nGradient", font_size=14, color=Theme.NEUTRAL).next_to(detach_cross, DOWN, buff=0.05)
        detach_grp = VGroup(detach_cross, detach_lbl)

        # === 1. CORRESPONDENCE LOSS (MŨI TÊN XANH - KHÓA Y TUYỆT ĐỐI 100% NGANG) ===
        y_green = traj_box.get_right()[1]
        p_green_left = [traj_box.get_right()[0], y_green, 0]
        p_green_right = [denoiser_bg.get_left()[0], y_green, 0]
        corr_arr = DoubleArrow(p_green_left, p_green_right, color=Theme.SUCCESS, stroke_width=4, buff=0.15)
        corr_lbl = Text("Correspondence Loss L_corr", font_size=16, color=Theme.SUCCESS, weight="BOLD").next_to(corr_arr, UP, buff=0.1)

        # === 2. DIFFUSION LOSS (MŨI TÊN ĐỎ - ĐƯỜNG VUÔNG GÓC HOÀN HẢO) ===
        p1 = output_lbl.get_top() + UP * 0.1
        # Điểm p2 nằm ngang, cao hơn đỉnh của sơ đồ đúng 0.5 (hoàn toàn chui lọt khe an toàn 1.2 bên dưới Title)
        p2 = [p1[0], all_elements.get_top()[1] + 0.5, 0] 
        p3 = [clean_vid.get_top()[0], p2[1], 0]
        p4 = clean_vid.get_top() + UP * 0.1

        diff_line1 = Line(p1, p2, color=Theme.ACCENT_RED, stroke_width=4)
        diff_line2 = Line(p2, p3, color=Theme.ACCENT_RED, stroke_width=4)
        diff_arr_down = Arrow(p3, p4, color=Theme.ACCENT_RED, stroke_width=4, buff=0)
        diff_arr_group = VGroup(diff_line1, diff_line2, diff_arr_down)
        
        diff_lbl = Text("Diffusion Loss (v-prediction) L_diff", font_size=18, color=Theme.ACCENT_RED, weight="BOLD")
        diff_lbl.next_to(diff_line2, UP, buff=0.1)

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.next_slide()

        self.play(FadeIn(clean_vid))
        self.play(Create(arr_add_noise), FadeIn(add_noise_lbl), Create(arr_noise_out), FadeIn(noisy_vid))
        self.play(Create(arr_to_traj), FadeIn(traj_group))
        self.next_slide()

        self.play(Create(arr_to_dn), FadeIn(denoiser_bg), FadeIn(dn_title))
        self.play(FadeIn(u_in), Create(a1), FadeIn(raw_feat), Create(a2), FadeIn(plus_grp), Create(a3), FadeIn(u_out))
        self.play(Create(arr_final), FadeIn(output_lbl))
        self.next_slide()

        self.play(Create(a_ref1), FadeIn(refiner))
        self.play(Create(a_ref2), FadeIn(refined_feat))
        self.play(Create(a_ref3), FadeIn(z_conv_grp), Create(a_ref4))
        self.play(FadeIn(detach_grp))
        self.next_slide()

        self.play(Create(corr_arr), FadeIn(corr_lbl))
        self.play(Create(diff_arr_group), FadeIn(diff_lbl))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 30 — MODULE 27: CONCEPT STEERER  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module27_ConceptSteerer(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề và Banner
        title = slide_title("Concept Steerer")
        
        banner_bg = RoundedRectangle(width=2.8, height=0.8, corner_radius=0.1, fill_color=Theme.BOX_FILL_ALT, fill_opacity=0.8, stroke_width=0)
        banner_lbl = Text("Supervised\nFinetuning", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM, line_spacing=1.2).move_to(banner_bg)
        banner = VGroup(banner_bg, banner_lbl).to_corner(UR, buff=0.4)

        # ─────────────────────────────────────────────────────────────────────
        # HÀM HỖ TRỢ VẼ KHỐI (BLOCK BUILDERS)
        # ─────────────────────────────────────────────────────────────────────
        
        def build_te(label_str: str) -> VGroup:
            """Text Encoder hướng từ trái sang phải (Trái to, phải nhỏ)"""
            poly = Polygon(
                [-0.8, 0.6, 0], [0.8, 0.3, 0], [0.8, -0.3, 0], [-0.8, -0.6, 0],
                fill_color=Theme.BOX_FILL_ALT, fill_opacity=1, stroke_color=ManimColor("#D485B8"), stroke_width=2
            )
            lbl = Text(label_str, font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL).move_to(poly)
            return VGroup(poly, lbl)

        def build_ksae() -> VGroup:
            """Khối k-SAE xây dựng theo trục dọc (Autoencoder thu hẹp ở giữa)"""
            def vec(colors):
                return VGroup(*[Square(side_length=0.25, fill_color=ManimColor(c), fill_opacity=1, stroke_color=WHITE, stroke_width=1) for c in colors]).arrange(RIGHT, buff=0.05)
            
            v_in = vec(["#555555"] * 5)
            enc = Polygon([-1.0, -0.3, 0], [1.0, -0.3, 0], [0.5, 0.3, 0], [-0.5, 0.3, 0], fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY)
            enc_lbl = Text("Encoder", font_size=16, color=Theme.NEUTRAL).move_to(enc)
            
            z_colors = ["#555555"] * 7
            z_colors[5] = Theme.ACCENT_RED.to_hex() # Vị trí được steer
            z = vec(z_colors)
            z_lambda = MathTex(r"*\lambda", font_size=20, color=Theme.ACCENT_RED).next_to(z, RIGHT, buff=0.1)
            z_group = VGroup(z, z_lambda)
            
            dec = Polygon([-0.5, -0.3, 0], [0.5, -0.3, 0], [1.0, 0.3, 0], [-1.0, 0.3, 0], fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY)
            dec_lbl = Text("Decoder", font_size=16, color=Theme.NEUTRAL).move_to(dec)
            v_out = vec(["#555555"] * 5)
            
            stack = VGroup(v_out, VGroup(dec, dec_lbl), z_group, VGroup(enc, enc_lbl), v_in).arrange(DOWN, buff=0.15)
            
            # Căn chỉnh khung nền bao trọn nội dung động
            bg = RoundedRectangle(width=stack.width + 0.8, height=stack.height + 0.6, corner_radius=0.3, fill_color=Theme.BOX_FILL, stroke_color=ManimColor("#F2CC8F"))
            stack.move_to(bg)
            title = Text("k-SAE", font=Theme.FONT_BODY, font_size=20, color=ManimColor("#F2CC8F")).next_to(bg, LEFT, buff=0.3)
            
            return VGroup(bg, stack, title)

        def build_output_img(is_safe=False) -> VGroup:
            """Trừu tượng hóa hình ảnh Unsafe/Safe bằng vector đồ họa"""
            rect = RoundedRectangle(width=2.2, height=2.2, corner_radius=0.1, fill_color=Theme.BOX_FILL, fill_opacity=1, stroke_color=Theme.NEUTRAL, stroke_width=2)
            
            # Khối cơ thể đơn giản
            head = Circle(radius=0.3, fill_color=Theme.NEUTRAL, fill_opacity=0.8, stroke_width=0).shift(UP*0.4)
            body = Ellipse(width=1.2, height=1.0, fill_color=Theme.NEUTRAL, fill_opacity=0.8, stroke_width=0).shift(DOWN*0.3)
            
            if not is_safe:
                censor = Rectangle(width=1.4, height=0.35, fill_color=BLACK, fill_opacity=1).move_to(body.get_center() + UP*0.1)
                img_content = VGroup(head, body, censor)
                lbl = Text("Unsafe", font=Theme.FONT_BODY, font_size=22, color=Theme.ACCENT_RED, weight="BOLD")
            else:
                img_content = VGroup(head, body)
                lbl = Text("Safe", font=Theme.FONT_BODY, font_size=22, color=Theme.SUCCESS, weight="BOLD")
                
            img_content.move_to(rect)
            lbl.next_to(rect, DOWN, buff=0.15)
            return VGroup(rect, img_content, lbl)

        def elbow_arrow(start, end, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15, x_first=True):
            """Tạo mũi tên rẽ góc vuông hoàn hảo thay thế CurvedArrow"""
            corner = np.array([end[0], start[1], 0]) if x_first else np.array([start[0], end[1], 0])
            l1 = Line(start, corner, color=color, stroke_width=stroke_width)
            l2 = Arrow(corner, end, color=color, stroke_width=stroke_width, buff=0, tip_length=tip_length)
            return VGroup(l1, l2)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: ĐỊNH VỊ TỌA ĐỘ NEO (GRID-ANCHORED COORDINATES)
        # Cố định Y cho các hàng ngang để mũi tên thẳng tắp 100%
        # ─────────────────────────────────────────────────────────────────────
        
        X_COL_1 = -4.5   # Prompt, Noise, Concept
        X_COL_2 = -2.0   # Encoders
        X_TRUNK =  1.0   # Diffusion, k-SAE, Addition Node
        X_OUT   =  4.5   # Outputs

        Y_DIFF =  2.4    # Hàng trên cùng (Noise -> Diff -> Unsafe)
        Y_TE1  =  0.5    # Hàng giữa (Prompt -> TE1 -> + node)
        Y_KSAE = -1.8    # Vị trí k-SAE
        Y_TE2  = -3.8    # Hàng dưới cùng (Concept -> TE2)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: KHỞI TẠO CÁC KHỐI THEO TỌA ĐỘ
        # ─────────────────────────────────────────────────────────────────────

        # Hàng trên (Diffusion & Noise)
        diff_rect = RoundedRectangle(width=2.8, height=1.2, corner_radius=0.2, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_RED)
        diff_lbl = Text("Diffusion model", font_size=20, color=Theme.NEUTRAL).move_to(diff_rect)
        diff_box = VGroup(diff_rect, diff_lbl).move_to([X_TRUNK, Y_DIFF, 0])
        
        noise_rect = Square(side_length=1.5, fill_color=ManimColor("#222222"), fill_opacity=1, stroke_color=Theme.NEUTRAL)
        noise_lbl = Text("Noise", font_size=20, color=Theme.NEUTRAL).move_to(noise_rect)
        noise_box = VGroup(noise_rect, noise_lbl).move_to([X_COL_1, Y_DIFF, 0])

        # Hàng giữa (Prompt & TE1 & + Node)
        prompt_rect = RoundedRectangle(width=2.2, height=1.2, corner_radius=0.2, fill_color=Theme.BOX_FILL, stroke_color=ManimColor("#D485B8"))
        prompt_lbl = Text("Text prompt\n\"Greek goddess\nposing...\"", font_size=18, color=Theme.NEUTRAL, line_spacing=1.2).move_to(prompt_rect)
        prompt_box = VGroup(prompt_rect, prompt_lbl).move_to([X_COL_1, Y_TE1, 0])
        
        te1 = build_te("Text\nEncoder").move_to([X_COL_2, Y_TE1, 0])
        
        plus_node = VGroup(
            Circle(radius=0.2, color=Theme.ACCENT_RED, fill_color=Theme.BG, fill_opacity=1, stroke_width=3),
            MathTex("+", color=Theme.ACCENT_RED, font_size=24)
        ).move_to([X_TRUNK, Y_TE1, 0])

        # Hàng dưới cùng (Concept & TE2 & k-SAE)
        concept_rect = RoundedRectangle(width=2.2, height=1.0, corner_radius=0.2, fill_color=Theme.BOX_FILL, stroke_color=ManimColor("#D485B8"))
        concept_lbl = Text("Concept C\n\"Nudity\"", font_size=18, color=Theme.NEUTRAL, line_spacing=1.2).move_to(concept_rect)
        concept_box = VGroup(concept_rect, concept_lbl).move_to([X_COL_1, Y_TE2, 0])
        
        te2 = build_te("Text\nEncoder").move_to([X_COL_2, Y_TE2, 0])
        
        ksae_box = build_ksae().move_to([X_TRUNK, Y_KSAE, 0])

        # Outputs
        unsafe_box = build_output_img(is_safe=False).move_to([X_OUT, Y_DIFF, 0])
        safe_box = build_output_img(is_safe=True).move_to([X_OUT, Y_KSAE, 0])

        # Legend
        leg_bg = RoundedRectangle(width=3.0, height=1.0, corner_radius=0.2, fill_color=Theme.BG, stroke_color=ManimColor("#D485B8"))
        leg_uns = VGroup(Line(LEFT, RIGHT, color=Theme.NEUTRAL).set_length(0.6), Text("Unsafe path", font_size=16, color=Theme.NEUTRAL)).arrange(RIGHT, buff=0.2)
        leg_saf = VGroup(Line(LEFT, RIGHT, color=Theme.ACCENT_RED).set_length(0.6), Text("Safe path", font_size=16, color=Theme.NEUTRAL)).arrange(RIGHT, buff=0.2)
        legend = VGroup(leg_bg, VGroup(leg_uns, leg_saf).arrange(DOWN, buff=0.15).move_to(leg_bg))
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM VÀ ĐỊNH TỶ LỆ TRƯỚC KHI VẼ MŨI TÊN (QUY TẮC AN TOÀN)
        # ─────────────────────────────────────────────────────────────────────
        
        all_layout = VGroup(noise_box, prompt_box, concept_box, te1, te2, diff_box, plus_node, ksae_box, unsafe_box, safe_box)
        all_layout.set_height(6.8) # Chống tràn trục dọc
        all_layout.center().shift(DOWN * 0.1) # Chừa chỗ cho Title
        legend.to_corner(DR, buff=0.4)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: VẼ MŨI TÊN (TRÍCH XUẤT TỌA ĐỘ SAU SCALE)
        # ─────────────────────────────────────────────────────────────────────
        
        c_w, c_r, sw = Theme.NEUTRAL, Theme.ACCENT_RED, 3
        
        # Nhánh Unsafe (Ngang hoàn toàn nhờ chung tọa độ Y)
        a_noise_diff = Arrow(noise_box.get_right(), diff_box.get_left(), color=c_w, stroke_width=sw, buff=0.15)
        a_prompt_te1 = Arrow(prompt_box.get_right(), te1.get_left(), color=c_w, stroke_width=sw, buff=0.15)
        a_te1_plus   = Arrow(te1.get_right(), plus_node.get_left(), color=c_w, stroke_width=sw, buff=0.15)
        a_plus_diff  = Arrow(plus_node.get_top(), diff_box.get_bottom(), color=c_w, stroke_width=sw, buff=0.15)
        a_diff_unsafe = Arrow(diff_box.get_right(), unsafe_box.get_left(), color=c_w, stroke_width=sw, buff=0.15)

        # Nhánh Concept (Steering)
        a_concept_te2 = Arrow(concept_box.get_right(), te2.get_left(), color=c_r, stroke_width=sw, buff=0.15)
        
        # Mũi tên Rẽ vuông góc (Elbow) từ TE2 lên đáy k-SAE (Ngang trước, Dọc sau)
        a_te2_ksae = elbow_arrow(te2.get_right(), ksae_box[0].get_bottom() + DOWN*0.1, color=c_r, x_first=True)
        
        a_ksae_plus = Arrow(ksae_box[0].get_top(), plus_node.get_bottom(), color=c_r, stroke_width=sw, buff=0.15)

        # Mũi tên Rẽ vuông góc (Elbow) từ Diffusion xuống Safe Box (Dọc trước, Ngang sau)
        # Xuất phát từ cạnh đáy gần bên phải của Diffusion để tránh đè lên mũi tên Unsafe
        safe_start_pt = diff_box.get_corner(DR) + LEFT*0.5
        a_diff_safe = elbow_arrow(safe_start_pt, safe_box.get_left() + LEFT*0.1, color=c_r, x_first=False)

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title), FadeIn(banner))
        self.next_slide()

        # 1. Luồng chạy Baseline (Unsafe Path)
        self.play(FadeIn(prompt_box), FadeIn(noise_box))
        self.play(Create(a_prompt_te1), FadeIn(te1))
        self.play(Create(a_te1_plus), FadeIn(plus_node))
        self.play(Create(a_plus_diff), Create(a_noise_diff), FadeIn(diff_box))
        self.play(Create(a_diff_unsafe), FadeIn(unsafe_box))
        self.next_slide()

        # 2. Đưa Concept và trích xuất đặc trưng
        self.play(FadeIn(concept_box))
        self.play(Create(a_concept_te2), FadeIn(te2))
        self.next_slide()

        # 3. Chạy qua k-SAE
        self.play(Create(a_te2_ksae))
        self.play(FadeIn(ksae_box))
        self.next_slide()

        # 4. Giao thoa Steering tại + Node
        self.play(Create(a_ksae_plus))
        self.play(Indicate(plus_node, color=Theme.ACCENT_RED, scale_factor=1.5))
        self.next_slide()

        # 5. Kết quả sau can thiệp (Safe Output)
        self.play(Create(a_diff_safe))
        self.play(FadeIn(safe_box))
        self.next_slide()

        # 6. Hiện chú giải (Legend)
        self.play(FadeIn(legend))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 31 — MODULE 28: SYNTHETIC DATA PIPELINE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module28_SyntheticDataPipeline(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề và Banner
        title = slide_title("Synthetic Data Generation Pipeline")
        
        banner_bg = RoundedRectangle(width=2.8, height=0.8, corner_radius=0.1, fill_color=Theme.BOX_FILL_ALT, fill_opacity=0.8, stroke_width=0)
        banner_lbl = Text("Supervised\nFinetuning", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM, line_spacing=1.2).move_to(banner_bg)
        banner = VGroup(banner_bg, banner_lbl).to_corner(UR, buff=0.4)

        # ─────────────────────────────────────────────────────────────────────
        # HÀM HỖ TRỢ VẼ CÁC THÀNH PHẦN
        # ─────────────────────────────────────────────────────────────────────
        
        def build_step_box(text_str: str) -> VGroup:
            """Tạo các hộp cho Step 1, 2, 3 (Theme sáng nhạt, viền xanh)"""
            box = RoundedRectangle(
                width=3.8, height=1.0, corner_radius=0.2, 
                fill_color=ManimColor("#1A2433"), fill_opacity=1, stroke_color=Theme.PRIMARY, stroke_width=2
            )
            lbl = Text(text_str, font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL, line_spacing=1.2).move_to(box)
            return VGroup(box, lbl)

        def build_image_mock(label_str: str, mark: str = None) -> VGroup:
            """Mô phỏng hình ảnh sinh ra với Text và ký hiệu Check/Cross"""
            rect = Rectangle(width=1.5, height=1.5, fill_color=Theme.BOX_FILL, fill_opacity=1, stroke_color=Theme.DIM, stroke_width=2)
            lbl = Text(label_str, font=Theme.FONT_BODY, font_size=14, color=Theme.NEUTRAL, line_spacing=1.2).move_to(rect)
            
            group = VGroup(rect, lbl)
            
            if mark == "cross":
                c1 = Line(UL, DR, color=Theme.ACCENT_RED, stroke_width=4).scale(0.15)
                c2 = Line(UR, DL, color=Theme.ACCENT_RED, stroke_width=4).scale(0.15)
                cross = VGroup(c1, c2).move_to(rect.get_corner(DR) + LEFT*0.2 + UP*0.2)
                group.add(cross)
            elif mark == "check":
                c1 = Line([-0.1, 0, 0], [0, -0.1, 0], color=Theme.SUCCESS, stroke_width=4)
                c2 = Line([0, -0.1, 0], [0.2, 0.2, 0], color=Theme.SUCCESS, stroke_width=4)
                check = VGroup(c1, c2).move_to(rect.get_corner(DR) + LEFT*0.25 + UP*0.15)
                group.add(check)
                
            return group

        def build_database_icon() -> VGroup:
            """Tạo biểu tượng Database hình trụ"""
            w, h = 1.2, 1.2
            base = Ellipse(width=w, height=0.3, fill_color=Theme.PRIMARY, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
            body = Rectangle(width=w, height=h, fill_color=Theme.PRIMARY, fill_opacity=0.8, stroke_color=WHITE, stroke_width=1)
            body.next_to(base, UP, buff=-0.15)
            top_el = Ellipse(width=w, height=0.3, fill_color=ManimColor("#8AB4F8"), fill_opacity=1, stroke_color=WHITE, stroke_width=1)
            top_el.move_to(body.get_top())
            
            line1 = Ellipse(width=w, height=0.3, stroke_color=WHITE, stroke_width=1).move_to(body.get_center() + UP*0.2)
            line2 = Ellipse(width=w, height=0.3, stroke_color=WHITE, stroke_width=1).move_to(body.get_center() + DOWN*0.2)
            
            # Chỉ lấy nửa dưới của các đường cắt ngang
            db_icon = VGroup(body, base, line1, line2, top_el)
            
            lbl = Text("Synthetic Dataset", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL, weight="BOLD")
            lbl.next_to(db_icon, DOWN, buff=0.2)
            
            return VGroup(db_icon, lbl)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG LÕI TRUNG TÂM (CENTRAL PIPELINE)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- Cột trái: Prompts -> Gen Images ---
        prompts_box = RoundedRectangle(width=3.0, height=1.8, corner_radius=0.2, fill_color=ManimColor("#33221A"), fill_opacity=1, stroke_color=Theme.ACCENT_GOLD)
        prompts_text = Text("List of prompts:\n- An empty table\n- An empty bottle\n- An empty bookshelf", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL, line_spacing=1.3)
        prompts_text.move_to(prompts_box)
        grp_prompts = VGroup(prompts_box, prompts_text)
        
        img1 = build_image_mock("Image:\nEmpty\nBookshelf")
        img2 = build_image_mock("Image:\nEmpty\nTable")
        grp_gen_imgs = VGroup(img1, img2).arrange(RIGHT, buff=0.2)
        
        # --- Cột giữa: VLM Node ---
        vlm_circle = Circle(radius=0.6, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1, stroke_color=Theme.NEUTRAL, stroke_width=2)
        vlm_txt = Text("VLM", font_size=20, weight="BOLD").move_to(vlm_circle)
        vlm_sub = Text("Filtering &\nRecaptioning", font_size=14, line_spacing=1.2).next_to(vlm_circle, DOWN, buff=0.15)
        grp_vlm = VGroup(vlm_circle, vlm_txt, vlm_sub)
        
        # --- Cột phải: Filtered Images -> Database ---
        img3 = build_image_mock("Bookshelf\n(Has books)", mark="cross")
        img4 = build_image_mock("Table\nwithout bottle", mark="check")
        grp_filt_imgs = VGroup(img3, img4).arrange(RIGHT, buff=0.2)
        
        grp_db = build_database_icon()

        # Tổ hợp thành Lưới trung tâm (Khóa trục bằng match_y)
        left_col = VGroup(grp_prompts, grp_gen_imgs).arrange(DOWN, buff=1.0)
        right_col = VGroup(grp_db, grp_filt_imgs).arrange(DOWN, buff=1.0)
        
        inner_grid = VGroup(left_col, grp_vlm, right_col).arrange(RIGHT, buff=0.8)
        
        # Khóa Y cho hàng dưới (Tạo đường thẳng ngang hoàn hảo)
        grp_vlm.match_y(grp_gen_imgs)
        grp_filt_imgs.match_y(grp_gen_imgs)
        # Khóa Y cho hàng trên
        grp_db.match_y(grp_prompts)

        # Hộp nét đứt bao ngoài Central Box
        central_bg = RoundedRectangle(
            width=inner_grid.width + 0.8, height=inner_grid.height + 0.8, corner_radius=0.4, 
            fill_color=Theme.BOX_FILL, fill_opacity=0.6, stroke_color=Theme.DIM, stroke_width=2
        )
        # Sử dụng DashedVMobject để tạo viền đứt nét an toàn
        from manim import DashedVMobject
        central_bg_dashed = DashedVMobject(central_bg, num_dashes=40)
        
        central_box = VGroup(central_bg_dashed, inner_grid)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: NEO CÁC KHỐI STEP VÀO CENTRAL BOX
        # ─────────────────────────────────────────────────────────────────────
        
        step1 = build_step_box("1. Create synthetic dataset\nwith varied object states")
        step1.next_to(left_col, UP, buff=0.8) # Neo trực tiếp trên đỉnh cột trái
        
        step2 = build_step_box("2. Filter and rephrase\nusing GPT-4o")
        step2.next_to(central_box, RIGHT, buff=1.0)
        step2.match_y(grp_filt_imgs) # Khóa ngang hàng dưới
        
        step3 = build_step_box("3. Fine-tune models\nwith the synthetic dataset")
        step3.next_to(central_box, RIGHT, buff=1.0)
        step3.match_y(grp_db) # Khóa ngang hàng trên
        
        # Căn lề trái cho Step 2 và Step 3 thẳng nhau
        step2.align_to(step3, LEFT)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: ĐÓNG GÓI, GIỚI HẠN TỶ LỆ TRƯỚC KHI VẼ MŨI TÊN
        # ─────────────────────────────────────────────────────────────────────
        
        all_layout = VGroup(step1, central_box, step2, step3)
        
        # Ép khung tỷ lệ tuyệt đối chống Lỗi 1, 2, 3
        all_layout.set_width(13.5)
        if all_layout.height > 6.2:
            all_layout.set_height(6.2)
            
        all_layout.center().shift(DOWN * 0.1)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: KHỞI TẠO MŨI TÊN (ORTHOGONAL ARROWS TỰ ĐỘNG DO GRID)
        # ─────────────────────────────────────────────────────────────────────
        
        arr_color = ManimColor("#6B9EEB") # Xanh lam nhạt giống ảnh gốc
        arr_kw = {"color": arr_color, "stroke_width": 6, "tip_length": 0.25}

        # Step 1 -> Prompts
        a_s1_prompts = Arrow(step1.get_bottom(), grp_prompts.get_top(), buff=0.1, **arr_kw)
        
        # Prompts -> Gen Imgs
        a_prompts_gen = Arrow(grp_prompts.get_bottom(), grp_gen_imgs.get_top(), buff=0.1, **arr_kw)
        txt_gen = Text("Image Generation", font_size=14).next_to(a_prompts_gen, RIGHT, buff=0.1)
        
        # Gen Imgs -> VLM -> Filtered Imgs
        a_gen_vlm = Arrow(grp_gen_imgs.get_right(), grp_vlm.get_left(), buff=0.15, **arr_kw)
        a_vlm_filt = Arrow(grp_vlm.get_right(), grp_filt_imgs.get_left(), buff=0.15, **arr_kw)
        
        # Step 2 -> Central Box (Chỉ vào hàng dưới)
        a_s2_filt = Arrow(step2.get_left(), central_bg_dashed.get_right() * np.array([1, 0, 0]) + step2.get_left() * np.array([0, 1, 0]), buff=0.1, **arr_kw)
        
        # Filtered Imgs -> Database
        a_filt_db = Arrow(grp_filt_imgs.get_top(), grp_db.get_bottom(), buff=0.1, **arr_kw)
        
        # Database -> Step 3
        a_db_s3 = Arrow(grp_db.get_right(), step3.get_left(), buff=0.15, **arr_kw)

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title), FadeIn(banner))
        self.next_slide()

        # 1. Khởi tạo Step 1 và Prompts
        self.play(FadeIn(central_bg_dashed))
        self.play(FadeIn(step1), Create(a_s1_prompts))
        self.play(FadeIn(grp_prompts))
        self.next_slide()

        # 2. Sinh ảnh thô
        self.play(Create(a_prompts_gen), FadeIn(txt_gen))
        self.play(FadeIn(grp_gen_imgs))
        self.next_slide()

        # 3. Step 2 can thiệp bằng VLM để lọc ảnh
        self.play(FadeIn(step2), Create(a_s2_filt))
        self.play(FadeIn(grp_vlm))
        self.play(Create(a_gen_vlm), Create(a_vlm_filt))
        self.play(FadeIn(grp_filt_imgs))
        self.next_slide()

        # 4. Lưu vào CSDL tổng hợp
        self.play(Create(a_filt_db))
        self.play(FadeIn(grp_db))
        self.next_slide()

        # 5. Xuất ra Step 3 để Finetune
        self.play(Create(a_db_s3))
        self.play(FadeIn(step3))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 32 — MODULE 29: COARSE TO FINE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module29_CoarseToFine(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề slide
        title = slide_title("From coarse to fine-grained")
        
        # 2. Banner góc trên bên phải (Test-time techniques)
        banner_bg = RoundedRectangle(
            width=2.8, height=0.8, corner_radius=0.1, 
            fill_color=ManimColor("#6A3B4C"), # Màu đỏ mận/hồng tối (chống chói trên nền đen)
            fill_opacity=0.8, stroke_width=1, stroke_color=ManimColor("#E07A5F")
        )
        banner_lbl = Text(
            "Test-time\ntechniques", 
            font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL, line_spacing=1.2
        ).move_to(banner_bg)
        banner = VGroup(banner_bg, banner_lbl).to_corner(UR, buff=0.4)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG HỘP THÔNG ĐIỆP TRUNG TÂM
        # ─────────────────────────────────────────────────────────────────────
        
        msg_bg = Rectangle(
            width=8.0, height=1.0, 
            fill_color=ManimColor("#1A2B4C"), # Màu xanh dương tối
            fill_opacity=1, stroke_width=0
        )
        
        # Dùng t2c để tô màu từng phần của từ khóa
        msg_text = Text(
            "Coarse-to-fine detail evolution during denoising",
            font=Theme.FONT_BODY, font_size=26, color=Theme.NEUTRAL,
            t2c={
                "Coarse": Theme.ACCENT_RED,
                "fine": Theme.PRIMARY
            }
        ).move_to(msg_bg)
        
        msg_box = VGroup(msg_bg, msg_text)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG TRỤC THỜI GIAN (TIMELINE) VÀ CÁC MỐC
        # ─────────────────────────────────────────────────────────────────────
        
        # Trục chính
        timeline_arrow = Arrow(
            LEFT * 6, RIGHT * 6, 
            buff=0, stroke_width=8, color=Theme.NEUTRAL, 
            max_stroke_width_to_length_ratio=999, tip_length=0.3
        )
        t_lbl = Text("t", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, slant="ITALIC")
        t_lbl.next_to(timeline_arrow.get_end(), DOWN+RIGHT, buff=0.1)

        # Trích xuất 4 điểm tọa độ dọc theo trục arrow
        pt_0 = timeline_arrow.get_start()
        pt_1 = timeline_arrow.point_from_proportion(0.35)
        pt_2 = timeline_arrow.point_from_proportion(0.68)
        pt_3 = timeline_arrow.point_from_proportion(0.92)

        # Tạo các Dot mốc thời gian (Mốc đầu to hơn)
        dots = VGroup(
            Dot(pt_0, radius=0.18, color=Theme.NEUTRAL),
            Dot(pt_1, radius=0.08, color=Theme.NEUTRAL),
            Dot(pt_2, radius=0.08, color=Theme.NEUTRAL),
            Dot(pt_3, radius=0.08, color=Theme.NEUTRAL)
        )

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: NHÃN CHO CÁC MỐC (SỬ DỤNG MATCH_Y ĐỂ ÉP THẲNG HÀNG)
        # ─────────────────────────────────────────────────────────────────────
        
        kw_text = {"font": Theme.FONT_BODY, "font_size": 22, "line_spacing": 1.2}

        # --- Nhãn Hàng Trên ---
        top_lbl_0 = Text("Coarse\nsub-prompts", color=Theme.ACCENT_RED, **kw_text)
        top_lbl_0.next_to(dots[0], UP, buff=0.4)

        top_lbl_3 = Text("Fine-grained\nsub-prompts", color=Theme.PRIMARY, **kw_text)
        top_lbl_3.next_to(dots[3], UP, buff=0.4)
        top_lbl_3.match_y(top_lbl_0) # Khóa trục Y an toàn

        # --- Nhãn Hàng Dưới ---
        bot_lbl_0 = Text("(scene\nlayout)", color=Theme.NEUTRAL, **kw_text)
        bot_lbl_0.next_to(dots[0], DOWN, buff=0.4)

        bot_lbl_1 = Text("(object + spatial\nrelations)", color=Theme.NEUTRAL, **kw_text)
        bot_lbl_1.next_to(dots[1], DOWN, buff=0.4)
        
        bot_lbl_2 = Text("(object + spatial\ndetails)", color=Theme.NEUTRAL, **kw_text)
        bot_lbl_2.next_to(dots[2], DOWN, buff=0.4)

        # Ép toàn bộ hàng dưới thẳng hàng với bot_lbl_0
        bot_lbl_1.match_y(bot_lbl_0)
        bot_lbl_2.match_y(bot_lbl_0)

        # Gom nhóm Timeline
        timeline_group = VGroup(
            timeline_arrow, t_lbl, dots, 
            top_lbl_0, top_lbl_3, bot_lbl_0, bot_lbl_1, bot_lbl_2
        )

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: GOM TỔNG THỂ VÀ CĂN CHỈNH AN TOÀN TRÊN MÀN HÌNH
        # ─────────────────────────────────────────────────────────────────────
        
        all_content = VGroup(msg_box, timeline_group).arrange(DOWN, buff=1.5)
        
        # Giới hạn kích thước tránh tràn màn hình (Width an toàn: 13.5, Height: 7.0)
        all_content.set_width(13.0)
        all_content.center().shift(DOWN * 0.2)

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        
        # 1. Hiện tiêu đề và banner
        self.play(Write(title), FadeIn(banner))
        self.next_slide()

        # 2. Hiện hộp thông điệp trung tâm
        self.play(FadeIn(msg_bg), Write(msg_text))
        self.next_slide()

        # 3. Vẽ trục thời gian
        self.play(GrowArrow(timeline_arrow), FadeIn(t_lbl), run_time=1.5)
        self.next_slide()

        # 4. Hiển thị tịnh tiến từ Coarse (Trái) sang Fine (Phải)
        # Mốc 1: Coarse
        self.play(
            GrowFromCenter(dots[0]),
            FadeIn(top_lbl_0, shift=UP*0.2),
            FadeIn(bot_lbl_0, shift=DOWN*0.2)
        )
        self.next_slide()

        # Mốc 2 & 3: Quá trình tiến hóa (Evolution)
        self.play(
            GrowFromCenter(dots[1]), FadeIn(bot_lbl_1, shift=DOWN*0.2)
        )
        self.play(
            GrowFromCenter(dots[2]), FadeIn(bot_lbl_2, shift=DOWN*0.2)
        )
        self.next_slide()

        # Mốc 4: Fine-grained
        self.play(
            GrowFromCenter(dots[3]),
            FadeIn(top_lbl_3, shift=UP*0.2)
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 33 — MODULE 30: PROGRESSIVE DETAILING & INTERPOLATION  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module30_ProgressiveDetailing(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        title = slide_title("From coarse to fine-grained")

        # ─────────────────────────────────────────────────────────────────────
        # HÀM HỖ TRỢ ĐÃ ĐƯỢC THIẾT KẾ LẠI (GIẢI QUYẾT TRIỆT ĐỂ LỖI)
        # ─────────────────────────────────────────────────────────────────────
        
        def route_arrow(start_pt, end_pt, mid_y, color=Theme.NEUTRAL, stroke_w=3):
            """Mũi tên đi luồng 3 khúc: Dọc -> Ngang -> Dọc (Đi qua hành lang an toàn)"""
            p1 = start_pt
            p2 = np.array([start_pt[0], mid_y, 0])
            p3 = np.array([end_pt[0], mid_y, 0])
            p4 = end_pt
            return VGroup(
                Line(p1, p2, color=color, stroke_width=stroke_w),
                Line(p2, p3, color=color, stroke_width=stroke_w),
                Arrow(p3, p4, color=color, stroke_width=stroke_w, buff=0, tip_length=0.15)
            )

        def build_trapezoid(color_fill: str, is_encoder=True):
            """Chỉ tạo Hình khối (Shape) riêng biệt, Text sẽ được gán sau"""
            w_w, w_n, h = 1.2, 0.6, 1.2
            pts = [[-w_w/2, h/2, 0], [w_w/2, h/2, 0], [w_n/2, -h/2, 0], [-w_n/2, -h/2, 0]] if is_encoder \
                  else [[-w_n/2, h/2, 0], [w_n/2, h/2, 0], [w_w/2, -h/2, 0], [-w_w/2, -h/2, 0]]
            poly = Polygon(*pts, fill_color=ManimColor(color_fill), fill_opacity=0.9, stroke_color=WHITE, stroke_width=1)
            return poly.rotate(PI/2 if is_encoder else -PI/2)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: KHỞI TẠO HÀNG TRÊN (PROMPTS)
        # ─────────────────────────────────────────────────────────────────────
        
        coarse_txt = Text(
            "1. A red tree...\n2. ...golden hour\n3. ...stands out\n4. ...dense forest",
            font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL, line_spacing=1.3
        )
        coarse_box = RoundedRectangle(width=coarse_txt.width + 0.6, height=coarse_txt.height + 0.6, corner_radius=0.2, fill_color=Theme.BOX_FILL, stroke_color=Theme.DIM)
        coarse_txt.move_to(coarse_box)
        c_lbl = Text("Coarse sub-prompts", font_size=16, color=Theme.ACCENT_RED).next_to(coarse_box, UP, buff=0.1)
        grp_coarse = VGroup(coarse_box, coarse_txt, c_lbl)

        llm_circle = Circle(radius=0.5, fill_color=ManimColor("#4A8A52"), fill_opacity=1, stroke_color=WHITE)
        llm_txt = Text("LLM", font_size=20, color=WHITE, weight="BOLD").move_to(llm_circle)
        grp_llm = VGroup(llm_circle, llm_txt)

        fine_txt = Text(
            "In a lush, dense forest bathed\nin soft golden hour light, vibrant\ngreen trees tower majestically...",
            font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL, line_spacing=1.3
        )
        fine_box = RoundedRectangle(width=fine_txt.width + 0.6, height=fine_txt.height + 0.6, corner_radius=0.2, fill_color=Theme.BOX_FILL, stroke_color=Theme.DIM)
        fine_txt.move_to(fine_box)
        f_lbl = Text("Fine-grained sub-prompt", font_size=16, color=Theme.PRIMARY).next_to(fine_box, UP, buff=0.1)
        grp_fine = VGroup(fine_box, fine_txt, f_lbl)

        row_top = VGroup(grp_coarse, grp_llm, grp_fine).arrange(RIGHT, buff=0.8)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: KHỞI TẠO HÀNG DƯỚI (TÁCH BIỆT SHAPE VÀ TEXT ĐỂ FIX LỖI LỆCH)
        # ─────────────────────────────────────────────────────────────────────
        
        # 2.1 - Khởi tạo các khung xương (Shapes)
        sub_lbl = Text("Sub-\nPrompts", font_size=20, color=Theme.NEUTRAL, line_spacing=1.2)
        te_poly = build_trapezoid("#D485B8", is_encoder=True)
        p_math = MathTex(r"\mathbf{p}", font_size=28, color=Theme.NEUTRAL)
        interp_box = Rectangle(width=1.5, height=1.2, fill_color=ManimColor("#A3C4ED"), fill_opacity=0.9, stroke_color=Theme.PRIMARY)
        unet_bg = Rectangle(width=2.8, height=1.5, fill_color=ManimColor("#DCE8FA"), fill_opacity=0.8, stroke_color=ManimColor("#85B57A"))
        dec_poly = build_trapezoid("#E07A5F", is_encoder=False)
        img_box = Rectangle(width=1.2, height=1.2, fill_color=ManimColor("#B294C7"), fill_opacity=0.9, stroke_color=WHITE)

        # XẾP KHUNG XƯƠNG THEO HÀNG NGANG TRƯỚC (QUAN TRỌNG NHẤT)
        core_shapes = VGroup(sub_lbl, te_poly, p_math, interp_box, unet_bg, dec_poly, img_box).arrange(RIGHT, buff=0.5)

        # 2.2 - Khởi tạo chữ (Text) và ghim chính xác vào khung xương đã chốt tọa độ
        te_sym = MathTex(r"\tau_\theta", font_size=24, color=BLACK).move_to(te_poly)
        te_txt = Text("Text encoder", font_size=14, color=Theme.DIM).next_to(te_poly, DOWN, buff=0.2)
        
        interp_math = MathTex(r"I(\mathbf{p}, t)", font_size=28, color=BLACK).move_to(interp_box)
        interp_lbl = VGroup(MathTex(r"t: T \to 1", font_size=20), Text("Interpolation", font_size=14)).arrange(DOWN, buff=0.1).next_to(interp_box, DOWN, buff=0.2)
        
        unet_txt = Text("Denoising U-Net", font_size=18, color=BLACK).move_to(unet_bg)
        
        dec_sym = MathTex(r"\mathcal{D}", font_size=24, color=BLACK).move_to(dec_poly)
        img_txt = Text("Image", font_size=20, color=BLACK).move_to(img_box)

        # Gom lại thành hàng hoàn chỉnh (VGroup lúc này đã chuẩn tọa độ)
        row_bot = VGroup(core_shapes, te_sym, te_txt, interp_math, interp_lbl, unet_txt, dec_sym, img_txt)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: QUY HOẠCH LƯỚI & ÉP TỶ LỆ CHỐNG TRÀN
        # ─────────────────────────────────────────────────────────────────────
        
        # Khoảng cách buff=1.5 tạo ra một "hành lang" rộng rãi giữa 2 hàng
        all_diagram = VGroup(row_top, row_bot).arrange(DOWN, buff=1.5)
        
        all_diagram.set_width(13.5)
        if all_diagram.height > 6.0:
            all_diagram.set_height(6.0)
            
        all_diagram.center().shift(DOWN * 0.2)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: VẼ MŨI TÊN
        # ─────────────────────────────────────────────────────────────────────
        
        c_line = Theme.NEUTRAL
        a_coarse_llm = Arrow(coarse_box.get_right(), llm_circle.get_left(), buff=0.1, color=c_line)
        a_llm_fine = Arrow(llm_circle.get_right(), fine_box.get_left(), buff=0.1, color=c_line)
        
        # TÍNH TOÁN HÀNH LANG AN TOÀN CHO MŨI TÊN TỪ TRÊN XUỐNG
        # mid_y nằm chính giữa khe hở của hàng trên và hàng dưới
        mid_y = (row_top.get_bottom()[1] + core_shapes.get_top()[1]) / 2

        a_down_c = route_arrow(coarse_box.get_bottom(), sub_lbl.get_top() + LEFT*0.1, mid_y, color=c_line)
        a_down_f = route_arrow(fine_box.get_bottom(), sub_lbl.get_top() + RIGHT*0.1, mid_y, color=c_line)

        # Mũi tên ngang (Chỉ neo vào Shape, đảm bảo cắt ngang chính giữa hộp)
        a_sub_te   = Arrow(sub_lbl.get_right(), te_poly.get_left(), buff=0.1, color=c_line)
        a_te_p     = Arrow(te_poly.get_right(), p_math.get_left(), buff=0.1, color=c_line)
        a_p_int    = Arrow(p_math.get_right(), interp_box.get_left(), buff=0.1, color=c_line)
        
        a_int_unet = Arrow(interp_box.get_right(), unet_bg.get_left(), buff=0.1, color=c_line)
        a_unet_dec = Arrow(unet_bg.get_right(), dec_poly.get_left(), buff=0.1, color=c_line)
        a_dec_img  = Arrow(dec_poly.get_right(), img_box.get_left(), buff=0.1, color=c_line)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 5: TẠO OVERLAY CLIP SPACE 
        # ─────────────────────────────────────────────────────────────────────
        
        # Đã fix opacity tuyệt đối = 1 để che triệt để
        overlay_bg = Rectangle(width=13.0, height=3.8, fill_color=ManimColor("#224DBA"), fill_opacity=1, stroke_width=0)
        overlay_bg.move_to(row_top.get_center()) 
        
        ov_title = Text("Similarity based sub-prompt weighting", font_size=28, color=Theme.ACCENT_RED).next_to(overlay_bg.get_top(), DOWN, buff=0.3)
        ov_math = MathTex(r"\text{Sim}_{\text{CLIP}}(p_3, p_2) > \text{Sim}_{\text{CLIP}}(p_2, p_1)", font_size=32).next_to(ov_title, DOWN, buff=0.2)
        
        # Mặt phẳng CLIP Space 3D
        plane = Polygon([-2.5, -1, 0], [1.5, -1, 0], [2.5, 1, 0], [-1.5, 1, 0], fill_color=ManimColor("#CDE0C4"), fill_opacity=0.9, stroke_color=Theme.DIM)
        plane_lbl = Text("CLIP Space", font_size=18, color=BLACK, slant="ITALIC").move_to(plane.get_bottom() + UP*0.2)
        
        d1 = Dot(plane.get_center() + LEFT*1.5, radius=0.1, color=Theme.ACCENT_GOLD)
        l1 = MathTex("p_1", color=BLACK).next_to(d1, UP, buff=0.1)
        d2 = Dot(plane.get_center() + UP*0.5, radius=0.1, color=Theme.ACCENT_GOLD)
        l2 = MathTex("p_2", color=BLACK).next_to(d2, UP, buff=0.1)
        d3 = Dot(plane.get_center() + RIGHT*1.0, radius=0.1, color=Theme.ACCENT_GOLD)
        l3 = MathTex("p_3", color=BLACK).next_to(d3, RIGHT, buff=0.1)
        
        plane_grp = VGroup(plane, plane_lbl, d1, l1, d2, l2, d3, l3).next_to(ov_math, DOWN, buff=0.4)
        
        overlay_grp = VGroup(overlay_bg, ov_title, ov_math, plane_grp)
        overlay_grp.set_z_index(100) # Đẩy lên lớp Layer trên cùng
        
        highlight_t = Ellipse(width=2.5, height=1.0, color=Theme.SUCCESS, stroke_width=4).move_to(interp_lbl)

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.next_slide()

        # --- STATE 1: Text Pipeline (Nửa bên trái của Denoising) ---
        self.play(FadeIn(grp_coarse))
        self.play(Create(a_coarse_llm), FadeIn(grp_llm))
        self.play(Create(a_llm_fine), FadeIn(grp_fine))
        
        self.play(Create(a_down_c), Create(a_down_f), FadeIn(sub_lbl))
        self.play(Create(a_sub_te), FadeIn(te_poly), FadeIn(te_sym), FadeIn(te_txt))
        self.play(Create(a_te_p), FadeIn(p_math))
        self.play(Create(a_p_int), FadeIn(interp_box), FadeIn(interp_math), FadeIn(interp_lbl))
        self.next_slide()

        # --- STATE 2: CLIP Space Overlay ---
        self.play(FadeIn(overlay_grp))
        self.play(Create(highlight_t))
        self.next_slide()

        # --- STATE 3: Diffusion Process (Hiển thị nửa bên phải) ---
        self.play(FadeOut(overlay_grp), FadeOut(highlight_t))
        self.play(Create(a_int_unet), FadeIn(unet_bg), FadeIn(unet_txt))
        self.play(Create(a_unet_dec), FadeIn(dec_poly), FadeIn(dec_sym))
        self.play(Create(a_dec_img), FadeIn(img_box), FadeIn(img_txt))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 34 — MODULE 31: DIFFUSION & FLOW-BASED MODELS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module31_DiffusionFlows(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề chính (Ghim sát góc trái trên)
        title = slide_title("Diffusion & Flow-based Models")
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: ĐỊNH NGHĨA CÁC HELPER ĐỒ HỌA VECTOR TỐI GIẢN
        # ─────────────────────────────────────────────────────────────────────
        
        def make_noise_box(width=1.3, height=1.3):
            # Tạo ô vuông nhiễu x_T giả lập bằng các chấm hạt ngẫu nhiên xác định
            box = Rectangle(width=width, height=height, stroke_color=Theme.NEUTRAL, stroke_width=2, fill_color=Theme.BG, fill_opacity=1)
            import random
            random.seed(42) # Seed cố định để tránh thay đổi giữa các lần render
            dots = VGroup()
            for _ in range(60):
                x = random.uniform(-width/2 + 0.1, width/2 - 0.1)
                y = random.uniform(-height/2 + 0.1, height/2 - 0.1)
                dot = Dot(point=[x, y, 0], radius=0.015, color=GRAY, fill_opacity=0.6)
                dots.add(dot)
            dots.move_to(box.get_center())
            label = Text("Noise\nx_T", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL).move_to(box.get_center())
            label_bg = Rectangle(width=label.width + 0.1, height=label.height + 0.1, fill_color=Theme.BG, fill_opacity=0.8, stroke_width=0)
            return VGroup(box, dots, label_bg, label)

        def make_noisy_box(width=1.3, height=1.3):
            # Tạo ô vuông chứa nhiễu trung gian x_t
            box = Rectangle(width=width, height=height, stroke_color=Theme.ACCENT_RED, stroke_width=2, fill_color=Theme.BOX_FILL, fill_opacity=1)
            label = Text("Noisy\nx_t", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_RED, weight="BOLD").move_to(box.get_center())
            import random
            random.seed(43)
            dots = VGroup()
            for _ in range(25):
                x = random.uniform(-width/2 + 0.1, width/2 - 0.1)
                y = random.uniform(-height/2 + 0.1, height/2 - 0.1)
                dot = Dot(point=[x, y, 0], radius=0.015, color=GRAY, fill_opacity=0.5)
                dots.add(dot)
            dots.move_to(box.get_center())
            return VGroup(box, dots, label)

        def make_clean_box(width=1.3, height=1.3):
            # Tạo ô vuông biểu diễn ảnh sạch gốc x_0
            box = Rectangle(width=width, height=height, stroke_color=Theme.PRIMARY, stroke_width=2, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1)
            label = Text("Data\nx_0", font=Theme.FONT_BODY, font_size=16, color=Theme.PRIMARY, weight="BOLD").move_to(box.get_center())
            return VGroup(box, label)

        def make_theta_box(width=0.7, height=1.3):
            # Khối tham số mạng phi tuyến theta (Khối màu xanh lục đậm dọc)
            box = Rectangle(width=width, height=height, stroke_color=Theme.NEUTRAL, stroke_width=1.5, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1)
            label = MathTex(r"\theta", font_size=32, color=Theme.PRIMARY).move_to(box.get_center())
            return VGroup(box, label)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG SƠ ĐỒ VÀ PHƯƠNG TRÌNH TOÁN HỌC
        # ─────────────────────────────────────────────────────────────────────
        
        # Sắp xếp các thành phần luồng ngang (Trái sang Phải)
        x_T = make_noise_box()
        theta1 = make_theta_box()
        x_t = make_noisy_box()
        dots = Text("...", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        theta2 = make_theta_box()
        x_0 = make_clean_box()
        
        flow_elements = VGroup(x_T, theta1, x_t, dots, theta2, x_0).arrange(RIGHT, buff=0.35)
        diagram_group = VGroup(flow_elements)

        # Định nghĩa các phương trình toán học ở cột bên phải
        eq1 = MathTex(
            r"\mathcal{L} = \mathbb{E}_t \left[ \omega_t \| \mathbf{D}_\theta(\mathbf{x}_t) - \mathbf{x}_0 \|_2^2 \right]",
            font_size=24, color=Theme.NEUTRAL
        )
        eq2 = MathTex(
            r"\mathbf{x}_{t-\Delta t} = \mathbf{x}_t + g(t)^2 s(\mathbf{x}_t, t) \Delta t + g(t)\sqrt{\Delta t} \, \epsilon_t",
            font_size=22, color=Theme.NEUTRAL
        )
        eq3 = MathTex(
            r"s_\theta(\mathbf{x}_t, t) \approx \frac{\mathbf{D}_\theta(\mathbf{x}_t, t) - \mathbf{x}_t}{\sigma_t}",
            font_size=22, color=Theme.NEUTRAL
        )
        
        # Sắp xếp dọc cột phương trình bên phải
        math_col = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM NHÓM VÀ KHỐNG CHẾ KÍCH THƯỚC TOÀN CỤC (TRÁNH OVERFLOW)
        # ─────────────────────────────────────────────────────────────────────
        
        all_content = VGroup(diagram_group, math_col).arrange(RIGHT, buff=0.8)
        all_content.set_width(13.2) # Giới hạn tuyệt đối chiều rộng sơ đồ
        all_content.center()
        all_content.shift(DOWN * 0.3) # Hạ thấp tạo khoảng trống phía trên cho tiêu đề slide

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: LIÊN KẾT MŨI TÊN CHÍNH XÁC (TÍNH TỌA ĐỘ SAU KHI SCALE)
        # ─────────────────────────────────────────────────────────────────────
        
        # Mũi tên tiến trình sinh (Denoising Flow - Màu đỏ san hô)
        arr_color = Theme.ACCENT_RED
        arrow1 = Arrow(x_T.get_right(), theta1.get_left(), buff=0.08, color=arr_color, stroke_width=3, tip_length=0.12)
        arrow2 = Arrow(theta1.get_right(), x_t.get_left(), buff=0.08, color=arr_color, stroke_width=3, tip_length=0.12)
        arrow3 = Arrow(x_t.get_right(), dots.get_left(), buff=0.08, color=Theme.DIM, stroke_width=2)
        arrow4 = Arrow(dots.get_right(), theta2.get_left(), buff=0.08, color=Theme.DIM, stroke_width=2)
        arrow5 = Arrow(theta2.get_right(), x_0.get_left(), buff=0.08, color=arr_color, stroke_width=3, tip_length=0.12)

        # Các mũi tên cong biểu diễn quá trình khuếch tán thuận ("Add Noise" - Màu vàng)
        curve1 = CurvedArrow(
            start_point=x_0.get_bottom() + LEFT * 0.1, 
            end_point=x_t.get_bottom() + RIGHT * 0.1, 
            angle=0.6, 
            color=Theme.ACCENT_GOLD,
            stroke_width=2.5,
            tip_length=0.12
        )
        
        curve2 = CurvedArrow(
            start_point=x_0.get_bottom() + LEFT * 0.2, 
            end_point=x_T.get_bottom() + RIGHT * 0.2, 
            angle=0.4, 
            color=Theme.ACCENT_GOLD,
            stroke_width=2.5,
            tip_length=0.12
        )
        
        add_noise_label = Text("Add Noise", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_GOLD, weight="BOLD")
        add_noise_label.next_to(curve2, DOWN, buff=0.12)

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ TRÊN SLIDE (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        # Bước 1: Hiện tiêu đề chính
        self.play(Write(title))
        self.next_slide()
        
        # Bước 2: Hiển thị tuần tự luồng Generation (từ nhiễu x_T sang ảnh sạch x_0)
        self.play(
            FadeIn(x_T), FadeIn(theta1), FadeIn(x_t), FadeIn(dots), FadeIn(theta2), FadeIn(x_0),
            Create(arrow1), Create(arrow2), Create(arrow3), Create(arrow4), Create(arrow5)
        )
        self.next_slide()
        
        # Bước 3: Xuất hiện tiến trình ngược "Add Noise" (Khuếch tán thuận)
        self.play(
            Create(curve1),
            Create(curve2),
            FadeIn(add_noise_label)
        )
        self.next_slide()
        
        # Bước 4: Trình bày cơ sở toán học từng dòng
        self.play(Write(eq1))
        self.next_slide()
        self.play(Write(eq2))
        self.play(Write(eq3))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 35 — MODULE 32: AUTOREGRESSIVE MODELS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module32_Autoregressive(Slide):
    def construct(self):
        # 1. Thiết lập màu nền slide
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề slide ghim ở góc trên bên trái (Y ≈ 3.2 -> 3.5)
        title = slide_title("Autoregressive Models")
        
        # =====================================================================
        # CHUYỂN CẢNH 1: DISCRETE VISUAL TOKENIZATION (VQ-VAE FLOW)
        # =====================================================================
        
        image_box = RoundedBox(
            lines=["Input Image", "(X)"], 
            width=2.0, height=1.4, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY
        )
        
        enc_box = RoundedBox(
            lines=["Encoder", "(E)"], 
            width=1.5, height=0.9, fill_color=Theme.BOX_FILL, stroke_color=Theme.NEUTRAL
        )
        
        # Chuỗi token rời rạc xếp dọc
        token_sequence = VGroup(
            RoundedBox(lines=["x1"], width=0.6, height=0.45, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16),
            RoundedBox(lines=["x2"], width=0.6, height=0.45, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16),
            Text("...", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL),
            RoundedBox(lines=["xN"], width=0.6, height=0.45, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16)
        ).arrange(DOWN, buff=0.12)
        
        dec_box = RoundedBox(
            lines=["Decoder", "(D)"], 
            width=1.5, height=0.9, fill_color=Theme.BOX_FILL, stroke_color=Theme.NEUTRAL
        )
        
        recon_box = RoundedBox(
            lines=["Reconstructed", "Image"], 
            width=2.0, height=1.4, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY
        )
        
        # GIẢI PHÁP 2: Tăng buff ngang lên 1.3 để tạo khoảng trống rộng rãi cho văn bản nằm giữa, không bị đè biên
        vq_flow = VGroup(image_box, enc_box, token_sequence, dec_box, recon_box).arrange(RIGHT, buff=1.3)
        vq_flow.set_width(13.0)
        vq_flow.center()
        vq_flow.shift(DOWN * 0.2)
        
        # Vẽ các mũi tên liên kết sau khi đã scale
        arr1 = Arrow(image_box.get_right(), enc_box.get_left(), color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        arr2 = Arrow(enc_box.get_right(), token_sequence.get_left(), color=Theme.PRIMARY, stroke_width=2.5, tip_length=0.12)
        arr3 = Arrow(token_sequence.get_right(), dec_box.get_left(), color=Theme.PRIMARY, stroke_width=2.5, tip_length=0.12)
        arr4 = Arrow(dec_box.get_right(), recon_box.get_left(), color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        
        # GIẢI PHÁP 1: Thiết lập .set_z_index(3) để đẩy chữ và mũi tên lên lớp hiển thị trên cùng (Front Layer)
        lbl_comp = Text("Compression", font=Theme.FONT_BODY, font_size=14, color=Theme.PRIMARY).next_to(arr2, UP, buff=0.08)
        lbl_comp.set_z_index(3)
        
        lbl_recon = Text("Reconstruction", font=Theme.FONT_BODY, font_size=14, color=Theme.PRIMARY).next_to(arr3, UP, buff=0.08)
        lbl_recon.set_z_index(3)
        
        # Đồng thời nâng z_index của các mũi tên đi kèm để có sự nhất quán trực quan
        for arr in [arr1, arr2, arr3, arr4]:
            arr.set_z_index(2)
            
        # --- Chạy kịch bản Trực quan hóa VQ-VAE ---
        self.play(Write(title))
        self.play(
            FadeIn(image_box), FadeIn(enc_box), FadeIn(token_sequence), FadeIn(dec_box), FadeIn(recon_box)
        )
        self.play(
            Create(arr1), Create(arr2), Create(arr3), Create(arr4),
            Write(lbl_comp), Write(lbl_recon)
        )
        self.next_slide() 
        
        # =====================================================================
        # CHUYỂN CẢNH 2: AUTOREGRESSIVE SEQUENCE MODELING (ĐÃ FIX LỖI OVERFLOW)
        # =====================================================================
        
        # Dọn dẹp chuyển cảnh 1
        self.play(
            FadeOut(vq_flow), FadeOut(arr1), FadeOut(arr2), FadeOut(arr3), FadeOut(arr4),
            FadeOut(lbl_comp), FadeOut(lbl_recon)
        )
        
        # Tạo chuỗi Input Tokens
        input_s = RoundedBox(lines=["[s]"], width=0.7, height=0.5, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_GOLD, font_size=16)
        input_x1 = RoundedBox(lines=["x1"], width=0.7, height=0.5, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16)
        input_x2 = RoundedBox(lines=["x2"], width=0.7, height=0.5, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16)
        input_dots = Text("...", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL)
        input_xN_1 = RoundedBox(lines=["xN-1"], width=0.9, height=0.5, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16)
        
        inputs_group = VGroup(input_s, input_x1, input_x2, input_dots, input_xN_1).arrange(RIGHT, buff=0.5)
        
        # Khối Transformer trung tâm
        ar_model = RoundedBox(
            lines=["Autoregressive Transformer Model"],
            width=6.2, height=1.0, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY, stroke_width=2.5
        )
        
        # Tạo chuỗi Output Tokens dự đoán
        output_x1 = RoundedBox(lines=["x1"], width=0.7, height=0.5, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16)
        output_x2 = RoundedBox(lines=["x2"], width=0.7, height=0.5, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16)
        output_x3 = RoundedBox(lines=["x3"], width=0.7, height=0.5, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16)
        output_dots = Text("...", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL)
        output_xN = RoundedBox(lines=["xN"], width=0.7, height=0.5, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS, font_size=16)
        
        outputs_group = VGroup(output_x1, output_x2, output_x3, output_dots, output_xN).arrange(RIGHT, buff=0.5)
        
        # Sắp xếp sơ đồ tự hồi quy dạng 3 tầng đứng
        ar_diagram = VGroup(inputs_group, ar_model, outputs_group).arrange(DOWN, buff=0.8)
        
        # Khống chế chiều cao tổng thể của sơ đồ ở mức an toàn tối đa là 4.2 để chống đè tiêu đề
        ar_diagram.set_height(4.2)
        ar_diagram.center() 
        
        # Tạo các mũi tên dọc liên kết
        arrow_in_s = Arrow(input_s.get_bottom(), [input_s.get_x(), ar_model.get_top()[1], 0], color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        arrow_in_x1 = Arrow(input_x1.get_bottom(), [input_x1.get_x(), ar_model.get_top()[1], 0], color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        arrow_in_x2 = Arrow(input_x2.get_bottom(), [input_x2.get_x(), ar_model.get_top()[1], 0], color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        arrow_in_xN_1 = Arrow(input_xN_1.get_bottom(), [input_xN_1.get_x(), ar_model.get_top()[1], 0], color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        
        arrow_out_x1 = Arrow([output_x1.get_x(), ar_model.get_bottom()[1], 0], output_x1.get_top(), color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        arrow_out_x2 = Arrow([output_x2.get_x(), ar_model.get_bottom()[1], 0], output_x2.get_top(), color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        arrow_out_x3 = Arrow([output_x3.get_x(), ar_model.get_bottom()[1], 0], output_x3.get_top(), color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        arrow_out_xN = Arrow([output_xN.get_x(), ar_model.get_bottom()[1], 0], output_xN.get_top(), color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        
        # Vòng lặp phản hồi tự hồi quy (Causal feedback) uốn cong ra phía bên trái 
        from manim import CurvedArrow
        feedback_x1 = CurvedArrow(
            start_point=output_x1.get_top() + LEFT * 0.05,
            end_point=input_x1.get_bottom() + LEFT * 0.05,
            angle=0.8,
            color=Theme.ACCENT_GOLD,
            stroke_width=2,
            tip_length=0.08
        )
        feedback_x2 = CurvedArrow(
            start_point=output_x2.get_top() + LEFT * 0.05,
            end_point=input_x2.get_bottom() + LEFT * 0.05,
            angle=0.8,
            color=Theme.ACCENT_GOLD,
            stroke_width=2,
            tip_length=0.08
        )
        
        # Phương trình Loss đặt ở sát biên dưới an toàn
        loss_formula = MathTex(
            r"\mathcal{L} = \log P(X) = \sum_{i=1}^{N} \log P(X_i \mid X_{<i})",
            font_size=32,
            color=Theme.NEUTRAL
        ).to_edge(DOWN, buff=0.35)
        
        # --- Chạy kịch bản Trực quan hóa Autoregressive ---
        self.play(
            FadeIn(inputs_group),
            FadeIn(ar_model),
            FadeIn(outputs_group)
        )
        self.play(
            Create(arrow_in_s), Create(arrow_in_x1), Create(arrow_in_x2), Create(arrow_in_xN_1),
            Create(arrow_out_x1), Create(arrow_out_x2), Create(arrow_out_x3), Create(arrow_out_xN)
        )
        self.next_slide()
        
        # Hiển thị các đường vòng lặp hồi quy nhân quả uốn cong mượt mà bên rìa trái
        self.play(
            Create(feedback_x1),
            Create(feedback_x2)
        )
        self.next_slide()
        
        # Viết phương trình tối ưu hóa mục tiêu toán học ở chân slide
        self.play(Write(loss_formula))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 36 — MODULE 33: AR COMBINED WITH DIFFUSION  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module33_ARDiffusion(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # ─────────────────────────────────────────────────────────────────────
        # VÙNG HEADER: CỐ ĐỊNH PHÍA TRÊN, KHÔNG BAO GIỜ DI CHUYỂN
        # ─────────────────────────────────────────────────────────────────────
        # Sửa lỗi 1: Rút ngắn tiêu đề và scale nhỏ lại để chống tràn viền
        title = slide_title("Autoregressive Models + Diffusion?").scale(0.85)
        
        q1 = Text(
            "• How to model p(x) in the continuous space with AR?", 
            font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.4)
        
        q2 = Text(
            "  • Two core problems: (1) Powerful Function (2) Train-test Mismatch", 
            font=Theme.FONT_BODY, font_size=24, color=Theme.DIM, weight="BOLD"
        ).next_to(q1, DOWN, aligned_edge=LEFT, buff=0.2)
        
        header_group = VGroup(title, q1, q2)
        
        # ─────────────────────────────────────────────────────────────────────
        # TỌA ĐỘ NEO AN TOÀN (Tránh Lỗi 4 & Lỗi 5)
        # ─────────────────────────────────────────────────────────────────────
        # Đồ họa luôn nằm bên trái, Công thức luôn nằm bên phải. 
        LEFT_ZONE = [-3.5, -1.0, 0]
        RIGHT_ZONE = [3.5, -1.0, 0]

        # =====================================================================
        # SCENE 1: AR -> DIFFUSION (e.g., MAR, Llama-Gen)
        # =====================================================================
        
        # --- Đồ họa Scene 1 ---
        # 1. Chuỗi AR
        ar_seq = VGroup(*[
            Square(side_length=0.6, fill_color=ManimColor("#9FA8DA"), fill_opacity=0.8, stroke_color=Theme.NEUTRAL)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.1)
        # Khối đang xét (Màu cam)
        ar_seq[3].set_fill(Theme.ACCENT_GOLD)
        # Khối chưa dự đoán (Màu nhạt)
        ar_seq[4].set_fill(Theme.DIM)
        
        # Mũi tên AR (từ quá khứ tới hiện tại)
        from manim import CurvedArrow
        ar_arrows = VGroup(*[
            CurvedArrow(ar_seq[i].get_top(), ar_seq[3].get_top(), angle=-1.0, color=Theme.NEUTRAL, stroke_width=2)
            for i in range(3)
        ])
        
        # 2. Khối Diffusion (MLP dự đoán nhiễu)
        mlp_box = RoundedBox(lines=["MLP"], width=1.5, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY)
        mlp_box.next_to(ar_seq[3], DOWN, buff=0.8)
        
        arr_to_mlp = Arrow(ar_seq[3].get_bottom(), mlp_box.get_top(), color=Theme.ACCENT_GOLD, stroke_width=2, tip_length=0.1)
        lbl_z = Text("condition z", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL).next_to(arr_to_mlp, LEFT, buff=0.1)
        
        xt_label = Text("noisy x_t", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_RED).next_to(mlp_box, LEFT, buff=0.5)
        arr_xt = Arrow(xt_label.get_right(), mlp_box.get_left(), color=Theme.ACCENT_RED, stroke_width=2, tip_length=0.1)
        
        eps_label = MathTex(r"\epsilon", font_size=32, color=Theme.NEUTRAL).next_to(mlp_box, RIGHT, buff=0.5)
        arr_eps = Arrow(mlp_box.get_right(), eps_label.get_left(), color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        
        diff_loss_lbl = Text("diffusion loss for p(x|z)", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM).next_to(mlp_box, DOWN, buff=0.3)
        
        # Đóng gói và ép khung (Tránh Lỗi 3)
        scene1_diagram = VGroup(ar_seq, ar_arrows, mlp_box, arr_to_mlp, lbl_z, xt_label, arr_xt, eps_label, arr_eps, diff_loss_lbl)
        scene1_diagram.set_height(4.0)
        scene1_diagram.move_to(LEFT_ZONE)
        
        # --- Công thức Scene 1 ---
        s1_math = MathTex(r"p(\mathbf{x}) =", r"\prod_i", r"\prod_t", r"p(\mathbf{x}_i^t \mid \mathbf{x}_i^{t+1}, \mathbf{x}_{<i})", font_size=40)
        
        # Sửa lỗi 2: Dịch chuyển chéo (offset) hai nhãn chữ để triệt tiêu sự chồng lấn
        s1_lbl_ar = Text("AR", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_RED, weight="BOLD")
        s1_lbl_ar.next_to(s1_math[1], DOWN, buff=0.3).shift(LEFT * 0.25)
        
        s1_lbl_diff = Text("Diffusion", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_RED, weight="BOLD")
        s1_lbl_diff.next_to(s1_math[2], DOWN, buff=0.3).shift(RIGHT * 0.4)
        
        scene1_math = VGroup(s1_math, s1_lbl_ar, s1_lbl_diff).move_to(RIGHT_ZONE)

        # =====================================================================
        # SCENE 2: DIFFUSION FORCING / FULL-SEQUENCE DIFFUSION
        # =====================================================================
        
        # --- Đồ họa Scene 2 ---
        grid = VGroup(*[
            VGroup(*[
                Square(side_length=0.6, fill_color=Theme.BG, stroke_color=Theme.NEUTRAL, stroke_width=2) 
                for _ in range(3)
            ]).arrange(RIGHT, buff=0.4)
            for _ in range(3)
        ]).arrange(DOWN, buff=0.5)
        
        grid[0][1].set_fill(ManimColor("#BBDEFB"), opacity=1)
        grid[1][1].set_fill(ManimColor("#1976D2"), opacity=1)
        grid[2][1].set_fill(Theme.BOX_FILL_ALT, opacity=1)
        
        s2_arrows = VGroup()
        for i in range(2):
            for j in range(3):
                s2_arrows.add(Arrow(grid[i][j].get_bottom(), grid[i+1][j].get_top(), color=Theme.PRIMARY, stroke_width=2, tip_length=0.1))
        for i in range(3):
            for j in range(2):
                s2_arrows.add(Arrow(grid[i][j].get_right(), grid[i][j+1].get_left(), color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1))
                
        lbl_diff_forcing = Text("Diffusion Forcing Grid", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD").next_to(grid, UP, buff=0.3)
        
        scene2_diagram = VGroup(grid, s2_arrows, lbl_diff_forcing)
        scene2_diagram.set_height(4.2)
        scene2_diagram.move_to(LEFT_ZONE)
        
        # --- Công thức Scene 2 ---
        s2_math = MathTex(r"p(\mathbf{x}) =", r"\prod_t", r"\prod_i", r"p(\mathbf{x}_i^t \mid \mathbf{x}_i^{t+1}, \mathbf{x}_{<i}^{\tau_i})", font_size=40)
        
        # Sửa lỗi 2: Dịch chuyển offset chống chồng chữ cho Scene 2
        s2_lbl_diff = Text("Diffusion", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_RED, weight="BOLD")
        s2_lbl_diff.next_to(s2_math[1], DOWN, buff=0.3).shift(LEFT * 0.4)
        
        s2_lbl_ar = Text("AR", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_RED, weight="BOLD")
        s2_lbl_ar.next_to(s2_math[2], DOWN, buff=0.3).shift(RIGHT * 0.25)
        
        scene2_math = VGroup(s2_math, s2_lbl_diff, s2_lbl_ar).move_to(RIGHT_ZONE)

        # =====================================================================
        # SCENE 3: DART (Denoising Auto-Regressive Transformer)
        # =====================================================================
        
        # --- Đồ họa Scene 3 ---
        ctx_box = RoundedBox(lines=["Context", "Encoder"], width=1.5, height=1.0, fill_color=ManimColor("#D1C4E9"), text_color=BLACK)
        dart_box = RoundedBox(lines=["Denoising Auto-Regressive", "Transformer (DART)"], width=4.0, height=1.0, fill_color=ManimColor("#C8E6C9"), stroke_color=Theme.SUCCESS, text_color=BLACK)
        
        s3_core = VGroup(ctx_box, dart_box).arrange(RIGHT, buff=0.6)
        arr_ctx_dart = Arrow(ctx_box.get_right(), dart_box.get_left(), color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1)
        
        in_patches = VGroup(*[
            Square(side_length=0.6, fill_color=GRAY, fill_opacity=1, stroke_color=Theme.ACCENT_RED)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.5).next_to(dart_box, DOWN, buff=0.6)
        
        out_patches = VGroup(*[
            Square(side_length=0.6, fill_color=Theme.PRIMARY, fill_opacity=0.6, stroke_color=Theme.PRIMARY)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.5).next_to(dart_box, UP, buff=0.6)
        
        out_patches[2].set_stroke(color=Theme.ACCENT_GOLD, width=4)
        out_patches[2].set_fill(Theme.ACCENT_GOLD, opacity=0.8)
        
        s3_up_arrows = VGroup(*[Arrow(in_patches[i].get_top(), [in_patches[i].get_x(), dart_box.get_bottom()[1], 0], color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1) for i in range(3)])
        s3_out_arrows = VGroup(*[Arrow([out_patches[i].get_x(), dart_box.get_top()[1], 0], out_patches[i].get_bottom(), color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1) for i in range(3)])
        
        scene3_diagram = VGroup(s3_core, arr_ctx_dart, in_patches, out_patches, s3_up_arrows, s3_out_arrows)
        scene3_diagram.set_height(4.0)
        scene3_diagram.move_to(LEFT_ZONE)
        
        # --- Công thức Scene 3 ---
        s3_math = MathTex(r"p(\mathbf{x}) =", r"\prod_t \prod_i", r"p(\mathbf{x}_i^t \mid \mathbf{x}_i^{t+1}, \mathbf{x}_{<i}^t)", font_size=40)
        s3_lbl_joint = Text('"Diffusion" AR', font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED, weight="BOLD").next_to(s3_math[1], DOWN, buff=0.3)
        scene3_math = VGroup(s3_math, s3_lbl_joint).move_to(RIGHT_ZONE)

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(header_group))
        self.next_slide()
        
        # --- CHUYỂN CẢNH 1 ---
        self.play(FadeIn(scene1_diagram), Write(scene1_math))
        self.next_slide()
        
        # --- CHUYỂN CẢNH 2 ---
        self.play(
            FadeOut(scene1_diagram, shift=UP), FadeOut(scene1_math, shift=UP)
        )
        self.play(
            FadeIn(scene2_diagram, shift=UP), Write(scene2_math)
        )
        self.next_slide()
        
        # --- CHUYỂN CẢNH 3 ---
        self.play(
            FadeOut(scene2_diagram, shift=UP), FadeOut(scene2_math, shift=UP)
        )
        self.play(
            FadeIn(scene3_diagram, shift=UP), Write(scene3_math)
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 37 — MODULE 34: NORMALIZING FLOWS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module34_NormalizingFlows(Slide):
    def construct(self):
        # 1. Cài đặt màu nền đồng nhất
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề chính (Ghim góc trái trên)
        title = slide_title("Normalizing Flows")
        self.play(Write(title))
        
        # =====================================================================
        # SCENE 1: KHÁI NIỆM NORMALIZING FLOWS & CHANGE OF VARIABLES
        # =====================================================================
        
        # --- Helper tạo các hộp đồ họa với kích thước cân đối ---
        def make_noise_box():
            box = Rectangle(width=1.3, height=1.3, stroke_color=Theme.NEUTRAL, stroke_width=2, fill_color=Theme.BG, fill_opacity=1)
            import random
            random.seed(42) # Khóa seed cho render nhất quán
            dots = VGroup(*[Dot(point=[random.uniform(-0.55, 0.55), random.uniform(-0.55, 0.55), 0], radius=0.012, color=GRAY, fill_opacity=0.6) for _ in range(75)])
            dots.move_to(box.get_center())
            return VGroup(box, dots)

        def make_clean_box():
            box = Rectangle(width=1.3, height=1.3, stroke_color=Theme.PRIMARY, stroke_width=2, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1)
            label = Text("Data", font=Theme.FONT_BODY, font_size=18, color=Theme.PRIMARY, weight="BOLD").move_to(box.get_center())
            return VGroup(box, label)

        def make_theta_box():
            box = Rectangle(width=0.7, height=1.3, stroke_color=Theme.NEUTRAL, stroke_width=1.5, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1)
            label = MathTex(r"\theta", font_size=32, color=Theme.PRIMARY).move_to(box.get_center())
            return VGroup(box, label)

        # --- Khối Đồ họa bên trái (Left Zone) ---
        noise_top = make_noise_box()
        theta_top = make_theta_box()
        clean_top = make_clean_box()
        
        noise_bot = make_noise_box()
        theta_bot = make_theta_box()
        clean_bot = make_clean_box()
        
        # Sắp xếp các khối hộp với khoảng đệm dọc 1.0 (Đủ rộng để nhãn không đè nhau)
        top_boxes = VGroup(noise_top, theta_top, clean_top).arrange(RIGHT, buff=0.8)
        bot_boxes = VGroup(noise_bot, theta_bot, clean_bot).arrange(RIGHT, buff=0.8)
        boxes_group = VGroup(top_boxes, bot_boxes).arrange(DOWN, buff=1.0)
        
        boxes_group.set_height(3.1) # Tăng kích thước trực quan của diagram
        boxes_group.move_to([-3.5, 0.4, 0]) # Cố định tâm tại Y = 0.4 để tránh chạm Tiêu đề và Công thức
        
        # Tạo liên kết mũi tên và nhãn sau khi đã scale hộp (Tránh sai lệch vị trí)
        arr1 = Arrow(clean_top.get_left(), theta_top.get_right(), color=Theme.ACCENT_RED, stroke_width=3, tip_length=0.15)
        arr2 = Arrow(theta_top.get_left(), noise_top.get_right(), color=Theme.ACCENT_RED, stroke_width=3, tip_length=0.15)
        f_label = MathTex("f", font_size=36, color=Theme.NEUTRAL).next_to(theta_top, UP, buff=0.15)
        
        arr3 = Arrow(noise_bot.get_right(), theta_bot.get_left(), color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.15)
        arr4 = Arrow(theta_bot.get_right(), clean_bot.get_left(), color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.15)
        finv_label = MathTex("f^{-1}", font_size=36, color=Theme.NEUTRAL).next_to(theta_bot, UP, buff=0.15)
        
        diag_full = VGroup(boxes_group, arr1, arr2, f_label, arr3, arr4, finv_label)
        
        # --- Khối Văn bản bên phải (Right Zone) ---
        expl_text = Tex(
            r"If we can train an invertible\\",
            r"neural network $f$ that\\",
            r"transforms data into noise, its\\",
            r"inverse $f^{-1}$ instantly becomes\\",
            r"a generative model.",
            font_size=32, color=Theme.NEUTRAL
        ).move_to([3.5, 0.4, 0])
        
        # --- Khối Công thức dưới cùng (Bottom Zone) ---
        # Phân tách công thức thành các cụm độc lập để tránh chồng lấn viền
        eq_part1 = MathTex(r"p(\mathbf{x}) =", font_size=42)
        eq_part2 = MathTex(r"p_0(f(\mathbf{x}))", font_size=42)
        eq_part3 = MathTex(r"\left| \det \left( \frac{\partial f(\mathbf{x})}{\partial \mathbf{x}} \right) \right|", font_size=42)
        
        # Đặt khoảng đệm ngang an toàn 0.4 giữa phần Prior và Determinant
        math_eq1 = VGroup(eq_part1, eq_part2, eq_part3).arrange(RIGHT, buff=0.4)
        eq_label = Text("Change-of-variables formula", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        
        eq_group = VGroup(math_eq1, eq_label).arrange(RIGHT, buff=0.8)
        eq_group.set_width(11.5)
        eq_group.move_to([0, -2.6, 0]) # Hạ sát sàn để dọn chỗ cho sơ đồ phía trên
        
        # Khởi tạo các khung bao quanh (Chạy sau khi toàn bộ cụm công thức đã cố định vị trí)
        box_prior = SurroundingRectangle(eq_part2, color=Theme.ACCENT_GOLD, buff=0.12, stroke_width=2)
        box_vol = SurroundingRectangle(eq_part3, color=Theme.PRIMARY, buff=0.12, stroke_width=2)
        lbl_prior = Text("Prior", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_GOLD).next_to(box_prior, UP, buff=0.12)
        lbl_vol = Text("Local Volume Change", font=Theme.FONT_BODY, font_size=18, color=Theme.PRIMARY).next_to(box_vol, UP, buff=0.12)
        
        eq_full = VGroup(eq_group, box_prior, box_vol, lbl_prior, lbl_vol)
        scene1_elements = VGroup(diag_full, expl_text, eq_full)
        
        # --- Kịch bản hiển thị Scene 1 ---
        self.play(FadeIn(diag_full))
        self.play(Write(expl_text))
        self.play(FadeIn(eq_full))
        self.next_slide()
        
        # =====================================================================
        # SCENE 2: MAXIMUM LIKELIHOOD TRAINING & RECURSIVE FLOW
        # =====================================================================
        
        # Xóa các thành phần scene 1 (giữ nguyên title)
        self.play(FadeOut(scene1_elements, shift=UP))
        
        # Chuẩn bị nội dung Text & Math cho chuyển cảnh 2
        s2_title_text = Text("Maximum Likelihood Training:", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        s2_eq1 = MathTex(
            r"\mathcal{L} = \log p(\mathbf{x}) = ", 
            r"\log p_0(f(\mathbf{x}))", 
            r"+ \log \left| \det \left( \frac{\partial f(\mathbf{x})}{\partial \mathbf{x}} \right) \right|",
            font_size=42
        )
        s2_text = Tex(
            r"Can be applied recursively, $f = f_T \circ f_{T-1} \circ \dots \circ f_1$, creating a sequence of\\",
            r"variables $\mathbf{x} = \mathbf{x}^0 \rightarrow \mathbf{x}^1 \rightarrow \dots \rightarrow \mathbf{x}^T = \mathbf{z}$ and let $\mathbf{z} \sim \mathcal{N}(0, I)$",
            font_size=32, color=Theme.NEUTRAL
        )
        s2_eq2 = MathTex(
            r"\mathcal{L} = \log p(\mathbf{x}) = -\frac{1}{2} \|\mathbf{z}\|_2^2 + \sum_{t=1}^T \log \left| \det \left( \frac{\partial \mathbf{x}^t}{\partial \mathbf{x}^{t-1}} \right) \right|",
            font_size=42
        )
        
        # Tránh xung đột phương thức định vị
        s2_eq1.move_to([0, 0.8, 0])
        s2_title_text.next_to(s2_eq1, UP, buff=0.6, aligned_edge=LEFT)
        s2_text.next_to(s2_eq1, DOWN, buff=1.3)
        s2_eq2.next_to(s2_text, DOWN, buff=0.8)
        
        # Khống chế chiều cao tổng thể
        scene2_core = VGroup(s2_title_text, s2_eq1, s2_text, s2_eq2)
        scene2_core.set_height(5.0)
        scene2_core.move_to([0, -0.6, 0])
        
        # Vẽ các thành phần bổ trợ sau cùng
        s2_box = SurroundingRectangle(s2_eq1[1], color=Theme.ACCENT_GOLD, buff=0.15, stroke_width=2)
        s2_arr = Arrow(s2_box.get_bottom(), s2_text.get_top(), color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.15)
        
        scene2_elements = VGroup(scene2_core, s2_box, s2_arr)
        
        # --- Kịch bản hiển thị Scene 2 ---
        self.play(FadeIn(scene2_elements, shift=UP))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 38 — MODULE 35: AUTOREGRESSIVE FLOWS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module35_KeyIngredient_ARFlow(Slide):
    def construct(self):
        # 1. Background
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề cố định không bao giờ di chuyển
        title = slide_title("Key Ingredient 1: Autoregressive Flow")
        self.play(Write(title))
        
        # =====================================================================
        # SCENE 1: DISCRETE VS CONTINUOUS
        # =====================================================================
        
        title_left = Text("Discrete AR Model", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD)
        eq_left_1 = MathTex(r"P(\mathbf{X}) = \prod_{i=1}^N P(X_i \mid \mathbf{X}_{<i})", font_size=36)
        eq_left_2 = MathTex(r"X_i \sim \text{multinomial}(g(\mathbf{X}_{<i}))", font_size=32)
        col_left = VGroup(title_left, eq_left_1, eq_left_2).arrange(DOWN, buff=0.8)
        
        divider = Line(UP*2, DOWN*2, color=Theme.DIM)
        
        title_right = Text("Autoregressive Flow", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD)
        eq_right_1 = MathTex(r"p(\mathbf{x}) = \prod_{i=1}^N \mathcal{N}(\mu(\mathbf{x}_{<i}), \sigma^2(\mathbf{x}_{<i}))", font_size=36)
        
        eq_right_box_text = VGroup(
            MathTex(r"\mathbf{x}_i = \mu(\mathbf{x}_{<i}) + \sigma(\mathbf{x}_{<i}) \cdot \mathbf{z}_i, \quad \mathbf{z}_i \sim p_0(\mathbf{z})", font_size=32),
            MathTex(r"\mathbf{z}_i = \frac{\mathbf{x}_i - \mu(\mathbf{x}_{<i})}{\sigma(\mathbf{x}_{<i})} \implies \mathbf{z} = f(\mathbf{x})", font_size=32)
        ).arrange(DOWN, buff=0.5)
        
        box_right = SurroundingRectangle(eq_right_box_text, color=Theme.ACCENT_GOLD, buff=0.3, stroke_width=2)
        box_group = VGroup(eq_right_box_text, box_right)
        
        col_right = VGroup(title_right, eq_right_1, box_group).arrange(DOWN, buff=0.6)
        
        scene1 = VGroup(col_left, divider, col_right).arrange(RIGHT, buff=1.0)
        scene1.set_height(4.8)
        scene1.move_to([0, -0.2, 0])
        
        self.play(FadeIn(scene1, shift=UP))
        self.next_slide()
        
        # =====================================================================
        # SCENE 2: PROPERTIES & STACKING
        # =====================================================================
        
        self.play(FadeOut(scene1, shift=UP))
        
        s2_title = Text("Why Autoregressive Flow?", font=Theme.FONT_BODY, font_size=32, color=Theme.PRIMARY)
        
        point1 = VGroup(
            Text("1. Triangular Jacobian makes determinant computation extremely cheap:", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL),
            MathTex(r"\log \left| \det \left( \frac{\partial f(\mathbf{x})}{\partial \mathbf{x}} \right) \right| = -\sum_{i=1}^N \log \sigma(\mathbf{x}_{<i})", font_size=40, color=Theme.ACCENT_GOLD)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        
        point2 = VGroup(
            Text("2. Single block is unimodal. We stack multiple blocks to gain expressiveness!", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL),
            MathTex(r"\mathbf{x} = \mathbf{x}^0 \rightarrow \mathbf{x}^1 \rightarrow \dots \rightarrow \mathbf{x}^T = \mathbf{z}", font_size=36),
            MathTex(r"\mathcal{L} = -\frac{1}{2} \|\mathbf{z}\|_2^2 - \sum_{t=1}^T \sum_{i=1}^N \log \sigma(\mathbf{x}^t_{<i})", font_size=40, color=Theme.ACCENT_GOLD)
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        
        scene2 = VGroup(s2_title, point1, point2).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        scene2.set_height(5.2)
        scene2.move_to([0, -0.2, 0])
        
        self.play(FadeIn(scene2, shift=UP))
        self.next_slide()

        # =====================================================================
        # SCENE 3: ARCHITECTURE COMPARISON (ĐÃ KHẮC PHỤC LỖI MẤT MŨI TÊN)
        # =====================================================================
        
        self.play(FadeOut(scene2, shift=UP))
        
        def m_box(color, label_text):
            box = Rectangle(width=1.2, height=1.2, stroke_color=color, stroke_width=2, fill_color=Theme.BOX_FILL, fill_opacity=1)
            lbl = Text(label_text, font_size=16, color=color, weight="BOLD").move_to(box.get_center())
            return VGroup(box, lbl)

        def math_rounded_box(latex_str, stroke_color, width=1.0, height=1.4):
            rect = RoundedRectangle(width=width, height=height, corner_radius=0.2, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1, stroke_color=stroke_color, stroke_width=2)
            tex = MathTex(latex_str, font_size=36, color=Theme.NEUTRAL).move_to(rect.get_center())
            return VGroup(rect, tex)

        # --- Khởi tạo hộp của Hàng 1 ---
        r1_noise = m_box(Theme.NEUTRAL, "Noise\nx_T")
        r1_theta1 = math_rounded_box(r"\theta", Theme.DIM, width=0.8, height=1.2)
        r1_noisy = m_box(Theme.ACCENT_RED, "Noisy\nx_t")
        r1_theta2 = math_rounded_box(r"\theta", Theme.DIM, width=0.8, height=1.2)
        r1_clean = m_box(Theme.PRIMARY, "Data\nx_o")
        
        row1_flow = VGroup(r1_noise, r1_theta1, r1_noisy, Text("...", font_size=24, color=Theme.NEUTRAL), r1_theta2, r1_clean).arrange(RIGHT, buff=0.3)
        row1_lbl = Text("Diffusion\n(10s-100s NFEs)", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL).next_to(row1_flow, RIGHT, buff=1.0)
        row1 = VGroup(row1_flow, row1_lbl)

        # --- Khởi tạo hộp của Hàng 2 ---
        r2_noise = m_box(Theme.NEUTRAL, "Noise\nz")
        r2_theta1 = math_rounded_box(r"f_T^{-1}", Theme.ACCENT_RED, width=1.0, height=1.4)
        r2_dots = Text("...", font_size=24, color=Theme.NEUTRAL)
        r2_theta2 = math_rounded_box(r"f_1^{-1}", Theme.ACCENT_RED, width=1.0, height=1.4)
        r2_clean = m_box(Theme.PRIMARY, "Data\nx")
        
        row2_flow = VGroup(r2_noise, r2_theta1, r2_dots, r2_theta2, r2_clean).arrange(RIGHT, buff=0.7)
        row2_lbl = Text("Autoregressive Flows\n(Generative Model)", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED, weight="BOLD").next_to(row2_flow, RIGHT, buff=0.6)
        row2 = VGroup(row2_flow, row2_lbl)
        
        # --- BƯỚC THIẾT LẬP LAYOUT HỘP TRƯỚC (BẮT BUỘC) ---
        scene3_boxes = VGroup(row1, row2).arrange(DOWN, buff=0.8)
        scene3_boxes.set_width(12.5) 
        scene3_boxes.move_to([0, -0.8, 0]) # Cố định vị trí hộp an toàn cách xa Title
        
        # --- BƯỚC VẼ MŨI TÊN SAU KHI HỘP ĐÃ CỐ ĐỊNH TỌA ĐỘ ---
        arrs1 = VGroup(
            Arrow(r1_noise.get_right(), r1_theta1.get_left(), buff=0.1, color=Theme.ACCENT_RED, stroke_width=3, tip_length=0.1),
            Arrow(r1_theta1.get_right(), r1_noisy.get_left(), buff=0.1, color=Theme.ACCENT_RED, stroke_width=3, tip_length=0.1),
            Arrow(r1_noisy.get_right(), row1_flow[3].get_left(), buff=0.1, color=Theme.DIM, stroke_width=2),
            Arrow(row1_flow[3].get_right(), r1_theta2.get_left(), buff=0.1, color=Theme.DIM, stroke_width=2),
            Arrow(r1_theta2.get_right(), r1_clean.get_left(), buff=0.1, color=Theme.ACCENT_RED, stroke_width=3, tip_length=0.1)
        )

        arrs2 = VGroup(
            DoubleArrow(r2_noise.get_right(), r2_theta1.get_left(), buff=0.1, color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.1),
            DoubleArrow(r2_theta1.get_right(), r2_dots.get_left(), buff=0.1, color=Theme.DIM, stroke_width=2, tip_length=0.1),
            DoubleArrow(r2_dots.get_right(), r2_theta2.get_left(), buff=0.1, color=Theme.DIM, stroke_width=2, tip_length=0.1),
            DoubleArrow(r2_theta2.get_right(), r2_clean.get_left(), buff=0.1, color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.1)
        )
        
        # Đóng gói tổng thể (Không gọi .arrange() ở đây để giữ nguyên vị trí mũi tên)
        scene3 = VGroup(scene3_boxes, arrs1, arrs2)
        
        self.play(FadeIn(scene3, shift=UP))
        self.next_slide()

        # =====================================================================
        # SCENE 4: GRAPHICAL MODEL & TOY EXAMPLE
        # =====================================================================
        
        self.play(FadeOut(scene3, shift=UP))
        
        s4_prop = Text(
            "Proposition: Stacked AR flows (T ≥ 3) are universal approximators.", 
            font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL, weight="BOLD"
        )
        s4_prop_bg = SurroundingRectangle(s4_prop, color=Theme.NEUTRAL, fill_color=Theme.NEUTRAL, fill_opacity=0.1, buff=0.2)
        header_s4 = VGroup(s4_prop_bg, s4_prop)
        
        def make_node(label, color):
            c = Circle(radius=0.4, fill_color=Theme.BG, stroke_color=color, stroke_width=2)
            l = MathTex(label, font_size=24, color=Theme.NEUTRAL).move_to(c.get_center())
            return VGroup(c, l)

        grid = VGroup()
        for r_color, r_lbl in [(Theme.NEUTRAL, "z"), (Theme.ACCENT_GOLD, "y"), (Theme.PRIMARY, "x")]:
            row = VGroup(*[make_node(f"{r_lbl}_{{{idx}}}", r_color) for idx in ["i-1", "i", "i+1"]]).arrange(RIGHT, buff=0.8)
            grid.add(row)
        grid.arrange(DOWN, buff=0.6)
        
        arrows_s4 = VGroup()
        for c in range(3):
            arrows_s4.add(Arrow(grid[0][c].get_bottom(), grid[1][c].get_top(), buff=0.1, color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1))
            arrows_s4.add(Arrow(grid[1][c].get_bottom(), grid[2][c].get_top(), buff=0.1, color=Theme.NEUTRAL, stroke_width=2, tip_length=0.1))
        for r in range(1, 3):
            for c in range(2):
                arrows_s4.add(Arrow(grid[r][c].get_right(), grid[r][c+1].get_left(), buff=0.1, color=Theme.DIM, stroke_width=2, tip_length=0.1))
                
        highlight_box = SurroundingRectangle(grid[1][2], color=Theme.ACCENT_RED, stroke_width=2, fill_color=Theme.ACCENT_RED, fill_opacity=0.2)
        
        lbl_hidden = VGroup(
            Text("Hidden", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_RED),
            Text('"future"', font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_RED),
            Text("info", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_RED)
        ).arrange(DOWN, buff=0.05)
        lbl_hidden.next_to(highlight_box, RIGHT, buff=0.3)
        
        diagram_s4 = VGroup(grid, arrows_s4, highlight_box, lbl_hidden)
        
        math_s4 = VGroup(
            Text("A toy example of 2 Blocks yields:", font_size=24, color=Theme.PRIMARY),
            MathTex(r"p(x_i \mid \mathbf{x}_{<i}) = \int \mathcal{N}(\hat{\mu}, \hat{\sigma}^2) \, d\mathbf{y}_{>i}", font_size=36),
            Text("→ Infinite Gaussian Mixture", font_size=28, color=Theme.ACCENT_GOLD, weight="BOLD")
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        
        body_s4 = VGroup(math_s4, diagram_s4).arrange(RIGHT, buff=1.0)
        scene4 = VGroup(header_s4, body_s4).arrange(DOWN, buff=0.8)
        scene4.set_height(5.2)
        scene4.move_to([0, -0.2, 0])
        
        self.play(FadeIn(scene4, shift=UP))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 39 — MODULE 36: TRANSFORMERS (ĐÃ SỬA LỖI TRÀN CHỮ)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module36_Transformers(Slide):
    def construct(self):
        # 1. Cài đặt màu nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề cố định
        title = slide_title("Key Ingredient 2: Transformers")
        
        # =====================================================================
        # VÙNG TRÁI: TEXT & CÔNG THỨC (LEFT ZONE)
        # =====================================================================
        
        t1 = Text(
            "• Most of the NF literature was before the\n  success of Transformer and LLMs", 
            font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL
        )
        t1_sub = Text(
            "→ standard architecture?", 
            font=Theme.FONT_BODY, font_size=28, color=Theme.ACCENT_GOLD, slant="ITALIC"
        )
        t1_sub.next_to(t1, DOWN, aligned_edge=LEFT, buff=0.2)
        b1 = VGroup(t1, t1_sub)
        
        t2 = Text("• Similar Analogy:", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        t2_b1 = Text("- U-Net → DiT", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        t2_b2 = Text(
            "- We modernize the step prediction with standard\n  Causal Transformer architectures", 
            font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL
        )
        
        # Căn lề thụt đầu dòng (Tránh lạm dụng shift thủ công theo note.txt Lỗi 5)
        t2_b1.next_to(t2, DOWN, aligned_edge=LEFT, buff=0.2).shift(RIGHT * 0.5)
        t2_b2.next_to(t2_b1, DOWN, aligned_edge=LEFT, buff=0.2)
        b2 = VGroup(t2, t2_b1, t2_b2)
        
        eq = MathTex(
            r"\mathbf{x}_i = \mu(\mathbf{x}_{<i}) + \sigma(\mathbf{x}_{<i}) \cdot \mathbf{z}_i", 
            font_size=40, color=Theme.NEUTRAL
        )
        
        # Đóng gói vùng trái và cố định kích thước
        left_col = VGroup(b1, b2, eq).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        left_col.set_width(6.2)
        left_col.move_to([-3.7, -0.5, 0]) # Dịch nhẹ sang trái để tăng không gian cho sơ đồ bên phải
        eq.match_x(left_col) # Ép công thức ra giữa khu vực văn bản
        
        # =====================================================================
        # VÙNG PHẢI: KIẾN TRÚC TRANSFORMER TỐI GIẢN (RIGHT ZONE)
        # =====================================================================
        
        # Bảng màu kiến trúc (Pink, Yellow, Blue, Purple, Green)
        PINK   = ManimColor("#F48FB1")
        YELLOW = ManimColor("#FFE082")
        BLUE   = ManimColor("#90CAF9")
        PURPLE = ManimColor("#CE93D8")
        GREEN  = ManimColor("#A5D6A7")
        
        def make_trans_box(lines, bg_color):
            # Tự động tăng chiều cao lên 0.85 nếu chữ dài cần xuống dòng (2 lines)
            box_height = 0.6 if len(lines) == 1 else 0.85
            return RoundedBox(
                lines=lines, width=2.5, height=box_height, corner_radius=0.1, # Giảm width xuống 2.5 để tăng biên an toàn biên phải
                fill_color=bg_color, text_color=Theme.BOX_FILL_ALT, 
                stroke_color=Theme.NEUTRAL, stroke_width=1.5, font_size=14 # Cỡ chữ 14 tối ưu tránh tràn hộp
            )

        # --- Cột Encoder ---
        enc_in = Text("Inputs", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL)
        enc_emb = make_trans_box(["Input Embedding"], PINK)
        enc_mha = make_trans_box(["Multi-Head", "Attention"], YELLOW) # Xuống dòng
        enc_ffn = make_trans_box(["Feed Forward"], BLUE)
        
        enc_stack = VGroup(enc_in, enc_emb, enc_mha, enc_ffn).arrange(UP, buff=0.35)
        
        # --- Cột Decoder ---
        dec_in = Text("Outputs (shifted)", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL)
        dec_emb = make_trans_box(["Output Embedding"], PINK)
        dec_mmha = make_trans_box(["Masked Multi-Head", "Attention"], YELLOW) # Xuống dòng tránh lỗi tràn chữ
        dec_mha = make_trans_box(["Multi-Head", "Attention"], YELLOW) # Xuống dòng
        dec_ffn = make_trans_box(["Feed Forward"], BLUE)
        dec_lin = make_trans_box(["Linear"], PURPLE)
        dec_soft = make_trans_box(["Softmax"], GREEN)
        dec_out = Text("Probabilities", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL)
        
        dec_stack = VGroup(dec_in, dec_emb, dec_mmha, dec_mha, dec_ffn, dec_lin, dec_soft, dec_out).arrange(UP, buff=0.22)
        
        # Gom nhóm Kiến trúc (Ép đáy bằng nhau để các cổng Input/Output ngang hàng)
        diagram = VGroup(enc_stack, dec_stack).arrange(RIGHT, buff=0.9, aligned_edge=DOWN)
        
        # Đóng băng tọa độ tuyệt đối TRƯỚC khi vẽ mũi tên (Dịch sang trái một chút để tăng biên an toàn bên phải)
        diagram.set_height(5.5)
        diagram.move_to([2.9, -0.2, 0]) 
        
        # --- Vẽ Mũi tên (Tuyệt đối an toàn vì tọa độ hộp đã cố định) ---
        arrows = VGroup()
        for i in range(len(enc_stack)-1):
            arrows.add(Arrow(enc_stack[i].get_top(), enc_stack[i+1].get_bottom(), buff=0.08, stroke_width=2.5, tip_length=0.12, color=Theme.NEUTRAL))
            
        dec_arr_start = len(arrows)
        for i in range(len(dec_stack)-1):
            arrows.add(Arrow(dec_stack[i].get_top(), dec_stack[i+1].get_bottom(), buff=0.08, stroke_width=2.5, tip_length=0.12, color=Theme.NEUTRAL))
            
        # Cross Attention: Nối ngang từ khối FFN Encoder sang MHA của Decoder
        arr_cross = Arrow(enc_ffn.get_right(), dec_mha.get_left(), buff=0.1, stroke_width=2.5, tip_length=0.12, color=Theme.PRIMARY)
        
        # --- Khung bao khối Nx (Đại diện cho N Layers) ---
        enc_nx = SurroundingRectangle(VGroup(enc_mha, enc_ffn), color=Theme.DIM, stroke_width=2, buff=0.15)
        enc_nx_lbl = Text("Nx", font=Theme.FONT_BODY, font_size=18, color=Theme.DIM).next_to(enc_nx, LEFT, buff=0.15)
        
        dec_nx = SurroundingRectangle(VGroup(dec_mmha, dec_mha, dec_ffn), color=Theme.DIM, stroke_width=2, buff=0.15)
        dec_nx_lbl = Text("Nx", font=Theme.FONT_BODY, font_size=18, color=Theme.DIM).next_to(dec_nx, RIGHT, buff=0.15)
        
        # =====================================================================
        # KỊCH BẢN ANIMATION
        # =====================================================================
        
        self.play(Write(title))
        self.next_slide()
        
        # Hiện vế trái phần lý thuyết đầu tiên
        self.play(FadeIn(b1, shift=UP))
        self.next_slide()
        
        # Hiện cột Encoder
        self.play(
            FadeIn(enc_stack),
            FadeIn(enc_nx), FadeIn(enc_nx_lbl),
            *[Create(arrows[i]) for i in range(dec_arr_start)]
        )
        self.next_slide()
        
        # Hiện vế trái phần Analogy
        self.play(FadeIn(b2, shift=UP))
        self.next_slide()
        
        # Hiện cột Decoder và Luồng Cross Attention
        self.play(
            FadeIn(dec_stack),
            FadeIn(dec_nx), FadeIn(dec_nx_lbl),
            *[Create(arrows[i]) for i in range(dec_arr_start, len(arrows))],
            Create(arr_cross)
        )
        self.next_slide()
        
        # Kết thúc với công thức phương trình
        self.play(Write(eq))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 40 — MODULE 37: TARFlow ARCHITECTURE (FINAL POLISHED)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module37_TARFlow(Slide):
    def construct(self):
        # 1. Nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề cố định
        title = slide_title("Transformer AutoRegressive Flows (TARFlow)")
        self.play(Write(title))
        
        # =====================================================================
        # HÀM HỖ TRỢ XÂY DỰNG KHỐI ĐỒ HỌA
        # =====================================================================
        
        # Nâng cấp width=0.8 để LaTeX thoải mái hơn, thêm text_color tùy chỉnh
        def make_seq(tex_template, count=4, width=0.8, height=0.7, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.NEUTRAL, text_color=Theme.NEUTRAL):
            boxes = VGroup()
            for i in range(count):
                tex_mob = MathTex(tex_template.format(i), font_size=24, color=text_color)
                boxes.add(make_custom_box(tex_mob, width, height, fill_color, stroke_color))
            return boxes.arrange(RIGHT, buff=0.15)

        def make_custom_box(mobject_content, width, height, fill_color, stroke_color):
            box = RoundedRectangle(
                corner_radius=0.15, width=width, height=height,
                fill_color=fill_color, fill_opacity=1,
                stroke_color=stroke_color, stroke_width=2
            )
            mobject_content.move_to(box.get_center())
            return VGroup(box, mobject_content)

        def make_noise_box(size=1.2):
            box = Rectangle(width=size, height=size, stroke_color=Theme.NEUTRAL, stroke_width=2, fill_color=Theme.BG, fill_opacity=1)
            import random
            random.seed(42)
            dots = VGroup(*[Dot(point=[random.uniform(-size/2.2, size/2.2), random.uniform(-size/2.2, size/2.2), 0], radius=0.015, color=GRAY, fill_opacity=0.6) for _ in range(80)])
            dots.move_to(box.get_center())
            return VGroup(box, dots)

        # =====================================================================
        # VÙNG TRÁI: MACRO FLOW
        # =====================================================================
        
        noise_img = make_noise_box(1.2)
        noise_patches = make_seq(r"\mathbf{{Z}}^T_{{{}}}", count=4, fill_color=Theme.BG, stroke_color=Theme.DIM)
        top_macro_items = VGroup(noise_img, noise_patches).arrange(RIGHT, buff=1.5)
        
        macro_block_txt1 = Text("Transformer AR Flow", font=Theme.FONT_BODY, font_size=18, color=Theme.PRIMARY)
        macro_block_txt2 = Text("Block F(·)", font=Theme.FONT_BODY, font_size=18, color=Theme.PRIMARY)
        macro_block_text = VGroup(macro_block_txt1, macro_block_txt2).arrange(DOWN, buff=0.08)
        
        macro_block = make_custom_box(macro_block_text, 3.8, 1.0, Theme.BOX_FILL_ALT, Theme.PRIMARY)
        xT_label = Text("xT", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD").next_to(macro_block, RIGHT, buff=0.2)
        mid_macro = VGroup(macro_block, xT_label)
        
        real_img = Rectangle(width=1.2, height=1.2, stroke_color=Theme.SUCCESS, stroke_width=2, fill_color=Theme.SUCCESS, fill_opacity=0.3)
        lbl_img = Text("Image", font_size=18, color=Theme.SUCCESS, weight="BOLD").move_to(real_img.get_center())
        real_img_group = VGroup(real_img, lbl_img)
        img_patches = make_seq(r"\mathbf{{Z}}^0_{{{}}}", count=4, fill_color=ManimColor("#1A3320"), stroke_color=Theme.SUCCESS)
        bot_macro_items = VGroup(real_img_group, img_patches).arrange(RIGHT, buff=1.5)
        
        macro_group = VGroup(top_macro_items, mid_macro, bot_macro_items).arrange(DOWN, buff=0.8)
        macro_group.set_height(4.8)
        macro_group.move_to([-3.5, -0.2, 0])
        
        # Mũi tên Patchify & Unpatchify chốt thẳng vị trí (không đè chữ)
        arr_patchify = Arrow(bot_macro_items[0].get_right(), bot_macro_items[1].get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        lbl_patchify = Text("Patchify", font_size=16, color=Theme.NEUTRAL).next_to(arr_patchify, UP, buff=0.1)
        
        arr_unpatchify = Arrow(top_macro_items[1].get_left(), top_macro_items[0].get_right(), buff=0.1, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12)
        lbl_unpatchify = Text("Unpatchify", font_size=16, color=Theme.NEUTRAL).next_to(arr_unpatchify, DOWN, buff=0.1)
        
        arr_up1 = Arrow(bot_macro_items[1].get_top(), macro_block.get_bottom(), buff=0.1, color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.15)
        arr_up2 = Arrow(macro_block.get_top(), top_macro_items[1].get_bottom(), buff=0.1, color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.15)
        
        macro_full = VGroup(macro_group, arr_patchify, lbl_patchify, arr_unpatchify, lbl_unpatchify, arr_up1, arr_up2)

        # =====================================================================
        # VÙNG PHẢI: MICRO ARCHITECTURE (BÊN TRONG BLOCK)
        # =====================================================================
        
        C_IN = ManimColor("#E1BEE7")   
        C_TRANS = ManimColor("#FFCCBC") 
        C_OUT = ManimColor("#C5CAE9")  
        
        # Đã cập nhật text_color=BLACK cho toàn bộ Z*
        m_out = make_seq(r"\mathbf{{z}}^{{t+1}}_{{{}}}", count=4, fill_color=C_OUT, stroke_color=C_OUT, text_color=BLACK)
        
        m_eq_tex = MathTex(r"(\tilde{\mathbf{z}}^t_i - \mu^t_i) \odot \exp(-\alpha^t_i) \oplus", font_size=32, color=Theme.NEUTRAL)
        m_eq = make_custom_box(m_eq_tex, 4.5, 0.6, Theme.BG, Theme.BG) 
        
        m_params_tex = Tex(r"Predicted Params ($\alpha^t, \mu^t$)", font_size=24, color=Theme.ACCENT_RED)
        m_params = make_custom_box(m_params_tex, 4.5, 0.6, Theme.BG, Theme.ACCENT_RED)
        
        m_trans_txt = Text("Causal Transformer", font=Theme.FONT_BODY, font_size=20, color=BLACK, weight="BOLD")
        m_transformer = make_custom_box(m_trans_txt, 4.5, 0.8, C_TRANS, Theme.NEUTRAL)
        
        m_tilde = make_seq(r"\tilde{{\mathbf{{z}}}}^t_{{{}}}", count=4, fill_color=C_IN, stroke_color=C_IN, text_color=BLACK)
        m_perm_lbl = Text("Permutation π(z)", font_size=18, color=Theme.NEUTRAL)
        
        m_in = make_seq(r"\mathbf{{z}}^t_{{{}}}", count=4, fill_color=C_IN, stroke_color=C_IN, text_color=BLACK)
        
        micro_stack = VGroup(m_out, m_eq, m_params, m_transformer, m_tilde, m_perm_lbl, m_in).arrange(DOWN, buff=0.25)
        
        micro_bg = SurroundingRectangle(micro_stack, color=Theme.PRIMARY, stroke_width=2, fill_color=Theme.BG, fill_opacity=0.4, corner_radius=0.2, buff=0.3)
        micro_lbl = Text("Transformer AR Flow Block", font_size=20, color=Theme.PRIMARY, weight="BOLD").next_to(micro_bg, DOWN, buff=0.15)
        
        micro_group = VGroup(micro_bg, micro_stack, micro_lbl)
        micro_group.set_height(5.2)
        micro_group.move_to([3.2, -0.2, 0])
        
        m_arrs = VGroup(
            Arrow(m_in.get_top(), m_tilde.get_bottom(), buff=0.08, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.1),
            Arrow(m_tilde.get_top(), m_transformer.get_bottom(), buff=0.08, color=Theme.ACCENT_GOLD, stroke_width=2.5, tip_length=0.1),
            Arrow(m_transformer.get_top(), m_params.get_bottom(), buff=0.08, color=Theme.ACCENT_GOLD, stroke_width=2.5, tip_length=0.1),
            Arrow(m_params.get_top(), m_eq.get_bottom(), buff=0.08, color=Theme.ACCENT_GOLD, stroke_width=2.5, tip_length=0.1),
            Arrow(m_eq.get_top(), m_out.get_bottom(), buff=0.08, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.1),
        )
        
        # ─────────────────────────────────────────────────────────────────
        # THAY THẾ HOÀN TOÀN CURVED_ARROW BẰNG ĐƯỜNG DẪN VUÔNG GÓC (SQUARE BRACKET)
        # ─────────────────────────────────────────────────────────────────
        x_max = m_eq.get_right()[0] + 0.3 # Tọa độ lề phải an toàn
        
        p_start = m_tilde.get_right()
        p_corner1 = [x_max, p_start[1], 0]
        p_corner2 = [x_max, m_eq.get_right()[1], 0]
        p_end = m_eq.get_right()
        
        l1 = Line(p_start, p_corner1, color=Theme.ACCENT_GOLD, stroke_width=2.5)
        l2 = Line(p_corner1, p_corner2, color=Theme.ACCENT_GOLD, stroke_width=2.5)
        l3 = Arrow(p_corner2, p_end, color=Theme.ACCENT_GOLD, stroke_width=2.5, tip_length=0.12, buff=0)
        
        skip_connection = VGroup(l1, l2, l3)
        # ─────────────────────────────────────────────────────────────────

        micro_full = VGroup(micro_group, m_arrs, skip_connection)

        # =====================================================================
        # ĐƯỜNG KẾT NỐI MACRO -> MICRO
        # =====================================================================
        
        zoom_line1 = DashedLine(macro_block.get_corner(UR), micro_bg.get_corner(UL), color=Theme.DIM, stroke_width=2)
        zoom_line2 = DashedLine(macro_block.get_corner(DR), micro_bg.get_corner(DL), color=Theme.DIM, stroke_width=2)
        zoom_lines = VGroup(zoom_line1, zoom_line2)

        # =====================================================================
        # KỊCH BẢN HIỂN THỊ
        # =====================================================================
        
        self.play(FadeIn(bot_macro_items, shift=UP))
        self.play(Create(arr_patchify), Write(lbl_patchify))
        self.next_slide()
        
        self.play(Create(arr_up1), FadeIn(mid_macro))
        self.play(Create(arr_up2), FadeIn(top_macro_items[1]))
        self.play(Create(arr_unpatchify), Write(lbl_unpatchify), FadeIn(top_macro_items[0]))
        self.next_slide()
        
        self.play(Create(zoom_lines))
        self.play(FadeIn(micro_bg), FadeIn(micro_lbl))
        self.next_slide()
        
        self.play(FadeIn(m_in))
        self.play(Create(m_arrs[0]), FadeIn(m_perm_lbl), FadeIn(m_tilde))
        self.play(Create(m_arrs[1]), FadeIn(m_transformer))
        self.play(Create(m_arrs[2]), FadeIn(m_params))
        self.next_slide()
        
        # Mũi tên góc vuông xuất hiện cực kỳ chuyên nghiệp
        self.play(Create(skip_connection))
        self.play(Create(m_arrs[3]), FadeIn(m_eq))
        self.play(Create(m_arrs[4]), FadeIn(m_out))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 41 — MODULE 38: DEEP-SHALLOW ARCHITECTURE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module38_DeepShallow(Slide):
    def construct(self):
        # 1. Thiết lập nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề và Subtitle cố định (Tránh Lỗi 1)
        title = slide_title("Key Ingredient 3: Deep-shallow Architecture")
        
        header = Text(
            "Best Arch: balance the #AF blocks v.s. #layers per block?",
            font=Theme.FONT_BODY, font_size=32, color=Theme.NEUTRAL
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.4)
        
        self.play(Write(title), FadeIn(header))
        
        # ─────────────────────────────────────────────────────────────────────
        # THIẾT LẬP CÁC HẰNG SỐ VÙNG AN TOÀN TUYỆT ĐỐI (Chống Lỗi 2, 3, 4)
        # ─────────────────────────────────────────────────────────────────────
        LEFT_ZONE_POS = [-3.8, -0.6, 0]
        RIGHT_ZONE_POS = [2.9, -0.6, 0]
        MAX_LEFT_WIDTH = 5.4
        MAX_RIGHT_WIDTH = 6.6
        MAX_HEIGHT = 4.8

        # Hàm helper khống chế tỷ lệ bao cảnh kép (Double-bounded box)
        def fit_in_box(mobject, max_w, max_h):
            if mobject.get_width() > max_w:
                mobject.set_width(max_w)
            if mobject.get_height() > max_h:
                mobject.set_height(max_h)
            return mobject

        def format_left_text(text_group):
            # Khống chế chiều rộng văn bản trái và đưa về đúng tâm vùng trái
            if text_group.get_width() > MAX_LEFT_WIDTH:
                text_group.set_width(MAX_LEFT_WIDTH)
            text_group.move_to(LEFT_ZONE_POS)
            return text_group

        # Hàm tạo hộp an toàn - Thu nhỏ chiều rộng xuống 1.6 để cực kỳ gọn gàng
        def make_block(width, height, text_str, bg_color=ManimColor("#455A64"), font_size=24, text_color=WHITE):
            rect = RoundedRectangle(
                corner_radius=0.1, width=width, height=height,
                fill_color=bg_color, fill_opacity=1,
                stroke_color=Theme.NEUTRAL, stroke_width=1
            )
            txt = Text(text_str, font_size=font_size, color=text_color, font=Theme.FONT_BODY)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt)

        # =====================================================================
        # SCENE 1: THE EVOLUTION (Slide 29 - Ảnh 1)
        # =====================================================================
        
        # --- Vùng Text Bên Trái ---
        s1_text = Text("• How many blocks are necessary?", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        format_left_text(s1_text)
        
        # Khối Equal-sized (4 blocks of 6) - Rộng 1.6
        stack_6x4_boxes = VGroup(*[make_block(1.6, 0.7, "6") for _ in range(4)]).arrange(DOWN, buff=0.15)
        stack_6x4 = VGroup(
            MathTex(r"\mathbf{Z}", font_size=32, color=WHITE).next_to(stack_6x4_boxes, UP, buff=0.2),
            stack_6x4_boxes,
            MathTex(r"\mathbf{X}", font_size=32, color=WHITE).next_to(stack_6x4_boxes, DOWN, buff=0.2)
        )
        
        s1_q_mark = Text("?", font_size=64, color=Theme.NEUTRAL)
        
        # Sắp xếp sơ đồ phải
        s1_diagram = VGroup(stack_6x4, s1_q_mark).arrange(RIGHT, buff=1.0)
        fit_in_box(s1_diagram, MAX_RIGHT_WIDTH, MAX_HEIGHT)
        s1_diagram.move_to(RIGHT_ZONE_POS)
        
        scene1_group = VGroup(s1_text, s1_diagram)
        self.play(FadeIn(scene1_group, shift=UP))
        self.next_slide()

        # =====================================================================
        # SCENE 2: SỰ TIẾN HÓA KIẾN TRÚC (Slide 30 - Ảnh 2)
        # =====================================================================
        
        self.play(FadeOut(scene1_group))
        
        s2_t1 = Text("• Prop 1 shows no need to have a\n  deep number of blocks.", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        s2_t2 = Text("• Should we keep each AF block\n  the same size or in-balanced?", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        s2_text = VGroup(s2_t1, s2_t2).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        format_left_text(s2_text)
        
        # Khối Single Deep (1 block of 18) - Rộng 1.6
        box_18 = make_block(1.6, 3.25, "18")
        stack_18 = VGroup(
            MathTex(r"\mathbf{Z}", font_size=32, color=WHITE).next_to(box_18, UP, buff=0.2),
            box_18,
            MathTex(r"\mathbf{X}", font_size=32, color=WHITE).next_to(box_18, DOWN, buff=0.2)
        )
        
        # Khối Deep-Shallow (18 + 3 blocks of 2) - Rộng 1.6
        stack_18_2x3_boxes = VGroup(
            make_block(1.6, 2.3, "18"),
            make_block(1.6, 0.25, "2", font_size=18),
            make_block(1.6, 0.25, "2", font_size=18),
            make_block(1.6, 0.25, "2", font_size=18)
        ).arrange(DOWN, buff=0.1)
        stack_18_2x3 = VGroup(
            MathTex(r"\mathbf{Z}", font_size=32, color=WHITE).next_to(stack_18_2x3_boxes, UP, buff=0.2),
            stack_18_2x3_boxes,
            MathTex(r"\mathbf{X}", font_size=32, color=WHITE).next_to(stack_18_2x3_boxes, DOWN, buff=0.2)
        )
        
        s2_q_mark = Text("?", font_size=48, color=Theme.NEUTRAL)
        
        # Sắp xếp ngang cả 3 cột (Căn đáy bằng nhau)
        s2_diagram = VGroup(stack_6x4.copy(), s2_q_mark, stack_18, stack_18_2x3).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        fit_in_box(s2_diagram, MAX_RIGHT_WIDTH, MAX_HEIGHT)
        s2_diagram.move_to(RIGHT_ZONE_POS)
        
        scene2_group = VGroup(s2_text, s2_diagram)
        self.play(FadeIn(scene2_group, shift=UP))
        self.next_slide()

        # =====================================================================
        # SCENE 3: KẾT QUẢ BẢNG (Slide 32 - Ảnh 3)
        # =====================================================================
        
        self.play(FadeOut(scene2_group))
        
        s3_t1 = Text("• Prop 1 shows no need to have a\n  deep number of blocks.", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        s3_t2 = Text("• A deep-shallow architecture is\n  more performant and efficient\n  than an equal-sized model.", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        
        # Bảng số liệu dạng lưới cột
        c1 = VGroup(
            Text("Arch Comparison", font=Theme.FONT_BODY, font_size=22, weight="BOLD", color=Theme.NEUTRAL),
            Text("Equal-sized", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL),
            Text("Deep-shallow", font=Theme.FONT_BODY, font_size=20, color=Theme.PRIMARY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        c2 = VGroup(
            Text("FID", font=Theme.FONT_BODY, font_size=22, weight="BOLD", color=Theme.NEUTRAL),
            Text("5.56", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL),
            Text("4.69", font=Theme.FONT_BODY, font_size=20, color=Theme.PRIMARY, weight="BOLD")
        ).arrange(DOWN, aligned_edge=ORIGIN, buff=0.4)
        
        c3 = VGroup(
            Text("Speed", font=Theme.FONT_BODY, font_size=22, weight="BOLD", color=Theme.NEUTRAL),
            Text("x1", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL),
            Text("x2", font=Theme.FONT_BODY, font_size=20, color=Theme.PRIMARY, weight="BOLD")
        ).arrange(DOWN, aligned_edge=ORIGIN, buff=0.4)
        
        table = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        h_line = Line(table.get_corner(UL) + DOWN*0.4, table.get_corner(UR) + DOWN*0.4, color=Theme.DIM, stroke_width=2)
        table_group = VGroup(table, h_line)
        
        s3_left = VGroup(s3_t1, s3_t2, table_group).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        format_left_text(s3_left)
        
        # Chỉ giữ lại khối đơn Deep-Shallow
        s3_diagram = stack_18_2x3.copy()
        fit_in_box(s3_diagram, MAX_RIGHT_WIDTH, MAX_HEIGHT)
        s3_diagram.move_to(RIGHT_ZONE_POS)
        
        scene3_group = VGroup(s3_left, s3_diagram)
        self.play(FadeIn(scene3_group, shift=UP))
        self.next_slide()

        # =====================================================================
        # SCENE 4: TÍCH HỢP LLM (Slide 34 - Ảnh 4)
        # =====================================================================
        
        self.play(FadeOut(scene3_group))
        
        s4_t1 = Text("• We can also only condition in\n  the deep block.", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        s4_t2 = Text("• Shallow blocks act as\n  \"tokenizers\".", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        s4_t3 = Text("• Unlock the possibility of fine-\n  tuning any pre-trained LLMs\n  into autoregressive flows.", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        
        s4_text_group = VGroup(s4_t1, s4_t2, s4_t3).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        format_left_text(s4_text_group)
        
        # 1. Lớp Đế
        ctx_enc = make_block(1.8, 1.2, "Context\nEncoder", bg_color=ManimColor("#8D6E63"), font_size=18)
        shallow_boxes_s4 = VGroup(
            make_block(3.2, 0.3, "Shallow Transformer (2)", font_size=16),
            make_block(3.2, 0.3, "Shallow Transformer (2)", font_size=16),
            make_block(3.2, 0.3, "Shallow Transformer (2)", font_size=16)
        ).arrange(DOWN, buff=0.1)
        base_layer = VGroup(ctx_enc, shallow_boxes_s4).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        
        # 2. Lớp Deep LLM (Rộng bằng đế)
        deep_block = make_block(base_layer.width, 2.8, "Shared Deep Autoregressive Transformer (18)", font_size=20)
        deep_block.next_to(base_layer, UP, buff=0.15)
        
        # 3. Ký hiệu Z, C, X (Dùng match_x căn lề chuẩn)
        lbl_z_s4 = MathTex(r"\mathbf{Z}", font_size=32, color=WHITE).next_to(deep_block, UP, buff=0.2).match_x(shallow_boxes_s4)
        lbl_c_s4 = MathTex(r"\mathbf{C}", font_size=32, color=WHITE).next_to(ctx_enc, DOWN, buff=0.2)
        lbl_x_s4 = MathTex(r"\mathbf{X}", font_size=32, color=WHITE).next_to(shallow_boxes_s4, DOWN, buff=0.2)
        
        # 4. Box highlight LLM
        llm_box = SurroundingRectangle(deep_block, color=Theme.ACCENT_RED, stroke_width=3, corner_radius=0.15, buff=0.1)
        llm_lbl = Text("e.g., Llama3, QWen3, Gemma3, ...", font_size=16, color=Theme.ACCENT_RED, weight="BOLD").next_to(llm_box, UP, aligned_edge=LEFT, buff=0.1)
        
        s4_diagram = VGroup(base_layer, deep_block, lbl_z_s4, lbl_c_s4, lbl_x_s4, llm_box, llm_lbl)
        
        # Ép khung kép an toàn cho sơ đồ Scene 4
        fit_in_box(s4_diagram, MAX_RIGHT_WIDTH, MAX_HEIGHT)
        s4_diagram.move_to(RIGHT_ZONE_POS)
        
        scene4_group = VGroup(s4_text_group, s4_diagram)
        self.play(FadeIn(scene4_group, shift=UP))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 42 — MODULE 39: LATENT NORMALIZING FLOWS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module39_LatentNormalizingFlows(Slide):
    def construct(self):
        # 1. Nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề cố định (Ghim sát góc trên bên trái)
        title = slide_title("Key Ingredient 4: Latent Normalizing Flows")
        
        # Hàm tạo hộp an toàn tại chỗ (Chống TypeError, Text đè viền)
        def safe_box(lines, width, height, bg_color, stroke_color):
            rect = RoundedRectangle(
                width=width, height=height, corner_radius=0.15,
                fill_color=bg_color, fill_opacity=1, stroke_color=stroke_color, stroke_width=2
            )
            txt = VGroup(*[Text(l, font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL) for l in lines]).arrange(DOWN, buff=0.1)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt)

        # =====================================================================
        # SCENE 1: ARCHITECTURE ANALOGY (U-NET -> TARFlow)
        # =====================================================================
        
        # --- 1. Rút gọn văn bản giải thích tránh chiếm chiều cao (Sửa lỗi Tràn dọc) ---
        s1_bullet1 = Text("• Towards High-resolution / Text-conditioned Generation", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        s1_bullet2 = Text("• Analogy: DDPM → LDM (SD-VAE 256x256 → 32x32)", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        
        s1_header = VGroup(s1_bullet1, s1_bullet2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        s1_header.next_to(title, DOWN, aligned_edge=LEFT, buff=0.4)
        
        # --- 2. Dựng Sơ đồ Kiến trúc ---
        # PANEL 1: PIXEL SPACE
        p_x = safe_box(["Input x"], 1.8, 0.8, Theme.BOX_FILL, Theme.ACCENT_RED)
        p_enc = safe_box(["Encoder E"], 1.8, 0.8, Theme.BOX_FILL_ALT, Theme.PRIMARY)
        p_dec = safe_box(["Decoder D"], 1.8, 0.8, Theme.BOX_FILL_ALT, Theme.PRIMARY)
        p_xout = safe_box(["Output x~"], 1.8, 0.8, Theme.BOX_FILL, Theme.ACCENT_RED)
        
        pixel_col = VGroup(p_x, p_enc, p_dec, p_xout).arrange(DOWN, buff=0.2)
        pixel_frame = SurroundingRectangle(pixel_col, color=Theme.ACCENT_RED, fill_color=Theme.BG, fill_opacity=0.3, corner_radius=0.2, buff=0.2)
        pixel_lbl = Text("Pixel Space", font_size=16, color=Theme.ACCENT_RED, weight="BOLD").next_to(pixel_frame, UP, buff=0.1)
        pixel_panel = VGroup(pixel_frame, pixel_col, pixel_lbl)
        
        # PANEL 3: CONDITIONING
        c_prompt = safe_box(["Semantic Map", "Text", "Images"], 2.0, 1.8, Theme.BOX_FILL, Theme.ACCENT_GOLD)
        c_enc = safe_box(["Conditioning", "Encoder (tau)"], 2.0, 0.8, Theme.BOX_FILL_ALT, Theme.PRIMARY)
        
        cond_col = VGroup(c_prompt, c_enc).arrange(DOWN, buff=0.4)
        cond_frame = SurroundingRectangle(cond_col, color=Theme.ACCENT_GOLD, fill_color=Theme.BG, fill_opacity=0.3, corner_radius=0.2, buff=0.2)
        cond_lbl = Text("Conditioning", font_size=16, color=Theme.ACCENT_GOLD, weight="BOLD").next_to(cond_frame, UP, buff=0.1)
        cond_panel = VGroup(cond_frame, cond_col, cond_lbl)
        
        # PANEL 2: LATENT SPACE (Khung ảo)
        latent_frame = RoundedRectangle(width=5.5, height=pixel_frame.height, corner_radius=0.2, stroke_color=Theme.SUCCESS, fill_color=Theme.BG, fill_opacity=0.3)
        latent_lbl = Text("Latent Space", font_size=16, color=Theme.SUCCESS, weight="BOLD").next_to(latent_frame, UP, buff=0.1)
        
        # Lõi A: U-Net
        unet_box = safe_box(["Denoising U-Net", "(Diffusion)"], 3.5, 1.5, Theme.BOX_FILL_ALT, Theme.SUCCESS)
        z_in = safe_box(["z"], 0.6, 1.5, Theme.DIM, Theme.SUCCESS)
        z_out = safe_box(["z_T"], 0.6, 1.5, Theme.DIM, Theme.SUCCESS)
        core_unet = VGroup(z_in, unet_box, z_out).arrange(RIGHT, buff=0.3)
        core_unet.move_to(latent_frame.get_center())
        
        latent_panel = VGroup(latent_frame, latent_lbl, core_unet)
        
        # --- 3. Gom và Neo tuyệt đối chống Lỗi Đè chữ & Tràn biên dọc ---
        architecture = VGroup(pixel_panel, latent_panel, cond_panel).arrange(RIGHT, buff=0.6)
        
        # FIX TRIỆT ĐỂ: Ép cứng chiều cao an toàn tối đa 3.8 để chống lỗi trôi ra ngoài biên dưới
        architecture.set_height(3.8)
        
        # Đặt nằm dưới s1_header thay vì dùng move_to cố định
        architecture.next_to(s1_header, DOWN, buff=0.4)
        architecture.set_x(0) # Chỉ căn giữa trục ngang, giữ nguyên trục dọc an toàn
        
        # --- 4. Tạo Lõi B (TARFlow) Kế thừa Scale (Chống Lỗi Vỡ khung) ---
        tarf_box = safe_box(["Transformer", "Autoregressive", "Flows"], 3.5, 1.5, ManimColor("#E3F2FD"), Theme.PRIMARY)
        for txt in tarf_box[1]: txt.set_color(BLACK) 
        z_block = safe_box(["Z"], 0.6, 1.5, ManimColor("#558B2F"), Theme.SUCCESS)
        
        core_tarf = VGroup(tarf_box, z_block).arrange(RIGHT, buff=0.5)
        # Ép kích thước của TARFlow hoàn toàn khớp với U-Net đã được scale
        core_tarf.match_height(core_unet)
        core_tarf.move_to(latent_frame.get_center())
        
        # --- 5. Vẽ Mũi tên External ---
        ext_arrows = VGroup(
            Arrow(p_x.get_bottom(), p_enc.get_top(), buff=0.05, color=Theme.NEUTRAL, stroke_width=2),
            Arrow(p_dec.get_bottom(), p_xout.get_top(), buff=0.05, color=Theme.NEUTRAL, stroke_width=2),
            Arrow(p_enc.get_right(), latent_frame.get_left(), buff=0.1, color=Theme.PRIMARY, stroke_width=3, tip_length=0.15),
            Arrow(latent_frame.get_left(), p_dec.get_right(), buff=0.1, color=Theme.PRIMARY, stroke_width=3, tip_length=0.15),
            Arrow(c_prompt.get_bottom(), c_enc.get_top(), buff=0.05, color=Theme.NEUTRAL, stroke_width=2),
            Arrow(c_enc.get_left(), latent_frame.get_right(), buff=0.1, color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.15)
        )

        # =====================================================================
        # SCENE 2: ELBO & PERFORMANCE TABLE
        # =====================================================================
        
        s2_t1 = Text("• Learning of Latent Normalizing Flows is equivalent to maximizing the\n  Evidence Lower Bound (ELBO).", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        s2_t2 = Text("• Following LDM, learn the latent space of a pre-trained autoencoder.", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        s2_header = VGroup(s2_t1, s2_t2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        s2_header.next_to(title, DOWN, aligned_edge=LEFT, buff=0.4)
        
        elbo_eq = MathTex(
            r"\mathcal{L} = \mathbb{E}_{\tilde{\mathbf{x}} \sim p_{enc}(\tilde{\mathbf{x}} \mid \mathbf{x})} \left[ ",
            r"\log p_{af}(\tilde{\mathbf{x}})", 
            r"+ \log p_{dec}(\mathbf{x} \mid \tilde{\mathbf{x}}) - \log p_{enc}(\tilde{\mathbf{x}} \mid \mathbf{x}) \right]",
            font_size=36, color=Theme.NEUTRAL
        )
        elbo_hl = SurroundingRectangle(elbo_eq[1], color=Theme.ACCENT_GOLD, stroke_width=2, buff=0.1)
        elbo_group = VGroup(elbo_eq, elbo_hl).next_to(s2_header, DOWN, buff=0.8)
        elbo_group.set_x(0)
        
        c1 = VGroup(
            Text("Model Comparison", font=Theme.FONT_BODY, font_size=20, weight="BOLD", color=Theme.NEUTRAL),
            Text("Pixel Space", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL),
            Text("Latent Space", font=Theme.FONT_BODY, font_size=18, color=Theme.PRIMARY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        c2 = VGroup(
            Text("FID", font=Theme.FONT_BODY, font_size=20, weight="BOLD", color=Theme.NEUTRAL),
            Text("4.69", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL),
            Text("2.40", font=Theme.FONT_BODY, font_size=18, color=Theme.PRIMARY, weight="BOLD")
        ).arrange(DOWN, aligned_edge=ORIGIN, buff=0.3)
        
        table = VGroup(c1, c2).arrange(RIGHT, buff=1.2, aligned_edge=UP)
        hline1 = Line(table.get_corner(UL) + DOWN*0.35, table.get_corner(UR) + DOWN*0.35, color=Theme.DIM, stroke_width=2)
        hline2 = Line(table.get_corner(DL) + UP*0.35, table.get_corner(DR) + UP*0.35, color=Theme.DIM, stroke_width=1)
        
        table_group = VGroup(table, hline1, hline2).next_to(elbo_group, DOWN, buff=0.8)
        table_group.set_x(0)

        # =====================================================================
        # KỊCH BẢN ANIMATION
        # =====================================================================
        
        self.play(Write(title))
        
        # --- SCENE 1 ---
        self.play(Write(s1_header))
        self.next_slide()
        
        self.play(FadeIn(architecture), FadeIn(ext_arrows))
        self.next_slide()
        
        # Transform U-Net -> TARFlow (Khớp tuyệt đối tỷ lệ đã co nhỏ)
        self.play(
            FadeOut(core_unet, scale=0.8),
            FadeIn(core_tarf, scale=1.2)
        )
        self.next_slide()
        
        # --- SCENE 2 ---
        self.play(
            FadeOut(s1_header, shift=UP),
            FadeOut(architecture, shift=UP),
            FadeOut(ext_arrows, shift=UP),
            FadeOut(core_tarf, shift=UP)
        )
        
        self.play(Write(s2_header))
        self.next_slide()
        
        self.play(FadeIn(elbo_eq, shift=UP))
        self.play(Create(elbo_hl))
        self.next_slide()
        
        self.play(FadeIn(table_group, shift=UP))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 43 — MODULE 40: STARFlow Architecture  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module40_STARFlow(Slide):
    def construct(self):
        # 1. Nền & Tiêu đề
        self.camera.background_color = Theme.BG
        title = slide_title("Scalable Transformer AutoRegressive Flows")
        self.play(Write(title))
        
        # =====================================================================
        # HÀM XÂY DỰNG KHỐI AN TOÀN (Ngăn chặn 100% lỗi tràn chữ)
        # =====================================================================
        def make_block(label, width, height, bg_color, text_color=Theme.NEUTRAL, stroke=Theme.NEUTRAL, font_size=18):
            rect = RoundedRectangle(
                width=width, height=height, corner_radius=0.1,
                fill_color=bg_color, fill_opacity=1, stroke_color=stroke, stroke_width=1.5
            )
            txt = Text(label, font=Theme.FONT_BODY, font_size=font_size, color=text_color, weight="BOLD")
            # Tự động thu nhỏ chữ nếu nó dài hơn hộp (Trừ đi 0.3 buff an toàn)
            if txt.width > width - 0.3:
                txt.scale((width - 0.3) / txt.width)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt)

        def make_math_block(tex_str, width, height, bg_color, text_color=Theme.NEUTRAL, stroke=Theme.NEUTRAL, font_size=24):
            rect = RoundedRectangle(
                width=width, height=height, corner_radius=0.1,
                fill_color=bg_color, fill_opacity=1, stroke_color=stroke, stroke_width=1.5
            )
            txt = MathTex(tex_str, font_size=font_size, color=text_color)
            if txt.width > width - 0.3:
                txt.scale((width - 0.3) / txt.width)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt)

        COL_WIDTH = 4.6 # Độ rộng đồng bộ cho tất cả các khối chính
        
        # =====================================================================
        # CỘT TRÁI: SAMPLING FLOW (z -> x)
        # =====================================================================
        
        l_header = Text("Sampling (z → x)", font_size=20, color=Theme.PRIMARY, weight="BOLD")
        l_img = make_block("Synthesized\nImage", 2.2, 0.9, Theme.BG, Theme.SUCCESS, Theme.SUCCESS, font_size=16)
        l_dec = make_block("Decoder", 2.2, 0.5, ManimColor("#64B5F6"), BLACK, Theme.NEUTRAL)
        l_x0 = make_math_block(r"[ \mathbf{x}_1^0, \mathbf{x}_2^0, \dots, \mathbf{x}_N^0 ]", COL_WIDTH, 0.5, Theme.BOX_FILL, Theme.NEUTRAL, Theme.DIM)
        
        # Ngắt dòng \n giúp text không đâm xuyên ra khỏi vỏ hộp
        l_shallow = make_block("Shallow Transformer Blocks\n(Alternating)", COL_WIDTH, 0.9, ManimColor("#E3F2FD"), BLACK, Theme.PRIMARY, font_size=16)
        l_deep = make_block("Deep Transformer Block (→)", COL_WIDTH, 0.7, ManimColor("#FFF9C4"), BLACK, Theme.ACCENT_GOLD, font_size=16)
        
        l_prompt = make_block("Prompt", 1.2, 0.5, ManimColor("#D1C4E9"), BLACK, font_size=16)
        l_z = make_math_block(r"[ \mathbf{z}_1, \mathbf{z}_2, \dots, \mathbf{z}_N ]", COL_WIDTH - 1.4, 0.5, Theme.BOX_FILL, Theme.NEUTRAL, Theme.DIM)
        l_z_layer = VGroup(l_prompt, l_z).arrange(RIGHT, buff=0.2) # Tổng width = 1.2 + 0.2 + (4.6 - 1.4) = 4.6
        
        l_eq_text = MathTex(r"\mathbf{x}_{\pi < d}^t = \mu_\theta(\cdot) + \sigma_\theta(\cdot) \cdot \mathbf{x}_{\pi < d}^{t+1}", font_size=22, color=BLACK)
        l_eq_box = SurroundingRectangle(l_eq_text, color=Theme.SUCCESS, fill_color=ManimColor("#E0F2F1"), fill_opacity=1, buff=0.15)
        l_eq = VGroup(l_eq_box, l_eq_text)
        if l_eq.width > COL_WIDTH: l_eq.scale(COL_WIDTH / l_eq.width)
        
        # Gom Cột Trái
        col_left = VGroup(l_header, l_img, l_dec, l_x0, l_shallow, l_deep, l_z_layer, l_eq).arrange(DOWN, buff=0.2)
        
        # =====================================================================
        # CỘT PHẢI: TRAINING FLOW (x -> z)
        # =====================================================================
        
        r_header = Text("Training (x → z)", font_size=20, color=Theme.ACCENT_GOLD, weight="BOLD")
        r_img = make_block("Real Image", 2.2, 0.9, Theme.BG, Theme.ACCENT_GOLD, Theme.ACCENT_GOLD, font_size=16)
        r_enc = make_block("Encoder", 2.2, 0.5, ManimColor("#FFB74D"), BLACK, Theme.NEUTRAL)
        r_x0 = make_math_block(r"[ \mathbf{x}_1^0, \mathbf{x}_2^0, \dots, \mathbf{x}_N^0 ]", COL_WIDTH, 0.5, Theme.BOX_FILL, Theme.NEUTRAL, Theme.DIM)
        
        r_shallow = make_block("Shallow Transformer Blocks\n(Alternating)", COL_WIDTH, 0.9, ManimColor("#E3F2FD"), BLACK, Theme.PRIMARY, font_size=16)
        r_deep = make_block("Deep Transformer Block (→)", COL_WIDTH, 0.7, ManimColor("#FFF9C4"), BLACK, Theme.ACCENT_GOLD, font_size=16)
        
        r_prompt = make_block("Prompt", 1.2, 0.5, ManimColor("#D1C4E9"), BLACK, font_size=16)
        r_z = make_math_block(r"[ \mathbf{z}_1, \mathbf{z}_2, \dots, \mathbf{z}_N ]", COL_WIDTH - 1.4, 0.5, Theme.BOX_FILL, Theme.NEUTRAL, Theme.DIM)
        r_z_layer = VGroup(r_prompt, r_z).arrange(RIGHT, buff=0.2)
        
        r_eq_text = MathTex(r"\max_\theta \ -\frac{1}{2}\|\mathbf{z}\|_2^2 - \sum_{t, d} \log \sigma_\theta^t(\mathbf{x}_{\pi < d}^t)", font_size=22, color=BLACK)
        r_eq_box = SurroundingRectangle(r_eq_text, color=Theme.SUCCESS, fill_color=ManimColor("#E8F5E9"), fill_opacity=1, buff=0.15)
        r_eq = VGroup(r_eq_box, r_eq_text)
        if r_eq.width > COL_WIDTH: r_eq.scale(COL_WIDTH / r_eq.width)
        
        # Gom Cột Phải
        col_right = VGroup(r_header, r_img, r_enc, r_x0, r_shallow, r_deep, r_z_layer, r_eq).arrange(DOWN, buff=0.2)
        
        # =====================================================================
        # ÉP KHUNG TOÀN CỤC & TẠO MŨI TÊN (KHẮC PHỤC TRIỆT ĐỂ LỖI)
        # =====================================================================
        
        diagram = VGroup(col_left, col_right).arrange(RIGHT, buff=1.2, aligned_edge=UP)
        
        # Thuật toán giới hạn an toàn 100% không đè title
        MAX_HEIGHT = 6.2
        MAX_WIDTH = 13.5
        if diagram.height > MAX_HEIGHT:
            diagram.scale(MAX_HEIGHT / diagram.height)
        if diagram.width > MAX_WIDTH:
            diagram.scale(MAX_WIDTH / diagram.width)
            
        # Ghim cứng ngay dưới Title
        diagram.next_to(title, DOWN, buff=0.25)
        
        divider = Line(diagram.get_corner(UP) + UP*0.2, diagram.get_corner(DOWN) + DOWN*0.2, color=Theme.DIM)
        
        # VẼ MŨI TÊN (Tọa độ các hộp lúc này đã khóa vĩnh viễn)
        def create_flow_arrows(col, is_sampling):
            arrs = VGroup()
            # Mạng đi lên: Z(6) -> Deep(5) -> Shallow(4) -> X0(3)
            arrs.add(Arrow(col[6].get_top(), col[5].get_bottom(), buff=0.1, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12))
            arrs.add(Arrow(col[5].get_top(), col[4].get_bottom(), buff=0.1, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12))
            arrs.add(Arrow(col[4].get_top(), col[3].get_bottom(), buff=0.1, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.12))

            if is_sampling:
                # Sampling: X0(3) -> Decoder(2) -> Image(1) [Đi Lên]
                arrs.add(Arrow(col[3].get_top(), col[2].get_bottom(), buff=0.1, color=Theme.PRIMARY, stroke_width=3, tip_length=0.15))
                arrs.add(Arrow(col[2].get_top(), col[1].get_bottom(), buff=0.1, color=Theme.PRIMARY, stroke_width=3, tip_length=0.15))
            else:
                # Training: Image(1) -> Encoder(2) -> X0(3) [Đi Xuống]
                arrs.add(Arrow(col[1].get_bottom(), col[2].get_top(), buff=0.1, color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.15))
                arrs.add(Arrow(col[2].get_bottom(), col[3].get_top(), buff=0.1, color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.15))
            return arrs

        arrows_left = create_flow_arrows(col_left, is_sampling=True)
        arrows_right = create_flow_arrows(col_right, is_sampling=False)
        
        # Nhãn bổ trợ bên hông
        lbl_N0I = Text("N(0, I)", font_size=16, color=Theme.NEUTRAL).next_to(arrows_left[0], LEFT, buff=0.1)
        lbl_log = Text("Log Prob(·)", font_size=16, color=Theme.NEUTRAL).next_to(arrows_right[0], LEFT, buff=0.1)
        
        # =====================================================================
        # KỊCH BẢN HIỂN THỊ
        # =====================================================================
        
        scene_left = VGroup(col_left, arrows_left, lbl_N0I)
        scene_right = VGroup(col_right, arrows_right, lbl_log)
        
        # 1. Hiển thị mạch Generation (Bên trái)
        self.play(FadeIn(scene_left, shift=RIGHT))
        self.next_slide()
        
        # 2. Hiển thị vách ngăn và mạch Training (Bên phải)
        self.play(Create(divider))
        self.play(FadeIn(scene_right, shift=LEFT))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 44 — MODULE 41: NOISE-AUGMENTED TRAINING  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Ellipse, Cross, Star, SurroundingRectangle, DashedLine

class Module41_NoiseAugmented(Slide):
    def construct(self):
        # 1. Nền & Tiêu đề cố định
        self.camera.background_color = Theme.BG
        title = slide_title("Key Ingredient 5: Noise-augmented Training")
        self.play(Write(title))

        # =====================================================================
        # SCENE 1: THE PROBLEM (MLE in High-D & Jacobian Cheat)
        # =====================================================================
        
        # --- Phương trình MLE cơ bản ---
        s1_eq = MathTex(
            r"p(\mathbf{x}) =", 
            r"p_0(f(\mathbf{x}))", 
            r"\left| \det\left(\frac{\partial f(\mathbf{x})}{\partial \mathbf{x}}\right) \right|",
            font_size=42, color=Theme.NEUTRAL
        )
        # Thu hẹp buff xuống 0.06 để hai viền bao quanh hoàn toàn không giao nhau
        s1_box1 = SurroundingRectangle(s1_eq[1], color=Theme.ACCENT_GOLD, buff=0.06, stroke_width=2)
        s1_lbl1 = Text("Prior", font_size=18, color=Theme.ACCENT_GOLD).next_to(s1_box1, UP, buff=0.1)
        
        s1_box2 = SurroundingRectangle(s1_eq[2], color=Theme.PRIMARY, buff=0.06, stroke_width=2)
        s1_lbl2 = Text("Local Volume Change", font_size=18, color=Theme.PRIMARY).next_to(s1_box2, UP, buff=0.1)
        
        s1_math_group = VGroup(s1_eq, s1_box1, s1_lbl1, s1_box2, s1_lbl2)
        
        # --- Giải thích Vấn đề ---
        s1_t1 = Text("• Limitation of MLE training in high-D:", font=Theme.FONT_BODY, font_size=28, color=Theme.ACCENT_GOLD, weight="BOLD")
        s1_t2 = Text("  Jacobian \"cheat\": MLE raises likelihood by shrinking volume (huge log|det|)", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        s1_t3 = Text("  Illusory score: High density ≠ High probability → Junk samples.", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_RED, slant="ITALIC")
        s1_text_group = VGroup(s1_t1, s1_t2, s1_t3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # --- Đồ họa: Jacobian Cheat ---
        ell_X = Ellipse(width=3.0, height=2.0, color=Theme.NEUTRAL, stroke_width=2)
        # Đưa nhãn X vào hẳn bên trong lòng đường Elip một cách an toàn
        lbl_X = MathTex(r"\mathbf{X}", font_size=36, color=Theme.NEUTRAL).move_to(ell_X.get_center() + DOWN*0.5 + LEFT*0.9)
        
        ell_Z = Ellipse(width=4.0, height=2.5, color=Theme.NEUTRAL, stroke_width=2)
        # Đưa nhãn Z vào hẳn bên trong lòng đường Elip một cách an toàn
        lbl_Z = MathTex(r"\mathbf{Z}", font_size=48, color=Theme.NEUTRAL).move_to(ell_Z.get_center() + UP*0.6 + RIGHT*1.2)
        
        set_group = VGroup(VGroup(ell_X, lbl_X), VGroup(ell_Z, lbl_Z)).arrange(RIGHT, buff=2.0)
        
        # Đóng băng tọa độ Set X và Z trước khi vẽ các điểm và mũi tên liên kết
        s1_diagram = VGroup(s1_math_group, s1_text_group, set_group).arrange(DOWN, buff=0.5)
        s1_diagram.set_height(5.5)
        s1_diagram.move_to([0, -0.2, 0])
        
        # Vẽ các điểm và mũi tên dựa theo tọa độ thực tế đã cố định
        dot_x = Dot(ell_X.get_center() + DOWN*0.5, color=WHITE)
        dot_z = Dot(ell_Z.get_center() + DOWN*0.5 + RIGHT*1.0, color=WHITE)
        arr_f = Arrow(dot_x.get_right(), dot_z.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=2)
        lbl_f = MathTex("f", font_size=24).next_to(arr_f, UP, buff=0.1)
        
        # Sample sinh ra rác (Junk sample)
        star_z = Star(outer_radius=0.15, inner_radius=0.07, color=Theme.ACCENT_GOLD, fill_opacity=1).move_to(ell_Z.get_center() + UP*0.5 + LEFT*0.5)
        cross_x = Cross(stroke_color=Theme.ACCENT_RED, stroke_width=4, scale_factor=0.2).move_to(ell_X.get_center() + UP*1.2 + LEFT*0.5)
        arr_inv = Arrow(star_z.get_left(), cross_x.get_right(), buff=0.1, color=Theme.ACCENT_GOLD, stroke_width=2)
        
        # Tăng buff của nhãn Junk Sample để không chạm vào dấu Cross đỏ
        s1_junk_lbl = Text("Junk Sample", font_size=16, color=Theme.ACCENT_RED).next_to(cross_x, LEFT, buff=0.2)
        
        s1_full = VGroup(s1_diagram, dot_x, dot_z, arr_f, lbl_f, star_z, cross_x, arr_inv, s1_junk_lbl)

        # =====================================================================
        # SCENE 2: THE SOLUTION (Noise-augmented Distribution)
        # =====================================================================
        
        s2_t1 = Text("Solution: Add a small and fixed amount of noise", font=Theme.FONT_BODY, font_size=32, color=Theme.ACCENT_GOLD, weight="BOLD")
        s2_eq = MathTex(r"q(\mathbf{y}) = \int p(\mathbf{y} - \epsilon) p_\epsilon(\epsilon) d\epsilon", font_size=42, color=Theme.NEUTRAL)
        s2_t2 = Text("Instead of exact points, we learn a flow on tubes (volumes) y = x + ε", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        s2_header = VGroup(s2_t1, s2_eq, s2_t2).arrange(DOWN, buff=0.4)
        
        # Tái sử dụng Set X và Z
        s2_ell_X = Ellipse(width=3.0, height=2.0, color=Theme.NEUTRAL, stroke_width=2)
        s2_lbl_X = MathTex(r"\mathbf{X}", font_size=36, color=Theme.NEUTRAL).move_to(s2_ell_X.get_center() + DOWN*0.5 + LEFT*0.9)
        s2_ell_Z = Ellipse(width=4.0, height=2.5, color=Theme.NEUTRAL, stroke_width=2)
        s2_lbl_Z = MathTex(r"\mathbf{Z}", font_size=48, color=Theme.NEUTRAL).move_to(s2_ell_Z.get_center() + UP*0.6 + RIGHT*1.2)
        s2_set_group = VGroup(VGroup(s2_ell_X, s2_lbl_X), VGroup(s2_ell_Z, s2_lbl_Z)).arrange(RIGHT, buff=2.0)
        
        s2_diagram = VGroup(s2_header, s2_set_group).arrange(DOWN, buff=0.8)
        s2_diagram.set_height(5.5)
        s2_diagram.move_to([0, -0.2, 0])
        
        # Vẽ "Tubes" (Vùng lân cận nhiễu)
        tube_x = Circle(radius=0.3, color=Theme.NEUTRAL, stroke_width=1.5).move_to(s2_ell_X.get_center() + UP*0.2)
        tube_z = Circle(radius=0.4, color=Theme.NEUTRAL, stroke_width=1.5).move_to(s2_ell_Z.get_center() + UP*0.5 + LEFT*0.2)
        
        s2_dot_x = Dot(tube_x.get_center(), color=WHITE)
        s2_star_z = Star(outer_radius=0.15, inner_radius=0.07, color=Theme.ACCENT_GOLD, fill_opacity=1).move_to(tube_z.get_center() + RIGHT*0.1)
        
        # Nối vùng (Tube mapping)
        line_top = Line(tube_x.get_top(), tube_z.get_top(), color=Theme.NEUTRAL, stroke_width=1.5)
        line_bot = Line(tube_x.get_bottom(), tube_z.get_bottom(), color=Theme.NEUTRAL, stroke_width=1.5)
        arr_s2_f = Arrow(s2_dot_x.get_right(), s2_star_z.get_left(), buff=0.1, color=Theme.ACCENT_GOLD, stroke_width=2)
        
        s2_lbl_f = MathTex("f", font_size=24).next_to(line_top, UP, buff=0.1)
        s2_lbl_tube = Text("Improves density\nwithin a volume", font_size=16, color=Theme.PRIMARY).next_to(tube_z, DOWN, buff=0.2)
        
        s2_full = VGroup(s2_diagram, tube_x, tube_z, s2_dot_x, s2_star_z, line_top, line_bot, arr_s2_f, s2_lbl_f, s2_lbl_tube)

        # =====================================================================
        # SCENE 3: RECOVERING X FROM Y
        # =====================================================================
        
        s3_title = Text("How can we recover x from y?", font=Theme.FONT_BODY, font_size=32, color=Theme.NEUTRAL)
        
        # Khối Option 1
        opt1_lbl = Text("Option 1: Score-based denoising", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD, weight="BOLD")
        opt1_eq = MathTex(r"\mathbf{x} = \mathbf{y} + \sigma_L^2 \nabla_{\mathbf{y}} \log p(\mathbf{y})", font_size=36, color=Theme.NEUTRAL)
        
        # Dựng ảnh giả lập (Tái sử dụng concept từ Module 31)
        box_noisy = RoundedRectangle(width=1.2, height=1.2, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_RED, stroke_width=2, fill_opacity=1)
        txt_noisy = Text("Noisy y", font_size=16, color=Theme.ACCENT_RED).move_to(box_noisy)
        box_clean = RoundedRectangle(width=1.2, height=1.2, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY, stroke_width=2, fill_opacity=1)
        txt_clean = Text("Clean x", font_size=16, color=Theme.PRIMARY).move_to(box_clean)
        
        arr_denoise = Arrow(box_noisy.get_right(), box_clean.get_left(), buff=0.2, color=Theme.SUCCESS, stroke_width=4)
        vis_opt1 = VGroup(VGroup(box_noisy, txt_noisy), arr_denoise, VGroup(box_clean, txt_clean)).arrange(RIGHT, buff=0.2)
        
        block_opt1 = VGroup(opt1_lbl, opt1_eq, vis_opt1).arrange(DOWN, buff=0.3)
        
        # Đường phân cách
        div_line = DashedLine(LEFT*5, RIGHT*5, color=Theme.DIM)
        
        # Khối Option 2
        opt2_lbl = Text("Option 2: Decoder denoising (Latent Space)", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD, weight="BOLD")
        opt2_eq = MathTex(
            r"\mathcal{L} = \mathbb{E}_{\mathbf{y} \sim p_{enc}(\mathbf{y}|\mathbf{x})} \Big[ ",
            r"\log p_{af}(\mathbf{y}) + \log p_{dec}(\mathbf{x}|\mathbf{y})", 
            r" - \log p_{enc}(\mathbf{y}|\mathbf{x}) \Big]",
            font_size=32, color=Theme.NEUTRAL
        )
        opt2_box = SurroundingRectangle(opt2_eq[1], color=Theme.ACCENT_GOLD, stroke_width=2, buff=0.1)
        opt2_note = Text("Fine-tune decoder with standard VAE loss", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL, slant="ITALIC")
        
        block_opt2 = VGroup(opt2_lbl, VGroup(opt2_eq, opt2_box), opt2_note).arrange(DOWN, buff=0.3)
        
        s3_full = VGroup(s3_title, block_opt1, div_line, block_opt2).arrange(DOWN, buff=0.5)
        s3_full.set_height(5.5)
        s3_full.move_to([0, -0.2, 0])

        # =====================================================================
        # KỊCH BẢN ANIMATION
        # =====================================================================
        
        # --- SCENE 1 ---
        self.play(Write(s1_math_group))
        self.next_slide()
        
        self.play(Write(s1_text_group))
        self.play(FadeIn(s1_diagram[2])) # Hiện set X, Z
        self.play(
            FadeIn(dot_x), FadeIn(dot_z), Create(arr_f), Write(lbl_f)
        )
        self.play(
            FadeIn(star_z), Create(arr_inv), FadeIn(cross_x), Write(s1_junk_lbl)
        )
        self.next_slide()
        
        # --- SCENE 2 ---
        self.play(FadeOut(s1_full, shift=UP))
        
        self.play(Write(s2_header))
        self.play(FadeIn(s2_set_group))
        self.play(
            Create(tube_x), Create(tube_z), FadeIn(s2_dot_x), FadeIn(s2_star_z)
        )
        self.play(
            Create(line_top), Create(line_bot), Create(arr_s2_f), Write(s2_lbl_f), FadeIn(s2_lbl_tube)
        )
        self.next_slide()
        
        # --- SCENE 3 ---
        self.play(FadeOut(s2_full, shift=UP))
        
        self.play(Write(s3_title))
        self.play(FadeIn(block_opt1, shift=UP))
        self.next_slide()
        
        self.play(Create(div_line))
        self.play(FadeIn(block_opt2, shift=UP))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 45 — MODULE 42: INFERENCE WITH GUIDANCE (CFG)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import SurroundingRectangle, Cross, CurvedArrow

class Module42_InferenceGuidance(Slide):
    def construct(self):
        # 1. Nền & Tiêu đề cố định
        self.camera.background_color = Theme.BG
        title = slide_title("Key Ingredient 6: Inference with Guidance")
        self.play(Write(title))

        # =====================================================================
        # SCENE 1: THE NAIVE APPROACH & ITS FAILURE
        # =====================================================================
        
        s1_t1 = Text("Classifier-free Guidance (CFG) is critical for high-quality samples.", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        
        # Phương trình CFG tổng quát (Sử dụng r"..." và KHÔNG dùng weight="BOLD" trong MathTex)
        s1_eq_base = MathTex(
            r"\nabla_{\mathbf{x}}\log \tilde{p}_c(\mathbf{x}) = \nabla_{\mathbf{x}}\log p_c(\mathbf{x}) + \omega \left( \nabla_{\mathbf{x}}\log p_c(\mathbf{x}) - \nabla_{\mathbf{x}}\log p_u(\mathbf{x}) \right)",
            font_size=36, color=Theme.ACCENT_GOLD
        )
        
        s1_t2 = Text("Naively guiding the mean/std independently:", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, slant="ITALIC")
        
        s1_eq_naive = MathTex(
            r"\tilde{\mu}_c = \mu_c + \omega(\mu_c - \mu_u) \quad \text{and} \quad \tilde{\sigma}_c = \sigma_c + \omega(\sigma_c - \sigma_u)",
            font_size=36, color=Theme.NEUTRAL
        )
        
        # Đồ họa so sánh: Pixel (Works) vs Latent (Fails)
        def make_result_box(title_str, bg_color, stroke_color, is_fail=False):
            box = RoundedRectangle(width=3.5, height=2.0, corner_radius=0.15, fill_color=bg_color, fill_opacity=0.2, stroke_color=stroke_color, stroke_width=2)
            lbl = Text(title_str, font_size=22, color=stroke_color, weight="BOLD").next_to(box.get_top(), DOWN, buff=0.2)
            
            content = VGroup()
            if is_fail:
                # Tạo một vùng nhiễu màu sắc lộn xộn để mô phỏng ảnh bị hỏng (junk sample)
                import random
                random.seed(1)
                dots = VGroup(*[Dot(point=[random.uniform(-1.5, 1.5), random.uniform(-0.5, 0.2), 0], radius=0.03, color=random.choice([BLUE, RED, GREEN, YELLOW])) for _ in range(150)])
                dots.move_to(box.get_center() + DOWN*0.2)
                cross = Cross(stroke_color=Theme.ACCENT_RED, stroke_width=6, scale_factor=0.3).move_to(box.get_center() + DOWN*0.2)
                content = VGroup(dots, cross)
            else:
                # Vùng sạch sẽ
                check = Text("Empirically quite well!", font_size=20, color=Theme.SUCCESS).move_to(box.get_center() + DOWN*0.2)
                content = VGroup(check)
                
            return VGroup(box, lbl, content)

        box_pixel = make_result_box("Pixel Space", Theme.SUCCESS, Theme.SUCCESS, is_fail=False)
        box_latent = make_result_box("Latent Flows", Theme.ACCENT_RED, Theme.ACCENT_RED, is_fail=True)
        
        s1_compare = VGroup(box_pixel, box_latent).arrange(RIGHT, buff=1.0)
        
        # Đóng gói và ép khung Scene 1
        scene1 = VGroup(s1_t1, s1_eq_base, s1_t2, s1_eq_naive, s1_compare).arrange(DOWN, buff=0.4)
        scene1.set_height(5.5)
        scene1.move_to([0, -0.2, 0])
        
        self.play(FadeIn(scene1, shift=UP))
        self.next_slide()
        
        # =====================================================================
        # SCENE 2: WHY IT FAILS & PERSPECTIVE SHIFT
        # =====================================================================
        
        self.play(FadeOut(scene1, shift=UP))
        
        s2_t1 = Text("Why do Latent Flows fail with naive CFG?", font=Theme.FONT_BODY, font_size=32, color=Theme.ACCENT_RED, weight="BOLD")
        
        s2_t2 = Text("• Compared to pixels, latent space is unbounded and highly\n  sensitive to extreme values (large w blows up the image).", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        s2_t3 = Text("• Solution: We need to re-derive CFG from the score perspective.", font=Theme.FONT_BODY, font_size=28, color=Theme.ACCENT_GOLD)
        
        s2_text_group = VGroup(s2_t1, s2_t2, s2_t3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        # Đồ họa: Chỉ Apply CFG ở khối Deep (Kế thừa concept module 38)
        deep_block = RoundedRectangle(width=8.0, height=1.5, fill_color=ManimColor("#455A64"), fill_opacity=1, stroke_color=Theme.NEUTRAL)
        deep_lbl = Text("Deep Autoregressive Transformer (Gaussian Space)", font_size=20, color=WHITE).move_to(deep_block)
        db_group = VGroup(deep_block, deep_lbl)
        
        shallow_block = RoundedRectangle(width=8.0, height=0.6, fill_color=ManimColor("#37474F"), fill_opacity=1, stroke_color=Theme.NEUTRAL)
        shallow_lbl = Text("Shallow Transformers", font_size=16, color=GRAY).move_to(shallow_block)
        sb_group = VGroup(shallow_block, shallow_lbl).next_to(db_group, DOWN, buff=0.1)
        
        arch_group = VGroup(db_group, sb_group)
        
        s2_insight = Text("Key Insight: Only need to guide ONCE here!", font_size=22, color=Theme.SUCCESS, weight="BOLD")
        
        scene2 = VGroup(s2_text_group, arch_group, s2_insight).arrange(DOWN, buff=0.6)
        scene2.set_height(5.5)
        scene2.move_to([0, -0.2, 0])
        
        # Vẽ mũi tên kết nối (Sau khi đóng băng tọa độ)
        arr_guide = CurvedArrow(
            start_point=s2_insight.get_top() + LEFT*0.5,
            end_point=deep_block.get_bottom() + LEFT*2.0,
            angle=-0.5, color=Theme.SUCCESS, stroke_width=3
        )
        s2_full = VGroup(scene2, arr_guide)
        
        self.play(FadeIn(s2_full, shift=UP))
        self.next_slide()
        
        # =====================================================================
        # SCENE 3: THE PROPOSED MATH (PROPOSITION 2)
        # =====================================================================
        
        self.play(FadeOut(s2_full, shift=UP))
        
        # Khung chứa Proposition (Mô phỏng giống paper)
        prop_bg = RoundedRectangle(width=12.5, height=3.2, corner_radius=0.15, fill_color=ManimColor("#ECEFF1"), fill_opacity=0.1, stroke_color=Theme.NEUTRAL, stroke_width=2)
        
        p_t1 = Text("Proposition 2: Correct Guidance for Gaussian", font=Theme.FONT_BODY, font_size=24, color=Theme.PRIMARY, weight="BOLD")
        p_t2 = MathTex(r"\text{Given } p_u = \mathcal{N}(\mu_u, \sigma_u^2 \mathbf{I}) \text{ and } p_c = \mathcal{N}(\mu_c, \sigma_c^2 \mathbf{I}), \text{ the guided } \tilde{p}_c \text{ satisfies:}", font_size=30, color=Theme.NEUTRAL)
        
        # Phương trình lõi (Rất cẩn thận với r"..." và \mathbf)
        p_eq1 = MathTex(r"\tilde{\mu}_c = \mu_c + \frac{\omega s}{1 + \omega - \omega s} \cdot (\mu_c - \mu_u)", font_size=36, color=Theme.ACCENT_GOLD)
        p_eq2 = MathTex(r"\tilde{\sigma}_c = \frac{1}{\sqrt{1 + \omega - \omega s}} \cdot \sigma_c", font_size=36, color=Theme.ACCENT_GOLD)
        
        p_eq_group = VGroup(p_eq1, p_eq2).arrange(RIGHT, buff=1.0)
        p_t3 = MathTex(r"\text{where } s = \sigma_c^2 / \sigma_u^2 \text{ and } \omega > 0.", font_size=28, color=Theme.DIM)
        
        prop_content = VGroup(p_t1, p_t2, p_eq_group, p_t3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(prop_bg)
        prop_group = VGroup(prop_bg, prop_content)
        
        # Đồ họa kết quả (Visual Result)
        res_t1 = Text("w = 6 (Extreme Guidance)", font_size=22, color=Theme.NEUTRAL, slant="ITALIC")
        
        box_bad = RoundedRectangle(width=2.5, height=1.5, fill_color=Theme.BG, stroke_color=Theme.ACCENT_RED, stroke_width=2)
        lbl_bad = Text("Original (Naive)\nBlows up!", font_size=18, color=Theme.ACCENT_RED).move_to(box_bad)
        
        box_good = RoundedRectangle(width=2.5, height=1.5, fill_color=Theme.BG, stroke_color=Theme.SUCCESS, stroke_width=2)
        lbl_good = Text("Proposed\nStable!", font_size=18, color=Theme.SUCCESS).move_to(box_good)
        
        res_boxes = VGroup(VGroup(box_bad, lbl_bad), VGroup(box_good, lbl_good)).arrange(RIGHT, buff=2.0)
        res_group = VGroup(res_t1, res_boxes).arrange(DOWN, buff=0.3)
        
        # Ép khung Scene 3
        scene3 = VGroup(prop_group, res_group).arrange(DOWN, buff=0.5)
        scene3.set_height(6.0)
        scene3.move_to([0, -0.2, 0])
        
        # Vẽ mũi tên so sánh
        arr_compare = Arrow(box_bad.get_right(), box_good.get_left(), buff=0.2, color=Theme.SUCCESS, stroke_width=3)
        
        self.play(FadeIn(scene3, shift=UP))
        self.play(Create(arr_compare))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 46 — MODULE 43: SUMMARY  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module43_Summary(Slide):
    def construct(self):
        # 1. Cài đặt Nền & Tiêu đề
        self.camera.background_color = Theme.BG
        title = slide_title("Summary")
        self.play(Write(title))

        # =====================================================================
        # HÀM HỖ TRỢ ĐỒ HỌA (An toàn tuyệt đối, không tràn viền)
        # =====================================================================
        
        # Bảng màu dựa trên ảnh gốc
        C_RED   = ManimColor("#7B1113")  # Đỏ đô
        C_BLUE  = ManimColor("#1C2A60")  # Xanh dương đậm
        C_GREEN = ManimColor("#4A5D23")  # Xanh rêu
        C_ARROW = ManimColor("#7CB342")  # Xanh lá mạ cho mũi tên
        
        def make_summary_box(lines, width, height, bg_color):
            """Hàm tạo hộp chữ nhật an toàn không bao giờ đè chữ"""
            rect = Rectangle(
                width=width, height=height, 
                fill_color=bg_color, fill_opacity=1, 
                stroke_color=Theme.NEUTRAL, stroke_width=1
            )
            txt = VGroup(*[
                Text(l, font=Theme.FONT_BODY, font_size=24, color=WHITE) 
                for l in lines
            ]).arrange(DOWN, buff=0.1)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt)

        def make_image_sequence():
            """Tạo chuỗi tiến trình Denoising trừu tượng (Từ nhiễu đến sạch)"""
            import random
            random.seed(99)
            boxes = VGroup()
            for i in range(4):
                box = Rectangle(width=0.8, height=0.8, stroke_color=WHITE, stroke_width=1, fill_color=Theme.BG, fill_opacity=1)
                if i < 3:
                    # Tạo hạt nhiễu (Giảm dần theo step)
                    num_dots = 80 - (i * 35)
                    dots = VGroup(*[
                        Dot(point=[random.uniform(-0.35, 0.35), random.uniform(-0.35, 0.35), 0], radius=0.02, color=random.choice([GRAY, BLUE, RED, YELLOW]))
                        for _ in range(num_dots)
                    ])
                    dots.move_to(box.get_center())
                    boxes.add(VGroup(box, dots))
                else:
                    # Ảnh sạch cuối cùng (Màu vàng đất tượng trưng cho Golden Retriever)
                    box.set_fill(color=Theme.ACCENT_GOLD, opacity=0.8)
                    lbl = Text("Img", font_size=16, color=BLACK, weight="BOLD").move_to(box.get_center())
                    boxes.add(VGroup(box, lbl))
                    
            # Thêm mũi tên nhỏ giữa các ảnh
            seq = VGroup()
            for i in range(3):
                seq.add(boxes[i])
                seq.add(MathTex(r"\rightarrow", font_size=24, color=WHITE))
            seq.add(boxes[3])
            return seq.arrange(RIGHT, buff=0.15)

        # =====================================================================
        # BƯỚC 1: XÂY DỰNG CÁC THÀNH PHẦN (LEFT & RIGHT COLUMNS)
        # =====================================================================
        
        # --- CỘT TRÁI (LEFT COLUMN) ---
        
        # 1. Khối Autoregressive (AR)
        ar_box = make_summary_box(["Autoregressive Models", "(e.g., LLMs)"], width=5.0, height=1.6, bg_color=C_RED)
        ar_txt = Text("A → cute → golden → retriever", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        ar_group = VGroup(ar_box, ar_txt).arrange(DOWN, buff=0.3)
        
        # 2. Khối Diffusion
        diff_box = make_summary_box(["Diffusion/Flow-based", "Models (e.g., DiTs)"], width=5.0, height=1.6, bg_color=C_BLUE)
        diff_seq = make_image_sequence()
        diff_group = VGroup(diff_box, diff_seq).arrange(DOWN, buff=0.3)
        
        # Gom Cột Trái
        left_col = VGroup(ar_group, diff_group).arrange(DOWN, buff=1.0)
        
        # --- CỘT PHẢI (RIGHT COLUMN) ---
        
        # Khối STARFlow
        star_box = make_summary_box(["STARFlow", "(best of both worlds?)"], width=4.5, height=2.0, bg_color=C_GREEN)
        # Ép khung chứa box phải lớn để cân bằng khi arrange (Chống Lỗi 4 Lệch Trục)
        right_col = VGroup(star_box)

        # =====================================================================
        # BƯỚC 2: KHÓA TỌA ĐỘ TỔNG THỂ (Tránh Lỗi 3, 4)
        # =====================================================================
        
        # Đặt 2 cột cách nhau một khoảng lớn để chừa chỗ cho mũi tên
        diagram = VGroup(left_col, right_col).arrange(RIGHT, buff=3.0)
        
        # Cắt gọt kích thước an toàn
        diagram.set_height(5.5)
        diagram.set_width(13.0)
        diagram.move_to([0, -0.2, 0])
        
        # =====================================================================
        # BƯỚC 3: VẼ MŨI TÊN LIÊN KẾT (Tránh Lỗi 2 đâm xuyên màn hình)
        # =====================================================================
        
        # Chỉ lấy tọa độ sau khi `diagram.move_to` đã thực thi
        arr_top = Arrow(
            start=ar_box.get_right(), end=star_box.get_left() + UP*0.5, 
            color=C_ARROW, stroke_width=8, tip_length=0.25, buff=0.2
        )
        lbl_top = Text("Architecture / Learning", font_size=20, color=Theme.NEUTRAL).next_to(arr_top, UP, buff=0.1)
        
        arr_bot = Arrow(
            start=diff_box.get_right(), end=star_box.get_left() + DOWN*0.5, 
            color=C_ARROW, stroke_width=8, tip_length=0.25, buff=0.2
        )
        lbl_bot = Text("Flow formulation", font_size=20, color=Theme.NEUTRAL).next_to(arr_bot, DOWN, buff=0.1)
        
        arrows_group = VGroup(arr_top, lbl_top, arr_bot, lbl_bot)

        # =====================================================================
        # BƯỚC 4: KỊCH BẢN HIỂN THỊ ANIMATION
        # =====================================================================
        
        # Hiện cột trái tuần tự (Các mô hình nền tảng)
        self.play(FadeIn(ar_group, shift=RIGHT))
        self.play(FadeIn(diff_group, shift=RIGHT))
        self.next_slide()
        
        # Bắn mũi tên thể hiện sự kế thừa
        self.play(
            GrowArrow(arr_top), Write(lbl_top),
            GrowArrow(arr_bot), Write(lbl_bot)
        )
        self.next_slide()
        
        # Đưa ra kết luận cuối cùng: STARFlow
        self.play(FadeIn(star_box, scale=1.2))
        
        # Highlight viền của STARFlow để chốt bài
        highlight = SurroundingRectangle(star_box, color=Theme.ACCENT_GOLD, stroke_width=4, buff=0)
        self.play(Create(highlight))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 47 — MODULE 44: HISTORY OF GENERATIVE MODELING  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module44_EndToEndGen(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # =====================================================================
        # HÀM HỖ TRỢ (HELPERS) ĐỂ TẠO CÁC KHỐI VÀ CHUỖI ĐẢM BẢO KHÔNG TRÀN VIỀN
        # =====================================================================
        
        def make_grid(mode="partial"):
            """Tạo khối lưới minh họa cho Autoregressive"""
            # Partial: Chỉ có 1 ô có màu. Full: Toàn bộ ô có màu.
            grid = VGroup(*[
                Square(
                    side_length=0.22, 
                    fill_color=Theme.ACCENT_GOLD if (mode=="full" or i==4) else Theme.BOX_FILL,
                    fill_opacity=0.8, 
                    stroke_color=Theme.NEUTRAL, 
                    stroke_width=1
                )
                for i in range(9)
            ]).arrange_in_grid(3, 3, buff=0.03)
            
            bg = RoundedRectangle(
                width=1.2, height=1.0, corner_radius=0.15, 
                fill_color=Theme.BOX_FILL_ALT, fill_opacity=1, stroke_color=Theme.DIM
            )
            return VGroup(bg, grid.move_to(bg.get_center()))

        def make_box(label_str, w=1.5, h=0.85):
            """Khởi tạo các nút (Node) dựa theo text đầu vào"""
            if label_str == "Image":
                return RoundedBox(["Image"], width=w, height=h, fill_color=Theme.ACCENT_RED, stroke_color=Theme.ACCENT_RED, font_size=20)
            elif label_str == "Noise":
                return RoundedBox(["Noise"], width=w, height=h, fill_color=Theme.DIM, stroke_color=Theme.NEUTRAL, font_size=20)
            elif label_str == "class":
                return Text("class", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
            elif label_str == "...":
                return Text("...", font=Theme.FONT_BODY, font_size=32, color=Theme.NEUTRAL)
            elif label_str == "Partial":
                return make_grid(mode="partial")
            elif label_str == "Full":
                return make_grid(mode="full")
            else:
                return RoundedBox([label_str], width=w, height=h, fill_color=Theme.BOX_FILL, stroke_color=Theme.DIM, font_size=20)

        def build_chain(labels, direction="RIGHT"):
            """
            Hàm xây dựng một chuỗi các khối.
            - Gom các khối và giới hạn chiều rộng an toàn (Tránh Lỗi 2).
            - Trả về (Toàn bộ chuỗi, Nút mũi tên gốc).
            """
            nodes = VGroup(*[make_box(lbl) for lbl in labels]).arrange(RIGHT, buff=0.5)
            
            # Ép chiều rộng nếu chuỗi quá dài
            if nodes.width > 12.0:
                nodes.set_width(12.0)

            arrows = VGroup()
            for i in range(len(nodes) - 1):
                # Hướng mũi tên (RIGHT cho luồng thuận, LEFT cho luồng ngược generation)
                if direction == "RIGHT":
                    start_mob = nodes[i].get_right()
                    end_mob = nodes[i+1].get_left()
                else: 
                    start_mob = nodes[i+1].get_left()
                    end_mob = nodes[i].get_right()

                arr = Arrow(
                    start_mob, end_mob, 
                    buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15
                )
                arrows.add(arr)

            chain_group = VGroup(nodes, arrows)
            return chain_group, nodes

        # =====================================================================
        # SCENE 1: A BIT OF HISTORY (RECOGNITION MODEL)
        # =====================================================================
        
        title1 = slide_title("A Bit of History ...")
        sub1 = Text(
            "Since AlexNet, recognition models have been generally end-to-end ...",
            font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL
        ).next_to(title1, DOWN, aligned_edge=LEFT, buff=0.25)

        recog_labels = ["Image", "layer 1", "layer 2", "layer 3", "...", "layer N", "class"]
        chain1_grp, nodes1 = build_chain(recog_labels, direction="RIGHT")

        # Thiết lập 2 mũi tên trục chính phía trên/dưới
        left_x = nodes1.get_left()[0]
        right_x = nodes1.get_right()[0]
        top_y = nodes1.get_top()[1] + 0.6
        bot_y = nodes1.get_bottom()[1] - 0.6

        arr_inf1 = Arrow([left_x, top_y, 0], [right_x, top_y, 0], buff=0, color=Theme.DIM, stroke_width=8)
        lbl_inf1 = Text("inference-time computation", font_size=20, color=Theme.NEUTRAL).next_to(arr_inf1, UP, buff=0.1)

        arr_bp1 = Arrow([right_x, bot_y, 0], [left_x, bot_y, 0], buff=0, color=Theme.DIM, stroke_width=8)
        lbl_bp1 = Text("backpropagation", font_size=20, color=Theme.NEUTRAL).next_to(arr_bp1, DOWN, buff=0.1)

        part1_content = VGroup(chain1_grp, arr_inf1, lbl_inf1, arr_bp1, lbl_bp1).center().shift(DOWN * 0.2)

        self.play(Write(title1), FadeIn(sub1))
        self.play(FadeIn(chain1_grp))
        self.play(Create(arr_inf1), FadeIn(lbl_inf1))
        self.play(Create(arr_bp1), FadeIn(lbl_bp1))
        self.next_slide()

        # =====================================================================
        # SCENE 2: HISTORY REPEATING (DIFFUSION & AUTOREGRESSIVE)
        # =====================================================================
        
        title2 = slide_title("History Repeating in Generative Models?")
        sub2 = Text(
            "Today's generative models are conceptually like \"layer-wise training\"",
            font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL
        ).next_to(title2, DOWN, aligned_edge=LEFT, buff=0.25)

        # Mạng Diffusion
        diff_labels = ["Noise", "step 1", "step 2", "step 3", "...", "step T", "Image"]
        chain_diff_grp, _ = build_chain(diff_labels, direction="RIGHT")
        lbl_diff = Text("Diffusion", font_size=20, color=Theme.PRIMARY, weight="BOLD").next_to(chain_diff_grp, DOWN, buff=0.2)
        diff_full = VGroup(chain_diff_grp, lbl_diff)

        # Mạng Autoregressive
        ar_labels = ["Partial", "step 1", "step 2", "step 3", "...", "step T", "Full"]
        chain_ar_grp, _ = build_chain(ar_labels, direction="RIGHT")
        lbl_ar = Text("Autoregressive", font_size=20, color=Theme.ACCENT_GOLD, weight="BOLD").next_to(chain_ar_grp, DOWN, buff=0.2)
        ar_full = VGroup(chain_ar_grp, lbl_ar)

        chains_part2 = VGroup(diff_full, ar_full).arrange(DOWN, buff=0.8)

        # Tái sử dụng mũi tên Inference phía trên
        left_x2 = chains_part2.get_left()[0]
        right_x2 = chains_part2.get_right()[0]
        top_y2 = chains_part2.get_top()[1] + 0.6
        
        arr_inf2 = Arrow([left_x2, top_y2, 0], [right_x2, top_y2, 0], buff=0, color=Theme.DIM, stroke_width=8)
        lbl_inf2 = Text("inference-time computation", font_size=20, color=Theme.NEUTRAL).next_to(arr_inf2, UP, buff=0.1)

        part2_content = VGroup(arr_inf2, lbl_inf2, chains_part2).center().shift(DOWN * 0.2)

        self.play(
            Transform(title1, title2),
            Transform(sub1, sub2),
            FadeOut(part1_content)
        )
        self.play(FadeIn(part2_content))
        self.next_slide()

        # =====================================================================
        # SCENE 3: TWO SIDES OF THE SAME COIN (RECOGNITION vs GENERATION)
        # =====================================================================
        
        title3 = slide_title("Recognition vs. Generation")

        # --- Nửa trên: Recognition (Trừu tượng hóa) ---
        chain_rec_grp, nodes_rec = build_chain(recog_labels, direction="RIGHT")
        
        arr_rec = Arrow([nodes_rec.get_left()[0], 0, 0], [nodes_rec.get_right()[0], 0, 0], buff=0, color=Theme.DIM, stroke_width=8)
        lbl_rec = Text("Recognition: Abstraction", font_size=20, color=Theme.NEUTRAL, weight="BOLD")
        arr_rec.next_to(chain_rec_grp, UP, buff=0.3)
        lbl_rec.next_to(arr_rec, UP, buff=0.1)
        
        top_block = VGroup(lbl_rec, arr_rec, chain_rec_grp)

        # --- Nửa dưới: Generation (Cụ thể hóa) ---
        # Chú ý luồng Generation đi từ Noise -> Image (Nghĩa là từ PHẢI sang TRÁI)
        gen_labels = ["Image", "step T", "step T-1", "step T-2", "...", "step 1", "Noise"]
        chain_gen_grp, nodes_gen = build_chain(gen_labels, direction="LEFT")
        
        arr_gen = Arrow([nodes_gen.get_right()[0], 0, 0], [nodes_gen.get_left()[0], 0, 0], buff=0, color=Theme.DIM, stroke_width=8)
        lbl_gen = Text("Generation: Concretization", font_size=20, color=Theme.NEUTRAL, weight="BOLD")
        arr_gen.next_to(chain_gen_grp, DOWN, buff=0.3)
        lbl_gen.next_to(arr_gen, DOWN, buff=0.1)
        
        bot_block = VGroup(chain_gen_grp, arr_gen, lbl_gen)

        # Đóng gói và căn chỉnh trục dọc (arrange(DOWN))
        part3_content = VGroup(top_block, bot_block).arrange(DOWN, buff=1.0).center().shift(DOWN * 0.1)

        self.play(
            Transform(title1, title3),
            FadeOut(sub1),
            FadeOut(part2_content)
        )
        self.play(FadeIn(part3_content))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 48 — MODULE 45: NEURAL NETWORK OPERATIONS AS MAPPINGS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

import random
from manim import Line, Arrow, Polygon, Arc, ArcBetweenPoints

class Module45_Operations(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề (Ghim góc trái trên)
        title = slide_title("Layer Operations as Space Transformations")
        self.play(Write(title))

        # =====================================================================
        # HÀM HỖ TRỢ 1: TẠO NHÃN NGHIÊNG (TILTED LABEL)
        # =====================================================================
        def make_tilted_label(text_str):
            rect = RoundedRectangle(
                corner_radius=0.2, width=1.8, height=0.7,
                stroke_color=Theme.NEUTRAL, stroke_width=2,
                fill_color=Theme.BOX_FILL, fill_opacity=1
            )
            lbl = Text(text_str, font="monospace", font_size=20, color=Theme.NEUTRAL)
            group = VGroup(rect, lbl)
            group.rotate(PI / 6) # Nghiêng 30 độ giống ảnh gốc
            return group

        # =====================================================================
        # HÀM HỖ TRỢ 2: TẠO CÔNG THỨC TOÁN HỌC CÓ MÀU
        # =====================================================================
        def make_formula(tex_str):
            # Sử dụng các lệnh LaTeX nguyên bản làm key để tránh việc tự động 
            # tách ký tự đơn lẻ (như "b") làm hỏng các lệnh hệ thống (như \mathbf)
            color_map = {
                r"\mathbf{x}_{out}": Theme.ACCENT_RED,
                r"\mathbf{x}_{in}": Theme.ACCENT_RED,
                r"x_{out}": Theme.ACCENT_RED,
                r"x_{in}": Theme.ACCENT_RED,
                r"\mathbf{W}": Theme.PRIMARY,
                r"\mathbf{b}": Theme.PRIMARY,
            }
            return MathTex(
                tex_str,
                font_size=36,
                tex_to_color_map=color_map
            )

        # =====================================================================
        # HÀM HỖ TRỢ 3: TẠO ĐỒ HỌA MÔ PHỎNG ÁNH XẠ KHÔNG GIAN (ISOMETRIC MAPPING)
        # =====================================================================
        def make_mapping_diagram(op_type):
            # Tọa độ mặt phẳng đáy (Xin) dạng Isometric 2.5D
            b_dl = np.array([-0.9, -0.3, 0])
            b_dr = np.array([ 0.7, -0.3, 0])
            b_ur = np.array([ 1.1,  0.3, 0])
            b_ul = np.array([-0.5,  0.3, 0])
            
            bottom_plane = Polygon(b_dl, b_dr, b_ur, b_ul, color=Theme.DIM, stroke_width=1.5, fill_color=Theme.BG, fill_opacity=0.8)
            
            # Trục mũi tên dọc (Thu ngắn lại một chút để tạo khoảng hở rõ rệt giữa các hàng)
            axis_arr = Arrow(np.array([1.5, -0.2, 0]), np.array([1.5, 1.1, 0]), buff=0, color=Theme.NEUTRAL, stroke_width=2, tip_length=0.12)
            
            # Đẩy nhãn sang bên TRÁI mũi tên để tuyệt đối không bị đè lên đầu/đuôi mũi tên
            xin_lbl = MathTex("X_{in}", font_size=18, color=Theme.ACCENT_RED).next_to(axis_arr.get_start(), LEFT, buff=0.08)
            xout_lbl = MathTex("X_{out}", font_size=18, color=Theme.ACCENT_RED).next_to(axis_arr.get_end(), LEFT, buff=0.08)

            diagram = VGroup(bottom_plane, axis_arr, xin_lbl, xout_lbl)
            
            # MẶT PHẲNG ĐỈNH (Xout): Vẽ cho CẢ 4 trường hợp để tạo sự đồng bộ trực quan
            if op_type == "linear":
                # Linear có mặt phẳng trên nghiêng theo phép xoay affine
                top_plane = Polygon(
                    *[p + np.array([0.3, 1.2 + p[0]*0.2, 0]) for p in [b_dl, b_dr, b_ur, b_ul]], 
                    color=Theme.DIM, stroke_width=1.0, fill_color=Theme.BG, fill_opacity=0.3
                )
            else:
                # ReLU, L2, Softmax có mặt phẳng trên phẳng song song ở độ cao 1.2
                top_plane = Polygon(
                    b_dl + UP*1.2, b_dr + UP*1.2, b_ur + UP*1.2, b_ul + UP*1.2,
                    color=Theme.DIM, stroke_width=1.0, fill_color=Theme.BG, fill_opacity=0.3
                )
            diagram.add(top_plane) # Luôn nằm ở index 4 của diagram

            # Khởi tạo các điểm ngẫu nhiên trên mặt đáy
            v1, v2 = b_dr - b_dl, b_ul - b_dl
            num_points = 35
            
            random.seed(42)
            pts_in = []
            for _ in range(num_points):
                u, v = random.random(), random.random()
                pts_in.append(b_dl + u * v1 + v * v2)

            top_shapes = VGroup()
            beams = VGroup()

            for pt in pts_in:
                x, y, _ = pt
                
                if op_type == "linear":
                    out_pt = np.array([x + 0.3, y + 1.2 + x*0.2, 0])
                elif op_type == "relu":
                    out_pt = np.array([x, 1.0 + max(0, x*0.6 + y*0.2), 0])
                elif op_type == "L2-norm":
                    center = (b_dl + b_ur) / 2
                    vec = pt - center
                    dist = np.linalg.norm(vec) + 0.001
                    out_pt = center + (vec / dist) * 0.5 + UP * 1.2
                elif op_type == "softmax":
                    out_pt = np.array([x*0.5 + 0.2, 1.2, 0])

                beam = Line(pt, out_pt, stroke_width=1.0, stroke_opacity=0.4, color=Theme.ACCENT_RED)
                beams.add(beam)
                
                dot = Dot(out_pt, radius=0.03, color=Theme.ACCENT_RED)
                top_shapes.add(dot)

            # Vẽ thêm các hình dạng đặc trưng trên mặt đỉnh (đường tròn L2, đường thẳng Softmax)
            if op_type == "L2-norm":
                t_circ = Arc(radius=0.6, angle=TAU, color=Theme.ACCENT_RED).scale([1, 0.4, 1]).move_to((b_dl+b_ur)/2 + UP*1.2)
                diagram.add(t_circ) # index 5
            elif op_type == "softmax":
                t_line = Line(np.array([-0.3, 1.2, 0]), np.array([0.7, 1.2, 0]), color=Theme.ACCENT_RED, stroke_width=3)
                diagram.add(t_line) # index 5

            diagram.add(beams, top_shapes)
            return diagram

        # =====================================================================
        # ĐỊNH VỊ TOÀN CỤC (ĐÃ GIÃN CÁCH CÁC HÀNG RỘNG HƠN)
        # =====================================================================
        rows_data = [
            ("linear",  r"\mathbf{x}_{out} = \mathbf{W}\mathbf{x}_{in} + \mathbf{b}"),
            ("relu",    r"x_{out}[i] = \max(x_{in}[i], 0)"),
            ("L2-norm", r"x_{out}[i] = \frac{x_{in}[i]}{\|\mathbf{x}_{in}\|_2}"),
            ("softmax", r"x_{out}[i] = \frac{e^{-\tau x_{in}[i]}}{\sum_{k=1}^K e^{-\tau x_{in}[k]}}")
        ]

        all_rows_group = VGroup()
        
        X_COL_1 = -4.5  
        X_COL_2 = -0.5  
        X_COL_3 =  4.2  
        
        Y_START = 2.0
        Y_STEP = 1.85 # Tăng từ 1.6 lên 1.85 để các hàng tách xa nhau ra hơn

        for i, (lbl_str, fml_str) in enumerate(rows_data):
            y_pos = Y_START - i * Y_STEP
            
            lbl = make_tilted_label(lbl_str).move_to([X_COL_1, y_pos, 0])
            fml = make_formula(fml_str).move_to([X_COL_2, y_pos, 0])
            diag = make_mapping_diagram(lbl_str).move_to([X_COL_3, y_pos - 0.2, 0])
            
            row_group = VGroup(lbl, fml, diag)
            all_rows_group.add(row_group)

        # Scale và dịch chuyển an toàn tuyệt đối
        all_rows_group.scale_to_fit_height(5.7) 
        all_rows_group.center().shift(DOWN * 0.4) 

        # =====================================================================
        # ANIMATION EFFECTS (ĐỒNG BỘ TRÌNH TỰ VẼ MẶT PHẲNG ĐỈNH)
        # =====================================================================
        
        for i, row in enumerate(all_rows_group):
            lbl, fml, diag = row[0], row[1], row[2]
            
            self.play(FadeIn(lbl, shift=RIGHT*0.5), Write(fml), run_time=0.8)
            
            # Cấu trúc đồng bộ của diag:
            bottom_plane = diag[0]
            axis = VGroup(*diag[1:4])
            top_plane = diag[4]
            beams = diag[-2]
            top_shapes = diag[-1]
            
            # 1. Hiện đồng thời cả hai mặt phẳng (Đáy & Đỉnh) và trục tọa độ
            self.play(FadeIn(bottom_plane), FadeIn(top_plane), FadeIn(axis), run_time=0.6)
            
            # 2. Hiệu ứng mô phỏng: Bắn các tia laser quét lên trên
            self.play(Create(beams, lag_ratio=0.05), run_time=1.2)
            
            # 3. Hiện các hình dạng biến đổi đặc trưng (và đường tròn/đường thẳng nếu có)
            if len(diag) > 7:
                extra_shape = diag[5] # t_circ hoặc t_line
                self.play(Create(extra_shape), FadeIn(top_shapes, scale=1.2), run_time=0.6)
            else:
                self.play(FadeIn(top_shapes, scale=1.2), run_time=0.6)
            
            self.next_slide()
            
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 49 — MODULE 46: NEURAL NETWORK AS A CONTINUOUS FLOW  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
import random
from manim import Line, Arrow, Polygon, Dot, DashedLine, ArcBetweenPoints

class Module46_Flow(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề Slide (Ghim cứng góc trái trên)
        title = slide_title("Recognition & Generation as 'Flows'")
        self.play(Write(title))

        # =====================================================================
        # THIẾT LẬP TỌA ĐỘ VÀ KIẾN TRÚC MẠNG TẦNG (FIXED BOUNDS ĐỂ TRÁNH LỖI 3)
        # =====================================================================
        NUM_LAYERS = 7
        Y_START = -2.6
        Y_STEP = 0.85
        X_CENTER = -2.0 # Đặt mạng nơ-ron hơi lệch trái để chừa không gian cho Text bên phải

        labels_text = ["Data", "linear", "relu", "linear", "relu", "linear", "softmax"]
        
        # Tọa độ mặt phẳng Isometric cơ sở (chưa dịch chuyển Y)
        # Dùng vector thuần túy để tính toán tịnh tiến cho chính xác
        p_dl = np.array([-1.2, -0.4, 0])
        p_dr = np.array([ 0.8, -0.4, 0])
        p_ur = np.array([ 1.2,  0.4, 0])
        p_ul = np.array([-0.8,  0.4, 0])

        planes = VGroup()
        labels = VGroup()

        for i in range(NUM_LAYERS):
            center_pos = np.array([X_CENTER, Y_START + i * Y_STEP, 0])
            
            # Khởi tạo mặt phẳng cho tầng i
            plane = Polygon(
                p_dl + center_pos, 
                p_dr + center_pos, 
                p_ur + center_pos, 
                p_ul + center_pos,
                color=Theme.DIM, stroke_width=1.5, fill_color=Theme.BG, fill_opacity=0.6
            )
            planes.add(plane)
            
            # Khởi tạo Text nhãn bên cạnh mặt phẳng (Cách một khoảng buff an toàn)
            lbl = Text(labels_text[i], font="monospace", font_size=16, color=Theme.NEUTRAL)
            lbl.next_to(plane, RIGHT, buff=0.4)
            labels.add(lbl)

        # Hiển thị bộ khung mạng lưới
        self.play(FadeIn(planes), FadeIn(labels), run_time=1.5)

        # =====================================================================
        # SINH DỮ LIỆU ĐIỂM (RED & BLUE) VÀ TÍNH TOÁN QUỸ ĐẠO CÁC TẦNG
        # =====================================================================
        random.seed(101) # Cố định seed
        NUM_POINTS = 20

        # Lưu trữ danh sách VGroup của các điểm tại mỗi tầng
        dots_red_layers = []
        dots_blue_layers = []
        
        # Lưu trữ mảng đường thẳng nối tầng i với i+1
        lines_red_layers = []
        lines_blue_layers = []

        # Tọa độ neo của Đỏ và Xanh ở mặt đáy (Trộn lẫn nhau)
        bottom_red_anchor = np.array([-0.2, 0.0, 0])
        bottom_blue_anchor = np.array([0.2, 0.0, 0])
        
        # Tọa độ neo của Đỏ và Xanh ở đỉnh (Tách biệt hoàn toàn về 2 góc)
        top_red_anchor = np.array([-0.7, 0.2, 0])
        top_blue_anchor = np.array([0.7, -0.2, 0])

        for i in range(NUM_LAYERS):
            layer_center = np.array([X_CENTER, Y_START + i * Y_STEP, 0])
            ratio = i / (NUM_LAYERS - 1) # Tỷ lệ tiến trình từ đáy (0) lên đỉnh (1)
            
            dots_red = VGroup()
            dots_blue = VGroup()
            
            for j in range(NUM_POINTS):
                # Khởi tạo nhiễu ngẫu nhiên cho từng điểm để tạo sự lan tỏa
                noise_r = np.array([random.uniform(-0.3, 0.3), random.uniform(-0.15, 0.15), 0])
                noise_b = np.array([random.uniform(-0.3, 0.3), random.uniform(-0.15, 0.15), 0])
                
                # Nội suy tuyến tính (Lerp) vị trí từ đáy lên đỉnh + nhiễu
                pos_r = layer_center + bottom_red_anchor * (1 - ratio) + top_red_anchor * ratio + noise_r
                pos_b = layer_center + bottom_blue_anchor * (1 - ratio) + top_blue_anchor * ratio + noise_b
                
                dots_red.add(Dot(pos_r, radius=0.035, color=Theme.ACCENT_RED))
                dots_blue.add(Dot(pos_b, radius=0.035, color=Theme.PRIMARY)) # Dùng PRIMARY (Xanh sky) thay vì xanh dương tối
                
            dots_red_layers.append(dots_red)
            dots_blue_layers.append(dots_blue)

        # Tính toán các đường Line nối giữa tầng i và i+1
        for i in range(NUM_LAYERS - 1):
            l_red = VGroup(*[
                Line(dots_red_layers[i][j].get_center(), dots_red_layers[i+1][j].get_center(), stroke_width=1.0, stroke_opacity=0.3, color=Theme.ACCENT_RED)
                for j in range(NUM_POINTS)
            ])
            l_blue = VGroup(*[
                Line(dots_blue_layers[i][j].get_center(), dots_blue_layers[i+1][j].get_center(), stroke_width=1.0, stroke_opacity=0.3, color=Theme.PRIMARY)
                for j in range(NUM_POINTS)
            ])
            lines_red_layers.append(l_red)
            lines_blue_layers.append(l_blue)

        # =====================================================================
        # THIẾT KẾ CÁC MŨI TÊN CHỈ HƯỚNG VÀ VĂN BẢN (RECOGNITION / GENERATION)
        # =====================================================================
        
        # --- UI Luồng Recognition (Hướng lên) ---
        rec_arrow = Arrow(
            start=np.array([1.5, Y_START, 0]), 
            end=np.array([1.5, Y_START + (NUM_LAYERS-1)*Y_STEP, 0]), 
            color=Theme.DIM, stroke_width=12, tip_length=0.4
        )
        rec_text_1 = Text("Recognition:", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL, weight="BOLD")
        rec_text_2 = Text('"Flow" from data to embeddings', font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL)
        rec_ui_group = VGroup(rec_text_1, rec_text_2).arrange(DOWN, aligned_edge=LEFT).next_to(rec_arrow, RIGHT, buff=0.5)

        # Mũi tên cong hai bên (Trái và Phải)
        left_arc_up = ArcBetweenPoints(np.array([-4.5, Y_START, 0]), np.array([-4.5, Y_START + 5.1, 0]), angle=TAU/8, color=Theme.DIM, stroke_width=3).add_tip(tip_length=0.2)
        right_arc_up = ArcBetweenPoints(np.array([0.5, Y_START, 0]), np.array([0.5, Y_START + 5.1, 0]), angle=-TAU/8, color=Theme.DIM, stroke_width=3).add_tip(tip_length=0.2)

        # --- UI Luồng Generation (Hướng xuống) ---
        gen_arrow = Arrow(
            start=np.array([1.5, Y_START + (NUM_LAYERS-1)*Y_STEP, 0]), 
            end=np.array([1.5, Y_START, 0]), 
            color=Theme.ACCENT_GOLD, stroke_width=12, tip_length=0.4
        )
        gen_text_1 = Text("Generation:", font=Theme.FONT_BODY, font_size=28, color=Theme.ACCENT_GOLD, weight="BOLD")
        gen_text_2 = Text('"Flow" from embeddings to data', font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL)
        gen_ui_group = VGroup(gen_text_1, gen_text_2).arrange(DOWN, aligned_edge=LEFT).next_to(gen_arrow, RIGHT, buff=0.5)

        left_arc_down = ArcBetweenPoints(np.array([-4.5, Y_START + 5.1, 0]), np.array([-4.5, Y_START, 0]), angle=-TAU/8, color=Theme.ACCENT_GOLD, stroke_width=3).add_tip(tip_length=0.2)
        right_arc_down = ArcBetweenPoints(np.array([0.5, Y_START + 5.1, 0]), np.array([0.5, Y_START, 0]), angle=TAU/8, color=Theme.ACCENT_GOLD, stroke_width=3).add_tip(tip_length=0.2)


        # =====================================================================
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # =====================================================================
        
        # BƯỚC 1: Hiển thị giao diện luồng Recognition và Data đáy
        self.play(
            FadeIn(rec_arrow), FadeIn(rec_ui_group),
            Create(left_arc_up), Create(right_arc_up)
        )
        self.play(
            FadeIn(dots_red_layers[0]), 
            FadeIn(dots_blue_layers[0])
        )
        self.next_slide()

        # BƯỚC 2: Mô phỏng quá trình truyền thẳng (Forward Flow - Recognition)
        # Dùng TransformFromCopy để giữ lại các điểm ở tầng cũ, kết hợp Create để vẽ tia Laser nối
        for i in range(NUM_LAYERS - 1):
            self.play(
                TransformFromCopy(dots_red_layers[i], dots_red_layers[i+1]),
                TransformFromCopy(dots_blue_layers[i], dots_blue_layers[i+1]),
                Create(lines_red_layers[i]),
                Create(lines_blue_layers[i]),
                run_time=0.6,
                rate_func=rate_functions.linear
            )
        self.next_slide()

        # BƯỚC 3: Đảo ngược mô hình sang Generation
        self.play(
            ReplacementTransform(rec_arrow, gen_arrow),
            ReplacementTransform(rec_ui_group, gen_ui_group),
            ReplacementTransform(left_arc_up, left_arc_down),
            ReplacementTransform(right_arc_up, right_arc_down),
            run_time=1.0
        )
        self.next_slide()

        # Dòng kết luận để người xem đọng lại kiến thức
        summary = Text("Generative models invert this path: converting structured semantic embeddings back into complex data manifolds.", 
                       font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(summary))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 50 — MODULE 47: NEURAL ODE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module47_NeuralODE(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề chính và Trích dẫn nguồn
        title_group = VGroup()
        title = slide_title("Neural ODE")
        cite = Text("[Chen et al, NeurIPS 2018]", font=Theme.FONT_BODY, font_size=20, color=Theme.DIM)
        cite.next_to(title, RIGHT, buff=0.5).align_to(title, DOWN)
        title_group.add(title, cite)
        
        self.play(Write(title), FadeIn(cite))

        # =====================================================================
        # HÀM HỖ TRỢ: VẼ ĐỒ THỊ TRƯỜNG VECTOR VÀ QUỸ ĐẠO
        # =====================================================================
        def make_plot(is_continuous=False):
            # Cấu hình kích thước cực kỳ an toàn để không tràn viền ngang/dọc
            axes = Axes(
                x_range=[-6, 6, 2],
                y_range=[0, 5, 1],
                x_length=3.0,
                y_length=3.2,
                axis_config={"color": Theme.NEUTRAL, "include_numbers": False, "tick_size": 0.05},
            )
            
            # Khung viền bọc quanh vùng vẽ (Giúp cố định giới hạn không gian)
            bbox = Rectangle(width=3.0, height=3.2, color=Theme.DIM, stroke_width=2, fill_color=Theme.BG, fill_opacity=0)
            bbox.move_to(axes.c2p(0, 2.5)) 
            
            # Nhãn cho các trục
            x_nums = VGroup(
                Text("-5", font_size=14, color=Theme.NEUTRAL).next_to(axes.c2p(-5, 0), DOWN, buff=0.1),
                Text("0", font_size=14, color=Theme.NEUTRAL).next_to(axes.c2p(0, 0), DOWN, buff=0.1),
                Text("5", font_size=14, color=Theme.NEUTRAL).next_to(axes.c2p(5, 0), DOWN, buff=0.1),
            )
            y_nums = VGroup(*[
                Text(str(i), font_size=14, color=Theme.NEUTRAL).next_to(axes.c2p(-6, i), LEFT, buff=0.1)
                for i in range(6)
            ])
            x_label = Text("Input/Hidden/Output", font_size=14, color=Theme.DIM).next_to(x_nums, DOWN, buff=0.2)
            y_label = Text("Depth", font_size=14, color=Theme.DIM).rotate(PI/2).next_to(y_nums, LEFT, buff=0.2)

            # Mô phỏng trường vector chìm phía sau
            vector_field = VGroup()
            for x in np.linspace(-5.5, 5.5, 9):
                for y in np.linspace(0.2, 4.8, 7):
                    # Toán học tạo vector hội tụ nhẹ về trung tâm để giống hình mẫu
                    dx = -0.4 * x
                    dy = 1
                    norm = np.hypot(dx, dy)
                    dx, dy = dx/norm * 0.4, dy/norm * 0.4
                    
                    arrow_color = Theme.ACCENT_GOLD if x > 0 else ManimColor("#9FA8DA") 
                    start_p = axes.c2p(x, y)
                    end_p = axes.c2p(x + dx, y + dy)
                    
                    arrow = Arrow(
                        start_p, end_p, buff=0, 
                        max_tip_length_to_length_ratio=0.25, stroke_width=1.5, 
                        color=arrow_color, stroke_opacity=0.4
                    )
                    vector_field.add(arrow)

            # Mô phỏng quỹ đạo dòng chảy của dữ liệu
            trajectories = VGroup()
            start_xs = [-5, -3, -1, 1, 3, 5]
            
            for sx in start_xs:
                if is_continuous:
                    # Mạng ODE: Đường cong mịn (Continuous Time)
                    curve = axes.plot_parametric_curve(
                        lambda t: np.array([sx * np.exp(-0.4 * t), t, 0]), 
                        t_range=[0, 5], color=Theme.NEUTRAL, stroke_width=2
                    )
                    trajectories.add(curve)
                    t_vals = np.linspace(0, 5, 12)
                    dots = VGroup(*[Dot(axes.c2p(sx * np.exp(-0.4 * t), t), radius=0.03, color=Theme.NEUTRAL) for t in t_vals])
                    trajectories.add(dots)
                else:
                    # Mạng ResNet: Gấp khúc rời rạc (Discrete Time)
                    t_vals = list(range(6))
                    points = [axes.c2p(sx * np.exp(-0.4 * t), t) for t in t_vals]
                    lines = VGroup(*[Line(points[i], points[i+1], color=Theme.NEUTRAL, stroke_width=2) for i in range(5)])
                    dots = VGroup(*[Dot(p, radius=0.04, color=Theme.NEUTRAL) for p in points])
                    trajectories.add(lines, dots)

            plot_group = VGroup(bbox, axes, x_nums, y_nums, x_label, y_label, vector_field, trajectories)
            return plot_group

        # =====================================================================
        # THIẾT LẬP CỘT TRÁI (RESIDUAL NETWORK)
        # =====================================================================
        title_res = Text("Residual Network", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        # Sử dụng mảng chuỗi để dễ dàng set_color độc lập, tuyệt đối không bị lỗi LaTeX parser
        formula_res = MathTex(
            r"\mathbf{h}_{t+1}", r" = ", r"\mathbf{h}_t", r" + f(\mathbf{h}_t, ", r"\theta_t", r")",
            font_size=32
        )
        formula_res[0].set_color(Theme.ACCENT_RED)
        formula_res[2].set_color(Theme.ACCENT_RED)
        formula_res[4].set_color(Theme.ACCENT_GOLD)

        plot_res = make_plot(is_continuous=False)
        res_group = VGroup(formula_res, title_res, plot_res).arrange(DOWN, buff=0.4)

        orange_txt_1 = VGroup(
            Text("• time-dependent", font_size=18, color=Theme.ACCENT_GOLD),
            Text("  parameterization", font_size=18, color=Theme.ACCENT_GOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        col1_side = VGroup(
            Text("• discrete time", font_size=18, color=Theme.ACCENT_RED),
            orange_txt_1
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)


        # =====================================================================
        # THIẾT LẬP CỘT PHẢI (ODE NETWORK)
        # =====================================================================
        title_ode = Text("ODE Network", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        formula_ode = MathTex(
            r"\frac{d\mathbf{h}(t)}{dt}", r" = ", r"f", r"(\mathbf{h}(t), t, ", r"\theta", r")",
            font_size=32
        )
        formula_ode[0].set_color(Theme.ACCENT_RED)
        formula_ode[2].set_color(ManimColor("#AB47BC")) # Purple
        formula_ode[4].set_color(Theme.ACCENT_GOLD)

        plot_ode = make_plot(is_continuous=True)
        ode_group = VGroup(formula_ode, title_ode, plot_ode).arrange(DOWN, buff=0.4)

        orange_txt_2 = VGroup(
            Text("• time-shared", font_size=18, color=Theme.ACCENT_GOLD),
            Text("  parameterization", font_size=18, color=Theme.ACCENT_GOLD)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        col2_side = VGroup(
            Text("• continuous time", font_size=18, color=Theme.ACCENT_RED),
            orange_txt_2,
            Text("• f is often a ResNet", font_size=18, color=ManimColor("#AB47BC"))
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)


        # =====================================================================
        # SẮP XẾP VÀ CĂN CHỈNH TỔNG THỂ (TRỤC MỎ NEO)
        # =====================================================================
        
        # 1. Neo hai cột chính để tạo thành móng
        main_cols = VGroup(res_group, ode_group).arrange(RIGHT, buff=1.0)
        
        # 2. Neo Text bên cạnh hông của plot để nó không nhảy lung tung
        col1_side.next_to(res_group, LEFT, buff=0.5).align_to(plot_res, UP).shift(DOWN*0.3)
        col2_side.next_to(ode_group, RIGHT, buff=0.5).align_to(plot_ode, UP).shift(DOWN*0.3)
        
        # 3. Đưa tất cả vào tâm khung hình (Cân đối hoàn hảo)
        all_content = VGroup(col1_side, main_cols, col2_side)
        all_content.center().shift(DOWN * 0.1)


        # =====================================================================
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # =====================================================================
        
        # BƯỚC 1: Hiển thị mảng kiến thức bên trái (Residual Network)
        self.play(FadeIn(res_group[0]), FadeIn(res_group[1])) # Hiện công thức và Title
        self.play(FadeIn(res_group[2]), run_time=1.0)         # Hiện Plot rời rạc
        self.play(FadeIn(col1_side, shift=RIGHT*0.3), run_time=0.8)
        self.next_slide()

        # BƯỚC 2: Hiển thị mảng kiến thức bên phải (ODE Network)
        self.play(FadeIn(ode_group[0]), FadeIn(ode_group[1])) 
        self.play(FadeIn(ode_group[2]), run_time=1.0)         # Hiện Plot liên tục (Curves)
        self.play(FadeIn(col2_side, shift=LEFT*0.3), run_time=0.8)
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 51 — MODULE 48: RECOGNITION VS GENERATION MAPPING  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import ArcBetweenPoints, DashedVMobject

class Module48_FlowMatching(Slide):
    def construct(self):
        # 1. Màu nền Slide thống nhất
        self.camera.background_color = Theme.BG

        # 2. Tiêu đề slide (Ghim góc trái trên)
        title = slide_title("Recognition vs. Generation Mapping")
        self.play(Write(title))

        # =====================================================================
        # HÀM CHIẾU TRỤC ĐO (ISOMETRIC MAPPING) CHO LĂNG KÍNH KHÔNG GIAN 3D
        # =====================================================================
        def to_iso(x, y, z):
            # x là chiều rộng [-1, 1], y là chiều sâu [-1, 1], z là chiều cao [-1, 1]
            X_2d = 1.1 * (x - y)
            Y_2d = 0.55 * (x + y) + 1.2 * z
            return np.array([X_2d, Y_2d, 0])

        # ─────────────────────────────────────────────────────────────────────
        # PHẦN TRUNG TÂM: LĂNG KÍNH KHÔNG GIAN 3D (PRISM & LAYERS)
        # ─────────────────────────────────────────────────────────────────────
        
        # Khung dây 3D (Wireframe Box)
        wireframe = VGroup()
        # 4 Cạnh đáy (z = -1)
        wireframe.add(Line(to_iso(-1,-1,-1), to_iso( 1,-1,-1), color=Theme.DIM, stroke_width=1.5))
        wireframe.add(Line(to_iso( 1,-1,-1), to_iso( 1, 1,-1), color=Theme.DIM, stroke_width=1.5))
        wireframe.add(Line(to_iso( 1, 1,-1), to_iso(-1, 1,-1), color=Theme.DIM, stroke_width=1.5))
        wireframe.add(Line(to_iso(-1, 1,-1), to_iso(-1,-1,-1), color=Theme.DIM, stroke_width=1.5))
        # 4 Cạnh đỉnh (z = 1)
        wireframe.add(Line(to_iso(-1,-1, 1), to_iso( 1,-1, 1), color=Theme.DIM, stroke_width=1.5))
        wireframe.add(Line(to_iso( 1,-1, 1), to_iso( 1, 1, 1), color=Theme.DIM, stroke_width=1.5))
        wireframe.add(Line(to_iso( 1, 1, 1), to_iso(-1, 1, 1), color=Theme.DIM, stroke_width=1.5))
        wireframe.add(Line(to_iso(-1, 1, 1), to_iso(-1,-1, 1), color=Theme.DIM, stroke_width=1.5))
        # 4 Cạnh đứng nối dọc
        wireframe.add(Line(to_iso(-1,-1,-1), to_iso(-1,-1, 1), color=Theme.DIM, stroke_width=1.5))
        wireframe.add(Line(to_iso( 1,-1,-1), to_iso( 1,-1, 1), color=Theme.DIM, stroke_width=1.5))
        wireframe.add(Line(to_iso( 1, 1,-1), to_iso( 1, 1, 1), color=Theme.DIM, stroke_width=1.5))
        wireframe.add(Line(to_iso(-1, 1,-1), to_iso(-1, 1, 1), color=Theme.DIM, stroke_width=1.5))

        # 3 Mặt phẳng trung gian (Layers) cắt ngang lăng kính
        layers_group = VGroup()
        for z_val in [-0.5, 0.0, 0.5]:
            layer = Polygon(
                to_iso(-1, -1, z_val),
                to_iso( 1, -1, z_val),
                to_iso( 1,  1, z_val),
                to_iso(-1,  1, z_val),
                fill_color=Theme.BG,
                fill_opacity=0.3,
                stroke_color=Theme.NEUTRAL,
                stroke_width=1.0
            )
            layers_group.add(layer)

        # Nhãn trên đỉnh và dưới đáy lăng kính (Đẩy chữ Embedding lên cao hơn để tránh đè đầu mũi tên)
        emb_lbl = Text("Embedding", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL, weight="BOLD").next_to(to_iso(0,0,1), UP, buff=0.35)
        data_lbl = Text("Data", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL, weight="BOLD").next_to(to_iso(0,0,-1), DOWN, buff=0.15)
        prism_labels = VGroup(emb_lbl, data_lbl)

        # Quỹ đạo dòng chảy cong (Arc Between Points) đi xuyên qua các lớp
        curves = VGroup()
        starts = [to_iso(-0.4, -0.4, -1.0), to_iso(0.4, -0.4, -1.0), to_iso(-0.4, 0.4, -1.0), to_iso(0.4, 0.4, -1.0)]
        
        # Hạ điểm kết thúc xuống z = 0.82 để các mũi tên dừng hẳn bên trong lòng lăng kính, không chạm vào chữ
        ends   = [to_iso(-0.3, -0.3,  0.82), to_iso(0.3, -0.3,  0.82), to_iso(-0.3, 0.3,  0.82), to_iso(0.3, 0.3,  0.82)]
        
        angles = [0.35, -0.35, 0.45, -0.45]

        for s, e, ang in zip(starts, ends, angles):
            # Tạo cung tròn gốc nối 2 điểm
            base_arc = ArcBetweenPoints(s, e, angle=ang, color=Theme.NEUTRAL, stroke_width=1.5)
            # Tạo phiên bản nét đứt thuần túy
            dashed_arc = DashedVMobject(base_arc, num_dashes=15)
            
            # Tạo riêng một cung tròn có mũi tên để trích xuất ArrowTip đặc
            arc_with_tip = ArcBetweenPoints(s, e, angle=ang, color=Theme.NEUTRAL, stroke_width=1.5)
            arc_with_tip.add_tip(tip_length=0.15)
            solid_tip = arc_with_tip.get_tip()
            solid_tip.set_color(Theme.NEUTRAL)
            
            # Nhóm nét đứt và mũi tên đặc lại thành một thực thể duy nhất
            dashed_arrow = VGroup(dashed_arc, solid_tip)
            curves.add(dashed_arrow)

        # Gom cụm lăng kính trung tâm
        center_prism = VGroup(wireframe, layers_group, prism_labels).move_to([0, 0, 0])

        # ─────────────────────────────────────────────────────────────────────
        # PHẦN BÊN TRÁI: RECOGNITION (X = -4.5)
        # ─────────────────────────────────────────────────────────────────────
        rec_title = Text("Recognition:", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD")
        rec_body_1 = Text("determined", font=Theme.FONT_BODY, font_size=20, color=Theme.PRIMARY, weight="BOLD")
        rec_body_2 = Text("data-to-label mapping", font=Theme.FONT_BODY, font_size=20, color=Theme.PRIMARY)
        rec_body = VGroup(rec_body_1, rec_body_2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        
        rec_group = VGroup(rec_title, rec_body).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-4.5, 0.0, 0])

        # Mũi tên hướng lên đại diện cho Recognition
        up_arrow = Arrow(
            start=np.array([-2.3, -1.8, 0]),
            end=np.array([-2.3, 1.8, 0]),
            color=Theme.DIM,
            stroke_width=8,
            tip_length=0.3
        )

        # ─────────────────────────────────────────────────────────────────────
        # PHẦN BÊN PHẢI: GENERATION (X = 4.5)
        # ─────────────────────────────────────────────────────────────────────
        gen_title = Text("Generation:", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD")
        gen_body_1 = Text("unknown", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED, weight="BOLD")
        gen_body_2 = Text('"noise"-to-data mapping', font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED)
        gen_body_3 = Text("(infinite possibilities)", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_RED)
        gen_body = VGroup(gen_body_1, gen_body_2, gen_body_3).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        
        gen_top_group = VGroup(gen_title, gen_body).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        # Câu hỏi và mục tiêu xây dựng thuật toán
        q_title = Text("Construct the mapping?", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_GOLD, weight="BOLD")
        bullet_1 = Text("• Continuous Normalizing Flow\n  (in Neural ODE)", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL, line_spacing=1.2)
        bullet_2 = Text("• Flow Matching", font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL, weight="BOLD")
        
        # Thêm đường gạch chân cho "Flow Matching" làm điểm nhấn
        underline = Line(bullet_2.get_left(), bullet_2.get_right(), color=Theme.NEUTRAL, stroke_width=1.5).next_to(bullet_2, DOWN, buff=0.05)
        bullet_2_with_line = VGroup(bullet_2, underline)
        
        gen_bot_group = VGroup(q_title, bullet_1, bullet_2_with_line).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        # Gom cụm cột phải
        gen_group = VGroup(gen_top_group, gen_bot_group).arrange(DOWN, aligned_edge=LEFT, buff=0.8).move_to([4.5, -0.2, 0])

        # Mũi tên hướng xuống đại diện cho Generation
        down_arrow = Arrow(
            start=np.array([2.3, 1.8, 0]),
            end=np.array([2.3, -1.8, 0]),
            color=Theme.DIM,
            stroke_width=8,
            tip_length=0.3
        )

        # ─────────────────────────────────────────────────────────────────────
        # SẮP XẾP TOÀN BỘ VÀ HẠ THẤP XUỐNG DƯỚI TIÊU ĐỀ
        # ─────────────────────────────────────────────────────────────────────
        content_group = VGroup(
            center_prism, curves, rec_group, up_arrow, gen_group, down_arrow
        )
        # Tịnh tiến toàn bộ cụm sơ đồ xuống dưới để tạo bố cục cân đối và thoáng mát
        content_group.shift(DOWN * 0.45) 

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        # Bước 1: Hiện tiêu đề chính và bộ khung Lăng kính dây 3D trống
        self.play(FadeIn(center_prism))
        self.next_slide()

        # Bước 2: Hiển thị luồng Recognition (Bên trái) cùng các quỹ đạo vector hướng lên
        self.play(FadeIn(rec_group), Create(up_arrow))
        self.play(*[Create(curve) for curve in curves], run_time=1.5)
        self.next_slide()

        # Bước 3: Hiển thị luồng Generation nghịch đảo (Bên phải)
        self.play(FadeIn(gen_top_group), Create(down_arrow))
        self.next_slide()

        # Bước 4: Đặt câu hỏi và đưa ra giải pháp (Flow Matching)
        self.play(FadeIn(gen_bot_group))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 52 — MODULE 49: FLOW MATCHING & ODE SOLVING  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

import random
import numpy as np
from manim import ValueTracker, DashedLine

class Module49_FlowMatching(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Khởi tạo mỏ neo lề trái cố định cho văn bản
        LEFT_ANCHOR = np.array([-6.0, 0.5, 0])

        # =====================================================================
        # THIẾT LẬP MÔ PHỎNG CONTINUOUS FLOW (CỘT PHẢI)
        # =====================================================================
        X_DATA = 1.0
        X_PRIOR = 5.5
        Y_CENTER = 0.0
        
        lbl_data = MathTex(r"x \sim p_{\text{data}}", font_size=24, color=Theme.DIM).move_to([X_DATA, 2.2, 0])
        lbl_prior = MathTex(r"\epsilon \sim p_{\text{prior}}", font_size=24, color=Theme.ACCENT_RED).move_to([X_PRIOR, 2.2, 0])
        
        v_arrow = Arrow([3.0, 1.8, 0], [3.7, 1.8, 0], buff=0, color=ManimColor("#AB47BC"), stroke_width=3, tip_length=0.15)
        v_lbl = MathTex(r"v(z_t, t)", font_size=24, color=ManimColor("#AB47BC")).next_to(v_arrow, UP, buff=0.1)
        
        NUM_POINTS = 60
        random.seed(42)
        
        start_points = []
        end_points = []
        data_dots = VGroup()
        prior_dots = VGroup()
        flow_dots = VGroup()
        bg_paths = VGroup()

        for _ in range(NUM_POINTS):
            y_start = random.gauss(0, 0.6) + Y_CENTER
            p_start = np.array([X_DATA + random.uniform(-0.1, 0.1), y_start, 0])
            
            y_end = random.gauss(0, 1.0) + Y_CENTER
            p_end = np.array([X_PRIOR + random.uniform(-0.1, 0.1), y_end, 0])
            
            start_points.append(p_start)
            end_points.append(p_end)
            
            data_dots.add(Dot(p_start, radius=0.02, color=Theme.DIM))
            prior_dots.add(Dot(p_end, radius=0.02, color=Theme.ACCENT_RED))
            
            # Đường cong Bezier mô phỏng trường vector
            ctrl1 = p_start + np.array([1.5, 0, 0])
            ctrl2 = p_end + np.array([-1.5, 0, 0])
            path = CubicBezier(p_start, ctrl1, ctrl2, p_end, color=ManimColor("#9FA8DA"), stroke_opacity=0.15, stroke_width=1.0)
            bg_paths.add(path)
            
            # Khởi tạo các hạt chuyển động
            flow_dot = Dot(p_start, radius=0.03, color=ManimColor("#AB47BC"))
            flow_dot.p_start = p_start
            flow_dot.p_end = p_end
            flow_dot.ctrl1 = ctrl1
            flow_dot.ctrl2 = ctrl2
            flow_dots.add(flow_dot)

        visualizer_group = VGroup(lbl_data, lbl_prior, data_dots, prior_dots, bg_paths, flow_dots, v_arrow, v_lbl)
        
        # ValueTracker tĩnh (Được cấp lực chuyển động trực tiếp bởi hoạt ảnh .animate)
        time_tracker = ValueTracker(0)

        def flow_updater(mob):
            t_val = time_tracker.get_value()
            ratio = (np.sin(t_val) + 1) / 2  # Hàm tuần hoàn hoàn hảo từ 0 -> 1 -> 0
            
            # Đảo hướng mũi tên vận tốc theo chu kỳ bay
            if np.cos(t_val) >= 0: 
                v_arrow.put_start_and_end_on([2.8, 1.8, 0], [3.7, 1.8, 0])
            else: 
                v_arrow.put_start_and_end_on([3.7, 1.8, 0], [2.8, 1.8, 0])

            # Di chuyển hạt theo thời gian
            for dot in mob:
                r_inv = 1 - ratio
                pos = (r_inv**3)*dot.p_start + 3*(r_inv**2)*ratio*dot.ctrl1 + 3*r_inv*(ratio**2)*dot.ctrl2 + (ratio**3)*dot.p_end
                dot.move_to(pos)

        flow_dots.add_updater(flow_updater)


        # =====================================================================
        # BƯỚC 2: KHỞI TẠO CÁC SLIDES VỚI CƠ CHẾ AUTO-NEXT (1-CLICK TRANSITION)
        # =====================================================================
        
        # --- Slide 0 (Intro): Hiện tiêu đề và lăng kính ---
        self.next_slide(auto_next=True) 
        title = slide_title("Flow Matching")
        self.play(Write(title))
        self.play(FadeIn(visualizer_group))

        # --- Slide 1: Vòng lặp hạt chạy trống ---
        self.next_slide(loop=True)
        self.play(time_tracker.animate.increment_value(TAU), run_time=3, rate_func=linear)

        # --- Slide 2 (Transition): Xuất hiện công thức Scene 1 ---
        self.next_slide(auto_next=True) 
        fml_zt = MathTex(r"z_t = (1 - t)x + t\epsilon", font_size=32, color=Theme.NEUTRAL)
        fml_cond = MathTex(r"\text{conditional velocity: }\quad v_t = \epsilon - x", font_size=28, color=Theme.NEUTRAL)
        fml_marg = MathTex(r"\text{marginal velocity: }\quad v(z_t, t) \triangleq \mathbb{E}_{p_t(v_t|z_t)}[v_t]", font_size=26, color=Theme.NEUTRAL)
        scene1_group = VGroup(fml_zt, fml_cond, fml_marg).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(LEFT_ANCHOR, aligned_edge=LEFT)

        self.play(
            FadeIn(fml_zt, shift=RIGHT*0.5),
            FadeIn(fml_cond, shift=RIGHT*0.5),
            FadeIn(fml_marg, shift=RIGHT*0.5),
            time_tracker.animate.increment_value(TAU/2),
            run_time=1.5
        )

        # --- Slide 3: Vòng lặp hạt ---
        self.next_slide(loop=True)
        self.play(time_tracker.animate.increment_value(TAU), run_time=3, rate_func=linear)

        # --- Slide 4 (Transition): Xuất hiện công thức Loss (ĐÃ ĐẢO CHIỀU: FM -> CFM) ---
        self.next_slide(auto_next=True) 
        loss_fm = MathTex(r"\mathcal{L}_{\text{FM}} = \mathbb{E}\|v_\theta(z_t, t) - v(z_t, t)\|^2", font_size=30, color=Theme.DIM) # FM nằm trên (Làm mờ đi vì là mục tiêu lý tưởng)
        loss_cfm = MathTex(r"\mathcal{L}_{\text{CFM}} = \mathbb{E}\|v_\theta(z_t, t) - v_t\|^2", font_size=30, color=Theme.PRIMARY) # CFM nằm dưới (Nổi bật màu xanh vì là mục tiêu thực tế)
        
        arrow_loss = Arrow(UP, DOWN, buff=0, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15).set_height(0.4)
        arrow_container = VGroup(arrow_loss).shift(RIGHT * 1.5)
        
        # Sắp xếp đúng logic toán học của bài báo: FM -> Arrow -> CFM
        loss_group = VGroup(loss_fm, arrow_container, loss_cfm).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        loss_group.next_to(scene1_group, DOWN, buff=0.4, aligned_edge=LEFT)
        
        self.play(
            FadeIn(loss_fm),
            Create(arrow_loss),
            FadeIn(loss_cfm, shift=DOWN*0.2),
            time_tracker.animate.increment_value(TAU/2),
            run_time=1.5
        )

        # --- Slide 5: Vòng lặp hạt ---
        self.next_slide(loop=True)
        self.play(time_tracker.animate.increment_value(TAU), run_time=3, rate_func=linear)

        # --- Slide 6 (Transition): Xóa công thức cũ, hiện tiêu đề & lý thuyết ODE ---
        self.next_slide(auto_next=True) 
        ode_title = Text("Solve ODE:", font=Theme.FONT_BODY, font_size=26, color=Theme.NEUTRAL, weight="BOLD")
        fml_ode = MathTex(r"\frac{d}{dt}z_t = v(z_t, t)", font_size=34, color=Theme.PRIMARY)
        
        txt_theory = MathTex(r"\bullet\ \text{In principle, w/ \textbf{ground-truth} field } v(z_t, t)", font_size=22, color=Theme.NEUTRAL)
        txt_prac = MathTex(r"\bullet\ \text{In practice, approximate by } v_\theta(z_t, t)", font_size=22, color=Theme.NEUTRAL)
        
        # Tách biệt hoàn toàn nhãn chữ và công thức thành các dòng độc lập xếp dọc
        lbl_integral = Text("Ideally, trajectory given by integral:", font=Theme.FONT_BODY, font_size=18, color=Theme.DIM)
        fml_integral = MathTex(r"\quad z_r = z_t - \int_{r}^{t} v(z_\tau, \tau)d\tau", font_size=28, color=Theme.NEUTRAL)

        lbl_euler = Text("In reality, approximate by finite sum:", font=Theme.FONT_BODY, font_size=18, color=Theme.DIM)
        fml_euler = MathTex(r"\quad z_r = z_t + (r - t)v(z_t, t)", font_size=28, color=Theme.NEUTRAL)

        # Toàn bộ cột trái được xếp dọc hoàn toàn (8 phần tử độc lập)
        scene3_group = VGroup(
            ode_title, fml_ode, 
            txt_theory, txt_prac, 
            lbl_integral, fml_integral, 
            lbl_euler, fml_euler
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        
        # Căn chỉnh vị trí lùi hẳn xuống dưới để tránh đè tiêu đề chính "Flow Matching"
        scene3_group.move_to(LEFT_ANCHOR, aligned_edge=LEFT).shift(DOWN * 0.6)

        self.play(
            FadeOut(scene1_group, shift=LEFT),
            FadeOut(loss_group, shift=LEFT),
            time_tracker.animate.increment_value(TAU/2),
            run_time=1.0
        )
        self.play(
            FadeIn(scene3_group[0:4], shift=RIGHT), 
            time_tracker.animate.increment_value(TAU/2),
            run_time=1.5
        )

        # --- Slide 7: Vòng lặp hạt ---
        self.next_slide(loop=True)
        self.play(time_tracker.animate.increment_value(TAU), run_time=3, rate_func=linear)
        
        # --- Slide 8 (Transition): Hiện công thức Tích phân & Euler ---
        self.next_slide(auto_next=True) 
        self.play(
            FadeIn(scene3_group[4:8], shift=UP*0.2), # lbl_integral, fml_integral, lbl_euler, fml_euler
            time_tracker.animate.increment_value(TAU/2),
            run_time=1.5
        )

        # --- Slide 9: Vòng lặp hạt cuối cùng ---
        self.next_slide(loop=True)
        self.play(time_tracker.animate.increment_value(TAU), run_time=3, rate_func=linear)

        # Giải phóng các updater khi kết thúc cảnh trình chiếu
        flow_dots.clear_updaters()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 53 — MODULE 50: WHAT WE DO VS WHAT WE WANT  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
from manim import Axes, Rectangle, Dot, Line, Arrow

class Module50_NeuralODE_Comparison(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề slide chính (Rút gọn sạch sẽ, ghim góc trái trên tránh đè chữ)
        title_group = VGroup()
        title = slide_title("Neural ODE")
        cite = Text("[Chen et al, NeurIPS 2018]", font=Theme.FONT_BODY, font_size=20, color=Theme.DIM)
        cite.next_to(title, RIGHT, buff=0.5).align_to(title, DOWN)
        title_group.add(title, cite)
        
        self.play(Write(title), FadeIn(cite))

        # =====================================================================
        # HÀM HỖ TRỢ: VẼ ĐỒ THỊ TRƯỜNG VECTOR VÀ QUỸ ĐẠO
        # =====================================================================
        def make_plot(is_continuous=False):
            # Thêm tips=False để tắt hai tam giác trắng khổng lồ bị lỗi hiển thị
            axes = Axes(
                x_range=[-6, 6, 2],
                y_range=[0, 5, 1],
                x_length=3.0,
                y_length=3.2,
                axis_config={"color": Theme.NEUTRAL, "include_numbers": False, "tick_size": 0.05},
                tips=False 
            )
            
            # Khung viền tĩnh định hình vùng vẽ
            bbox = Rectangle(width=3.0, height=3.2, color=Theme.DIM, stroke_width=2, fill_color=Theme.BG, fill_opacity=0)
            bbox.move_to(axes.c2p(0, 2.5)) 
            
            # Nhãn cho các trục tọa độ
            x_nums = VGroup(
                Text("-5", font_size=14, color=Theme.NEUTRAL).next_to(axes.c2p(-5, 0), DOWN, buff=0.1),
                Text("0", font_size=14, color=Theme.NEUTRAL).next_to(axes.c2p(0, 0), DOWN, buff=0.1),
                Text("5", font_size=14, color=Theme.NEUTRAL).next_to(axes.c2p(5, 0), DOWN, buff=0.1),
            )
            y_nums = VGroup(*[
                Text(str(i), font_size=14, color=Theme.NEUTRAL).next_to(axes.c2p(-6, i), LEFT, buff=0.1)
                for i in range(6)
            ])
            x_label = Text("Input/Hidden/Output", font_size=14, color=Theme.DIM).next_to(x_nums, DOWN, buff=0.2)
            y_label = Text("Depth", font_size=14, color=Theme.DIM).rotate(PI/2).next_to(y_nums, LEFT, buff=0.2)

            # Mô phỏng trường vector chìm phía sau
            vector_field = VGroup()
            for x in np.linspace(-5.5, 5.5, 9):
                for y in np.linspace(0.2, 4.8, 7):
                    dx = -0.4 * x
                    dy = 1
                    norm = np.hypot(dx, dy)
                    dx, dy = dx/norm * 0.4, dy/norm * 0.4
                    
                    arrow_color = Theme.ACCENT_GOLD if x > 0 else ManimColor("#9FA8DA") 
                    start_p = axes.c2p(x, y)
                    end_p = axes.c2p(x + dx, y + dy)
                    
                    arrow = Arrow(
                        start_p, end_p, buff=0, 
                        max_tip_length_to_length_ratio=0.25, stroke_width=1.5, 
                        color=arrow_color, stroke_opacity=0.4
                    )
                    vector_field.add(arrow)

            # Mô phỏng quỹ đạo dòng chảy của dữ liệu
            trajectories = VGroup()
            start_xs = [-5, -3, -1, 1, 3, 5]
            
            for sx in start_xs:
                if is_continuous:
                    # Mạng ODE: Đường cong mịn (Continuous Time)
                    curve = axes.plot_parametric_curve(
                        lambda t: np.array([sx * np.exp(-0.4 * t), t, 0]), 
                        t_range=[0, 5], color=Theme.NEUTRAL, stroke_width=2
                    )
                    trajectories.add(curve)
                    t_vals = np.linspace(0, 5, 12)
                    dots = VGroup(*[Dot(axes.c2p(sx * np.exp(-0.4 * t), t), radius=0.03, color=Theme.NEUTRAL) for t in t_vals])
                    trajectories.add(dots)
                else:
                    # Mạng ResNet: Gấp khúc rời rạc (Discrete Time)
                    t_vals = list(range(6))
                    points = [axes.c2p(sx * np.exp(-0.4 * t), t) for t in t_vals]
                    lines = VGroup(*[Line(points[i], points[i+1], color=Theme.NEUTRAL, stroke_width=2) for i in range(5)])
                    dots = VGroup(*[Dot(p, radius=0.04, color=Theme.NEUTRAL) for p in points])
                    trajectories.add(lines, dots)

            plot_group = VGroup(bbox, axes, x_nums, y_nums, x_label, y_label, vector_field, trajectories)
            return plot_group

        # =====================================================================
        # THIẾT LẬP CỘT TRÁI: WHAT WE DO (RESIDUAL NETWORK)
        # =====================================================================
        header_res = Text("What we do:", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD, weight="BOLD")
        
        formula_res = MathTex(
            r"z_r", r" = ", r"z_t", r" + (r - t)", r"v(z_t, t)",
            font_size=32
        )
        formula_res[0].set_color(Theme.ACCENT_RED)
        formula_res[2].set_color(Theme.ACCENT_RED)
        formula_res[4].set_color(Theme.PRIMARY)

        title_res = Text("Residual Network", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        plot_res = make_plot(is_continuous=False)
        
        res_group = VGroup(header_res, formula_res, title_res, plot_res).arrange(DOWN, buff=0.35)

        # =====================================================================
        # THIẾT LẬP CỘT PHẢI: WHAT WE WANT (ODE NETWORK)
        # =====================================================================
        header_ode = Text("What we want:", font=Theme.FONT_BODY, font_size=24, color=Theme.ACCENT_GOLD, weight="BOLD")
        
        formula_ode = MathTex(
            r"\frac{d}{dt}z_t", r" = ", r"v(z_t, t)", r"\quad\text{or}\quad", r"z_r", r" = ", r"z_t", r" - \int_{r}^{t} v(z_\tau, \tau)d\tau",
            font_size=30
        )
        formula_ode[0].set_color(Theme.PRIMARY)
        formula_ode[2].set_color(Theme.PRIMARY)
        formula_ode[4].set_color(Theme.ACCENT_RED)
        formula_ode[6].set_color(Theme.ACCENT_RED)

        title_ode = Text("ODE Network", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        plot_ode = make_plot(is_continuous=True)
        
        ode_group = VGroup(header_ode, formula_ode, title_ode, plot_ode).arrange(DOWN, buff=0.35)

        # =====================================================================
        # CĂN CHỈNH ĐỐI XỨNG TUYỆT ĐỐI GIỮA HAI CỘT (TRÁNH LỆCH TRỤC)
        # =====================================================================
        header_res.align_to(header_ode, UP)
        formula_res.align_to(formula_ode, UP)
        title_res.align_to(title_ode, UP)
        plot_res.align_to(plot_ode, UP)

        # Xếp ngang 2 cột
        main_cols = VGroup(res_group, ode_group).arrange(RIGHT, buff=1.2)
        
        # Căn trung tâm và hạ thấp xuống DOWN * 0.4 để tránh hoàn toàn việc đè tiêu đề
        main_cols.center().shift(DOWN * 0.4)

        # =====================================================================
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # =====================================================================
        
        # Bước 1: Hiển thị thực tế của Residual Network (Rời rạc)
        self.play(
            FadeIn(header_res, shift=DOWN*0.2),
            FadeIn(formula_res, shift=UP*0.2)
        )
        self.play(FadeIn(title_res))
        self.play(FadeIn(plot_res), run_time=1.2)
        self.next_slide()

        # Bước 2: Hiển thị mục tiêu lý tưởng của ODE Network (Liên tục)
        self.play(
            FadeIn(header_ode, shift=DOWN*0.2),
            FadeIn(formula_ode, shift=UP*0.2)
        )
        self.play(FadeIn(title_ode))
        self.play(FadeIn(plot_ode), run_time=1.2)
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 54 — MODULE 51: AVERAGE VELOCITY  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Axes, SurroundingRectangle

class Module51_AverageVelocity(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề slide
        title = slide_title("Average Velocity")
        self.play(Write(title))

        COLOR_U = Theme.ACCENT_GOLD
        COLOR_V = ManimColor("#7E57C2") # Purple

        # =====================================================================
        # BƯỚC 1: XÂY DỰNG SCENE 1 (LÝ THUYẾT TOÁN HỌC)
        # =====================================================================
        
        # Row 1: What we want
        lbl_want = Text("What we want:", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        fml_want = MathTex(r"z_r = z_t - \int_{r}^{t} v(z_\tau, \tau)d\tau", font_size=36, color=Theme.NEUTRAL)
        
        # Row 2: What we do
        lbl_do = Text("What we do:", font=Theme.FONT_BODY, font_size=28, color=Theme.NEUTRAL)
        fml_do = MathTex(r"z_r = z_t - (t - r)", r"v(z_t, t)", font_size=36, color=Theme.NEUTRAL)

        # Định vị các thành phần hàng đầu
        lbl_want.move_to([-2, 1.5, 0], aligned_edge=RIGHT)
        fml_want.next_to(lbl_want, RIGHT, buff=0.8)
        
        lbl_do.move_to([-2, 0.2, 0], aligned_edge=RIGHT)
        fml_do.next_to(lbl_do, RIGHT, buff=0.8)

        # Gạch chéo bỏ v(z_t, t)
        cross1 = Line(fml_do[1].get_bottom() + DL*0.1, fml_do[1].get_top() + UR*0.1, color=Theme.ACCENT_RED, stroke_width=3)
        cross2 = Line(fml_do[1].get_bottom() + DR*0.1, fml_do[1].get_top() + UL*0.1, color=Theme.ACCENT_RED, stroke_width=3)
        red_cross = VGroup(cross1, cross2)

        # Mũi tên chỉ xuống
        arr_down = MathTex(r"\Downarrow", font_size=48, color=Theme.ACCENT_RED).next_to(fml_do[1], DOWN, buff=0.3)

        # Phương trình định nghĩa Average Velocity
        fml_u = MathTex(
            r"u(z_t, r, t)", 
            r"\triangleq \frac{1}{t-r} \int_{r}^{t}", 
            r"v(z_\tau, \tau)", 
            r"d\tau",
            font_size=40
        )
        fml_u.next_to(arr_down, DOWN, buff=0.4).align_to(fml_want, LEFT).shift(RIGHT*0.5)

        # Gạch dưới và chú thích màu
        line_u = Line(fml_u[0].get_left(), fml_u[0].get_right(), color=COLOR_U, stroke_width=2).next_to(fml_u[0], DOWN, buff=0.1)
        lbl_u = Text("u: average velocity", font=Theme.FONT_BODY, font_size=24, color=COLOR_U).next_to(line_u, DOWN, buff=0.1)

        line_v = Line(fml_u[2].get_left(), fml_u[2].get_right(), color=COLOR_V, stroke_width=2).next_to(fml_u[2], DOWN, buff=0.1)
        lbl_v = Text("v: instantaneous velocity", font=Theme.FONT_BODY, font_size=24, color=COLOR_V).next_to(line_v, DOWN, buff=0.1)

        # Nhóm các đối tượng sẽ biến mất ở Scene 2
        scene1_fadeout_group = VGroup(lbl_want, fml_want, lbl_do, fml_do, red_cross, arr_down, line_u, lbl_u, line_v, lbl_v)

        # Trình diễn Scene 1
        self.play(FadeIn(lbl_want), FadeIn(fml_want))
        self.play(FadeIn(lbl_do), FadeIn(fml_do))
        self.play(Create(red_cross))
        self.play(FadeIn(arr_down))
        self.play(FadeIn(fml_u))
        self.play(Create(line_u), FadeIn(lbl_u), Create(line_v), FadeIn(lbl_v))
        self.next_slide()


        # =====================================================================
        # BƯỚC 2: CHUYỂN CẢNH SANG SCENE 2 (KHÔNG BỊ CHE KHUẤT CÔNG THỨC)
        # =====================================================================
        self.play(FadeOut(scene1_fadeout_group, shift=LEFT))

        # Di chuyển công thức u lên góc phải
        fml_u.generate_target()
        fml_u.target.scale(0.8)
        fml_u.target.move_to([4.0, 2.5, 0])
        
        # SỬA LỖI: Tạo hộp bao quanh hoàn toàn trong suốt (không sử dụng fill_opacity=1)
        boxed_fml = SurroundingRectangle(
            fml_u.target, 
            color=Theme.DIM, 
            stroke_width=2, 
            corner_radius=0.1
        )
        
        self.play(
            MoveToTarget(fml_u),
            FadeIn(boxed_fml)
        )

        # ─────────────────────────────────────────────────────────────────────
        # KHỐI ĐỒ HỌA TRÁI (MAIN PLOT)
        # ─────────────────────────────────────────────────────────────────────
        axes_main = Axes(x_range=[-3, 3], y_range=[-3, 3], x_length=6.5, y_length=5.0)
        axes_main.move_to([-3.5, -0.5, 0]) 

        # Hàm mô phỏng quỹ đạo đường cong tự nhiên
        def func(x): return 2*np.sin(x*0.8) - 0.1*x**2
        def dfunc(x): return 1.6*np.cos(x*0.8) - 0.2*x

        curve_main = axes_main.plot(func, color=Theme.DIM, stroke_width=3)
        
        x_r = -2.0
        x_t = 2.5
        p_r = axes_main.c2p(x_r, func(x_r))
        p_t = axes_main.c2p(x_t, func(x_t))

        dot_r = Dot(p_r, color=Theme.ACCENT_RED, radius=0.08)
        lbl_dot_r = MathTex("r", font_size=36, color=Theme.NEUTRAL).next_to(dot_r, DOWN)

        dot_t = Dot(p_t, color=Theme.ACCENT_RED, radius=0.08)
        lbl_dot_t = MathTex("t", font_size=36, color=Theme.NEUTRAL).next_to(dot_t, RIGHT)

        # Đường Displacement 
        disp_line = Line(p_r, p_t, color=Theme.DIM, stroke_width=1.5)
        disp_lbl = MathTex(r"(t-r)u(z, r, t)", font_size=24, color=Theme.NEUTRAL)
        disp_lbl.move_to(disp_line.point_from_proportion(0.6) + DOWN*0.4 + RIGHT*0.2)
        disp_lbl2 = Text("displacement", font_size=16, color=Theme.NEUTRAL).next_to(disp_lbl, DOWN, buff=0.05)

        # Tangent Vectors (Instantaneous Velocity)
        tangents = VGroup()
        for x in np.linspace(x_r, x_t, 8):
            p1 = axes_main.c2p(x, func(x))
            p2 = axes_main.c2p(x + 0.1, func(x + 0.1))
            vec = p2 - p1
            vec = vec / np.linalg.norm(vec) * 0.9 
            tangent = Arrow(p1, p1 + vec, buff=0, color=COLOR_V, stroke_width=3, tip_length=0.15)
            tangents.add(tangent)

        lbl_v_arrow = Text("instant. vel.", font_size=20, color=COLOR_V)
        lbl_v_math = MathTex("v", font_size=32, color=COLOR_V)
        lbl_v_group = VGroup(lbl_v_arrow, lbl_v_math).arrange(DOWN, buff=0.05).next_to(tangents[4].get_end(), UP+LEFT, buff=0.1)

        # Secant Vector (Average Velocity)
        vec_u = p_t - p_r
        vec_u = vec_u / np.linalg.norm(vec_u) * 1.8 
        arrow_u = Arrow(p_r, p_r + vec_u, buff=0, color=COLOR_U, stroke_width=4, tip_length=0.2)
        
        lbl_u_arr_1 = Text("avg. vel.", font_size=20, color=COLOR_U)
        lbl_u_arr_2 = MathTex("u(z, r, t)", font_size=32, color=COLOR_U)
        lbl_u_arr_group = VGroup(lbl_u_arr_1, lbl_u_arr_2).arrange(DOWN, buff=0.05).next_to(arrow_u.get_end(), DOWN+RIGHT, buff=0.1)

        main_plot_group = VGroup(curve_main, disp_line, dot_r, lbl_dot_r, dot_t, lbl_dot_t, disp_lbl, disp_lbl2, tangents, lbl_v_group, arrow_u, lbl_u_arr_group)

        # ─────────────────────────────────────────────────────────────────────
        # KHỐI ĐỒ HỌA PHẢI (SMALL MULTIPLES)
        # ─────────────────────────────────────────────────────────────────────
        def make_small_plot(x_center, t_val, lbl_str):
            axes = Axes(x_range=[-3, 3], y_range=[-3, 3], x_length=1.8, y_length=1.3)
            axes.move_to([x_center, 0.4, 0]) 
            
            curve = axes.plot(func, color=Theme.DIM, stroke_width=1.5)
            p_r_sm = axes.c2p(x_r, func(x_r))
            x_t_curr = x_r + (x_t - x_r) * t_val
            p_t_curr = axes.c2p(x_t_curr, func(x_t_curr))
            
            d_r = Dot(p_r_sm, color=Theme.ACCENT_RED, radius=0.04)
            d_t = Dot(p_t_curr, color=Theme.ACCENT_RED, radius=0.04)
            
            fans = VGroup()
            num_fans = int(8 * t_val)
            if num_fans > 0:
                for x in np.linspace(x_r + 0.1, x_t_curr, num_fans):
                    p = axes.c2p(x, func(x))
                    fan = Arrow(p_r_sm, p, buff=0, color=COLOR_U, stroke_width=1.5, tip_length=0.08, max_stroke_width_to_length_ratio=999)
                    fans.add(fan)
                    
            lbl = MathTex(lbl_str, font_size=20, color=Theme.NEUTRAL).next_to(axes.c2p(0, -3), DOWN, buff=0.2)
            u_lbl = MathTex("u(z, r, t)", font_size=16, color=COLOR_U).next_to(axes.c2p(-1, 0), DOWN, buff=0.1)
            
            return VGroup(curve, fans, d_r, d_t, lbl, u_lbl)

        # Ghim theo tọa độ để tạo khoảng cách đều nhau
        sp1 = make_small_plot(1.5, 0.3, "t = 0.5")
        sp2 = make_small_plot(4.0, 0.6, "t = 0.7")
        sp3 = make_small_plot(6.5, 1.0, "t = 1.0")
        small_plots_group = VGroup(sp1, sp2, sp3)

        # ─────────────────────────────────────────────────────────────────────
        # KHỐI TEXT CHÚ THÍCH (PROPERTIES)
        # ─────────────────────────────────────────────────────────────────────
        prop_title = Text("Properties:", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD")
        b1 = Tex(r"$\bullet$ condition on \textbf{two time variables}", font_size=28, color=Theme.NEUTRAL)
        b2 = Tex(r"$\bullet$ network \textbf{independent}", font_size=28, color=Theme.NEUTRAL)
        b3 = Tex(r"$\bullet$ \textbf{ground-truth field} that pre-exists", font_size=28, color=Theme.NEUTRAL)
        
        props = VGroup(prop_title, b1, b2, b3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        props.move_to([1.5, -1.8, 0], aligned_edge=LEFT)

        # Hiện Scene 2 đồng loạt
        self.play(FadeIn(main_plot_group), run_time=1.0)
        self.play(FadeIn(small_plots_group), run_time=1.0)
        self.play(FadeIn(props), run_time=1.0)
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 55 — MODULE 52: THE MEANFLOW IDENTITY  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import SurroundingRectangle

class Module52_MeanFlowIdentity(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # =====================================================================
        # 1. TIÊU ĐỀ VÀ PHỤ ĐỀ (Giao diện 2 dòng gọn gàng, tránh lỗi Overlap)
        # =====================================================================
        title = slide_title("The MeanFlow Identity")
        sub_title = Text(
            "• Integral is intractable.\n  Differentiate it instead.", 
            font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL,
            line_spacing=1.2
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.25)
        
        self.play(Write(title), FadeIn(sub_title))

        # =====================================================================
        # BƯỚC 2: XÂY DỰNG TRỤC TRUNG TÂM (CÁC PHƯƠNG TRÌNH TOÁN HỌC)
        # =====================================================================
        FS = 34 # Kích thước font chuẩn cho toán học trong module này

        # Phương trình 1 (Định nghĩa)
        eq1 = MathTex(r"u(z_t, r, t) \triangleq \frac{1}{t-r} \int_r^t v(z_\tau, \tau) d\tau", font_size=FS, color=Theme.NEUTRAL)
        box1 = SurroundingRectangle(eq1, color=Theme.DIM, stroke_width=2, fill_color=Theme.BG, fill_opacity=1)
        row1 = VGroup(box1, eq1)

        # Phương trình 2 (Nhân chéo)
        eq2 = MathTex(r"(t-r)u(z_t, r, t) = \int_r^t v(z_\tau, \tau) d\tau", font_size=FS, color=Theme.NEUTRAL)

        # Phương trình 3 (Đạo hàm 2 vế)
        eq3 = MathTex(r"\frac{d}{dt} (t-r)u(z_t, r, t) = \frac{d}{dt} \int_r^t v(z_\tau, \tau) d\tau", font_size=FS, color=Theme.NEUTRAL)

        # Phương trình 4 (Khai triển)
        eq4 = MathTex(r"u(z_t, r, t) + (t-r)\frac{d}{dt}u(z_t, r, t) = v(z_t, t)", font_size=FS, color=Theme.NEUTRAL)

        # Phương trình 5 (Kết quả cuối cùng)
        eq5 = MathTex(
            r"u(z_t, r, t)",                # 0: avg. vel.
            r" = ",                         # 1: =
            r"v(z_t, t)",                   # 2: instant. vel.
            r" - ",                         # 3: -
            r"(t-r)",                       # 4: two time variables
            r"\frac{d}{dt}u(z_t, r, t)",    # 5: t-derivative
            font_size=38, color=Theme.NEUTRAL
        )
        box5 = SurroundingRectangle(eq5, color=Theme.DIM, stroke_width=2, fill_color=Theme.BG, fill_opacity=1)
        row5 = VGroup(box5, eq5)

        # Xếp dọc các phương trình tạo thành "Trục xương sống" (Spine)
        spine = VGroup(row1, eq2, eq3, eq4, row5).arrange(DOWN, buff=0.55)

        # =====================================================================
        # BƯỚC 3: NEO CÁC CHI TIẾT PHỤ VÀO TRỤC TRUNG TÂM
        # =====================================================================
        def make_arrow():
            return Arrow(LEFT, RIGHT, buff=0, color=Theme.DIM, stroke_width=7, tip_length=0.15).set_width(0.5)

        arr2 = make_arrow().next_to(eq2, LEFT, buff=0.4)

        arr3 = make_arrow().next_to(eq3, LEFT, buff=0.4)
        txt3 = Text("differentiate wrt t", font_size=20, color=Theme.NEUTRAL).next_to(arr3, LEFT, buff=0.25)

        arr4 = make_arrow().next_to(eq4, LEFT, buff=0.4)
        txt4_lhs = Text("lhs:\nproduct rule", font_size=20, color=Theme.NEUTRAL).set_line_spacing(1.2).next_to(arr4, LEFT, buff=0.25)
        txt4_rhs = Text("rhs: fundamental\ntheorem of calculus", font_size=20, color=Theme.NEUTRAL).set_line_spacing(1.2).next_to(eq4, RIGHT, buff=0.3)

        arr5 = make_arrow().next_to(row5, LEFT, buff=0.4)
        txt5 = Text("MeanFlow\nIdentity", font_size=24, color=Theme.ACCENT_RED, weight="BOLD").set_line_spacing(1.2).next_to(row5, RIGHT, buff=0.3)

        # Gom toàn bộ hệ thống
        scene1_group = VGroup(spine, arr2, arr3, txt3, arr4, txt4_lhs, txt4_rhs, arr5, txt5)
        
        # Khống chế chiều cao an toàn (hạ xuống 4.8) và đẩy sâu xuống dưới (shift DOWN 0.5) để tránh đè phụ đề
        scene1_group.scale_to_fit_height(4.8)
        scene1_group.center().shift(DOWN * 0.5)

        # =====================================================================
        # KỊCH BẢN ANIMATION: SCENE 1
        # =====================================================================
        self.play(FadeIn(row1))
        self.play(Create(arr2), FadeIn(eq2, shift=RIGHT*0.3))
        self.play(FadeIn(txt3), Create(arr3), FadeIn(eq3, shift=RIGHT*0.3))
        self.play(FadeIn(txt4_lhs), FadeIn(txt4_rhs), Create(arr4), FadeIn(eq4, shift=RIGHT*0.3))
        self.play(Create(arr5), FadeIn(row5, shift=RIGHT*0.3), FadeIn(txt5))
        self.next_slide()


        # =====================================================================
        # CHUYỂN CẢNH VÀ XÂY DỰNG SCENE 2 (ANNOTATIONS)
        # =====================================================================
        
        # Làm mờ tất cả ngoại trừ Phương trình chốt (row5) và dòng phụ đề cũ
        fadeout_group = VGroup(row1, eq2, arr2, eq3, arr3, txt3, eq4, arr4, txt4_lhs, txt4_rhs, arr5, txt5, sub_title)
        self.play(FadeOut(fadeout_group, shift=LEFT))

        # Phóng to và đưa phương trình chốt lên vị trí trung tâm
        row5.generate_target()
        row5.target.scale(1.3)
        row5.target.center().shift(UP * 1.5)
        self.play(MoveToTarget(row5))

        # Các màu chuẩn bị cho nhãn
        c_u  = Theme.ACCENT_GOLD
        c_v  = ManimColor("#7E57C2") # Tím (Purple)
        c_t2 = Theme.ACCENT_RED
        c_dt = Theme.PRIMARY         # Xanh (Sky Blue)

        # Tạo gạch dưới và Text chú giải
        l_u = Line(eq5[0].get_left(), eq5[0].get_right(), color=c_u).next_to(eq5[0], DOWN, buff=0.1)
        t_u = Text("avg. vel.", font_size=20, color=c_u).next_to(l_u, DOWN, buff=0.1)

        l_v = Line(eq5[2].get_left(), eq5[2].get_right(), color=c_v).next_to(eq5[2], DOWN, buff=0.1)
        t_v = Text("instant. vel.", font_size=20, color=c_v).next_to(l_v, DOWN, buff=0.1)

        l_t2 = Line(eq5[4].get_left(), eq5[4].get_right(), color=c_t2).next_to(eq5[4], DOWN, buff=0.1)
        t_t2 = Text("two time\nvariables", font_size=20, color=c_t2).set_line_spacing(1.2).next_to(l_t2, DOWN, buff=0.1)

        l_dt = Line(eq5[5].get_left(), eq5[5].get_right(), color=c_dt).next_to(eq5[5], DOWN, buff=0.1)
        t_dt = Text("t-derivative", font_size=20, color=c_dt).next_to(l_dt, DOWN, buff=0.1)

        # Căn chỉnh hàng ngang cho các Text có 1 dòng để tránh bị thò thụt
        t_u.set_y(t_v.get_y())
        t_dt.set_y(t_v.get_y())

        # Kịch bản Animation Scene 2
        self.play(Create(l_u), FadeIn(t_u, shift=UP*0.2))
        self.play(Create(l_v), FadeIn(t_v, shift=UP*0.2))
        self.play(Create(l_t2), FadeIn(t_t2, shift=UP*0.2))
        self.play(Create(l_dt), FadeIn(t_dt, shift=UP*0.2))
        
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 56 — MODULE 53: COMPUTING THE TIME DERIVATIVE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Ellipse, Matrix, MarkupText, SurroundingRectangle

class Module53_TimeDerivative(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        # 1. Tiêu đề
        title = slide_title("Computing the time derivative")
        self.play(Write(title))

        # =====================================================================
        # BƯỚC 1: XÂY DỰNG CÁC PHƯƠNG TRÌNH (TRỤC CĂN CHỈNH)
        # =====================================================================
        
        # Phương trình 1 (Chain Rule) - Tách mảng để vẽ vòng chú thích chính xác
        eq1 = MathTex(
            r"\frac{d}{dt} u(z_t, r, t)",   # 0
            r"=",                           # 1
            r"\partial_z u",                # 2
            r"\frac{dz_t}{dt}",             # 3
            r"+ \partial_r u",              # 4
            r"\frac{dr}{dt}",               # 5
            r"+ \partial_t u",              # 6
            r"\frac{dt}{dt}",               # 7
            font_size=38, color=Theme.NEUTRAL
        )

        # Phương trình 2 (Dạng Matrix)
        eq2_eq = MathTex(r"=", font_size=38, color=Theme.NEUTRAL)
        eq2_row = MathTex(r"\big[ \partial_z u, \partial_r u, \partial_t u \big]", font_size=38, color=Theme.NEUTRAL)
        
        # Sử dụng đối tượng Matrix tích hợp của Manim để quản lý vector cột dễ dàng
        col_vec = Matrix([[r"v(z_t, t)"], ["0"], ["1"]], v_buff=0.8).scale(0.7)
        col_vec.set_color(Theme.NEUTRAL)
        
        line2 = VGroup(eq2_eq, eq2_row, col_vec).arrange(RIGHT, buff=0.2)

        # =====================================================================
        # BƯỚC 2: CĂN CHỈNH VÀ SẮP XẾP BỐ CỤC KHỐI TRÊN
        # =====================================================================
        
        top_eq_group = VGroup(eq1, line2).arrange(DOWN, buff=0.8)
        # Gióng thẳng dấu "=" của hai phương trình để tạo sự liên kết toán học
        line2.shift((eq1[1].get_center()[0] - eq2_eq.get_center()[0]) * RIGHT)

        # Khối hộp giải thích "The ODE we are solving"
        ode_title = Text("The ODE we are solving", font_size=22, color=Theme.PRIMARY)
        ode_eq = MathTex(r"\frac{d}{dt}z_t = v(z_t, t)", font_size=32, color=Theme.NEUTRAL)
        ode_rect = SurroundingRectangle(ode_eq, color=Theme.PRIMARY, stroke_width=2, fill_opacity=0, buff=0.2)
        ode_box = VGroup(ode_rect, ode_eq)
        ode_box_group = VGroup(ode_title, ode_box).arrange(DOWN, buff=0.2)

        # Đặt khối ODE sang bên phải của line2
        ode_box_group.next_to(line2, RIGHT, buff=1.0)
        ode_box_group.set_y(line2.get_y()) # Cân bằng ngang hàng với line2

        ode_arrow = Arrow(
            start=col_vec.get_right() + RIGHT*0.1, 
            end=ode_box_group.get_left() + LEFT*0.1, 
            color=Theme.PRIMARY, buff=0, tip_length=0.15
        )

        # Đóng gói và căn giữa tổng thể nửa trên màn hình (Tránh Lỗi 4 & 5)
        top_block = VGroup(top_eq_group, ode_box_group, ode_arrow)
        top_block.center().shift(UP * 0.8)

        # =====================================================================
        # BƯỚC 3: TẠO CÁC CHÚ THÍCH (ANNOTATIONS) DỰA TRÊN TỌA ĐỘ ĐÃ GHIM
        # =====================================================================
        
        # Chú thích trên Equation 1
        circ_z = Ellipse(width=eq1[3].width + 0.3, height=eq1[3].height + 0.4, color=Theme.PRIMARY, stroke_width=2).move_to(eq1[3])
        circ_r = Ellipse(width=eq1[5].width + 0.3, height=eq1[5].height + 0.4, color=Theme.ACCENT_GOLD, stroke_width=2).move_to(eq1[5])
        circ_t = Ellipse(width=eq1[7].width + 0.3, height=eq1[7].height + 0.4, color=Theme.ACCENT_GOLD, stroke_width=2).move_to(eq1[7])

        text_r = MathTex("= 0", font_size=24, color=Theme.ACCENT_GOLD).move_to(circ_r.get_corner(UR) + UR*0.1)
        text_t = MathTex("= 1", font_size=24, color=Theme.ACCENT_GOLD).move_to(circ_t.get_corner(UR) + UR*0.1)

        # Chú thích trên Equation 2 (Jacobian & Vector)
        u_line1 = Line(eq2_row.get_left(), eq2_row.get_right(), color=Theme.ACCENT_RED, stroke_width=2).next_to(eq2_row, DOWN, buff=0.1)
        u_line2 = Line(eq2_row.get_left(), eq2_row.get_right(), color=Theme.ACCENT_RED, stroke_width=2).next_to(u_line1, DOWN, buff=0.05)
        jacob_text = Text("Jacobian matrix", font_size=22, color=Theme.ACCENT_RED).next_to(VGroup(u_line1, u_line2), LEFT, buff=0.2)

        v_element = col_vec.get_entries()[0]
        v_line = Line(v_element.get_left(), v_element.get_right(), color=Theme.PRIMARY, stroke_width=2).next_to(v_element, DOWN, buff=0.05)

        # =====================================================================
        # BƯỚC 4: KHỐI VĂN BẢN KẾT LUẬN Ở ĐÁY
        # =====================================================================
        
        bp1_text = Text("• Jacobian-vector product (JVP):", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        # Sử dụng MarkupText để tô màu code trực tiếp trong một chuỗi, tránh lỗi font khi ghép khối
        bp1_code = MarkupText('<span fgcolor="#E91E63">jvp</span>(fn, (z, r, t), (v, 0, 1))', font="monospace", font_size=22, color=Theme.NEUTRAL)
        bp1 = VGroup(bp1_text, bp1_code).arrange(RIGHT, buff=0.2)

        bp2_text = Text("• c.f. vector-Jacobian product (VJP): ", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        bp2_quote = Text('"backpropagation"', font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD")
        bp2 = VGroup(bp2_text, bp2_quote).arrange(RIGHT, buff=0.1)

        bottom_section = VGroup(bp1, bp2).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        # Neo lề trái cùng khối trên để đồng bộ, chừa biên dưới an toàn
        bottom_section.to_edge(DOWN, buff=0.6).align_to(top_block, LEFT).shift(RIGHT*0.5)

        # =====================================================================
        # KỊCH BẢN ANIMATION
        # =====================================================================
        
        self.play(FadeIn(eq1))
        self.next_slide()
        
        self.play(Create(circ_r), FadeIn(text_r))
        self.play(Create(circ_t), FadeIn(text_t))
        self.play(Create(circ_z))
        self.next_slide()

        self.play(FadeIn(line2))
        self.play(Create(u_line1), Create(u_line2), FadeIn(jacob_text))
        self.play(Create(v_line))
        self.next_slide()

        self.play(FadeIn(ode_box_group), Create(ode_arrow))
        self.next_slide()

        self.play(FadeIn(bp1))
        self.play(FadeIn(bp2))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 57 — MODULE 54: TRAINING MEANFLOW MODELS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import DashedLine, SurroundingRectangle, RoundedRectangle

class Module54_Training(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG

        title = slide_title("Training MeanFlow Models")
        self.play(Write(title))

        # =====================================================================
        # BƯỚC 1: XÂY DỰNG KHỐI NEO CỐ ĐỊNH Ở DƯỚI (ANCHOR BLOCK - LỆCH TRÁI SÂU HƠN)
        # =====================================================================
        # Đẩy hẳn sang X = -2.3 để tạo khoảng trống lớn cho CFG Box bên phải
        X_LEFT_ANCHOR = -2.3

        # 1.1 Hàm Loss (Cỡ chữ 36 để tối ưu không gian chiều ngang)
        loss_fml = MathTex(
            r"\mathcal{L}(\theta) = \mathbb{E} \big\| ",   # 0
            r"u_\theta(z_t, r, t)",                       # 1
            r" - ",                                       # 2
            r"\text{sg}(u_{\text{tgt}})",                 # 3
            r" \big\|_2^2",                               # 4
            font_size=36, color=Theme.NEUTRAL
        )
        loss_fml[1].set_color(Theme.ACCENT_GOLD)
        loss_fml[3].set_color(Theme.ACCENT_RED)
        loss_fml.move_to([X_LEFT_ANCHOR, -0.3, 0])

        # Đẩy chữ chú thích vàng/đỏ ra xa nhau tránh tuyệt đối Overlap
        l_line1 = Line(loss_fml[1].get_left(), loss_fml[1].get_right(), color=Theme.ACCENT_GOLD).next_to(loss_fml[1], DOWN, buff=0.1)
        l_lbl1 = Text("parameterize u directly", font_size=14, color=Theme.ACCENT_GOLD)
        l_lbl1.next_to(l_line1, DOWN, buff=0.1).align_to(l_line1, RIGHT).shift(LEFT * 0.4)
        loss_part1 = VGroup(l_line1, l_lbl1)

        l_line2 = Line(loss_fml[3].get_left(), loss_fml[3].get_right(), color=Theme.ACCENT_RED).next_to(loss_fml[3], DOWN, buff=0.1)
        l_lbl2 = Text("target w/ stopgrad", font_size=14, color=Theme.ACCENT_RED)
        l_lbl2.next_to(l_line2, DOWN, buff=0.1).align_to(l_line2, LEFT).shift(RIGHT * 0.4)
        loss_part2 = VGroup(l_line2, l_lbl2)

        # 1.2 Hàm Target (Cỡ chữ 36)
        tgt_fml = MathTex(
            r"u_{\text{tgt}} = ",                         # 0
            r"v(z_t, t)",                                 # 1
            r" - (t-r)",                                  # 2
            r"\big( ",                                    # 3
            r"v(z_t, t)",                                 # 4
            r"\partial_z u_\theta + \partial_t u_\theta", # 5
            r" \big)",                                    # 6
            font_size=36, color=Theme.NEUTRAL
        )
        tgt_fml[1].set_color(ManimColor("#7E57C2"))
        tgt_fml[4].set_color(ManimColor("#7E57C2"))
        tgt_fml.move_to([X_LEFT_ANCHOR, -2.4, 0])

        t_line1 = Line(tgt_fml[1].get_left(), tgt_fml[1].get_right(), color=ManimColor("#7E57C2")).next_to(tgt_fml[1], DOWN, buff=0.1)
        t_lbl1 = Text("instant. vel.", font_size=18, color=ManimColor("#7E57C2")).next_to(t_line1, DOWN, buff=0.1)
        tgt_part1 = VGroup(t_line1, t_lbl1)

        sub_jvp = VGroup(tgt_fml[3], tgt_fml[4], tgt_fml[5], tgt_fml[6])
        t_line2 = Line(sub_jvp.get_left(), sub_jvp.get_right(), color=Theme.PRIMARY).next_to(sub_jvp, DOWN, buff=0.1)
        t_lbl2 = Text("computed by JVP", font_size=18, color=Theme.PRIMARY).next_to(t_line2, DOWN, buff=0.1)
        tgt_part2 = VGroup(t_line2, t_lbl2)

        bottom_anchor = VGroup(loss_fml, loss_part1, loss_part2, tgt_fml, tgt_part1, tgt_part2)


        # =====================================================================
        # BƯỚC 2: KHỐI TOP CHO SCENE 1 (RECAP THE IDENTITY)
        # =====================================================================
        mf_fml = MathTex(
            r"u(z_t, r, t)",                 # 0
            r" = ",                          # 1
            r"v(z_t, t)",                    # 2
            r" - (t-r)",                     # 3
            r"\frac{d}{dt}u(z_t, r, t)",     # 4
            font_size=38, color=Theme.NEUTRAL
        )
        mf_box = SurroundingRectangle(mf_fml, color=Theme.DIM, stroke_width=1.5, fill_opacity=0, buff=0.2)
        mf_group = VGroup(mf_box, mf_fml).move_to([0, 2.0, 0])

        m_l1 = Line(mf_fml[0].get_left(), mf_fml[0].get_right(), color=Theme.ACCENT_GOLD).next_to(mf_fml[0], DOWN, buff=0.1)
        m_t1 = Text("avg. vel.", font_size=18, color=Theme.ACCENT_GOLD).next_to(m_l1, DOWN, buff=0.1)
        
        m_l2 = Line(mf_fml[2].get_left(), mf_fml[2].get_right(), color=ManimColor("#7E57C2")).next_to(mf_fml[2], DOWN, buff=0.1)
        m_t2 = Text("instant. vel.", font_size=18, color=ManimColor("#7E57C2")).next_to(m_l2, DOWN, buff=0.1)
        
        m_l3 = Line(mf_fml[4].get_left(), mf_fml[4].get_right(), color=Theme.PRIMARY).next_to(mf_fml[4], DOWN, buff=0.1)
        m_t3 = Text("t-derivative", font_size=18, color=Theme.PRIMARY).next_to(m_l3, DOWN, buff=0.1)

        top_text = Text("No neural net up till now; only about the ground-truth field", font_size=18, color=Theme.DIM).move_to([0, 0.7, 0])
        dashed = DashedLine([-6, 0.4, 0], [6, 0.4, 0], color=Theme.DIM)

        scene1_top = VGroup(mf_group, m_l1, m_t1, m_l2, m_t2, m_l3, m_t3, top_text, dashed)


        # =====================================================================
        # BƯỚC 3: CÁC KHỐI TOP DẠNG BULLET POINTS CHO SCENE 2 & 3
        # =====================================================================
        b1 = Tex(r"$\bullet$ if $u_\theta$ has zero loss, it satisfies the \textbf{MeanFlow Identity}", font_size=28, color=Theme.NEUTRAL)
        b2 = VGroup(
            Tex(r"$\bullet$ \textbf{no integral}; only derivatives.", font_size=28, color=Theme.NEUTRAL),
            Text("(proven equivalent; see paper)", font_size=18, color=Theme.DIM)
        ).arrange(RIGHT, aligned_edge=DOWN, buff=0.2)
        b3 = Tex(r"$\bullet$ \textbf{stopgrad} prevents \textbf{higher-order gradients}", font_size=28, color=Theme.NEUTRAL)
        b4 = Tex(r"$\bullet$ a single-time function $u_\theta$ is \textbf{insufficient}", font_size=28, color=Theme.NEUTRAL)
        
        scene2_top = VGroup(b1, b2, b3, b4).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-1.0, 1.3, 0], aligned_edge=LEFT)


        c1 = Tex(r"$\bullet$ \textbf{marginal velocity} is not explicitly accessible", font_size=28, color=Theme.NEUTRAL)
        c2 = VGroup(
            Tex(r"$\bullet$ use \textbf{conditional velocity} instead", font_size=28, color=Theme.NEUTRAL),
            Text("(as in Flow Matching)", font_size=18, color=Theme.DIM)
        ).arrange(RIGHT, aligned_edge=DOWN, buff=0.2)
        
        scene3_top = VGroup(c1, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-1.5, 1.5, 0], aligned_edge=LEFT)

        # Các chi tiết đồ họa phát sinh thêm ở Scene 3
        cross1 = Line(tgt_fml[1].get_left(), tgt_fml[1].get_right(), color=ManimColor("#7E57C2"), stroke_width=3)
        cross2 = Line(tgt_fml[4].get_left(), tgt_fml[4].get_right(), color=ManimColor("#7E57C2"), stroke_width=3)

        # Đặt vt_box thay thế vào đúng không gian trống của instant_vel cũ
        vt_fml = MathTex(r"v_t = \epsilon - x", font_size=22, color=ManimColor("#7E57C2"))
        vt_rect = SurroundingRectangle(vt_fml, color=ManimColor("#7E57C2"), stroke_width=1.5, fill_opacity=0, buff=0.12)
        vt_box = VGroup(vt_rect, vt_fml).next_to(tgt_fml[1], DOWN, buff=0.3)

        # Thu gọn chiều rộng hộp CFG thành 4.8 và đẩy hẳn sang phải X = 4.3 để tạo khe hở tối ưu
        cfg_bg = RoundedRectangle(width=4.8, height=1.4, corner_radius=0.1, color=Theme.DIM, stroke_width=1, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1)
        cfg_txt = Text("CFG can be handled similarly (see paper):", font_size=14, color=Theme.NEUTRAL)
        cfg_fml = MathTex(r"\tilde{v}_t \triangleq \omega v_t + (1-\omega) u_\theta(z_t, t, t)", font_size=20, color=Theme.NEUTRAL)
        cfg_group = VGroup(cfg_txt, cfg_fml).arrange(DOWN, buff=0.15)
        cfg_bg.move_to(cfg_group.get_center())
        cfg_box = VGroup(cfg_bg, cfg_group).move_to([4.3, -1.8, 0])


        # =====================================================================
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # =====================================================================
        
        # --- SCENE 1 ---
        self.play(FadeIn(scene1_top))
        self.play(FadeIn(bottom_anchor))
        self.next_slide()

        # --- SCENE 2 ---
        self.play(
            FadeOut(scene1_top, shift=UP),
            FadeIn(scene2_top, shift=UP)
        )
        self.next_slide()

        # --- SCENE 3 ---
        self.play(
            FadeOut(scene2_top, shift=UP),
            FadeIn(scene3_top, shift=UP)
        )
        
        # Loại bỏ text cũ và đè các nhãn mới vào theo luồng tư duy, không bao giờ bị đè hình
        self.play(
            FadeOut(tgt_part1), 
            Create(cross1), 
            Create(cross2)
        )
        self.play(FadeIn(vt_box))
        self.play(FadeIn(cfg_box))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 58 — MODULE 55: INTERNET DATA AND FOUNDATION MODELS  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import color_gradient

class Module55_FoundationModels(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG
        
        # 1. Tiêu đề slide
        title = slide_title("Internet Data and Foundation Models")
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG 3 CỘT NỘI DUNG CHÍNH (KHÔNG BAO GỒM TIÊU ĐỀ CỘT)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- CỘT 1: BROAD DATASETS ---
        # Mô phỏng các tập dữ liệu lớn bằng các khối nhãn màu sắc
        ds_imagenet = RoundedBox(lines=["ImageNet", "(Vision)"], width=2.4, height=0.8, fill_color=ManimColor("#2E7D32"), stroke_color=Theme.SUCCESS)
        ds_crawl = RoundedBox(lines=["Common Crawl", "(Text)"], width=2.4, height=0.8, fill_color=ManimColor("#E65100"), stroke_color=Theme.ACCENT_GOLD)
        ds_wiki = RoundedBox(lines=["Wikipedia", "(Knowledge)"], width=2.4, height=0.8, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.NEUTRAL)
        ds_yt = RoundedBox(lines=["YouTube", "(Video)"], width=2.4, height=0.8, fill_color=ManimColor("#C62828"), stroke_color=Theme.ACCENT_RED)
        
        col1_content = VGroup(ds_imagenet, ds_crawl, ds_wiki, ds_yt).arrange(DOWN, buff=0.2)
        col1_bg = RoundedRectangle(width=col1_content.width + 0.6, height=4.6, corner_radius=0.2, fill_color=Theme.BOX_FILL, fill_opacity=0.5, stroke_color=Theme.DIM)
        col1_content.move_to(col1_bg.get_center())
        col1 = VGroup(col1_bg, col1_content)
        
        # --- CỘT 2: FOUNDATION MODELS ---
        # Mô phỏng các kiến trúc mạng nơ-ron phức tạp thành các block trừu tượng
        fm_llm = RoundedBox(lines=["Transformers", "(BERT / GPT)"], width=3.2, height=1.0, fill_color=ManimColor("#1A3B5C"), stroke_color=Theme.PRIMARY)
        fm_vit = RoundedBox(lines=["Vision Transformers", "(ViT / CLIP)"], width=3.2, height=1.0, fill_color=ManimColor("#4A148C"), stroke_color=ManimColor("#9C27B0"))
        fm_diff = RoundedBox(lines=["Diffusion Models", "(Latent / DiT)"], width=3.2, height=1.0, fill_color=ManimColor("#006064"), stroke_color=ManimColor("#00BCD4"))
        
        col2_content = VGroup(fm_llm, fm_vit, fm_diff).arrange(DOWN, buff=0.3)
        col2_bg = RoundedRectangle(width=col2_content.width + 0.8, height=4.6, corner_radius=0.2, fill_color=Theme.BOX_FILL, fill_opacity=0.5, stroke_color=Theme.PRIMARY)
        col2_content.move_to(col2_bg.get_center())
        col2 = VGroup(col2_bg, col2_content)
        
        # --- CỘT 3: VIDEO GENERATION ---
        # Mô phỏng các khung video kết quả bằng các khối gradient
        def create_video_frame(name, color1, color2):
            frame = RoundedRectangle(width=2.8, height=1.2, corner_radius=0.1, fill_color=color_gradient([color1, color2], 10), fill_opacity=0.8, stroke_color=Theme.NEUTRAL, stroke_width=1)
            lbl = Text(name, font=Theme.FONT_BODY, font_size=24, color=WHITE, weight="BOLD").move_to(frame)
            return VGroup(frame, lbl)

        vid_veo = create_video_frame("Veo-2", ManimColor("#FF9A9E"), ManimColor("#FECFEF")) # Gradient đỏ/hồng
        vid_gaia = create_video_frame("GAIA-2", ManimColor("#84FAB0"), ManimColor("#8FD3F4")) # Gradient xanh
        vid_genie = create_video_frame("Genie-2", ManimColor("#A18CD1"), ManimColor("#FBC2EB")) # Gradient tím
        
        col3_content = VGroup(vid_veo, vid_gaia, vid_genie).arrange(DOWN, buff=0.2)
        col3_bg = RoundedRectangle(width=col3_content.width + 0.6, height=4.6, corner_radius=0.2, fill_color=Theme.BOX_FILL, fill_opacity=0.5, stroke_color=Theme.DIM)
        col3_content.move_to(col3_bg.get_center())
        col3 = VGroup(col3_bg, col3_content)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: CĂN CHỈNH TƯƠNG ĐỐI & GẮN TIÊU ĐỀ TỪNG CỘT
        # ─────────────────────────────────────────────────────────────────────
        # Đặt cột 2 (Foundation Models) làm trung tâm, neo cột 1 và cột 3 vào 2 bên
        col1.next_to(col2, LEFT, buff=1.2)
        col3.next_to(col2, RIGHT, buff=1.2)
        
        # Khởi tạo Text tiêu đề và neo thẳng đứng lên đỉnh của từng BG tương ứng
        title_c1 = Text("Broad Datasets", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD")
        title_c1.next_to(col1_bg, UP, buff=0.25)
        
        title_c2 = Text("Foundation Models", font=Theme.FONT_BODY, font_size=28, color=Theme.PRIMARY, weight="BOLD")
        title_c2.next_to(col2_bg, UP, buff=0.25)
        
        title_c3 = Text("Video Generation", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD")
        title_c3.next_to(col3_bg, UP, buff=0.25)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM NHÓM, SCALE AN TOÀN VÀ VẼ MŨI TÊN
        # ─────────────────────────────────────────────────────────────────────
        all_columns = VGroup(
            col1, title_c1, 
            col2, title_c2, 
            col3, title_c3
        )
        
        # Giới hạn chiều rộng ở mức 13.5 để chừa biên 2 bên màn hình
        all_columns.set_width(13.5)
        all_columns.center().shift(DOWN * 0.2) # Dịch xuống chừa chỗ cho Slide Title
        
        # Vẽ mũi tên liên kết (Arrow) với nét dày
        arr_1_2 = Arrow(col1_bg.get_right(), col2_bg.get_left(), buff=0.2, color=Theme.PRIMARY, stroke_width=8, tip_length=0.25)
        text_pretrain = Text("Pretrain", font=Theme.FONT_BODY, font_size=22, color=Theme.PRIMARY, weight="BOLD").next_to(arr_1_2, UP, buff=0.1)
        
        arr_2_3 = Arrow(col2_bg.get_right(), col3_bg.get_left(), buff=0.2, color=Theme.PRIMARY, stroke_width=8, tip_length=0.25)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        # 1. Slide Title
        self.play(Write(title))
        self.next_slide()
        
        # 2. Xuất hiện Cột 1: Dữ liệu thô khổng lồ từ Internet
        self.play(FadeIn(col1_bg), Write(title_c1))
        self.play(FadeIn(col1_content), run_time=1.5)
        self.next_slide()
        
        # 3. Quá trình Pretrain -> Cột 2: Các mô hình nền tảng
        self.play(GrowArrow(arr_1_2), FadeIn(text_pretrain))
        self.play(FadeIn(col2_bg), Write(title_c2))
        self.play(
            FadeIn(fm_llm, shift=RIGHT*0.5),
            FadeIn(fm_vit, shift=RIGHT*0.5),
            FadeIn(fm_diff, shift=RIGHT*0.5),
            run_time=1.5
        )
        self.next_slide()
        
        # 4. Quá trình sinh -> Cột 3: Các siêu mô hình Video Generation
        self.play(GrowArrow(arr_2_3))
        self.play(FadeIn(col3_bg), Write(title_c3))
        self.play(
            FadeIn(vid_veo, scale=0.8),
            FadeIn(vid_gaia, scale=0.8),
            FadeIn(vid_genie, scale=0.8),
            run_time=1.5
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 59 — MODULE 56: SCALABLE VIDEO GENERATION ARCHITECTURES  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

class Module56_ScalableVideo(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG
        title = slide_title("Scalable Video Generation Architectures")
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: KHỐI TEXT BÊN TRÁI (Neo an toàn bên trái màn hình)
        # ─────────────────────────────────────────────────────────────────────
        def bullet_inline(label, desc):
            l = Text(label + ":", font=Theme.FONT_BODY, font_size=20, color=WHITE, weight="BOLD")
            d = Text(desc, font=Theme.FONT_BODY, font_size=20, color=Theme.DIM)
            return VGroup(l, d).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)

        left_text = VGroup(
            bullet_inline("Video diffusion models", "3D UNet (DiT/latent diffusion)"),
            bullet_inline("Classifier-free guidance", "Text conditioning"),
            bullet_inline("Model cascade", "Temporal and spatial super-resolution"),
            bullet_inline("Image conditioning", "Block-wise autoregressive rollouts")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        # Đưa text sang trái, căn giữa theo chiều dọc
        left_text.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: HÀM TẠO NODE ĐỒ HỌA (Nhỏ gọn, kích thước cố định)
        # ─────────────────────────────────────────────────────────────────────
        def make_grid(rows, cols, size=0.14, fill=Theme.DIM):
            return VGroup(*[
                VGroup(*[
                    Square(side_length=size, fill_color=fill, fill_opacity=1, stroke_color=Theme.NEUTRAL, stroke_width=1)
                    for _ in range(cols)
                ]).arrange(RIGHT, buff=0)
                for _ in range(rows)
            ]).arrange(DOWN, buff=0)

        def z_node(label_str, empty=False):
            if empty:
                # Khung rỗng để đón Feedback
                return Rectangle(width=0.42, height=0.42, fill_color=Theme.BG, fill_opacity=1, stroke_color=Theme.PRIMARY, stroke_width=2)
            grid = make_grid(3, 3, size=0.14, fill=Theme.DIM)
            lbl = MathTex(label_str, font_size=20, color=Theme.NEUTRAL).next_to(grid, LEFT, buff=0.15)
            return VGroup(grid, lbl)

        def act_node(label_str):
            grid = make_grid(3, 1, size=0.14, fill=ManimColor("#9575CD")) # Tím
            lbl = MathTex(label_str, font_size=20, color=Theme.NEUTRAL).next_to(grid, DOWN, buff=0.1)
            return VGroup(grid, lbl)

        def img_node(label_str, pos=UP):
            box = Square(side_length=0.6, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1, stroke_color=Theme.NEUTRAL, stroke_width=1.5)
            icon = MathTex(r"\approx", font_size=24, color=Theme.DIM).move_to(box)
            lbl = MathTex(label_str, font_size=20, color=Theme.NEUTRAL).next_to(box, pos, buff=0.1)
            return VGroup(box, icon, lbl)

        def trapezoid(text, bottom_w, top_w, height, color):
            poly = Polygon(
                [-bottom_w/2, -height/2, 0], [bottom_w/2, -height/2, 0],
                [top_w/2, height/2, 0], [-top_w/2, height/2, 0],
                fill_color=color, fill_opacity=1.0, stroke_color=Theme.NEUTRAL, stroke_width=1.5
            )
            lbl = Text(text, font_size=12, color=WHITE).move_to(poly)
            return VGroup(poly, lbl)

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: HỆ TỌA ĐỘ TUYỆT ĐỐI (Thu hẹp chiều cao trục Y dương phía trên)
        # ─────────────────────────────────────────────────────────────────────
        # Trục Y tĩnh (World Model giữ ở 0.0, nửa trên nén lại dãn khoảng cách tiêu đề)
        y_img_in = -2.5
        y_enc    = -1.6
        y_in     = -0.8
        y_wm     =  0.0   # GIỮ NGUYÊN tọa độ World Model theo yêu cầu
        y_z_out  =  0.7   # Nén từ 1.0 xuống 0.7
        y_dec    =  1.4   # Nén từ 2.0 xuống 1.4
        y_img_out=  2.1   # Nén từ 3.0 xuống 2.1 (Tuyệt đối an toàn trước Title)

        # Trục X tĩnh (Cụm Diagram neo bên Phải)
        cx = 3.6  # Tâm của toàn bộ Diagram
        x1 = cx - 2.0  # Cột t=1 (x = 1.6)
        x2 = cx        # Cột t=2 (x = 3.6)
        x3 = cx + 2.0  # Cột t=3 (x = 5.6)

        # 1. World Model (Rộng 5.5, Cao 0.6)
        wm_box = RoundedRectangle(width=5.8, height=0.6, corner_radius=0.1, fill_color=Theme.PRIMARY, fill_opacity=1.0, stroke_color=Theme.NEUTRAL, stroke_width=2)
        wm_box.set_z_index(2) 
        wm_lbl = Text("World Model", font_size=20, color=WHITE).move_to(wm_box)
        wm_lbl.set_z_index(3)
        wm = VGroup(wm_box, wm_lbl).move_to([cx, y_wm, 0])

        # 2. Các Node tại Cột t=1 (x1)
        x0 = img_node("x_0", DOWN).move_to([x1 - 0.4, y_img_in, 0])
        enc = trapezoid("Encoder", 1.0, 0.5, 0.5, Theme.PRIMARY).move_to([x1 - 0.4, y_enc, 0])
        z0 = z_node("z_0").move_to([x1 - 0.4, y_in, 0])
        a1 = act_node("a_1").move_to([x1 + 0.3, y_in, 0])
        z1 = z_node("z_1").move_to([x1, y_z_out, 0])
        dec1 = trapezoid("Decoder", 0.5, 1.0, 0.5, Theme.PRIMARY).move_to([x1, y_dec, 0])
        x1_out = img_node("x_1", UP).move_to([x1, y_img_out, 0])

        # 3. Các Node tại Cột t=2 (x2)
        z1_in = z_node("", empty=True).move_to([x2 - 0.4, y_in, 0])
        a2 = act_node("a_2").move_to([x2 + 0.3, y_in, 0])
        z2 = z_node("z_2").move_to([x2, y_z_out, 0])
        dec2 = trapezoid("Decoder", 0.5, 1.0, 0.5, Theme.PRIMARY).move_to([x2, y_dec, 0])
        x2_out = img_node("x_2", UP).move_to([x2, y_img_out, 0])

        # 4. Các Node tại Cột t=3 (x3)
        z2_in = z_node("", empty=True).move_to([x3 - 0.4, y_in, 0])
        a3 = act_node("a_3").move_to([x3 + 0.3, y_in, 0])
        z3 = z_node("z_3").move_to([x3, y_z_out, 0])
        dec3 = trapezoid("Decoder", 0.5, 1.0, 0.5, Theme.PRIMARY).move_to([x3, y_dec, 0])
        x3_out = img_node("x_3", UP).move_to([x3, y_img_out, 0])

        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: VẼ MŨI TÊN LIÊN KẾT (Tự động thích ứng toạ độ mới)
        # ─────────────────────────────────────────────────────────────────────
        def straight_arrow(m1, m2, start_pos="top", end_pos="bottom"):
            c1 = m1[0] if isinstance(m1, VGroup) else m1
            c2 = m2[0] if isinstance(m2, VGroup) else m2
            
            p1 = c1.get_top() if start_pos == "top" else [c1.get_center()[0], wm_box.get_top()[1], 0]
            p2 = c2.get_bottom() if end_pos == "bottom" else [c1.get_center()[0], wm_box.get_bottom()[1], 0]
            
            arr = Arrow(p1, p2, buff=0.08, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.1)
            arr.set_z_index(0)
            return arr

        def feedback_arrow(start_x, end_x, z_out_y, in_y, in_box_width):
            p1 = [start_x + 0.25, z_out_y, 0]
            mid_x = (start_x + end_x) / 2
            p2 = [mid_x, z_out_y, 0]
            p3 = [mid_x, in_y, 0]
            p4 = [end_x - 0.4 - in_box_width/2, in_y, 0]

            path = VGroup(
                Line(p1, p2, color=Theme.NEUTRAL, stroke_width=2.5),
                Line(p2, p3, color=Theme.NEUTRAL, stroke_width=2.5),
                Arrow(p3, p4, buff=0.05, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.1)
            )
            path.set_z_index(-1) # Nằm dưới khối World Model
            return path

        arrows = VGroup(
            straight_arrow(x0, enc), straight_arrow(enc, z0),
            straight_arrow(z0, wm, end_pos="wm_bottom"), straight_arrow(a1, wm, end_pos="wm_bottom"),
            straight_arrow(z1_in, wm, end_pos="wm_bottom"), straight_arrow(a2, wm, end_pos="wm_bottom"),
            straight_arrow(z2_in, wm, end_pos="wm_bottom"), straight_arrow(a3, wm, end_pos="wm_bottom"),
            
            straight_arrow(wm, z1, start_pos="wm_top"), straight_arrow(wm, z2, start_pos="wm_top"), straight_arrow(wm, z3, start_pos="wm_top"),
            
            straight_arrow(z1, dec1), straight_arrow(dec1, x1_out),
            straight_arrow(z2, dec2), straight_arrow(dec2, x2_out),
            straight_arrow(z3, dec3), straight_arrow(dec3, x3_out),
            
            feedback_arrow(x1, x2, y_z_out, y_in, 0.42),
            feedback_arrow(x2, x3, y_z_out, y_in, 0.42)
        )

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION)
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        self.play(FadeIn(left_text))
        self.next_slide()
        
        # Step 1: Input t=0 & World Model
        self.play(
            FadeIn(wm), 
            FadeIn(VGroup(x0, enc, z0, a1)),
            Create(arrows[0]), Create(arrows[1]), Create(arrows[2]), Create(arrows[3])
        )
        self.next_slide()
        
        # Step 2: Output t=1
        self.play(
            FadeIn(VGroup(z1, dec1, x1_out)),
            Create(arrows[8]), Create(arrows[11]), Create(arrows[12])
        )
        self.next_slide()
        
        # Step 3: Autoregressive t=1 -> t=2
        self.play(Create(arrows[17]), FadeIn(z1_in)) 
        self.play(FadeIn(a2), Create(arrows[4]), Create(arrows[5]))
        self.play(
            FadeIn(VGroup(z2, dec2, x2_out)),
            Create(arrows[9]), Create(arrows[13]), Create(arrows[14])
        )
        self.next_slide()
        
        # Step 4: Autoregressive t=2 -> t=3
        self.play(Create(arrows[18]), FadeIn(z2_in))
        self.play(FadeIn(a3), Create(arrows[6]), Create(arrows[7]))
        self.play(
            FadeIn(VGroup(z3, dec3, x3_out)),
            Create(arrows[10]), Create(arrows[15]), Create(arrows[16])
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 60 — MODULE 57: PLANNING IN A WORLD MODEL (PERFECTED)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Group

class Module57_PlanningWorldModel(Slide):
    def construct(self):
        self.camera.background_color = Theme.BG
        
        # ─────────────────────────────────────────────────────────────────────
        # 1. TIÊU ĐỀ & SUBTITLE (Khắc phục lỗi dính chữ bằng cách dùng buff thay vì space)
        # ─────────────────────────────────────────────────────────────────────
        title = slide_title("Planning in a World Model")
        
        def make_sub(prefix, text):
            p = Text(prefix, font=Theme.FONT_BODY, font_size=24, color=Theme.DIM, weight="BOLD")
            t = Text(text, font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
            # Dùng buff=0.15 cố định thay vì " " để tránh bị Manim tự động cắt khoảng trắng
            vg = VGroup(p, t).arrange(RIGHT, buff=0.15)
            vg.next_to(title, DOWN, aligned_edge=LEFT, buff=0.3)
            return vg

        sub1 = make_sub("Problem:", "Learning control policies mapping from observation to action")
        sub2 = make_sub("Prior approach:", "Learning one policy for each environment and each robot")
        sub3 = make_sub("Proposal:", "Text-to-video as a universal policy")

        # ─────────────────────────────────────────────────────────────────────
        # 2. HỆ TỌA ĐỘ LƯỚI HOÀN HẢO (CHỐNG TRÀN BIÊN & CHỒNG LÊN CHỮ)
        # ─────────────────────────────────────────────────────────────────────
        Y_TOP = 1.0
        Y_MID = -0.6
        Y_BOT = -2.2
        
        # Nén chặt toạ độ X hơn nữa để giải phóng biên phải cho nhãn "No knowledge sharing"
        X_IN  = -5.4
        X_POL = -2.9
        X_VID = -0.6
        X_INV =  1.6
        X_ROB =  3.8

        # ─────────────────────────────────────────────────────────────────────
        # 3. FACTORY FUNCTIONS (Đã tích hợp khả năng co giãn tự động theo độ dài chữ)
        # ─────────────────────────────────────────────────────────────────────
        def make_input(label, instruct=""):
            lbl = Text(label, font=Theme.FONT_BODY, font_size=18, color=WHITE)
            # Khắc phục lỗi Cloth on Table tràn box: Tự động tính toán chiều rộng hộp
            box_width = max(1.8, lbl.get_width() + 0.4)
            
            box = RoundedRectangle(width=box_width, height=1.2, corner_radius=0.1, fill_color=Theme.BOX_FILL, fill_opacity=1, stroke_color=Theme.DIM, stroke_width=2)
            lbl.move_to(box)
            grp = VGroup(box, lbl)
            
            # Box prompt tự co giãn thông minh cho "Open drawer"
            if instruct:
                p_txt = Text(instruct, font=Theme.FONT_BODY, font_size=14, color=BLACK, weight="BOLD")
                pill_w = max(1.4, p_txt.get_width() + 0.4)
                pill = RoundedRectangle(width=pill_w, height=0.35, corner_radius=0.17, fill_color=WHITE, fill_opacity=0.9, stroke_color=WHITE)
                p_txt.move_to(pill)
                instr_grp = VGroup(pill, p_txt).next_to(box, UP, buff=0.08)
                grp.add(instr_grp)
            return grp

        def make_policy(label, w=1.8, h=1.0):
            box = RoundedRectangle(width=w, height=h, corner_radius=0.2, fill_color=Theme.BG, fill_opacity=1, stroke_color=Theme.NEUTRAL, stroke_width=2)
            txt = Tex(label, font_size=32, color=Theme.NEUTRAL).move_to(box)
            return VGroup(box, txt)

        def make_video(is_top=False):
            box = RoundedRectangle(width=1.8, height=1.3, corner_radius=0.1, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1, stroke_color=Theme.PRIMARY, stroke_width=3)
            play = Polygon([0,0,0], [0,0.3,0], [0.25,0.15,0], fill_color=Theme.DIM, fill_opacity=1, stroke_width=0).move_to(box)
            grp = VGroup(box, play)
            if is_top:
                lbl = Text("Generated video", font=Theme.FONT_BODY, font_size=18, color=Theme.PRIMARY).next_to(box, UP, buff=0.1)
                grp.add(lbl)
            return grp

        def make_inv_dyn(txt1, txt2):
            l1 = Text(txt1, font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL)
            l2 = MathTex(txt2, font_size=24, color=Theme.NEUTRAL)
            return VGroup(l1, l2).arrange(DOWN, buff=0.1)

        def make_robot(txt1, txt2):
            icon = Text("🤖", font="sans-serif", font_size=32)
            l1 = Text(txt1, font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL)
            l2 = MathTex(txt2, font_size=24, color=Theme.NEUTRAL)
            txt_grp = VGroup(l1, l2).arrange(DOWN, buff=0.1)
            return VGroup(icon, txt_grp).arrange(DOWN, buff=0.1)

        def draw_arrow(m1, m2, start_pt=None, end_pt=None):
            p1 = m1.get_right() if start_pt is None else start_pt
            p2 = m2.get_left() if end_pt is None else end_pt
            return Arrow(p1, p2, buff=0.15, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.15)

        # ─────────────────────────────────────────────────────────────────────
        # 4. KHỞI TẠO CÁC OBJECTS (Chưa hiện ra màn hình)
        # ─────────────────────────────────────────────────────────────────────
        in_1 = make_input("Drawer", "Open drawer").move_to([X_IN, Y_TOP, 0])
        in_2 = make_input("Cloth on Table").move_to([X_IN, Y_MID, 0])
        in_3 = make_input("Blocks").move_to([X_IN, Y_BOT, 0])

        pol_1 = make_policy(r"Policy $\pi$").move_to([X_POL, Y_TOP, 0])
        pol_1a = make_policy(r"Policy $\pi_1$").move_to([X_POL, Y_TOP, 0])
        pol_2  = make_policy(r"Policy $\pi_2$").move_to([X_POL, Y_MID, 0])
        pol_3  = make_policy(r"Policy $\pi_3$").move_to([X_POL, Y_BOT, 0])
        
        giant_pol = make_policy(r"Policy $\pi$", w=2.0, h=3.8).move_to([X_POL, Y_MID, 0])

        vid_1 = make_video(is_top=True).move_to([X_VID, Y_TOP, 0])
        vid_2 = make_video().move_to([X_VID, Y_MID, 0])
        vid_3 = make_video().move_to([X_VID, Y_BOT, 0])

        inv_1_scene3 = make_inv_dyn("Inverse dynamics", r"f(\cdot|\mathbf{x})").move_to([X_INV, Y_TOP, 0])
        inv_1 = make_inv_dyn("Inverse dynamics", r"f_1(\cdot|\mathbf{x})").move_to([X_INV, Y_TOP, 0])
        inv_2 = make_inv_dyn("Optical flow", r"f_2(\cdot|\mathbf{x})").move_to([X_INV, Y_MID, 0])
        inv_3 = make_inv_dyn("Goal-conditioned", r"f_3(\cdot|\mathbf{x})").move_to([X_INV, Y_BOT, 0])

        rob_1 = make_robot("Robot control", r"\Delta x, \Delta y").move_to([X_ROB, Y_TOP, 0])
        rob_2 = make_robot("Arm joint control", r"\Delta \omega, \Delta \alpha").move_to([X_ROB, Y_MID, 0])
        rob_3 = make_robot("End-effector", r"\Delta a, \Delta b").move_to([X_ROB, Y_BOT, 0])

        # Đã kéo lùi trục X của robot sang trái, nhãn "No knowledge sharing" nay nằm an toàn trong màn hình
        no_share = Text("No knowledge\nsharing", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED, weight="BOLD")
        no_share.next_to(rob_2, RIGHT, buff=0.4)

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN CHUYỂN CẢNH (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        
        # --- SCENE 1 ---
        self.play(FadeIn(sub1))
        
        arr_in1_pol1 = draw_arrow(in_1, pol_1)
        arr_pol1_rob1 = draw_arrow(pol_1, rob_1)
        
        self.play(
            FadeIn(in_1), FadeIn(pol_1), FadeIn(rob_1),
            Create(arr_in1_pol1), Create(arr_pol1_rob1)
        )
        self.next_slide()

        # --- SCENE 2 ---
        self.play(ReplacementTransform(sub1, sub2))
        
        self.play(ReplacementTransform(pol_1, pol_1a))
        arr_in1_pol1a = draw_arrow(in_1, pol_1a)
        arr_pol1a_rob1 = draw_arrow(pol_1a, rob_1)
        self.add(arr_in1_pol1a, arr_pol1a_rob1)
        self.remove(arr_in1_pol1, arr_pol1_rob1)

        arr_in2_pol2 = draw_arrow(in_2, pol_2)
        arr_pol2_rob2 = draw_arrow(pol_2, rob_2)
        arr_in3_pol3 = draw_arrow(in_3, pol_3)
        arr_pol3_rob3 = draw_arrow(pol_3, rob_3)

        self.play(
            FadeIn(in_2), FadeIn(pol_2), FadeIn(rob_2), Create(arr_in2_pol2), Create(arr_pol2_rob2),
            FadeIn(in_3), FadeIn(pol_3), FadeIn(rob_3), Create(arr_in3_pol3), Create(arr_pol3_rob3)
        )
        self.play(FadeIn(no_share))
        self.next_slide()

        # --- SCENE 3 ---
        self.play(ReplacementTransform(sub2, sub3))
        
        self.play(
            FadeOut(in_2), FadeOut(pol_2), FadeOut(rob_2), FadeOut(arr_in2_pol2), FadeOut(arr_pol2_rob2),
            FadeOut(in_3), FadeOut(pol_3), FadeOut(rob_3), FadeOut(arr_in3_pol3), FadeOut(arr_pol3_rob3),
            FadeOut(no_share), FadeOut(arr_pol1a_rob1)
        )
        
        self.play(ReplacementTransform(pol_1a, pol_1))
        self.add(arr_in1_pol1)
        self.remove(arr_in1_pol1a)

        arr_pol1_vid1 = draw_arrow(pol_1, vid_1)
        arr_vid1_inv1_s3 = draw_arrow(vid_1, inv_1_scene3)
        arr_inv1_rob1_s3 = draw_arrow(inv_1_scene3, rob_1)

        self.play(
            FadeIn(vid_1), FadeIn(inv_1_scene3),
            Create(arr_pol1_vid1), Create(arr_vid1_inv1_s3), Create(arr_inv1_rob1_s3)
        )
        self.next_slide()

        # --- SCENE 4 ---
        self.play(FadeIn(in_2), FadeIn(in_3))
        
        self.play(
            ReplacementTransform(pol_1, giant_pol),
            FadeOut(arr_in1_pol1), FadeOut(arr_pol1_vid1), 
            ReplacementTransform(inv_1_scene3, inv_1) 
        )

        def arrow_to_giant(inp, y): return draw_arrow(inp, giant_pol, end_pt=[giant_pol.get_left()[0], y, 0])
        def arrow_from_giant(vid, y): return draw_arrow(giant_pol, vid, start_pt=[giant_pol.get_right()[0], y, 0])

        arr_in1_g = arrow_to_giant(in_1, Y_TOP)
        arr_in2_g = arrow_to_giant(in_2, Y_MID)
        arr_in3_g = arrow_to_giant(in_3, Y_BOT)

        arr_g_vid1 = arrow_from_giant(vid_1, Y_TOP)
        arr_g_vid2 = arrow_from_giant(vid_2, Y_MID)
        arr_g_vid3 = arrow_from_giant(vid_3, Y_BOT)

        arr_vid2_inv2 = draw_arrow(vid_2, inv_2)
        arr_inv2_rob2 = draw_arrow(inv_2, rob_2)
        arr_vid3_inv3 = draw_arrow(vid_3, inv_3)
        arr_inv3_rob3 = draw_arrow(inv_3, rob_3)

        arr_vid1_inv1 = draw_arrow(vid_1, inv_1)
        arr_inv1_rob1 = draw_arrow(inv_1, rob_1)

        self.play(
            Create(arr_in1_g), Create(arr_in2_g), Create(arr_in3_g),
            Create(arr_g_vid1),
            FadeIn(vid_2), FadeIn(vid_3), Create(arr_g_vid2), Create(arr_g_vid3),
            FadeIn(inv_2), FadeIn(rob_2), Create(arr_vid2_inv2), Create(arr_inv2_rob2),
            FadeIn(inv_3), FadeIn(rob_3), Create(arr_vid3_inv3), Create(arr_inv3_rob3),
            Transform(arr_vid1_inv1_s3, arr_vid1_inv1),
            Transform(arr_inv1_rob1_s3, arr_inv1_rob1)
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 61 — MODULE 58: EVALUATING POLICIES IN A WORLD MODEL  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Arc

class Module58_PolicyEvaluation(Slide):
    def construct(self):
        # 1. Thiết lập nền slide
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề và Subtitle (Ghim góc trái, an toàn tuyệt đối)
        title = slide_title("Evaluating Policies in a World Model")
        subtitle = Text(
            "How good is a world model for policy evaluation?",
            font=Theme.FONT_BODY,
            font_size=28,
            color=Theme.DIM
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.2)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG TRỤC CHUẨN - DẢI KHUNG HÌNH (ROLLOUT FRAMES)
        # ─────────────────────────────────────────────────────────────────────
        def create_frames_grid(stroke_color):
            """Hàm tiện ích tạo một dải các ô vuông đại diện cho video frames."""
            frames = VGroup(*[
                RoundedRectangle(
                    corner_radius=0.05, width=0.6, height=0.6,
                    fill_color=Theme.BOX_FILL, fill_opacity=1,
                    stroke_color=Theme.DIM, stroke_width=1.5
                ) for _ in range(5)
            ]).arrange(RIGHT, buff=0.08)
            
            border = Rectangle(
                width=frames.width + 0.2,
                height=frames.height + 0.2,
                stroke_color=stroke_color,
                stroke_width=3,
                fill_opacity=0
            )
            border.move_to(frames.get_center())
            return VGroup(border, frames)
            
        gt_frames = create_frames_grid(Theme.ACCENT_RED)
        wm_frames = create_frames_grid(Theme.PRIMARY)
        
        # Xếp dải Ground Truth ở trên, World Model ở dưới
        wm_frames.next_to(gt_frames, DOWN, buff=0.8)
        
        # Gắn nhãn cho các dải khung hình
        gt_label = Text("Ground truth rollout", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED, weight="BOLD")
        gt_label.next_to(gt_frames, UP, buff=0.15)
        
        wm_label = Text("Generated rollout", font=Theme.FONT_BODY, font_size=20, color=Theme.PRIMARY, weight="BOLD")
        wm_label.next_to(wm_frames, DOWN, buff=0.15)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: NEO CÁC KHỐI BÊN TRÁI (ENVIRONMENTS & POLICY LOOP)
        # ─────────────────────────────────────────────────────────────────────
        gt_env = RoundedBox(
            lines=["Ground", "truth env"], 
            width=2.2, height=1.2, 
            fill_color=Theme.BOX_FILL, stroke_color=Theme.NEUTRAL
        )
        gt_env.next_to(gt_frames, LEFT, buff=0.8)
        
        wm_env = RoundedBox(
            lines=["World", "model"], 
            width=2.2, height=1.2, 
            fill_color=ManimColor("#1A3B5C"), stroke_color=Theme.PRIMARY # Màu xanh dương sẫm
        )
        wm_env.next_to(wm_frames, LEFT, buff=0.8)
        wm_env.align_to(gt_env, LEFT) # Gióng lề trái cho cẩn thận
        
        # Cụm biểu tượng vòng lặp Rollout Pi
        rollout_text = VGroup(
            Text("Rollout", font=Theme.FONT_BODY, font_size=22, color=Theme.NEUTRAL, weight="BOLD"),
            MathTex(r"\pi", font_size=32, color=Theme.NEUTRAL)
        ).arrange(RIGHT, buff=0.1)
        
        # Vòng lặp mũi tên kép (Double arc loop)
        arc1 = Arc(radius=0.25, start_angle=PI/4, angle=PI*0.8, color=Theme.NEUTRAL, stroke_width=3).add_tip(tip_length=0.12)
        arc2 = Arc(radius=0.25, start_angle=PI*1.25, angle=PI*0.8, color=Theme.NEUTRAL, stroke_width=3).add_tip(tip_length=0.12)
        loop_icon = VGroup(arc1, arc2)
        
        rollout_group = VGroup(rollout_text, loop_icon).arrange(RIGHT, buff=0.25)
        rollout_group.next_to(VGroup(gt_env, wm_env), LEFT, buff=0.6)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: NEO CÁC KHỐI BÊN PHẢI (OUTCOMES & EVALUATION)
        # ─────────────────────────────────────────────────────────────────────
        gt_success = Text("Ground truth task success", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL)
        gt_success.next_to(gt_frames, RIGHT, buff=0.8)
        
        # Nhóm đánh giá của World Model (VLM + Text)
        vlm_box = RoundedBox(
            lines=["VLM", "reward"], 
            width=1.6, height=0.9, 
            fill_color=ManimColor("#8F5902"), stroke_color=Theme.ACCENT_GOLD, font_size=18
        )
        pred_success = Text("Predicted task success", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL)
        
        wm_outcome = VGroup(vlm_box, pred_success).arrange(RIGHT, buff=0.6)
        wm_outcome.next_to(wm_frames, RIGHT, buff=0.8)
        
        # Gióng hàng khối đánh giá (GT Success & WM Outcome)
        # gt_success.align_to(wm_outcome, LEFT)
        
        # Ngoặc ôm (Brace) để đối chiếu "Agree?"
        outcomes_group = VGroup(gt_success, wm_outcome)
        brace = Brace(outcomes_group, direction=RIGHT, color=Theme.NEUTRAL, buff=0.3)
        agree_text = Text("Agree?", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL, weight="BOLD")
        agree_text.next_to(brace, RIGHT, buff=0.2)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: GOM NHÓM & SCALE AN TOÀN (TRÁNH TRÀN VIỀN)
        # ─────────────────────────────────────────────────────────────────────
        all_flow = VGroup(
            rollout_group, gt_env, wm_env, 
            gt_frames, wm_frames, gt_label, wm_label,
            gt_success, wm_outcome, brace, agree_text
        )
        all_flow.set_width(13.2) # Ép khung bảo vệ tránh Error 2
        all_flow.center().shift(DOWN * 0.2) # Hạ xuống một chút chừa chỗ cho Title/Subtitle
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 5: KHỞI TẠO MŨI TÊN (SAU KHI ĐÃ CỐ ĐỊNH TỌA ĐỘ)
        # ─────────────────────────────────────────────────────────────────────
        arr_gt_env_fr = Arrow(gt_env.get_right(), gt_frames.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.12)
        arr_wm_env_fr = Arrow(wm_env.get_right(), wm_frames.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.12)
        
        arr_gt_fr_succ = Arrow(gt_frames.get_right(), gt_success.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.12)
        arr_wm_fr_vlm = Arrow(wm_frames.get_right(), vlm_box.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.12)
        arr_vlm_pred = Arrow(vlm_box.get_right(), pred_success.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.12)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        # 1. Hiển thị Tiêu đề
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.next_slide()
        
        # 2. Hiển thị Policy Rollout Loop và 2 Môi trường đầu vào
        self.play(FadeIn(rollout_group))
        self.play(FadeIn(gt_env), FadeIn(wm_env))
        self.next_slide()
        
        # 3. Hiển thị nhánh Ground Truth (Trên)
        self.play(Create(arr_gt_env_fr), FadeIn(gt_frames), FadeIn(gt_label))
        self.play(Create(arr_gt_fr_succ), FadeIn(gt_success))
        self.next_slide()
        
        # 4. Hiển thị nhánh World Model sinh ra chuỗi hành động (Dưới)
        self.play(Create(arr_wm_env_fr), FadeIn(wm_frames), FadeIn(wm_label))
        self.next_slide()
        
        # 5. Dùng VLM để đánh giá Reward từ World Model Rollout
        self.play(Create(arr_wm_fr_vlm), FadeIn(vlm_box))
        self.play(Create(arr_vlm_pred), FadeIn(pred_success))
        self.next_slide()
        
        # 6. Đặt câu hỏi so sánh (Agree?)
        self.play(Create(brace), Write(agree_text))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 62 — MODULE 59: IMPROVE POLICIES IN A WORLD MODEL  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Arc, CurvedArrow

class Module59_PolicyImprovement(Slide):
    def construct(self):
        # 1. Nền slide
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề và Subtitle (Ghim cứng góc trên bên trái)
        title = slide_title("Improve Policies in a World Model")
        subtitle = Text(
            "Running RL (policy gradient) using rollouts from the world model",
            font=Theme.FONT_BODY,
            font_size=28,
            color=Theme.DIM
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.2)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: TẠO BẢNG CHUẨN XÁC ROW-BY-ROW (SỬA LỆCH CỘT VALUE)
        # ─────────────────────────────────────────────────────────────────────
        # Cột trái (Gồm 1 ô ẩn làm spacer giúp gióng lề cột phải tuyệt đối)
        cell_00 = Text("UniSim-RL", font_size=18, fill_opacity=0, stroke_opacity=0)
        cell_10 = Text("VLA-BC", font_size=18, color=Theme.NEUTRAL)
        cell_20 = Text("UniSim-RL", font_size=18, color=Theme.NEUTRAL)
        col_left = VGroup(cell_00, cell_10, cell_20).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        # Cột phải
        cell_01 = Text("Succ. rate (all)", font_size=18, color=Theme.NEUTRAL)
        cell_11 = Text("0.58", font_size=18, color=Theme.NEUTRAL)
        cell_21 = Text("0.81", font_size=18, weight="BOLD", color=Theme.NEUTRAL)

        # Khóa DUY NHẤT một tọa độ X cho cột phải để đảm bảo thẳng hàng tuyệt đối
        right_column_x = col_left.get_right()[0] + 1.2
        cell_01.move_to([right_column_x, cell_00.get_center()[1], 0])
        cell_11.move_to([right_column_x, cell_10.get_center()[1], 0])
        cell_21.move_to([right_column_x, cell_20.get_center()[1], 0])
        
        col_right = VGroup(cell_01, cell_11, cell_21)

        # Vẽ đường kẻ bảng căn theo biên hình học của các cell
        x_left = col_left.get_left()[0] - 0.2
        x_right = col_right.get_right()[0] + 0.2
        
        # Đường kẻ ngang 1 (Giữa Header và Row 1)
        y_mid1 = (cell_00.get_bottom()[1] + cell_10.get_top()[1]) / 2
        hline1 = Line([x_left, y_mid1, 0], [x_right, y_mid1, 0], color=Theme.NEUTRAL, stroke_width=1.5)
        
        # Đường kẻ ngang 2 (Dưới đáy bảng)
        y_bottom = cell_20.get_bottom()[1] - 0.12
        hline2 = Line([x_left, y_bottom, 0], [x_right, y_bottom, 0], color=Theme.NEUTRAL, stroke_width=1.5)
        
        # Đường dọc phân chia cột
        x_mid = (col_left.get_right()[0] + col_right.get_left()[0]) / 2
        y_top = cell_01.get_top()[1] + 0.12
        vline = Line([x_mid, y_top, 0], [x_mid, y_bottom, 0], color=Theme.NEUTRAL, stroke_width=1.5)
        
        table_group = VGroup(col_left, col_right, hline1, hline2, vline)
        table_group.next_to(subtitle, DOWN, aligned_edge=LEFT, buff=0.4)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG TRỤC SƠ ĐỒ ĐƯỜNG THẲNG (BOTTOM SPINE)
        # ─────────────────────────────────────────────────────────────────────
        
        # 2.1. Cụm Rollout
        rollout_txt = Text("Rollout", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL)
        pi_txt = MathTex(r"\pi", font_size=32, color=Theme.NEUTRAL)
        rollout_label = VGroup(rollout_txt, pi_txt).arrange(RIGHT, buff=0.15)

        arc1 = Arc(radius=0.3, start_angle=PI/4, angle=PI*0.8, color=Theme.NEUTRAL, stroke_width=3).add_tip(tip_length=0.15)
        arc2 = Arc(radius=0.3, start_angle=PI*1.25, angle=PI*0.8, color=Theme.NEUTRAL, stroke_width=3).add_tip(tip_length=0.15)
        a_label = MathTex("a", font_size=28, color=Theme.NEUTRAL).next_to(arc1, UP, buff=0.05)
        loop_icon = VGroup(arc1, arc2, a_label)
        
        rollout_full = VGroup(rollout_label, loop_icon).arrange(RIGHT, buff=0.25)
        
        # 2.2. Hộp World Model
        wm_box = RoundedBox(
            lines=["World", "model"], 
            width=2.2, height=1.2, 
            fill_color=ManimColor("#8BAEE0"), stroke_color=ManimColor("#1C3A70"), 
            text_color=BLACK 
        )
        wm_box.label[0].set_color(BLACK)
        wm_box.label[1].set_color(BLACK)
        
        # 2.3. Lưới các cấu hình (Generated Rollouts Grid)
        def create_image_grid():
            grid = VGroup()
            for _ in range(3): 
                row = VGroup(*[
                    Rectangle(width=1.0, height=0.6, fill_color=Theme.BOX_FILL_ALT, fill_opacity=1, stroke_color=Theme.DIM, stroke_width=1.5)
                    for _ in range(4) 
                ]).arrange(RIGHT, buff=0.05)
                grid.add(row)
            return grid.arrange(DOWN, buff=0.05)
            
        frames_grid = create_image_grid()
        
        # 2.4. Hộp VLM Reward
        vlm_box = RoundedBox(
            lines=["VLM", "reward"], 
            width=1.8, height=1.2, 
            fill_color=ManimColor("#F5C68A"), stroke_color=ManimColor("#915000"), 
            text_color=BLACK
        )
        vlm_box.label[0].set_color(BLACK)
        vlm_box.label[1].set_color(BLACK)
        
        # 2.5. Kết quả Reward R
        reward_r = MathTex("R", font_size=42, color=Theme.NEUTRAL)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: SẮP XẾP SƠ ĐỒ VÀ ÉP KHUNG AN TOÀN TRÁNH TRÀN VIỀN
        # ─────────────────────────────────────────────────────────────────────
        flow_spine = VGroup(rollout_full, wm_box, frames_grid, vlm_box, reward_r).arrange(RIGHT, buff=0.6)
        flow_spine.set_width(13.0) 
        flow_spine.to_edge(DOWN, buff=0.6) 
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: VẼ MŨI TÊN LIÊN KẾT & CÔNG THỨC (KHẮC PHỤC MŨI TÊN CONG)
        # ─────────────────────────────────────────────────────────────────────
        
        # Mũi tên thẳng trong luồng Forward
        arr_to_wm = Arrow(rollout_full.get_right(), wm_box.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15)
        arr_to_grid = Arrow(wm_box.get_right(), frames_grid.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15)
        arr_to_vlm = Arrow(frames_grid.get_right(), vlm_box.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15)
        arr_to_r = Arrow(vlm_box.get_right(), reward_r.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3, tip_length=0.15)
        
        # Mũi tên cong khổng lồ cho Feedback Loop (Góc dương angle=1.1 đưa cung vồng lên trên chuẩn xác)
        feedback_loop = CurvedArrow(
            start_point=reward_r.get_top() + UP * 0.1,
            end_point=rollout_full.get_top() + UP * 0.1 + RIGHT * 0.2, 
            angle=1.1, 
            color=Theme.NEUTRAL,
            stroke_width=3,
            tip_length=0.2
        )
        
        # Công thức Policy Gradient đặt dưới đỉnh cao nhất của vòng cung đối xứng
        formula = MathTex(r"\nabla_\theta \pi_\theta(a|s)R", font_size=42, color=Theme.NEUTRAL)
        mid_x = (reward_r.get_center()[0] + rollout_full.get_center()[0]) / 2
        formula.move_to([mid_x, flow_spine.get_top()[1] + 1.25, 0])
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.play(FadeIn(table_group))
        self.next_slide()
        
        self.play(FadeIn(rollout_full))
        self.next_slide()
        
        self.play(Create(arr_to_wm), FadeIn(wm_box))
        self.play(Create(arr_to_grid), FadeIn(frames_grid))
        self.next_slide()
        
        self.play(Create(arr_to_vlm), FadeIn(vlm_box))
        self.play(Create(arr_to_r), FadeIn(reward_r))
        self.next_slide()
        
        self.play(Create(feedback_loop), run_time=1.5)
        self.play(Write(formula))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 63 — MODULE 60: IMPROVING A WORLD MODEL WITH FEEDBACK  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Circle, CurvedArrow

class Module60_SelfImproving(Slide):
    def construct(self):
        # 1. Thiết lập màu nền slide
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề slide (Ghim sát góc trên bên trái)
        title = slide_title("Improving a World Model with Feedback")
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: KHỞI TẠO CÁC KHỐI NODE CHÍNH (ĐỊNH VỊ TƯƠNG ĐỐI)
        # ─────────────────────────────────────────────────────────────────────
        
        wm_box = RoundedBox(
            lines=["World model"], 
            width=2.4, height=1.2, 
            fill_color=ManimColor("#C2D2ED"), stroke_color=ManimColor("#1C3A70"), 
            text_color=BLACK
        )
        
        vlm_box = RoundedBox(
            lines=["VLM", "reward"], 
            width=1.8, height=1.2, 
            fill_color=ManimColor("#FCE487"), stroke_color=ManimColor("#D4A017"), 
            text_color=BLACK
        )
        
        # Tạo khối môi trường (Trái Đất)
        env_circle = Circle(radius=0.9, fill_color=ManimColor("#2C4B7E"), fill_opacity=1, stroke_color=Theme.PRIMARY)
        env_lbl = Text("Real World\nEnvironment", font=Theme.FONT_BODY, font_size=18, color=WHITE).move_to(env_circle)
        env_node = VGroup(env_circle, env_lbl)
        
        # Khối Video giả lập (Generated Video)
        gen_vid = RoundedBox(
            lines=["Generated video", "[Rollouts]"], 
            width=2.4, height=1.0, 
            fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY
        )
        gen_lbl = Text("Generated video", font=Theme.FONT_BODY, font_size=20, color=Theme.PRIMARY)
        gen_group = VGroup(gen_vid, gen_lbl).arrange(UP, buff=0.15)
        
        # Khối Video thực thi thật (Real-world execution)
        real_vid = RoundedBox(
            lines=["Real-world", "execution"], 
            width=2.4, height=1.0, 
            fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.ACCENT_RED
        )
        real_lbl = Text("Real-world execution", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED)
        real_group = VGroup(real_vid, real_lbl).arrange(DOWN, buff=0.15)
        
        # Thiết lập khoảng cách gióng ngang chuẩn cho 3 cột chính
        vlm_box.next_to(wm_box, RIGHT, buff=2.8)
        env_node.next_to(vlm_box, RIGHT, buff=2.5)
        
        # Đưa các khối video lên/xuống theo lề dọc của các trục
        gen_group.next_to(wm_box, RIGHT, buff=0.4).shift(UP * 1.5)
        real_group.next_to(env_node, DOWN, buff=0.6).shift(LEFT * 1.5)
        
        # Nhóm tất cả các hộp mốc để chuẩn bị dựng liên kết
        all_nodes = VGroup(wm_box, vlm_box, env_node, gen_group, real_group)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: KHỞI TẠO ĐƯỜNG CONG LIÊN KẾT CHUẨN XÁC (TRÁNH LỆCH HƯỚNG)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- LUỒNG NGOÀI (OUTER LOOP - THỰC TẾ) ---
        # 1. World Model -> Env: Đi từ Trái sang Phải. Góc âm (angle < 0) phình cong LÊN TRÊN.
        arc_top = CurvedArrow(
            wm_box.get_top() + RIGHT * 0.1, 
            env_node.get_top() + LEFT * 0.1, 
            angle=-1.3, 
            color=Theme.NEUTRAL, stroke_width=3
        )
        
        # Gắn nhãn Robot Control ngay trên đỉnh đường cong lớn (Tuyệt đối không bị che khuất)
        robot_txt = Text("Robot control", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL, weight="BOLD")
        robot_math = MathTex(r"\Delta x, \Delta y", font_size=24, color=Theme.NEUTRAL)
        robot_group = VGroup(robot_txt, robot_math).arrange(DOWN, buff=0.1)
        robot_group.next_to(arc_top.point_from_proportion(0.5), UP, buff=0.15)
        
        # 2. Env -> Real Video
        arr_env_real = Arrow(env_node.get_bottom(), real_vid.get_right(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3)
        
        # 3. Real Video -> World Model: Đi từ Phải sang Trái. Góc âm (angle < 0) phình cong XUỐNG DƯỚI.
        arr_real_wm = CurvedArrow(
            real_vid.get_left(), 
            wm_box.get_bottom() + RIGHT * 0.1, 
            angle=-0.9, 
            color=Theme.NEUTRAL, stroke_width=3
        )
        fb_outer_txt = Text("Feedback and\nmore data", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL)
        fb_outer_txt.next_to(arr_real_wm.point_from_proportion(0.5), DOWN, buff=0.15)
        
        # --- LUỒNG TRONG (INNER LOOP - MÔ PHỎNG) ---
        # World Model -> Gen Video
        arr_wm_gen = Arrow(wm_box.get_top(), gen_vid.get_left(), buff=0.1, color=Theme.NEUTRAL, stroke_width=3)
        
        # Gen Video -> VLM (Dashed)
        arr_gen_vlm = DashedLine(gen_vid.get_right(), vlm_box.get_top(), dash_length=0.1, color=Theme.NEUTRAL).add_tip(tip_length=0.15)
        
        # VLM -> World Model: Đi từ Phải sang Trái. Góc âm (angle < 0) phình cong nhẹ XUỐNG DƯỚI.
        arr_vlm_wm = CurvedArrow(
            vlm_box.get_left(), 
            wm_box.get_right() + DOWN * 0.1, 
            angle=-0.9, 
            color=Theme.DIM, stroke_width=2.5
        )
        fb_inner_txt = Text("Feedback", font=Theme.FONT_BODY, font_size=18, color=Theme.NEUTRAL)
        fb_inner_txt.next_to(arr_vlm_wm.point_from_proportion(0.5), DOWN, buff=0.1)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM NHÓM & KHỐNG CHẾ CHIỀU CAO TỔNG THỂ TRÁNH TRÀN BIÊN
        # ─────────────────────────────────────────────────────────────────────
        master_diagram = VGroup(
            all_nodes, arc_top, robot_group, 
            arr_env_real, arr_real_wm, fb_outer_txt,
            arr_wm_gen, arr_gen_vlm, arr_vlm_wm, fb_inner_txt
        )
        
        # Khống chế chiều cao tổng thể nghiêm ngặt (5.5 / 8.0) để bảo vệ lề trên/dưới slide
        master_diagram.set_height(5.5)
        master_diagram.center().shift(DOWN * 0.2)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        # 1. Hiện tiêu đề chính và hai khối đầu-cuối
        self.play(Write(title))
        self.play(FadeIn(wm_box), FadeIn(env_node))
        self.next_slide()
        
        # 2. Vòng lặp ngoài (Outer Loop): Phát lệnh robot và thực thi thế giới thực
        self.play(Create(arc_top))
        self.play(FadeIn(robot_group))
        self.next_slide()
        
        # 3. Thu thập dữ liệu thực tế và đẩy ngược về tối ưu hoá World Model
        self.play(Create(arr_env_real), FadeIn(real_group))
        self.play(Create(arr_real_wm), FadeIn(fb_outer_txt))
        self.next_slide()
        
        # 4. Vòng lặp trong (Inner Loop): Tự tưởng tượng rollouts ảo trong World Model
        self.play(Create(arr_wm_gen), FadeIn(gen_group))
        self.next_slide()
        
        # 5. Phản hồi nội bộ: Chấm điểm bằng VLM và tự cập nhật liên tục
        self.play(Create(arr_gen_vlm), FadeIn(vlm_box))
        self.play(Create(arr_vlm_wm), FadeIn(fb_inner_txt))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 64 — MODULE 61: DISCRETE TO CONTINUOUS DIFFUSION  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import interpolate_color

class Module61_DiscreteToContinuous(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: TIÊU ĐỀ VÀ PHỤ ĐỀ (TITLE & SUBTITLE)
        # ─────────────────────────────────────────────────────────────────────
        # Khởi tạo Tiêu đề/Phụ đề cho Scene 1 (Discrete)
        title_d = slide_title("Discrete-Time Diffusion Models")
        subtitle_d = Text(
            "• Formal definition of forward and reverse processes in T steps:", 
            font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL
        )
        subtitle_d.next_to(title_d, DOWN, aligned_edge=LEFT, buff=0.3)

        # Khởi tạo Tiêu đề/Phụ đề cho Scene 2 (Continuous)
        title_c = slide_title("Continuous-Time Diffusion Models")
        subtitle_c = Text(
            "• Formal definition of forward and reverse processes in infinite steps:", 
            font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL
        )
        subtitle_c.next_to(title_c, DOWN, aligned_edge=LEFT, buff=0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: TRỤC TRỰC QUAN TRUNG TÂM (CENTRAL VISUAL SEQUENCE)
        # ─────────────────────────────────────────────────────────────────────
        # Dãy 7 ô vuông chuyển tiếp màu từ Ảnh (Accent Gold) sang Nhiễu (Dim/Gray)
        squares = VGroup(*[
            Square(
                side_length=1.2, 
                fill_color=interpolate_color(Theme.ACCENT_GOLD, Theme.DIM, i/6.0),
                fill_opacity=1,
                stroke_width=0
            ) for i in range(7)
        ]).arrange(RIGHT, buff=0.1)
        
        data_lbl = Text("Data", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL).next_to(squares, LEFT, buff=0.5)
        noise_lbl = Text("Noise", font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL).next_to(squares, RIGHT, buff=0.5)
        
        # Mũi tên và Nhãn cho Forward Process (Nằm trên)
        fwd_arr = Arrow(
            squares.get_corner(UL) + UP*0.15, squares.get_corner(UR) + UP*0.15, 
            buff=0, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.15
        )
        fwd_txt = Text("Forward diffusion process (fixed)", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL)
        fwd_txt.next_to(fwd_arr, UP, buff=0.15)
        
        # Mũi tên và Nhãn cho Reverse Process (Nằm dưới)
        rev_arr = Arrow(
            squares.get_corner(DR) + DOWN*0.15, squares.get_corner(DL) + DOWN*0.15, 
            buff=0, color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.15
        )
        rev_txt = Text("Reverse denoising process (generative)", font=Theme.FONT_BODY, font_size=20, color=Theme.NEUTRAL)
        rev_txt.next_to(rev_arr, DOWN, buff=0.15)

        # Trục hình ảnh cố định (Xài chung cho cả 2 Scene)
        center_seq = VGroup(data_lbl, squares, noise_lbl, fwd_arr, fwd_txt, rev_arr, rev_txt)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: ĐỊNH NGHĨA PHƯƠNG TRÌNH & ĐỊNH VỊ TƯƠNG ĐỐI
        # ─────────────────────────────────────────────────────────────────────
        # --- THÀNH PHẦN DISCRETE ---
        math_d_fwd = MathTex(
            r"q(\mathbf{x}_{1:T}|\mathbf{x}_0) = \prod_{t \ge 1} q(\mathbf{x}_t|\mathbf{x}_{t-1}), \quad q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t\mathbf{I})",
            font_size=32, color=Theme.NEUTRAL
        )
        math_d_rev = MathTex(
            r"p_\theta(\mathbf{x}_{0:T}) = p(\mathbf{x}_T) \prod_{t \ge 1} p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t), \quad p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; ",
            r"\mu_\theta(\mathbf{x}_t, t)", 
            r", \sigma_t^2\mathbf{I})",
            font_size=32, color=Theme.NEUTRAL
        )
        
        # Căn chỉnh Discrete tương đối với trục giữa
        math_d_fwd.next_to(fwd_txt, UP, buff=0.5)
        math_d_rev.next_to(rev_txt, DOWN, buff=0.5)
        
        # --- THÀNH PHẦN CONTINUOUS ---
        math_c_fwd = MathTex(
            r"d\mathbf{x} = -\frac{1}{2}\beta(t)\mathbf{x} dt + \sqrt{\beta(t)} d\mathbf{w}",
            font_size=38, color=Theme.NEUTRAL
        )
        math_c_rev = MathTex(
            r"d\mathbf{x} = -\frac{1}{2}\beta(t)(\mathbf{x} + 2",
            r"\nabla_{\mathbf{x}} \log p_t(\mathbf{x})",
            r") dt + \sqrt{\beta(t)} d\mathbf{w}",
            font_size=38, color=Theme.NEUTRAL
        )
        
        # Căn chỉnh Continuous trùng khớp với vị trí của Discrete
        math_c_fwd.move_to(math_d_fwd, aligned_edge=DOWN)
        math_c_rev.move_to(math_d_rev, aligned_edge=UP)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: GHÉP KHUNG CHÍNH VÀ NEO CHẶT DƯỚI PHỤ ĐỀ (CHỐNG OVERLAP)
        # ─────────────────────────────────────────────────────────────────────
        main_layout = VGroup(
            center_seq, 
            math_d_fwd, math_d_rev,
            math_c_fwd, math_c_rev
        )
        
        # Khống chế chiều cao sơ đồ
        main_layout.set_height(4.8)
        
        # NEO TUYỆT ĐỐI dưới subtitle_d để bảo đảm không bao giờ bị đè chữ ở trên
        main_layout.next_to(subtitle_d, DOWN, buff=0.4)
        
        # Căn giữa sơ đồ theo phương ngang
        main_layout.set_x(0)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 5: TẠO NGOẶC NHỌN (BRACES) CHO PHƯƠNG TRÌNH DƯỚI ĐÁY
        # ─────────────────────────────────────────────────────────────────────
        brace_d = Brace(math_d_rev[1], DOWN, buff=0.12, color=Theme.DIM)
        brace_txt_d = Text(
            "Trainable network (U-net, Denoising Autoencoder)", 
            font=Theme.FONT_BODY, font_size=15, color=Theme.NEUTRAL
        ).next_to(brace_d, DOWN, buff=0.08)
        
        brace_c = Brace(math_c_rev[1], DOWN, buff=0.12, color=Theme.DIM)
        brace_txt_c = Text(
            "Score function (U-net)", 
            font=Theme.FONT_BODY, font_size=15, color=Theme.NEUTRAL
        ).next_to(brace_c, DOWN, buff=0.08)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ (ANIMATION STEPS)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- SCENE 1: DISCRETE-TIME DIFFUSION ---
        self.play(Write(title_d), FadeIn(subtitle_d))
        self.play(
            FadeIn(center_seq),
            FadeIn(math_d_fwd)
        )
        self.play(
            FadeIn(math_d_rev),
            GrowFromCenter(brace_d),
            FadeIn(brace_txt_d)
        )
        self.next_slide()
        
        # --- SCENE 2: CHUYỂN TIẾP SANG CONTINUOUS-TIME DIFFUSION ---
        self.play(
            ReplacementTransform(title_d, title_c),
            ReplacementTransform(subtitle_d, subtitle_c),
            ReplacementTransform(math_d_fwd, math_c_fwd),
            ReplacementTransform(math_d_rev, math_c_rev),
            ReplacementTransform(brace_d, brace_c),
            ReplacementTransform(brace_txt_d, brace_txt_c),
            run_time=1.5
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 65 — MODULE 62: SYNTHESIS WITH SDE VS. ODE  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
from manim import rate_functions, interpolate_color

class Module62_SDE_vs_ODE(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề slide
        title = slide_title("Synthesis with SDE vs. ODE")
        
        # ─────────────────────────────────────────────────────────────────────
        # HÀM TẠO PANEL QUỸ ĐẠO (TRAJECTORIES) TỐI GIẢN CHỐNG TRÀN VIỀN
        # ─────────────────────────────────────────────────────────────────────
        def build_trajectory_panel(is_sde=True):
            # Khung biểu diễn không gian Latent -> Data
            frame = RoundedRectangle(
                width=5.0, height=3.0, corner_radius=0.2,
                stroke_color=Theme.DIM, stroke_width=2,
                fill_color=Theme.BG, fill_opacity=0.5
            )
            
            # Text đại diện cho hai phân phối ở 2 đầu
            q0_label = MathTex("q(\mathbf{x}_0)", font_size=24, color=Theme.ACCENT_GOLD).next_to(frame, LEFT, buff=0.1)
            qT_label = MathTex("q(\mathbf{x}_T)", font_size=24, color=Theme.DIM).next_to(frame, RIGHT, buff=0.1)
            
            # Vẽ các đường quỹ đạo (Trajectories)
            paths = VGroup()
            start_ys = [-0.9, -0.6, -0.3, 0.4, 0.7, 1.0] # Giả lập phân phối bimodal (2 đỉnh) ở x0
            end_ys = np.linspace(-0.5, 0.5, len(start_ys)) # Giả lập phân phối unimodal (1 đỉnh Gaussian) ở xT
            
            left_x = frame.get_left()[0]
            right_x = frame.get_right()[0]
            
            for i, sy in enumerate(start_ys):
                ey = end_ys[i]
                start_p = np.array([left_x, frame.get_center()[1] + sy, 0])
                end_p = np.array([right_x, frame.get_center()[1] + ey, 0])
                
                path = VMobject()
                points = [start_p]
                
                steps = 50 if is_sde else 25
                for j in range(1, steps):
                    alpha = j / steps
                    # Tọa độ X nội suy tuyến tính
                    current_x = start_p[0] * (1 - alpha) + end_p[0] * alpha
                    
                    if not is_sde:
                        # ODE: Quỹ đạo cong mượt mà (smooth)
                        smooth_alpha = rate_functions.smooth(alpha)
                        current_y = start_p[1] * (1 - smooth_alpha) + end_p[1] * smooth_alpha
                    else:
                        # SDE: Quỹ đạo có nhiễu (brownian motion)
                        base_y = start_p[1] * (1 - alpha) + end_p[1] * alpha
                        noise = np.random.normal(0, 0.08) if 0 < alpha < 0.9 else 0 # Tắt nhiễu ở 2 đầu mút
                        current_y = base_y + noise
                        
                    points.append(np.array([current_x, current_y, 0]))
                
                points.append(end_p)
                
                # Áp dụng màu gradient và kiểu vẽ
                color = interpolate_color(Theme.PRIMARY, ManimColor("#9C27B0"), i / len(start_ys))
                if is_sde:
                    path.set_points_as_corners(points)
                    path.set_stroke(color=color, width=1.5, opacity=0.7)
                else:
                    path.set_points_smoothly(points)
                    path.set_stroke(color=color, width=2.5, opacity=0.9)
                    
                paths.add(path)
            
            # Chuỗi hình ảnh bên dưới khung
            squares = VGroup(*[
                Square(
                    side_length=0.7, 
                    fill_color=interpolate_color(Theme.ACCENT_GOLD, Theme.DIM, i/4.0),
                    fill_opacity=1, stroke_width=0
                ) for i in range(5)
            ]).arrange(RIGHT, buff=0.15)
            squares.next_to(frame, DOWN, buff=0.3)
            
            # Nhãn cho hình ảnh
            labels = VGroup(
                MathTex("X_0", font_size=20).next_to(squares[0], DOWN, buff=0.1),
                MathTex("X_t", font_size=20).next_to(squares[2], DOWN, buff=0.1),
                Text("...", font_size=16).next_to(squares[3], DOWN, buff=0.1),
                MathTex("X_T", font_size=20).next_to(squares[4], DOWN, buff=0.1)
            )
            
            # Nhãn phía trên khung
            panel_title = Text(
                "Generation with Reverse Diffusion SDE" if is_sde else "Generation with Probability Flow ODE",
                font=Theme.FONT_BODY, font_size=16, color=Theme.NEUTRAL
            ).next_to(frame, UP, buff=0.15)
            
            return VGroup(panel_title, q0_label, frame, paths, qT_label, squares, labels)

        # ─────────────────────────────────────────────────────────────────────
        # KHỞI TẠO NỘI DUNG 2 CỘT (SDE vs ODE)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- CỘT TRÁI: SDE ---
        sde_visual = build_trajectory_panel(is_sde=True)
        sde_eq_title = Text("Generative Reverse Diffusion SDE (stochastic):", font=Theme.FONT_BODY, font_size=20, weight="BOLD")
        sde_eq_math = MathTex(
            r"d\mathbf{x}_t = -\frac{1}{2}\beta(t) \left[ \mathbf{x}_t + 2s_\theta(\mathbf{x}_t, t) \right] dt + \sqrt{\beta(t)} d\mathbf{w}_t",
            font_size=26, color=Theme.NEUTRAL
        )
        sde_col = VGroup(sde_visual, sde_eq_title, sde_eq_math).arrange(DOWN, buff=0.4)
        
        # --- CỘT PHẢI: ODE ---
        ode_visual = build_trajectory_panel(is_sde=False)
        ode_eq_title = Text("Generative Probability Flow ODE (deterministic):", font=Theme.FONT_BODY, font_size=20, weight="BOLD")
        ode_eq_math = MathTex(
            r"d\mathbf{x}_t = -\frac{1}{2}\beta(t) \left[ \mathbf{x}_t + s_\theta(\mathbf{x}_t, t) \right] dt",
            font_size=26, color=Theme.NEUTRAL
        )
        ode_col = VGroup(ode_visual, ode_eq_title, ode_eq_math).arrange(DOWN, buff=0.4)
        
        # Đồng bộ chiều cao phương trình (kéo dãn nhẹ khoảng cách) để 2 cột thẳng tắp
        ode_eq_math.align_to(sde_eq_math, DOWN)
        
        # ─────────────────────────────────────────────────────────────────────
        # GOM NHÓM VÀ TỐI ƯU HIỂN THỊ (TRÁNH LỖI OVERFLOW VÀ CĂN LỆCH TRỤC)
        # ─────────────────────────────────────────────────────────────────────
        mega_group = VGroup(sde_col, ode_col).arrange(RIGHT, buff=0.8)
        
        # Giới hạn kích thước siêu chuẩn: Rộng Max 13.5, Cao Max 6.0
        mega_group.set_width(13.5)
        if mega_group.height > 6.0:
            mega_group.set_height(6.0)
            
        mega_group.center().shift(DOWN * 0.2) # Nhường không gian cho Title

        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        self.next_slide()
        
        # SCENE 1: Hiển thị đồ họa và công thức của SDE (Nhấn mạnh tính ngẫu nhiên)
        self.play(FadeIn(sde_visual[0:3])) # Hiện khung và text
        self.play(Create(sde_visual[3]), run_time=2.5) # Vẽ các quỹ đạo ziczac ngẫu nhiên
        self.play(FadeIn(sde_visual[4:])) # Hiện dãy ảnh X0...XT
        self.play(FadeIn(sde_col[1]), Write(sde_col[2]))
        self.next_slide()
        
        # SCENE 2: Hiển thị đồ họa và công thức của ODE (Nhấn mạnh tính mượt mà)
        self.play(FadeIn(ode_visual[0:3]))
        self.play(Create(ode_visual[3]), run_time=2.5) # Vẽ các quỹ đạo smooth trơn tru
        self.play(FadeIn(ode_visual[4:]))
        self.play(FadeIn(ode_col[1]), Write(ode_col[2]))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 66 — MODULE 63: GENERATIVE ODEs  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import DashedLine, SurroundingRectangle

class Module63_GenerativeODEs(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề và Phụ đề (Đã tinh gọn chữ và giảm size để chống đè lên hộp Zoom)
        title = slide_title("Generative ODEs")
        subtitle = Text(
            "Solve ODEs with minimal function evaluations", 
            font=Theme.FONT_BODY, font_size=20, color=Theme.SUCCESS
        )
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG CỘT TRÁI (GLOBAL TRAJECTORY PLOT)
        # ─────────────────────────────────────────────────────────────────────
        
        # Phương trình chính
        main_eq = MathTex(r"d\mathbf{x} = \epsilon_\theta(\mathbf{x}, t)dt", font_size=42, color=Theme.NEUTRAL)
        
        # Khung đồ thị tổng thể
        global_frame = RoundedRectangle(
            width=5.0, height=3.5, corner_radius=0.1,
            stroke_color=Theme.DIM, stroke_width=2,
            fill_color=Theme.BOX_FILL, fill_opacity=1
        )
        
        # Vẽ các quỹ đạo (Trajectories) giả lập bằng VMobject mượt
        global_paths = VGroup()
        start_ys = [-1.2, -0.6, 0.0, 0.6, 1.2]
        for sy in start_ys:
            path = VMobject(
                color=Theme.SUCCESS, stroke_width=1.5, stroke_opacity=0.6
            )
            # Khởi tạo đường cong mượt đi qua 3 điểm nút định vị
            path.set_points_smoothly([
                global_frame.get_left() + UP * sy,
                global_frame.get_center() + UP * (sy * 0.7),
                global_frame.get_right() + UP * (sy * 0.3)
            ])
            global_paths.add(path)
            
        # Hộp Zoom (Zoom box) định vị trên một quỹ đạo
        zoom_box_global = Rectangle(
            width=0.8, height=0.5, 
            stroke_color=Theme.NEUTRAL, stroke_width=1.5, stroke_opacity=0.8
        )
        # Đặt hộp zoom ở giữa nửa bên trái
        zoom_box_global.move_to(global_frame.get_left() + RIGHT * 1.2 + UP * 0.1)
        
        # Nhãn trục X (p(x0) và p(x1))
        lbl_x0 = MathTex("p(\mathbf{x}_0)", font_size=24).next_to(global_frame, DOWN, buff=0.15).align_to(global_frame, LEFT)
        lbl_x1 = MathTex("p(\mathbf{x}_1)", font_size=24).next_to(global_frame, DOWN, buff=0.15).align_to(global_frame, RIGHT)
        lbl_mid = Text("ODE Trajectories", font=Theme.FONT_BODY, font_size=18).next_to(global_frame, DOWN, buff=0.18)
        
        global_plot_group = VGroup(global_frame, global_paths, zoom_box_global, lbl_x0, lbl_x1, lbl_mid)
        left_column = VGroup(main_eq, global_plot_group).arrange(DOWN, buff=0.6)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG CỘT PHẢI (ZOOMED PLOT & MATH)
        # ─────────────────────────────────────────────────────────────────────
        
        # Khung Zoom phóng to
        zoom_frame = RoundedRectangle(
            width=4.5, height=2.2, corner_radius=0.1,
            stroke_color=Theme.NEUTRAL, stroke_width=2,
            fill_color=Theme.BOX_FILL_ALT, fill_opacity=1
        )
        
        # Vẽ minh họa cập nhật Vector bên trong hộp Zoom
        start_pt = zoom_frame.get_left() + RIGHT * 0.5 + DOWN * 0.2
        
        # Đường cong Ground Truth thực tế (sử dụng VMobject để vẽ mượt)
        true_curve = VMobject(color=Theme.SUCCESS, stroke_width=3)
        true_curve.set_points_smoothly([
            start_pt, 
            start_pt + RIGHT * 1.5 + UP * 0.1, 
            start_pt + RIGHT * 3 + UP * 0.4
        ])
        
        dot_current = Dot(start_pt, color=Theme.NEUTRAL, radius=0.06)
        
        # Mũi tên xấp xỉ bậc 1 (Euler - Tuyến tính)
        vec_euler = Arrow(
            start_pt, start_pt + RIGHT * 2.5 + UP * 0.8,
            buff=0, color=Theme.PRIMARY, stroke_width=3, tip_length=0.15
        )
        # Mũi tên xấp xỉ bậc cao (Higher order - Bám sát đường cong hơn)
        vec_higher = Arrow(
            start_pt, start_pt + RIGHT * 2.8 + UP * 0.35,
            buff=0, color=Theme.ACCENT_GOLD, stroke_width=3, tip_length=0.15
        )
        
        zoom_plot_group = VGroup(zoom_frame, true_curve, dot_current, vec_euler, vec_higher)
        
        # --- CÁC PHƯƠNG TRÌNH XẤP XỈ ---
        # 1. Euler (Xấp xỉ tuyến tính)
        line_euler_legend = Line(LEFT, RIGHT*0.5, color=Theme.PRIMARY, stroke_width=3)
        math_euler = MathTex(
            r"\mathbf{x}_{t+\Delta t} \approx \mathbf{x}_t + \Delta t \epsilon_\theta(\mathbf{x}_t, t)",
            font_size=28, color=Theme.NEUTRAL
        )
        row_euler = VGroup(line_euler_legend, math_euler).arrange(RIGHT, buff=0.3)
        
        # 2. Higher Order (Xấp xỉ bậc cao)
        line_higher_legend = Line(LEFT, RIGHT*0.5, color=Theme.ACCENT_GOLD, stroke_width=3)
        # Chia nhỏ chuỗi để đóng khung riêng phần đạo hàm
        math_higher = MathTex(
            r"\mathbf{x}_{t+\Delta t} \approx \mathbf{x}_t + \Delta t \epsilon_\theta(\mathbf{x}_t, t) + \frac{\Delta t^2}{2}",
            r"\frac{d\epsilon_\theta(\mathbf{x}_t, t)}{dt}",
            font_size=28, color=Theme.NEUTRAL
        )
        row_higher = VGroup(line_higher_legend, math_higher).arrange(RIGHT, buff=0.3)
        
        math_group = VGroup(row_euler, row_higher).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        # --- Ý TƯỞNG CHƯNG CẤT (DISTILLATION) ---
        # Icon bóng đèn và text
        idea_icon = Text("💡", font="Segoe UI Emoji", font_size=32)
        idea_text = Text("Distill the higher order term to a neural network", font=Theme.FONT_BODY, font_size=20, color=Theme.ACCENT_RED)
        idea_row = VGroup(idea_icon, idea_text).arrange(RIGHT, buff=0.2)
        
        # Hàm loss
        loss_math = MathTex(
            r"\min_\psi \left\| k_\psi(\mathbf{x}_t, t) - \frac{d\epsilon_\theta(\mathbf{x}_t, t)}{dt} \right\|_2^2",
            font_size=32, color=Theme.NEUTRAL
        )
        
        distill_group = VGroup(idea_row, loss_math).arrange(DOWN, buff=0.3)
        
        right_column = VGroup(zoom_plot_group, math_group, distill_group).arrange(DOWN, buff=0.5)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM NHÓM & CĂN CHỈNH TỔNG THỂ (ĐÃ CẬP NHẬT BIÊN AN TOÀN)
        # ─────────────────────────────────────────────────────────────────────
        mega_group = VGroup(left_column, right_column).arrange(RIGHT, buff=1.2) # Tăng buff ngang
        
        # Khống chế khung hình gọn hơn (set_width=12.8 thay vì 13.2 để đẩy hộp Zoom ra xa rìa chữ hơn)
        mega_group.set_width(12.8)
        if mega_group.height > 5.8:
            mega_group.set_height(5.8)
            
        mega_group.center().shift(DOWN * 0.4) # Hạ thấp đồ thị xuống để cách biệt hoàn toàn với phụ đề
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: LIÊN KẾT HẬU KỲ (TỰ ĐỘNG CẬP NHẬT THEO CÁC TỌA ĐỘ MỚI)
        # ─────────────────────────────────────────────────────────────────────
        # Hai đường đứt nét nối từ hộp nhỏ (Global) sang khung lớn (Zoom)
        dash_top = DashedLine(
            zoom_box_global.get_corner(UR), zoom_frame.get_corner(UL), 
            color=Theme.DIM, stroke_width=2
        )
        dash_bottom = DashedLine(
            zoom_box_global.get_corner(DR), zoom_frame.get_corner(DL), 
            color=Theme.DIM, stroke_width=2
        )
        
        # Khung đỏ bao quanh phần tử đạo hàm của phương trình Higher Order
        red_box = SurroundingRectangle(math_higher[1], color=Theme.ACCENT_RED, stroke_width=2, buff=0.08)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title), FadeIn(subtitle))
        self.next_slide()
        
        # 1. Hiện ODE tổng quát và đồ thị
        self.play(FadeIn(main_eq))
        self.play(
            FadeIn(global_frame), FadeIn(lbl_x0), FadeIn(lbl_x1), FadeIn(lbl_mid),
            Create(global_paths, run_time=2.0)
        )
        self.next_slide()
        
        # 2. Focus vào một điểm cập nhật và phóng to
        self.play(Create(zoom_box_global))
        self.play(
            Create(dash_top), Create(dash_bottom),
            FadeIn(zoom_frame), FadeIn(dot_current), Create(true_curve)
        )
        self.next_slide()
        
        # 3. Hiện xấp xỉ Euler (Tuyến tính)
        self.play(Create(vec_euler), FadeIn(row_euler))
        self.next_slide()
        
        # 4. Hiện xấp xỉ bậc cao (Bám sát hơn) và đóng khung đạo hàm khó tính
        self.play(Create(vec_higher), FadeIn(row_higher))
        self.play(Create(red_box))
        self.next_slide()
        
        # 5. Đưa ra giải pháp Distillation
        self.play(FadeIn(idea_row))
        self.play(Write(loss_math))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 67 — MODULE 64: PROGRESSIVE DISTILLATION  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Brace, Triangle

# --- ĐỐI TƯỢNG ĐỒ HỌA MỚI: MŨI TÊN KHỐI VÀNG CHỨA CHỮ ---
class BlockArrow(VGroup):
    def __init__(self, label: str, width: float = 2.0, height: float = 0.5, **kwargs):
        super().__init__(**kwargs)
        # Thân mũi tên (Rectangle)
        rect = Rectangle(
            width=width - 0.4, 
            height=height, 
            fill_color=Theme.ACCENT_GOLD, 
            fill_opacity=1, 
            stroke_width=0
        )
        # Đầu mũi tên (Triangle xoay sang phải)
        tip = Triangle(
            fill_color=Theme.ACCENT_GOLD, 
            fill_opacity=1, 
            stroke_width=0
        ).rotate(-PI / 2) # Xoay -90 độ để chỉ sang phải
        tip.scale_to_fit_height(height)
        tip.scale_to_fit_width(0.4)
        tip.next_to(rect, RIGHT, buff=0)
        
        arrow_shape = VGroup(rect, tip)
        
        # Chữ nằm trên thân mũi tên
        text = Text(
            label, 
            font=Theme.FONT_BODY, 
            font_size=15, 
            color=Theme.BG, # Màu chữ tối tương phản trên nền vàng
            weight="BOLD"
        )
        text.move_to(rect.get_center())
        
        self.add(arrow_shape, text)


class Module64_ProgressiveDistillation(Slide):
    def construct(self):
        # 1. Thiết lập màu nền
        self.camera.background_color = Theme.BG
        
        # 2. Tiêu đề Slide (Ghim cố định ở UL)
        title = slide_title("Progressive Distillation")
        
        # 3. Bullets mô tả (Được ghim dưới tiêu đề, bảo đảm không bị đè chữ)
        bullet_1 = Text(
            "• Distill a deterministic ODE sampler: 2 Teacher steps → 1 Student step.", 
            font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL
        )
        bullet_2 = Text(
            "• Progressive: The student from stage i becomes the teacher for stage i+1.", 
            font=Theme.FONT_BODY, font_size=24, color=Theme.NEUTRAL
        )
        bullets = VGroup(bullet_1, bullet_2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        bullets.next_to(title, DOWN, aligned_edge=LEFT, buff=0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # XÂY DỰNG SƠ ĐỒ ĐỒ HOẠ (DIAGRAM)
        # ─────────────────────────────────────────────────────────────────────
        diagram_group = VGroup()
        
        # Thiết lập lưới tọa độ nội bộ của sơ đồ
        x_cols = [-3.5, 0, 3.5] # Vị trí X của 3 cột
        y_top = 2.0
        y_bot = -2.0
        total_h = y_top - y_bot
        
        # Hàm tạo cột mũi tên dọc đại diện cho các bước lấy mẫu
        def build_col(x_pos, num_steps):
            col_group = VGroup()
            arrows = VGroup()
            step_h = total_h / num_steps
            
            for i in range(num_steps):
                start_y = y_top - i * step_h
                end_y = y_top - (i + 1) * step_h
                arr = Arrow(
                    start=[x_pos, start_y, 0], 
                    end=[x_pos, end_y, 0], 
                    buff=0.08, color=Theme.SUCCESS, stroke_width=12, tip_length=0.2
                )
                arrows.add(arr)
            
            lbl_top = MathTex(r"\epsilon", font_size=36, color=Theme.NEUTRAL).next_to(arrows, UP, buff=0.1)
            lbl_bot = MathTex(r"\mathbf{X}", font_size=36, color=Theme.NEUTRAL).next_to(arrows, DOWN, buff=0.1)
            
            col_group.add(arrows, lbl_top, lbl_bot)
            return col_group, arrows
            
        # Dựng 3 cột mũi tên chính
        col1, arrs1 = build_col(x_cols[0], 4)
        col2, arrs2 = build_col(x_cols[1], 2)
        col3, arrs3 = build_col(x_cols[2], 1)
        diagram_group.add(col1, col2, col3)
        
        # Dựng các mũi tên chưng cất màu vàng khối (BlockArrow)
        # Cột 1 (4 bước) -> Cột 2 (2 bước)
        y_pos_top = (arrs1[0].get_center()[1] + arrs1[1].get_center()[1]) / 2
        d1_top = BlockArrow("Distill").move_to([(x_cols[0] + x_cols[1])/2, y_pos_top, 0])
        
        y_pos_bot = (arrs1[2].get_center()[1] + arrs1[3].get_center()[1]) / 2
        d1_bot = BlockArrow("Distill").move_to([(x_cols[0] + x_cols[1])/2, y_pos_bot, 0])
        
        # Cột 2 (2 bước) -> Cột 3 (1 bước)
        y_pos_mid = (arrs2[0].get_center()[1] + arrs2[1].get_center()[1]) / 2
        d2 = BlockArrow("Distill").move_to([(x_cols[1] + x_cols[2])/2, y_pos_mid, 0])
        
        diagram_group.add(d1_top, d1_bot, d2)
        
        # Thêm mốc thời gian t=1 và t=0 bên trái cột 1
        t1_lbl = MathTex("t=1", font_size=28).next_to(col1[1], LEFT, buff=0.8).align_to(col1[0], UP)
        t0_lbl = MathTex("t=0", font_size=28).next_to(col1[2], LEFT, buff=0.8).align_to(col1[0], DOWN)
        diagram_group.add(t1_lbl, t0_lbl)
        
        # Tạo ngoặc chú thích toán học cho cột 1 và cột 3
        math_labels = VGroup()
        
        braces_c1 = VGroup()
        for i in range(4):
            b = Brace(arrs1[i], LEFT, buff=0.1)
            braces_c1.add(b)
            
        eq1 = MathTex(r"\mathbf{z}_{3/4} = f(\mathbf{z}_1; \eta)", font_size=20).next_to(braces_c1[0], LEFT, buff=0.1)
        eq2 = MathTex(r"\mathbf{z}_{1/2} = f(\mathbf{z}_{3/4}; \eta)", font_size=20).next_to(braces_c1[1], LEFT, buff=0.1)
        eq3 = MathTex(r"\mathbf{z}_{1/4} = f(\mathbf{z}_{1/2}; \eta)", font_size=20).next_to(braces_c1[2], LEFT, buff=0.1)
        eq4 = MathTex(r"\mathbf{x} = f(\mathbf{z}_{1/4}; \eta)", font_size=20).next_to(braces_c1[3], LEFT, buff=0.1)
        
        brace_c3 = Brace(arrs3[0], RIGHT, buff=0.1)
        eq_final = MathTex(r"\mathbf{x} = f(\mathbf{z}_1; \theta)", font_size=24, color=Theme.PRIMARY).next_to(brace_c3, RIGHT, buff=0.1)
        
        math_labels.add(braces_c1, eq1, eq2, eq3, eq4, brace_c3, eq_final)
        diagram_group.add(math_labels)
        
        # Trục nằm ngang biểu thị tiến trình Distillation Stage ở đáy sơ đồ
        stage_arrow = Arrow(
            [x_cols[0], y_bot - 1.0, 0], [x_cols[2], y_bot - 1.0, 0], 
            color=Theme.NEUTRAL, stroke_width=2.5, tip_length=0.15
        )
        stage_lbl = Text("Distillation stage", font=Theme.FONT_BODY, font_size=20).next_to(stage_arrow, LEFT, buff=0.2)
        diagram_group.add(stage_arrow, stage_lbl)
        
        # ─────────────────────────────────────────────────────────────────────
        # ÉP KHUÔN SƠ ĐỒ VÀ ĐỊNH VỊ DƯỚI TEXT MÔ TẢ (CHỐNG TRÀN VÀ ĐÈ CHỮ)
        # ─────────────────────────────────────────────────────────────────────
        # Đặt kích thước cố định cho sơ đồ cao tối đa 4.2 (Phù hợp tuyệt đối với không gian trống còn lại)
        diagram_group.set_height(4.2)
        
        # Định vị sơ đồ nằm ngay dưới bullets, căn giữa chiều ngang màn hình
        diagram_group.next_to(bullets, DOWN, buff=0.4)
        diagram_group.set_x(0)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title))
        self.play(FadeIn(bullets))
        self.next_slide()
        
        # 1. Hiện Teacher ban đầu (4 bước) cùng ngoặc và công thức
        self.play(
            FadeIn(col1), FadeIn(t1_lbl), FadeIn(t0_lbl),
            FadeIn(math_labels[0:5])
        )
        self.next_slide()
        
        # 2. Hiện mũi tên khối vàng "Distill" mượt mà chỉ sang cột 2
        self.play(FadeIn(d1_top), FadeIn(d1_bot))
        self.play(FadeIn(col2))
        self.next_slide()
        
        # 3. Tiếp tục chưng cất bước tiếp theo sang cột 3 (1 bước lấy mẫu)
        self.play(FadeIn(d2))
        self.play(FadeIn(col3))
        self.next_slide()
        
        # 4. Vẽ ngoặc cuối cùng, ghi nhận kết quả và trục thời gian dưới đáy
        self.play(GrowFromCenter(brace_c3), Write(eq_final))
        self.play(GrowArrow(stage_arrow), FadeIn(stage_lbl))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 68 — MODULE 65: CONSISTENCY DISTILLATION  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
from manim import CurvedArrow

class Module65_ConsistencyDistillation(Slide):
    def construct(self):
        # 1. Background và Title
        self.camera.background_color = Theme.BG
        title = slide_title("Consistency Distillation")
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: CỘT TRÁI - TEXT ĐƯỢC CÔ ĐỌNG (LÝ THUYẾT)
        # ─────────────────────────────────────────────────────────────────────
        col_left = VGroup()
        
        # Ý tưởng cốt lõi
        t1 = Text(
            "Key Idea: Points on the same ODE trajectory\nmust map to the same origin.", 
            font=Theme.FONT_BODY, font_size=24, color=Theme.PRIMARY
        )
        
        # Khái niệm hàm F
        t2 = Text("Estimation Network:", font=Theme.FONT_BODY, font_size=22)
        eq1 = MathTex(r"f_\theta(\mathbf{x}_t, t) \approx \mathbf{x}_0", font_size=32)
        
        # Mục tiêu huấn luyện
        t3 = Text(
            "Training Objective:\nMinimize difference between adjacent steps", 
            font=Theme.FONT_BODY, font_size=22
        )
        eq2 = MathTex(
            r"\min_\theta \left\| f_{\text{EMA}}(\mathbf{x}_t, t) - f_\theta(\mathbf{x}_{t'}, t') \right\|_2^2", 
            font_size=32
        )
        
        # Kết luận (Đạo hàm theo thời gian bằng 0)
        arr_down = Arrow(UP, DOWN, color=Theme.SUCCESS, buff=0, stroke_width=4, tip_length=0.15).scale(0.6)
        eq3 = MathTex(r"\Rightarrow \frac{d}{dt} f_\theta(\mathbf{x}(t), t) = 0", font_size=34, color=Theme.SUCCESS)
        
        col_left.add(t1, t2, eq1, t3, eq2, arr_down, eq3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: CỘT PHẢI - DIAGRAM TỰ CODE (KHÔNG DÙNG ẢNH NGOÀI)
        # ─────────────────────────────────────────────────────────────────────
        diagram = VGroup()
        x_left = -3.5
        x_right = 3.5
        
        # A. Vẽ đường PDF (Data: Bimodal 2 đỉnh, Noise: Gaussian 1 đỉnh)
        data_pts = []
        noise_pts = []
        for y in np.linspace(-2.5, 2.5, 50):
            d_val = -(y**2 - 1.5)**2 * 0.3  # Bimodal curve ngược hướng trái
            n_val = np.exp(-y**2 * 1.5) * 1.0 # Gaussian curve hướng phải
            data_pts.append([x_left + d_val, y, 0])
            noise_pts.append([x_right + n_val, y, 0])
            
        data_curve = VMobject().set_points_smoothly(data_pts).set_stroke(Theme.ACCENT_GOLD, 3)
        noise_curve = VMobject().set_points_smoothly(noise_pts).set_stroke(Theme.PRIMARY, 3)
        
        data_lbl = Text("Data", font=Theme.FONT_BODY, font_size=22).next_to(data_curve, UP, buff=0.1)
        noise_lbl = Text("Noise", font=Theme.FONT_BODY, font_size=22).next_to(noise_curve, UP, buff=0.1)
        
        # B. Quỹ đạo phụ (Background ODE trajectories)
        trajectories = VGroup()
        for ys in [-1.5, -0.8, 0.8, 1.5]:
            p1 = np.array([x_left, ys, 0])
            p3 = np.array([x_right, ys * 0.2, 0])
            p2 = np.array([0, (ys + ys*0.2)/2 + 0.3*np.sign(ys), 0])
            path = VMobject().set_points_smoothly([p1, p2, p3]).set_stroke(Theme.SUCCESS, 1.5, opacity=0.3)
            trajectories.add(path)
            
        traj_lbl = Text("ODE trajectories", font=Theme.FONT_BODY, font_size=18, color=Theme.SUCCESS).move_to([0, 2.2, 0])
        
        # C. Quỹ đạo chính (Main path để diễn giải)
        main_path = VMobject()
        p0 = np.array([x_left, 0, 0])
        pT = np.array([x_right, 0, 0])
        pmid = np.array([0, 0.4, 0])
        main_path.set_points_smoothly([p0, pmid, pT]).set_stroke(Theme.SUCCESS, 3, opacity=0.8)
        
        # Lấy tọa độ các điểm t và t' nằm trên quỹ đạo chính
        pt = main_path.point_from_proportion(0.35)
        pt_prime = main_path.point_from_proportion(0.65)
        
        d0 = Dot(p0, color=Theme.ACCENT_GOLD, radius=0.06)
        dt = Dot(pt, color=Theme.ACCENT_RED, radius=0.06)
        dt_prime = Dot(pt_prime, color=Theme.ACCENT_RED, radius=0.06)
        dT = Dot(pT, color=Theme.ACCENT_RED, radius=0.06)
        dots = VGroup(d0, dt, dt_prime, dT)
        
        # Nhãn tọa độ điểm
        l0 = MathTex(r"(\mathbf{x}_0, 0)", font_size=18).next_to(d0, LEFT, buff=0.1)
        lt = MathTex(r"(\mathbf{x}_t, t)", font_size=18).next_to(dt, DOWN, buff=0.1)
        ltp = MathTex(r"(\mathbf{x}_{t'}, t')", font_size=18).next_to(dt_prime, DOWN, buff=0.1)
        lT = MathTex(r"(\mathbf{x}_T, T)", font_size=18).next_to(dT, RIGHT, buff=0.1)
        dot_labels = VGroup(l0, lt, ltp, lT)
        
        # D. Các mũi tên "Consistency" (Chỉ chung về một gốc)
        arr_t = CurvedArrow(pt, p0, angle=-0.3, color=Theme.ACCENT_RED, stroke_width=2.5, tip_length=0.15)
        arr_tp = CurvedArrow(pt_prime, p0, angle=-0.4, color=Theme.ACCENT_RED, stroke_width=2.5, tip_length=0.15)
        arr_T = CurvedArrow(pT, p0, angle=-0.5, color=Theme.ACCENT_RED, stroke_width=2.5, tip_length=0.15)
        
        la_t = MathTex(r"f_\theta(\mathbf{x}_t, t)", font_size=18, color=Theme.ACCENT_RED).next_to(arr_t, UP, buff=0.05)
        la_tp = MathTex(r"f_\theta(\mathbf{x}_{t'}, t')", font_size=18, color=Theme.ACCENT_RED).next_to(arr_tp, UP, buff=0.05)
        la_T = MathTex(r"f_\theta(\mathbf{x}_T, T)", font_size=18, color=Theme.ACCENT_RED).next_to(arr_T, DOWN, buff=0.05)
        
        consistency_group = VGroup(arr_t, arr_tp, arr_T, la_t, la_tp, la_T)
        
        diagram.add(
            data_curve, data_lbl, noise_curve, noise_lbl, 
            trajectories, traj_lbl, main_path,
            dots, dot_labels, consistency_group
        )
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GỘP NHÓM & CĂN CHỈNH AN TOÀN TRÁNH ĐÈ TITLE (ANTI-ERROR)
        # ─────────────────────────────────────────────────────────────────────
        content_group = VGroup(col_left, diagram).arrange(RIGHT, buff=0.8)
        
        # Ép khung ngang
        content_group.set_width(13.2)
        
        # Ép khung dọc với TRẦN CHIỀU CAO THẤP HƠN (5.8) để tuyệt đối không với tới Title
        if content_group.height > 5.8:
            content_group.set_height(5.8)
            
        # Dịch nhẹ xuống dưới 0.3 đơn vị để đảm bảo khoảng cách an toàn với phần đầu
        content_group.center().shift(DOWN * 0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        self.next_slide()
        
        # 1. Hiện ý tưởng và khái niệm Hàm F (Bên trái)
        self.play(FadeIn(col_left[0:3]))
        
        # 2. Hiện Khung phân phối Data / Noise và Quỹ đạo phụ (Bên phải)
        self.play(
            Create(data_curve), FadeIn(data_lbl),
            Create(noise_curve), FadeIn(noise_lbl)
        )
        self.play(Create(trajectories), FadeIn(traj_lbl), Create(main_path))
        self.next_slide()
        
        # 3. Hiện các điểm đánh dấu trên đường quỹ đạo chính
        self.play(FadeIn(dots), FadeIn(dot_labels))
        self.next_slide()
        
        # 4. Vẽ các mũi tên đỏ bay ngược về điểm xuất phát (Đại diện cho Consistency)
        self.play(
            Create(arr_t), FadeIn(la_t),
            Create(arr_tp), FadeIn(la_tp),
            Create(arr_T), FadeIn(la_T)
        )
        self.next_slide()
        
        # 5. Hiện Objective tính Loss & Rút ra đạo hàm (Bên trái)
        self.play(FadeIn(col_left[3:5]))
        self.play(GrowArrow(col_left[5]), Write(col_left[6]))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 69 — MODULE 66: DISTRIBUTIONAL MATCHING (DMD)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Ellipse, CurvedArrow, SurroundingRectangle

class Module66_DMD(Slide):
    def construct(self):
        # 1. Background và Title
        self.camera.background_color = Theme.BG
        title = slide_title("Distributional matching with reverse-KL (DMD)")
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG PHƯƠNG TRÌNH TOÁN HỌC TRUNG TÂM
        # ─────────────────────────────────────────────────────────────────────
        eq = MathTex(
            r"\nabla_\theta D_{\text{reverse-KL}}(", 
            r"p_t", 
            r"||", 
            r"q_t", 
            r") = \mathbb{E}_{\mathbf{z}, \epsilon} - \left[ \left(", 
            r"\nabla_\mathbf{x} \log p_t(\mathbf{x})", 
            r"-", 
            r"\nabla_\mathbf{x} \log q_t(\mathbf{x})", 
            r"\right) \nabla_\theta G_\theta(\mathbf{z}) \right]",
            font_size=36, color=Theme.NEUTRAL
        )
        
        # Khung màu nền đằng sau Real Score và Fake Score
        bg_real = SurroundingRectangle(eq[5], color=Theme.DIM, fill_opacity=0.4, stroke_width=0, buff=0.1)
        bg_fake = SurroundingRectangle(eq[7], color=Theme.PRIMARY, fill_opacity=0.4, stroke_width=0, buff=0.1)
        lbl_real_eq = Text("real score", font=Theme.FONT_BODY, font_size=12, color=Theme.NEUTRAL).next_to(bg_real, DOWN, buff=0.05)
        lbl_fake_eq = Text("fake score", font=Theme.FONT_BODY, font_size=12, color=Theme.NEUTRAL).next_to(bg_fake, DOWN, buff=0.05)
        
        # Hình elip đỏ bao quanh KL Divergence
        ellipse_kl = Ellipse(width=eq[0:4].width + 0.4, height=eq[0:4].height + 0.6, color=Theme.ACCENT_RED, stroke_width=2).move_to(eq[0:4])
        mode_txt = Text("Mode-seeking!", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_RED, slant="ITALIC", weight="BOLD")
        mode_txt.next_to(ellipse_kl, UP, buff=0.1)
        
        # Khắc phục lỗi đè chữ bằng cách sử dụng các mũi tên chỉ hướng thay vì dấu ngoặc nhọn
        txt_p = Text("Pre-trained teacher", font=Theme.FONT_BODY, font_size=13, color=Theme.DIM)
        txt_q = Text("One-step student", font=Theme.FONT_BODY, font_size=13, color=Theme.PRIMARY)
        
        # Định vị lệch hai nhãn sang hai bên để tránh chồng lấn
        txt_p.next_to(eq[1], DOWN, buff=0.8).shift(LEFT * 0.5)
        txt_q.next_to(eq[3], DOWN, buff=0.8).shift(RIGHT * 0.5)
        
        # Tạo hai mũi tên trỏ vào biến tương ứng
        arrow_p = Arrow(
            txt_p.get_top(), eq[1].get_bottom() + DOWN * 0.05,
            buff=0.05, color=Theme.DIM, stroke_width=2, tip_length=0.1
        )
        arrow_q = Arrow(
            txt_q.get_top(), eq[3].get_bottom() + DOWN * 0.05,
            buff=0.05, color=Theme.PRIMARY, stroke_width=2, tip_length=0.1
        )
        
        math_group = VGroup(
            bg_real, bg_fake, lbl_real_eq, lbl_fake_eq, 
            eq, ellipse_kl, mode_txt, 
            txt_p, txt_q, arrow_p, arrow_q
        )
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG LƯU ĐỒ (FLOWCHART) TỐI GIẢN
        # ─────────────────────────────────────────────────────────────────────
        box_z = RoundedBox(lines=["Random", "Latent z"], width=1.5, height=1.0, fill_color=ManimColor("#424242"))
        box_G = RoundedBox(lines=["Generator", "G_theta"], width=1.5, height=1.0, fill_color=Theme.ACCENT_RED, stroke_color=Theme.NEUTRAL)
        box_fake = RoundedBox(lines=["Fake", "Image"], width=1.5, height=1.0, fill_color=Theme.ACCENT_GOLD)
        box_noisy = RoundedBox(lines=["Noisy", "Fake Image"], width=1.6, height=1.0, fill_color=ManimColor("#5D4037"))
        
        spine = VGroup(box_z, box_G, box_fake, box_noisy).arrange(RIGHT, buff=0.6)
        
        arr_zG = Arrow(box_z.get_right(), box_G.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_Gf = Arrow(box_G.get_right(), box_fake.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_fn = DashedLine(box_fake.get_right(), box_noisy.get_left(), buff=0.1, stroke_width=2.5).add_tip(tip_length=0.15)
        txt_diff = Text("diffusion", font=Theme.FONT_BODY, font_size=14).next_to(arr_fn, UP, buff=0.05)
        
        spine_arrows = VGroup(arr_zG, arr_Gf, arr_fn, txt_diff)
        
        net_real = RoundedBox(lines=["Real Score", "Function 🔒"], width=2.0, height=0.9, fill_color=Theme.DIM)
        net_real.next_to(box_noisy, RIGHT, buff=0.8).shift(UP * 0.8)
        
        net_fake = RoundedBox(lines=["Fake Score", "Function"], width=2.0, height=0.9, fill_color=Theme.PRIMARY)
        net_fake.next_to(box_noisy, RIGHT, buff=0.8).shift(DOWN * 0.8)
        
        arr_n_real = Arrow(box_noisy.get_right(), net_real.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_n_fake = Arrow(box_noisy.get_right(), net_fake.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        
        out_real = Text("real score", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM).next_to(net_real, RIGHT, buff=0.2)
        out_fake = Text("fake score", font=Theme.FONT_BODY, font_size=16, color=Theme.PRIMARY).next_to(net_fake, RIGHT, buff=0.2)
        
        flowchart = VGroup(spine, spine_arrows, net_real, net_fake, arr_n_real, arr_n_fake, out_real, out_fake)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GỘP MEGA-GROUP VÀ ÉP KHUÔN AN TOÀN
        # ─────────────────────────────────────────────────────────────────────
        mega_group = VGroup(math_group, flowchart).arrange(DOWN, buff=1.0)
        
        mega_group.set_width(13.2)
        if mega_group.height > 5.5:
            mega_group.set_height(5.5)
            
        mega_group.center().shift(DOWN * 0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: LIÊN KẾT HẬU KỲ VÀ PHÂN LỚP HIỂN THỊ (Z-INDEX)
        # ─────────────────────────────────────────────────────────────────────
        # Thiết lập các hộp nằm ở lớp trên cùng (z_index = 3)
        box_z.set_z_index(3)
        box_G.set_z_index(3)
        box_fake.set_z_index(3)
        box_noisy.set_z_index(3)
        net_real.set_z_index(3)
        net_fake.set_z_index(3)
        out_real.set_z_index(3)
        out_fake.set_z_index(3)
        
        # Tạo đường nối ở lớp dưới cùng (z_index = 1) để không đè lên các khối hộp
        link_real = CurvedArrow(
            out_real.get_top(), lbl_real_eq.get_bottom() + DOWN * 0.1, 
            angle=-0.5, color=Theme.DIM, stroke_width=2.5, tip_length=0.15
        )
        link_real.set_z_index(1)
        
        link_fake = CurvedArrow(
            out_fake.get_right(), lbl_fake_eq.get_bottom() + DOWN * 0.1, 
            angle=-1.5, color=Theme.PRIMARY, stroke_width=2.5, tip_length=0.15
        )
        link_fake.set_z_index(1)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 5: PHỤ CHÚ DƯỚI CÙNG
        # ─────────────────────────────────────────────────────────────────────
        aux_txt = Text(
            "+ Auxiliary GAN loss on high-quality data", 
            font=Theme.FONT_BODY, font_size=20, color=ManimColor("#9C27B0"), slant="ITALIC"
        ).to_corner(DR, buff=0.4)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        self.next_slide()
        
        # 1. Hiện phương trình gốc
        self.play(FadeIn(eq))
        self.next_slide()
        
        # 2. Phân tích phương trình (KL Divergence, Teacher, Student)
        self.play(Create(ellipse_kl), Write(mode_txt))
        self.play(
            FadeIn(txt_p), Create(arrow_p),
            FadeIn(txt_q), Create(arrow_q)
        )
        self.next_slide()
        
        # 3. Tạo trục ngang lưu đồ
        self.play(FadeIn(spine[0:3]), Create(spine_arrows[0:2]))
        self.play(Create(spine_arrows[2]), FadeIn(spine_arrows[3]), FadeIn(spine[3]))
        self.next_slide()
        
        # 4. Nhánh Teacher (Real Score)
        self.play(FadeIn(bg_real), FadeIn(lbl_real_eq))
        self.play(Create(arr_n_real), FadeIn(net_real), FadeIn(out_real))
        self.play(Create(link_real))
        self.next_slide()
        
        # 5. Nhánh Student (Fake Score)
        self.play(FadeIn(bg_fake), FadeIn(lbl_fake_eq))
        self.play(Create(arr_n_fake), FadeIn(net_fake), FadeIn(out_fake))
        self.play(Create(link_fake))
        self.next_slide()
        
        # 6. Hiện dòng phụ chú GAN Loss
        self.play(FadeIn(aux_txt))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 70 — MODULE 67: f-DISTILL  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import Ellipse, CurvedArrow, SurroundingRectangle, DashedLine

class Module67_fDistill(Slide):
    def construct(self):
        # 1. Background
        self.camera.background_color = Theme.BG
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: SCENE 1 - GIỚI THIỆU VỀ f-DIVERGENCE
        # ─────────────────────────────────────────────────────────────────────
        title1 = slide_title("f-Divergences: Generalizing DMD")
        
        # Công thức định nghĩa tổng quát
        eq_fdiv = MathTex(
            r"D_f(p||q) = \int q(\mathbf{x})f\left(\frac{p(\mathbf{x})}{q(\mathbf{x})}\right)d\mathbf{x}",
            font_size=42, color=Theme.NEUTRAL
        )
        
        # Rút gọn ý tưởng cốt lõi của bảng (Table) thành Text súc tích
        txt_idea_1 = Text("Idea: Borrow tools from statistics to select optimal f-divergences.", font=Theme.FONT_BODY, font_size=24, color=Theme.SUCCESS)
        bullet_1 = Text("• Control trade-offs between mode-seeking behavior, saturation, and variance.", font=Theme.FONT_BODY, font_size=22, color=Theme.NEUTRAL)
        bullet_2 = Text("• Examples: reverse-KL, forward-KL, Jensen-Shannon, squared Hellinger.", font=Theme.FONT_BODY, font_size=22, color=Theme.NEUTRAL)
        bullets_1 = VGroup(bullet_1, bullet_2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        mega_scene1 = VGroup(txt_idea_1, eq_fdiv, bullets_1).arrange(DOWN, buff=0.8)
        
        # Ép khuôn Scale cho Scene 1
        mega_scene1.set_width(12.0)
        if mega_scene1.height > 5.5:
            mega_scene1.set_height(5.5)
        mega_scene1.center().shift(DOWN * 0.2)
        
        # Play Scene 1
        self.play(Write(title1))
        self.play(FadeIn(mega_scene1))
        self.next_slide()
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: TRANSITION SANG SCENE 2 - f-DISTILL
        # ─────────────────────────────────────────────────────────────────────
        title2 = slide_title("f-distill: Arbitrary f-Divergences")
        self.play(
            ReplacementTransform(title1, title2),
            FadeOut(mega_scene1)
        )
        self.next_slide()
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: XÂY DỰNG SCENE 2 - PHƯƠNG TRÌNH & LƯU ĐỒ (CÓ DISCRIMINATOR)
        # ─────────────────────────────────────────────────────────────────────
        # Text Idea & Result được thiết kế gọn lại để chừa chỗ
        t_idea = Text("Idea: Enable more divergences with different properties (less mode-seeking, non-saturation).", font=Theme.FONT_BODY, font_size=18, color=Theme.SUCCESS)
        t_result = Text("Result: KL/JS divergences achieve current state-of-the-art on distributional matching.", font=Theme.FONT_BODY, font_size=18, color=Theme.ACCENT_GOLD)
        summary_group = VGroup(t_idea, t_result).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        
        # Phương trình Gradient f-Distill (Chia mảng để bôi đậm và vẽ ngoặc)
        eq = MathTex(
            r"\nabla_\theta D_f(", 
            r"p_t", 
            r"||", 
            r"q_t", 
            r") = \mathbb{E}_{\mathbf{z}, \epsilon} - \Bigg[ ",
            r"f''\left(\frac{p_t(\mathbf{x})}{q_t(\mathbf{x})}\right) \left(\frac{p_t(\mathbf{x})}{q_t(\mathbf{x})}\right)^2", 
            r"\Bigg(", 
            r"\nabla_\mathbf{x} \log p_t(\mathbf{x})", 
            r"-", 
            r"\nabla_\mathbf{x} \log q_t(\mathbf{x})", 
            r"\Bigg) \nabla_\theta G_\theta(\mathbf{z}) \Bigg]",
            font_size=32, color=Theme.NEUTRAL
        )
        
        # Các khung background Highlight (Bao gồm màu hồng mới cho Discriminator term)
        bg_weight = SurroundingRectangle(eq[5], color=ManimColor("#D81B60"), fill_opacity=0.3, stroke_width=0, buff=0.1)
        bg_real = SurroundingRectangle(eq[7], color=Theme.DIM, fill_opacity=0.4, stroke_width=0, buff=0.1)
        bg_fake = SurroundingRectangle(eq[9], color=Theme.PRIMARY, fill_opacity=0.4, stroke_width=0, buff=0.1)
        
        lbl_real_eq = Text("real score", font=Theme.FONT_BODY, font_size=12, color=Theme.NEUTRAL).next_to(bg_real, DOWN, buff=0.05)
        lbl_fake_eq = Text("fake score", font=Theme.FONT_BODY, font_size=12, color=Theme.NEUTRAL).next_to(bg_fake, DOWN, buff=0.05)
        
        # Áp dụng fix của bạn: Neo chéo nhãn tránh đè lên nhau
        txt_p = Text("Pre-trained teacher", font=Theme.FONT_BODY, font_size=13, color=Theme.DIM).next_to(eq[1], DOWN, buff=0.8).shift(LEFT * 0.5)
        txt_q = Text("One-step student", font=Theme.FONT_BODY, font_size=13, color=Theme.PRIMARY).next_to(eq[3], DOWN, buff=0.8).shift(RIGHT * 0.5)
        arrow_p = Arrow(txt_p.get_top(), eq[1].get_bottom() + DOWN * 0.05, buff=0.05, color=Theme.DIM, stroke_width=2, tip_length=0.1)
        arrow_q = Arrow(txt_q.get_top(), eq[3].get_bottom() + DOWN * 0.05, buff=0.05, color=Theme.PRIMARY, stroke_width=2, tip_length=0.1)
        
        math_group = VGroup(
            bg_weight, bg_real, bg_fake, lbl_real_eq, lbl_fake_eq, 
            eq, txt_p, txt_q, arrow_p, arrow_q
        )
        
        # --- Lưu đồ (Thêm Discriminator) ---
        box_z = RoundedBox(lines=["Random", "Latent z"], width=1.4, height=0.9, fill_color=ManimColor("#424242"))
        box_G = RoundedBox(lines=["Generator", "G_theta"], width=1.4, height=0.9, fill_color=Theme.ACCENT_RED, stroke_color=Theme.NEUTRAL)
        box_fake = RoundedBox(lines=["Fake", "Image"], width=1.4, height=0.9, fill_color=Theme.ACCENT_GOLD)
        box_noisy = RoundedBox(lines=["Noisy", "Fake Image"], width=1.5, height=0.9, fill_color=ManimColor("#5D4037"))
        
        spine = VGroup(box_z, box_G, box_fake, box_noisy).arrange(RIGHT, buff=0.5)
        arr_zG = Arrow(box_z.get_right(), box_G.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_Gf = Arrow(box_G.get_right(), box_fake.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_fn = DashedLine(box_fake.get_right(), box_noisy.get_left(), buff=0.1, stroke_width=2.5).add_tip(tip_length=0.15)
        txt_diff = Text("diffusion", font=Theme.FONT_BODY, font_size=14).next_to(arr_fn, UP, buff=0.05)
        spine_arrows = VGroup(arr_zG, arr_Gf, arr_fn, txt_diff)
        
        net_real = RoundedBox(lines=["Real Score", "Function 🔒"], width=1.8, height=0.8, fill_color=Theme.DIM)
        net_real.next_to(box_noisy, RIGHT, buff=0.6).shift(UP * 0.6)
        
        net_fake = RoundedBox(lines=["Fake Score", "Function"], width=1.8, height=0.8, fill_color=Theme.PRIMARY)
        net_fake.next_to(box_noisy, RIGHT, buff=0.6).shift(DOWN * 0.6)
        
        # Bổ sung Discriminator (Neo trực tiếp phía trên Noisy Box)
        box_disc = RoundedBox(lines=["Discriminator"], width=1.6, height=0.6, fill_color=ManimColor("#D81B60"), font_size=18)
        box_disc.next_to(box_noisy, UP, buff=0.6)
        
        arr_n_real = Arrow(box_noisy.get_right(), net_real.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_n_fake = Arrow(box_noisy.get_right(), net_fake.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_n_disc = Arrow(box_noisy.get_top(), box_disc.get_bottom(), buff=0.1, stroke_width=3, tip_length=0.15)
        
        out_real = Text("real score", font=Theme.FONT_BODY, font_size=14, color=Theme.DIM).next_to(net_real, RIGHT, buff=0.15)
        out_fake = Text("fake score", font=Theme.FONT_BODY, font_size=14, color=Theme.PRIMARY).next_to(net_fake, RIGHT, buff=0.15)
        
        flowchart = VGroup(
            spine, spine_arrows, 
            net_real, net_fake, box_disc, 
            arr_n_real, arr_n_fake, arr_n_disc, 
            out_real, out_fake
        )
        
        # Ép khung cho toàn bộ Scene 2
        mega_scene2 = VGroup(summary_group, math_group, flowchart).arrange(DOWN, buff=0.5)
        mega_scene2.set_width(13.2)
        if mega_scene2.height > 5.5:
            mega_scene2.set_height(5.5)
        mega_scene2.center().shift(DOWN * 0.3)
        
        # Phân lớp (Z-Index) để đồ hoạ không đè lên nhau
        eq.set_z_index(2)
        bg_weight.set_z_index(0); bg_real.set_z_index(0); bg_fake.set_z_index(0)
        box_z.set_z_index(3); box_G.set_z_index(3); box_fake.set_z_index(3); box_noisy.set_z_index(3)
        net_real.set_z_index(3); net_fake.set_z_index(3); box_disc.set_z_index(3)
        out_real.set_z_index(3); out_fake.set_z_index(3)
        
        # Vẽ các kết nối lên phương trình sau khi mega_group đã cố định
        link_real = CurvedArrow(
            out_real.get_top(), lbl_real_eq.get_bottom() + DOWN * 0.1, 
            angle=-0.5, color=Theme.DIM, stroke_width=2.5, tip_length=0.15
        ).set_z_index(1)
        
        link_fake = CurvedArrow(
            out_fake.get_right(), lbl_fake_eq.get_bottom() + DOWN * 0.1, 
            angle=-1.5, color=Theme.PRIMARY, stroke_width=2.5, tip_length=0.15
        ).set_z_index(1)
        
        link_disc = DashedLine(
            box_disc.get_top(), bg_weight.get_bottom() + DOWN * 0.05, 
            color=ManimColor("#D81B60"), stroke_width=2.5
        ).add_tip(tip_length=0.15).set_z_index(1)
        
        aux_txt = Text(
            "+ Auxiliary GAN loss on high-quality data", 
            font=Theme.FONT_BODY, font_size=18, color=ManimColor("#9C27B0"), slant="ITALIC"
        ).to_corner(DR, buff=0.4)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: KỊCH BẢN HIỂN THỊ ANIMATION (SCENE 2)
        # ─────────────────────────────────────────────────────────────────────
        self.play(FadeIn(summary_group))
        self.play(FadeIn(eq))
        self.next_slide()
        
        # Focus Teacher/Student
        self.play(
            FadeIn(txt_p), Create(arrow_p),
            FadeIn(txt_q), Create(arrow_q)
        )
        self.next_slide()
        
        # Trục ngang lưu đồ
        self.play(FadeIn(spine[0:3]), Create(spine_arrows[0:2]))
        self.play(Create(spine_arrows[2]), FadeIn(spine_arrows[3]), FadeIn(spine[3]))
        self.next_slide()
        
        # Nhánh Discriminator (Khác biệt chính so với Module 66)
        self.play(Create(arr_n_disc), FadeIn(box_disc))
        self.play(FadeIn(bg_weight), Create(link_disc))
        self.next_slide()
        
        # Nhánh Real Score
        self.play(FadeIn(bg_real), FadeIn(lbl_real_eq))
        self.play(Create(arr_n_real), FadeIn(net_real), FadeIn(out_real))
        self.play(Create(link_real))
        self.next_slide()
        
        # Nhánh Fake Score
        self.play(FadeIn(bg_fake), FadeIn(lbl_fake_eq))
        self.play(Create(arr_n_fake), FadeIn(net_fake), FadeIn(out_fake))
        self.play(Create(link_fake))
        self.next_slide()
        
        self.play(FadeIn(aux_txt))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 71 — MODULE 68: LATENT DIFFUSION MODELS (VAE + PRIOR)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
from manim import Brace, DoubleArrow

class Module68_LDM_Prior(Slide):
    def construct(self):
        # 1. Background và Title
        self.camera.background_color = Theme.BG
        title = slide_title("Latent Diffusion Models")
        subtitle = Text("Variational autoencoder + score-based prior", font=Theme.FONT_BODY, font_size=24, color=Theme.SUCCESS)
        subtitle.next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG DIAGRAM (KHÔNG GIAN VAE & KHÔNG GIAN DIFFUSION)
        # ─────────────────────────────────────────────────────────────────────
        
        # === PHẦN 1: VARIATIONAL AUTOENCODER (BÊN TRÁI) ===
        box_x = RoundedBox(lines=["Data x"], width=1.4, height=0.8, fill_color=ManimColor("#263238"))
        box_enc = RoundedBox(lines=["Encoder"], width=1.6, height=0.8, fill_color=Theme.DIM)
        
        box_x_rec = RoundedBox(lines=["Reconst.", "p(x|z_0)"], width=1.4, height=0.8, fill_color=ManimColor("#263238"))
        box_dec = RoundedBox(lines=["Decoder"], width=1.6, height=0.8, fill_color=Theme.DIM)
        
        box_z0_q = RoundedBox(lines=["Latent", "q(z_0|x)"], width=1.6, height=1.0, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.PRIMARY)
        
        # Xếp vị trí nội bộ cho VAE (Tránh lệnh arrange để chống Lỗi 4)
        box_z0_q.move_to(ORIGIN)
        box_enc.next_to(box_z0_q, LEFT, buff=0.6).shift(UP * 0.6)
        box_x.next_to(box_enc, LEFT, buff=0.6)
        
        box_dec.next_to(box_z0_q, LEFT, buff=0.6).shift(DOWN * 0.6)
        box_x_rec.next_to(box_dec, LEFT, buff=0.6)
        
        vae_blocks = VGroup(box_x, box_enc, box_x_rec, box_dec, box_z0_q)
        
        # === PHẦN 2: DENOISING DIFFUSION PRIOR (BÊN PHẢI) ===
        diff_frame = RoundedRectangle(
            width=4.5, height=2.0, corner_radius=0.1, 
            stroke_color=Theme.SUCCESS, stroke_width=2,
            fill_color=ManimColor("#1A0020"), fill_opacity=0.8 # Màu nền tối tạo cảm giác "nhiễu"
        )
        
        # Vẽ các quỹ đạo nhiễu giả lập (Trajectories)
        trajectories = VGroup()
        for i in range(7):
            start_y = np.random.uniform(-0.8, 0.8)
            points = []
            steps = 20
            for j in range(steps + 1):
                alpha = j / steps
                # Hội tụ dần về 0 (Gaussian)
                curr_y = start_y * (1 - alpha) + np.random.normal(0, 0.1) * (1 - abs(2*alpha - 1))
                curr_x = diff_frame.get_left()[0] + (diff_frame.width * alpha)
                points.append([curr_x, curr_y, 0])
                
            path = VMobject().set_points_as_corners(points)
            path.make_smooth()
            # Gradient màu từ vàng sang tím
            color = interpolate_color(Theme.ACCENT_GOLD, ManimColor("#9C27B0"), i/6)
            path.set_stroke(color, width=1.5, opacity=0.6)
            trajectories.add(path)
            
        box_z0_p = RoundedBox(lines=["Latent", "p(z_0)"], width=1.4, height=1.0, fill_color=Theme.BOX_FILL_ALT, stroke_color=Theme.SUCCESS)
        box_z1_p = RoundedBox(lines=["Noise", "p(z_T)"], width=1.4, height=1.0, fill_color=Theme.DIM)
        
        box_z0_p.next_to(diff_frame, LEFT, buff=0)
        box_z1_p.next_to(diff_frame, RIGHT, buff=0)
        
        diff_blocks = VGroup(box_z0_p, diff_frame, trajectories, box_z1_p)
        
        # Định vị Diffusion Group nằm bên phải VAE Group
        diff_blocks.next_to(vae_blocks, RIGHT, buff=1.2)
        
        diagram_blocks = VGroup(vae_blocks, diff_blocks)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG NỘI DUNG TEXT (THAY ĐỔI THEO SCENE)
        # ─────────────────────────────────────────────────────────────────────
        
        # --- TEXT SCENE 1: MAIN IDEA ---
        idea_title = Text("Main Idea", font=Theme.FONT_BODY, font_size=28, color=ManimColor("#D81B60"), weight="BOLD")
        idea_b1 = Text("• Encoder maps the complex data to a compact embedding space.", font=Theme.FONT_BODY, font_size=22)
        idea_b2 = Text("• Diffusion models are strictly applied in this latent space.", font=Theme.FONT_BODY, font_size=22)
        idea_bullets = VGroup(idea_b1, idea_b2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        scene1_text = VGroup(idea_title, idea_bullets).arrange(DOWN, buff=0.3)
        
        # --- TEXT SCENE 2: ADVANTAGES ---
        adv_title = Text("Advantages", font=Theme.FONT_BODY, font_size=28, color=ManimColor("#D81B60"), weight="BOLD")
        adv_b1 = Text("(1) Near-Normal latent space ➔ Simpler denoising, Faster Synthesis!", font=Theme.FONT_BODY, font_size=22)
        adv_b1[0][24:60].set_color(ManimColor("#D81B60")).set_slant("ITALIC") # Bôi màu chữ đoạn kết quả
        
        adv_b2 = Text("(2) Tailored Autoencoders ➔ Universal application (Text, 3D, Graphs)!", font=Theme.FONT_BODY, font_size=22)
        adv_b2[0][24:65].set_color(ManimColor("#D81B60")).set_slant("ITALIC")
        
        adv_bullets = VGroup(adv_b1, adv_b2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        scene2_text = VGroup(adv_title, adv_bullets).arrange(DOWN, buff=0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM MEGA-GROUP VÀ KHỐNG CHẾ KÍCH THƯỚC (ANTI-ERROR)
        # ─────────────────────────────────────────────────────────────────────
        # Đưa Scene1_text vào làm chuẩn đo kích thước
        mega_group = VGroup(diagram_blocks, scene1_text).arrange(DOWN, buff=1.2)
        
        # Ép khung ngang & dọc (Trần 5.5 đảm bảo tuyệt đối không đè Title)
        mega_group.set_width(13.2)
        if mega_group.height > 5.5:
            mega_group.set_height(5.5)
            
        mega_group.center().shift(DOWN * 0.2)
        
        # Cho Scene 2 text đè đúng vị trí của Scene 1 text (Dùng để Transform)
        scene2_text.move_to(scene1_text, aligned_edge=UP)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: VẼ MŨI TÊN & NGOẶC (CHỈ THỰC HIỆN SAU KHI ĐÃ ĐỊNH VỊ)
        # ─────────────────────────────────────────────────────────────────────
        # Mũi tên nội bộ VAE
        arr_xe = Arrow(box_x.get_right(), box_enc.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_eq = Arrow(box_enc.get_right(), box_z0_q.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_qd = Arrow(box_z0_q.get_left(), box_dec.get_right(), buff=0.1, stroke_width=3, tip_length=0.15)
        arr_dr = Arrow(box_dec.get_left(), box_x_rec.get_right(), buff=0.1, stroke_width=3, tip_length=0.15)
        
        # KL Divergence Matching (Nối giữa VAE và Prior)
        arr_kl = DoubleArrow(box_z0_q.get_right(), box_z0_p.get_left(), buff=0.1, color=Theme.DIM, stroke_width=3)
        lbl_kl = MathTex(r"\text{KL}(q(\mathbf{z}_0|\mathbf{x}) || p(\mathbf{z}_0))", font_size=20).next_to(arr_kl, DOWN, buff=0.1)
        
        # Mũi tên quá trình Diffusion
        arr_fwd = Arrow(box_z0_p.get_top(), box_z1_p.get_top(), buff=0.2, color=Theme.DIM, stroke_width=2.5, tip_length=0.12)
        lbl_fwd = Text("Latent Space Forward Diffusion", font=Theme.FONT_BODY, font_size=16).next_to(arr_fwd, UP, buff=0.1)
        
        arr_rev = Arrow(box_z1_p.get_bottom(), box_z0_p.get_bottom(), buff=0.2, color=Theme.SUCCESS, stroke_width=2.5, tip_length=0.12)
        lbl_rev = Text("Latent Space Generative Denoising", font=Theme.FONT_BODY, font_size=16).next_to(arr_rev, DOWN, buff=0.1)
        
        arrows_group = VGroup(arr_xe, arr_eq, arr_qd, arr_dr, arr_kl, lbl_kl, arr_fwd, lbl_fwd, arr_rev, lbl_rev)
        
        # Vẽ Ngoặc gộp (Braces)
        brace_vae = Brace(vae_blocks, DOWN, buff=0.3, color=Theme.DIM)
        lbl_vae = Text("Variational Autoencoder", font=Theme.FONT_BODY, font_size=22).next_to(brace_vae, DOWN, buff=0.15)
        
        brace_diff = Brace(diff_blocks, DOWN, buff=0.3, color=Theme.DIM)
        lbl_diff = Text("Denoising Diffusion Prior", font=Theme.FONT_BODY, font_size=22).next_to(brace_diff, DOWN, buff=0.15)
        
        braces_group = VGroup(brace_vae, lbl_vae, brace_diff, lbl_diff)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # ─────────────────────────────────────────────────────────────────────
        
        self.play(Write(title), FadeIn(subtitle))
        self.next_slide()
        
        # 1. Trình bày khối VAE bên trái
        self.play(FadeIn(vae_blocks), Create(arrows_group[0:4]))
        self.play(GrowFromCenter(brace_vae), FadeIn(lbl_vae))
        self.next_slide()
        
        # 2. Trình bày khối Diffusion bên phải
        self.play(FadeIn(diff_blocks[0]), FadeIn(diff_blocks[3])) # Hiện 2 phân phối trước
        self.play(FadeIn(diff_blocks[1]), Create(diff_blocks[2], run_time=2.0)) # Khung và Trajectories
        self.play(Create(arr_fwd), FadeIn(lbl_fwd), Create(arr_rev), FadeIn(lbl_rev))
        self.play(GrowFromCenter(brace_diff), FadeIn(lbl_diff))
        self.next_slide()
        
        # 3. Kết nối hai không gian bằng KL Divergence
        self.play(Create(arr_kl), Write(lbl_kl))
        self.next_slide()
        
        # 4. Hiển thị Text Scene 1 (Main Idea)
        self.play(FadeIn(scene1_text))
        self.next_slide()
        
        # 5. Chuyển cảnh Text mượt mà sang Scene 2 (Advantages)
        self.play(ReplacementTransform(scene1_text, scene2_text))
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 72 — MODULE 69: TWO-STAGE TRAINING (LDM)  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

from manim import DashedLine, DoubleArrow

class Module69_TwoStageTraining(Slide):
    def construct(self):
        # 1. Background và Title ngang hàng (Khắc phục lỗi chồng lấn chữ)
        self.camera.background_color = Theme.BG
        
        title_main = Text("Latent Diffusion Models", font=Theme.FONT_TITLE, font_size=34, color=Theme.NEUTRAL)
        title_sub = Text(" — Two-stage Training", font=Theme.FONT_TITLE, font_size=24, color=Theme.SUCCESS)
        title_group = VGroup(title_main, title_sub).arrange(RIGHT, aligned_edge=DOWN, buff=0.15).to_corner(UL, buff=0.6)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: TEXT RÚT GỌN (SÚC TÍCH, NHƯỜNG CHỖ CHO ĐỒ HOẠ)
        # ─────────────────────────────────────────────────────────────────────
        b1 = Text("• Two-stage training: Train autoencoder first, then train the diffusion prior.", font=Theme.FONT_BODY, font_size=24)
        b2 = Text("• Focus on compression without perceptual loss in the autoencoder.", font=Theme.FONT_BODY, font_size=24)
        bullets = VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG DIAGRAM THEO LƯỚI TỌA ĐỘ (GRID ANCHORING)
        # Khắc phục hoàn toàn lỗi lệch cột giữa các hàng có kích thước khác nhau.
        # ─────────────────────────────────────────────────────────────────────
        # Trục X quy chuẩn cho 5 cột
        x_col = [-4.0, -1.8, 0.4, 2.6, 4.8]
        y_s1 = 1.0   # Tọa độ Y cho Stage 1
        y_s2 = -1.5  # Tọa độ Y cho Stage 2
        
        # === STAGE 1: AUTOENCODER ===
        b_x = RoundedBox(lines=["Data", "x"], width=1.2, height=1.0, fill_color=ManimColor("#263238")).move_to([x_col[0], y_s1, 0])
        b_E = RoundedBox(lines=["Encoder", "E"], width=1.4, height=1.0, fill_color=Theme.DIM).move_to([x_col[1], y_s1, 0])
        # Latent Z có màu nổi bật
        b_z = RoundedBox(lines=["Latent", "Z"], width=1.2, height=1.0, fill_color=Theme.ACCENT_GOLD, text_color=Theme.BOX_FILL).move_to([x_col[2], y_s1, 0])
        b_D = RoundedBox(lines=["Decoder", "D"], width=1.4, height=1.0, fill_color=Theme.DIM).move_to([x_col[3], y_s1, 0])
        b_xt = RoundedBox(lines=["Reconst.", "x~"], width=1.2, height=1.0, fill_color=ManimColor("#263238")).move_to([x_col[4], y_s1, 0])
        
        # Các nhãn bên trái Stage 1
        lbl_s1 = VGroup(
            Text("Stage 1:", font=Theme.FONT_BODY, font_size=20, weight="BOLD"),
            Text("Train Autoencoder", font=Theme.FONT_BODY, font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(b_x, LEFT, buff=0.6)
        
        # === STAGE 2: DIFFUSION PRIOR ===
        # Hộp Diffusion kéo dài từ cột 1 (Input) tới cột 3 (Latent Z)
        diff_w = (x_col[2] - x_col[0]) + 1.2
        diff_x = (x_col[0] + x_col[2]) / 2
        b_diff = RoundedBox(
            lines=["Generative Denoising Process", "(Latent Diffusion Model)"], 
            width=diff_w, height=1.2, fill_color=ManimColor("#1A0020"), stroke_color=Theme.SUCCESS
        ).move_to([diff_x, y_s2, 0])
        
        b_D2 = RoundedBox(lines=["Decoder D", "(Frozen)"], width=1.4, height=1.0, fill_color=Theme.DIM).move_to([x_col[3], y_s2, 0])
        b_new = RoundedBox(lines=["Generated", "Images"], width=1.2, height=1.0, fill_color=ManimColor("#263238")).move_to([x_col[4], y_s2, 0])
        
        # Các nhãn bên trái Stage 2
        lbl_s2 = VGroup(
            Text("Stage 2:", font=Theme.FONT_BODY, font_size=20, weight="BOLD"),
            Text("Train Latent\nDiffusion Model", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_RED)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(b_diff, LEFT, buff=0.6).align_to(lbl_s1, LEFT)
        
        # Đường đứt nét phân cách 2 Stage
        divider = DashedLine(
            start=[lbl_s1.get_left()[0], (y_s1 + y_s2)/2, 0], 
            end=[x_col[4] + 1.0, (y_s1 + y_s2)/2, 0], 
            color=Theme.DIM, stroke_width=2
        )
        
        diagram_boxes = VGroup(b_x, b_E, b_z, b_D, b_xt, lbl_s1, b_diff, b_D2, b_new, lbl_s2, divider)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM MEGA-GROUP VÀ ÉP KHUÔN AN TOÀN
        # ─────────────────────────────────────────────────────────────────────
        mega_group = VGroup(bullets, diagram_boxes).arrange(DOWN, buff=0.8)
        
        # Chốt chặn rộng <= 13.2, Cao <= 5.5
        mega_group.set_width(13.2)
        if mega_group.height > 5.5:
            mega_group.set_height(5.5)
            
        # Căn giữa và dịch xuống dưới sâu hơn một chút để tạo khoảng không trống thoáng đãng với tiêu đề
        mega_group.center().shift(DOWN * 0.45)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 4: VẼ MŨI TÊN LIÊN KẾT (CHỈ THỰC HIỆN KHI BOX ĐÃ CỐ ĐỊNH TỌA ĐỘ)
        # ─────────────────────────────────────────────────────────────────────
        # Mũi tên Stage 1
        arr_s1 = VGroup(
            Arrow(b_x.get_right(), b_E.get_left(), buff=0.1, stroke_width=3, tip_length=0.15),
            Arrow(b_E.get_right(), b_z.get_left(), buff=0.1, stroke_width=3, tip_length=0.15),
            Arrow(b_z.get_right(), b_D.get_left(), buff=0.1, stroke_width=3, tip_length=0.15),
            Arrow(b_D.get_right(), b_xt.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        )
        
        # Loss Label của Stage 1
        loss_lbl = Text("Perceptual\nReconstruction\nObjective", font=Theme.FONT_BODY, font_size=16, color=Theme.ACCENT_RED).next_to(b_xt, UP, buff=0.15)
        
        # Mũi tên Stage 2
        arr_s2 = VGroup(
            Arrow(b_diff.get_right(), b_D2.get_left(), buff=0.1, stroke_width=3, tip_length=0.15),
            Arrow(b_D2.get_right(), b_new.get_left(), buff=0.1, stroke_width=3, tip_length=0.15)
        )
        
        # Trục dọc kết nối Latent Z (Stage 1) xuống Diffusion Model (Stage 2)
        vert_arrow = DoubleArrow(
            start=b_z.get_bottom() + DOWN * 0.05, 
            end=[b_z.get_x(), b_diff.get_top()[1] - 0.05, 0], 
            color=Theme.PRIMARY, stroke_width=3
        )
        vert_lbl = Text("Latent embedding modeled\nwith Diffusion Model", font=Theme.FONT_BODY, font_size=14, color=Theme.PRIMARY)
        vert_lbl.next_to(vert_arrow, LEFT, buff=0.15)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # ─────────────────────────────────────────────────────────────────────
        
        # Hiển thị tiêu đề ngang hàng chuyên nghiệp
        self.play(Write(title_main), FadeIn(title_sub))
        self.play(FadeIn(bullets))
        self.next_slide()
        
        # 1. Vẽ Stage 1 (Autoencoder)
        self.play(FadeIn(lbl_s1), FadeIn(b_x))
        self.play(
            Create(arr_s1[0]), FadeIn(b_E),
            Create(arr_s1[1]), FadeIn(b_z)
        )
        self.play(
            Create(arr_s1[2]), FadeIn(b_D),
            Create(arr_s1[3]), FadeIn(b_xt)
        )
        self.play(FadeIn(loss_lbl))
        self.next_slide()
        
        # 2. Xuất hiện vạch kẻ ngang và Text kết nối Latent
        self.play(Create(divider))
        self.play(GrowArrow(vert_arrow), FadeIn(vert_lbl))
        self.next_slide()
        
        # 3. Vẽ Stage 2 (Diffusion)
        self.play(FadeIn(lbl_s2), FadeIn(b_diff))
        self.play(
            Create(arr_s2[0]), FadeIn(b_D2),
            Create(arr_s2[1]), FadeIn(b_new)
        )
        self.next_slide()
        
# ─────────────────────────────────────────────────────────────────────────────
# ██████╗  SECTION 73 — MODULE 70: MOMENTUM-BASED DIFFUSION  ██████╗
# ─────────────────────────────────────────────────────────────────────────────

import numpy as np
from manim import ValueTracker, DecimalNumber, always_redraw

class Module70_MomentumDiffusion(Slide):
    def construct(self):
        # 1. Background và Title
        self.camera.background_color = Theme.BG
        title = slide_title('"Momentum-based" diffusion')
        
        # Đẩy khối text xanh lá xuống sát đáy slide để tránh overlap hoàn toàn
        idea_txt = Text(
            "Main idea: Couple each data variable with a velocity variable.\nDefine the diffusion process in the augmented space.", 
            font=Theme.FONT_BODY, font_size=20, color=Theme.SUCCESS
        ).to_edge(DOWN, buff=0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 1: XÂY DỰNG KHÔNG GIAN MỞ RỘNG (EXTENDED SPACE TRAJECTORIES)
        # ─────────────────────────────────────────────────────────────────────
        # Khung cho Velocity (Nhiễu loạn)
        v_frame = RoundedRectangle(width=6.0, height=1.5, corner_radius=0.1, fill_color=Theme.BOX_FILL, fill_opacity=1, stroke_color=Theme.DIM)
        v_lbl = MathTex("v_t", font_size=24, color=Theme.ACCENT_RED).next_to(v_frame, LEFT, buff=0.2)
        v_desc = Text("Velocity (Highly Noisy)", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM).next_to(v_frame, UP, buff=0.1)
        
        # Tạo quỹ đạo dích dắc ngẫu nhiên cho V
        np.random.seed(42)
        v_points = []
        for x_val in np.linspace(-2.8, 2.8, 60):
            y_val = np.random.uniform(-0.5, 0.5)
            v_points.append([v_frame.get_center()[0] + x_val, v_frame.get_center()[1] + y_val, 0])
        v_path = VMobject().set_points_as_corners(v_points).set_stroke(Theme.ACCENT_RED, 2)
        
        group_v = VGroup(v_frame, v_lbl, v_desc, v_path)
        
        # Khung cho Data (Mượt mà)
        x_frame = RoundedRectangle(width=6.0, height=1.5, corner_radius=0.1, fill_color=Theme.BOX_FILL, fill_opacity=1, stroke_color=Theme.DIM)
        x_lbl = MathTex("x_t", font_size=24, color=Theme.PRIMARY).next_to(x_frame, LEFT, buff=0.2)
        x_desc = Text("Data (Smooth Denoising)", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM).next_to(x_frame, UP, buff=0.1)
        
        # Tạo quỹ đạo cong mượt cho X
        x_points = []
        for x_val in np.linspace(-2.8, 2.8, 40):
            y_val = 0.4 * np.sin(x_val * 2) # Dùng hàm Sin tạo đường mượt
            x_points.append([x_frame.get_center()[0] + x_val, x_frame.get_center()[1] + y_val, 0])
        x_path = VMobject().set_points_smoothly(x_points).set_stroke(Theme.PRIMARY, 3)
        
        group_x = VGroup(x_frame, x_lbl, x_desc, x_path)
        
        # Xếp 2 khung này lên nhau
        trajectories_group = VGroup(group_v, group_x).arrange(DOWN, buff=0.5)
        
        # Gắn Brace gộp chung
        brace_space = Brace(trajectories_group, LEFT, buff=0.5, color=Theme.NEUTRAL)
        lbl_space = Text("Extended\nSpace", font=Theme.FONT_BODY, font_size=18).next_to(brace_space, LEFT, buff=0.15)
        top_visual = VGroup(trajectories_group, brace_space, lbl_space)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 2: XÂY DỰNG MÔ PHỎNG TRẠNG THÁI (IMAGE & VELOCITY BOXES)
        # ─────────────────────────────────────────────────────────────────────
        # Tracker quản lý thời gian t (Từ 0.0 -> 1.0)
        t_tracker = ValueTracker(0.08)
        
        # Hộp chứa Data x_t
        img_box = Square(side_length=2.0, stroke_color=Theme.PRIMARY, stroke_width=2)
        img_lbl = MathTex("\text{Image } x_t", font_size=20).next_to(img_box, DOWN, buff=0.2)
        
        # Lớp nhiễu (Noise Overlay) phủ lên Image, độ mờ (opacity) phụ thuộc vào t
        noise_overlay_x = always_redraw(lambda: 
            Square(side_length=1.95, fill_color=ManimColor("#555555"), fill_opacity=t_tracker.get_value(), stroke_width=0)
            .move_to(img_box)
        )
        base_img = Square(side_length=1.95, fill_color=Theme.ACCENT_GOLD, fill_opacity=0.8, stroke_width=0).move_to(img_box)
        group_img = VGroup(base_img, noise_overlay_x, img_box, img_lbl)
        
        # Hộp chứa Velocity v_t (Luôn là nhiễu xám tĩnh)
        vel_box = Square(side_length=2.0, fill_color=ManimColor("#444444"), fill_opacity=0.9, stroke_color=Theme.ACCENT_RED, stroke_width=2)
        vel_lbl = MathTex("\text{Velocity } v_t", font_size=20).next_to(vel_box, DOWN, buff=0.2)
        group_vel = VGroup(vel_box, vel_lbl)
        
        # Biểu diễn thời gian t
        t_text = Text("t = ", font=Theme.FONT_BODY, font_size=28)
        t_number = always_redraw(lambda: DecimalNumber(t_tracker.get_value(), num_decimal_places=2, font_size=32).next_to(t_text, RIGHT, buff=0.1))
        group_time = VGroup(t_text, t_number)
        
        bottom_visual = VGroup(group_img, group_vel, group_time).arrange(RIGHT, buff=1.0)
        
        # Mũi tên tiến trình
        arr_process = Arrow(group_img.get_right(), group_vel.get_left(), buff=0.2, stroke_width=2)
        lbl_process = Text("Forward / Reverse", font=Theme.FONT_BODY, font_size=16, color=Theme.DIM).next_to(arr_process, UP, buff=0.1)
        bottom_visual.add(arr_process, lbl_process)
        
        # ─────────────────────────────────────────────────────────────────────
        # BƯỚC 3: GOM MEGA-GROUP VÀ ÉP KHUÔN AN TOÀN (ANTI-ERROR)
        # ─────────────────────────────────────────────────────────────────────
        mega_group = VGroup(top_visual, bottom_visual).arrange(DOWN, buff=0.8)
        
        # Thu nhỏ bớt chiều cao tối đa của sơ đồ để tạo không gian cho text ở dưới đáy slide
        mega_group.set_width(12.5)
        if mega_group.height > 4.5:
            mega_group.set_height(4.5)
            
        # Căn giữa và dịch nhẹ lên trên (UP * 0.3) để tránh va chạm với cả Title lẫn Đáy slide
        mega_group.center().shift(UP * 0.3)
        
        # ─────────────────────────────────────────────────────────────────────
        # KỊCH BẢN HIỂN THỊ ANIMATION
        # ─────────────────────────────────────────────────────────────────────
        self.play(Write(title))
        self.next_slide()
        
        # 1. Hiển thị Extended Space
        self.play(FadeIn(group_v[0:3]), FadeIn(group_x[0:3]))
        self.play(GrowFromCenter(brace_space), FadeIn(lbl_space))
        
        self.play(
            Create(v_path, run_time=2.5),
            Create(x_path, run_time=2.5)
        )
        self.next_slide()
        
        # 2. Hiển thị mô phỏng bên dưới
        self.play(FadeIn(group_img), FadeIn(group_vel))
        self.play(Create(arr_process), FadeIn(lbl_process), FadeIn(group_time))
        self.next_slide()
        
        # 3. Hiển thị khối lý thuyết xanh lá ở đáy slide
        self.play(FadeIn(idea_txt))
        self.next_slide()
        
        # 4. Chạy mô phỏng Forward Process
        self.play(t_tracker.animate.set_value(0.98), run_time=3.0, rate_func=rate_functions.smooth)
        self.next_slide()
        
        # 5. Chạy mô phỏng Reverse Process
        self.play(t_tracker.animate.set_value(0.00), run_time=3.0, rate_func=rate_functions.smooth)
        self.next_slide()

if __name__ == "__main__":
    print("Use:  manim -qh cvpr_tutorial.py Module1_Intro")
    print("  or: manim-slides render cvpr_tutorial.py Module1_Intro")