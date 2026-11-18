# ui_theme.py
# โมดูลจัดการธีม CSS, การ์ดแสดงผล, กราฟแท่ง และแผนผัง Single-Line Diagram (SLD)

from datetime import datetime
import pandas as pd
import streamlit as st


def apply_custom_theme():
    """โหลดฟอนต์ Noto Sans Thai และตกแต่งธีม Midnight Blueprint Engineering โดยไม่ทับไอคอนระบบ"""
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;500;600;700&display=swap');

html, body, .stApp, .stMarkdown, .stDataFrame, input, select, textarea, button, p, label, h1, h2, h3, h4, h5, h6 {
    font-family: 'Noto Sans Thai', sans-serif !important;
}

/* คงฟอนต์ไอคอน Material Symbols ของ Streamlit ไม่ให้ทับตัวหนังสือ */
[data-testid="stIconMaterial"], .material-symbols-rounded, .material-icons {
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
}

/* พื้นหลังหลักลายพิมพ์เขียว */
.stApp {
    background-color: #081021;
    background-image:
        radial-gradient(circle at 85% 12%, rgba(37, 99, 235, 0.16), transparent 38%),
        radial-gradient(circle at 15% 85%, rgba(16, 185, 129, 0.08), transparent 40%),
        linear-gradient(rgba(30, 58, 138, 0.12) 1px, transparent 1px),
        linear-gradient(90deg, rgba(30, 58, 138, 0.12) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 36px 36px, 36px 36px;
    color: #f1f5f9;
}

header[data-testid="stHeader"] {
    background: rgba(8, 16, 33, 0.75) !important;
    backdrop-filter: blur(8px);
}

/* แถบ Sidebar ด้านซ้าย */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b152c 0%, #070e1d 100%) !important;
    border-right: 1px solid rgba(59, 130, 246, 0.22);
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background: transparent;
    border-radius: 10px;
    padding: 8px 12px;
    margin-bottom: 4px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: rgba(37, 99, 235, 0.15);
    border-color: rgba(59, 130, 246, 0.3);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
    background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important;
    border-color: #60a5fa !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
}

/* การ์ดคอนเทนเนอร์และฟอร์ม */
div[data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stForm"] {
    background: rgba(14, 24, 48, 0.88) !important;
    border: 1px solid rgba(56, 139, 253, 0.25) !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 24px rgba(2, 6, 23, 0.45);
}

/* ช่องกรอกข้อมูล */
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
    background-color: #0b1428 !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
}

/* ปุ่มสีฟ้า (Primary) */
button[kind="primaryFormSubmit"], button[kind="primary"] {
    background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    padding: 0.55rem 1rem !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.38) !important;
}
button[kind="primaryFormSubmit"]:hover, button[kind="primary"]:hover {
    filter: brightness(1.08);
}

/* ปุ่มสีเขียวมรกต (Secondary Form Submit) */
button[kind="secondaryFormSubmit"] {
    background: linear-gradient(90deg, #059669 0%, #10b981 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    padding: 0.55rem 1rem !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35) !important;
}
button[kind="secondaryFormSubmit"]:hover {
    filter: brightness(1.08);
}

/* ปุ่มดาวน์โหลด CSV */
div[data-testid="stDownloadButton"] button[kind="secondary"] {
    background: rgba(16, 185, 129, 0.15) !important;
    border: 1px solid rgba(16, 185, 129, 0.45) !important;
    color: #6ee7b7 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

details[data-testid="stExpander"] {
    background: rgba(14, 24, 48, 0.85) !important;
    border: 1px solid rgba(56, 139, 253, 0.22) !important;
    border-radius: 12px !important;
}
</style>
""",
        unsafe_allow_html=True,
    )


def render_sidebar_brand():
    """แสดงโลโก้บ้านสายฟ้าตามต้นแบบและชื่อผู้พัฒนาด้านบน Sidebar"""
    logo_svg = (
        '<svg viewBox="0 0 100 92" width="66" height="62" style="display:block; margin:0 auto 8px auto; filter:drop-shadow(0 4px 12px rgba(24,132,255,0.35));">'
        '<defs>'
        '<linearGradient id="boltGrad" x1="0%" y1="0%" x2="0%" y2="100%">'
        '<stop offset="0%" stop-color="#fde047"/>'
        '<stop offset="100%" stop-color="#f59e0b"/>'
        '</linearGradient>'
        '</defs>'
        '<path d="M 14 44 L 50 16 L 86 44" fill="none" stroke="#1884ff" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M 67 29 L 67 21" fill="none" stroke="#1884ff" stroke-width="7.5" stroke-linecap="round"/>'
        '<path d="M 24 37 L 24 75 L 35 75" fill="none" stroke="#1884ff" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M 76 37 L 76 75 L 65 75" fill="none" stroke="#1884ff" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/>'
        '<polygon points="48,38 58,38 51,55 61,55 44,82 49,61 40,61" fill="url(#boltGrad)" stroke="#f59e0b" stroke-width="1" stroke-linejoin="round"/>'
        '</svg>'
    )
    html = (
        '<div style="text-align:center; padding:6px 4px 14px 4px;">'
        f'{logo_svg}'
        '<div style="font-size:15px; font-weight:700; color:#f8fafc; line-height:1.35;">'
        'ระบบออกแบบ<br>ระบบไฟฟ้าบ้านพักอยู่อาศัย</div>'
        '<div style="font-size:12.5px; font-weight:600; color:#e2e8f0; margin-top:4px;">By Phanuwit Phonphimal</div>'
        '<div style="font-size:11.5px; color:#60a5fa; margin-top:2px;">(มาตรฐาน วสท. 2564)</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_sidebar_version():
    """แสดงป้ายสถานะเวอร์ชันด้านล่าง Sidebar"""
    html = (
        '<div style="margin-top:14px; padding:10px 12px; border-radius:12px;'
        'background:rgba(16, 185, 129, 0.1); border:1px solid rgba(16, 185, 129, 0.3);'
        'display:flex; align-items:center; gap:10px;">'
        '<span style="font-size:18px;">✅</span>'
        '<div>'
        '<div style="font-size:12px; font-weight:600; color:#6ee7b7;">เวอร์ชันปัจจุบัน</div>'
        '<div style="font-size:11px; color:#94a3b8;">v2.5 — Modular UI</div>'
        '</div></div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_hero_banner(project_name: str, designer_name: str):
    """แสดงแบนเนอร์หัวเว็บพร้อมข้อมูลโครงการและเวลาปัจจุบัน"""
    now_str = datetime.now().strftime("%d/%m/%Y  เวลา %H:%M น.")
    html = (
        '<div style="position:relative; overflow:hidden; border-radius:18px; padding:22px 26px; margin-bottom:18px;'
        'background:linear-gradient(115deg, #0b1938 0%, #112654 55%, #16336e 100%);'
        'border:1px solid rgba(96, 165, 250, 0.32); box-shadow:0 10px 30px rgba(2, 6, 23, 0.5);">'
        '<svg viewBox="0 0 320 140" style="position:absolute; right:0; top:0; height:100%; opacity:0.22; pointer-events:none;">'
        '<polygon points="140,120 210,55 295,55 295,120" fill="none" stroke="#60a5fa" stroke-width="1.5"/>'
        '<polygon points="175,55 210,25 275,25 295,55" fill="none" stroke="#93c5fd" stroke-width="1.5"/>'
        '<rect x="195" y="72" width="32" height="32" fill="none" stroke="#60a5fa" stroke-width="1.2"/>'
        '<rect x="242" y="72" width="36" height="48" fill="none" stroke="#60a5fa" stroke-width="1.2"/>'
        '<line x1="110" y1="120" x2="315" y2="120" stroke="#38bdf8" stroke-width="1.5"/>'
        '</svg>'
        '<div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">'
        '<div style="border-left:4px solid #3b82f6; padding-left:16px;">'
        '<div style="font-size:24px; font-weight:700; color:#ffffff; letter-spacing:-0.2px; line-height:1.25;">'
        'ระบบออกแบบระบบไฟฟ้าบ้านพักอยู่อาศัย (มาตรฐาน วสท. 2564)</div>'
        '<div style="font-size:13.5px; color:#93c5fd; margin-top:4px;">'
        'ออกแบบอย่างมืออาชีพ คำนวณอย่างแม่นยำ ใช้งานง่ายในที่เดียว</div>'
        '</div>'
        '<div style="display:flex; gap:8px; align-items:center;">'
        '<span style="background:rgba(15, 23, 42, 0.65); border:1px solid rgba(148, 163, 184, 0.3);'
        'color:#e2e8f0; padding:5px 12px; border-radius:20px; font-size:12px;">🌙 Blueprint Dark</span>'
        '<span style="background:rgba(16, 185, 129, 0.18); border:1px solid rgba(16, 185, 129, 0.5);'
        'color:#6ee7b7; padding:5px 14px; border-radius:20px; font-size:12px; font-weight:600;">● โครงการพร้อมใช้งาน</span>'
        '</div></div>'
        '<div style="margin-top:16px; display:inline-flex; flex-wrap:wrap; align-items:center; gap:14px;'
        'background:rgba(8, 16, 33, 0.65); border:1px solid rgba(59, 130, 246, 0.3);'
        'padding:8px 16px; border-radius:12px; font-size:13px;">'
        f'<span>🏠 <span style="color:#94a3b8;">ชื่อโครงการ :</span> <strong style="color:#ffffff;">{project_name}</strong></span>'
        '<span style="color:#334155;">|</span>'
        f'<span style="color:#94a3b8;">ผู้ออกแบบ : <span style="color:#e2e8f0;">{designer_name}</span></span>'
        '<span style="color:#334155;">|</span>'
        f'<span style="color:#94a3b8;">อัปเดต : <span style="color:#e2e8f0;">{now_str}</span></span>'
        '</div></div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_stepper(active_step: int = 4):
    """ตัดแถบขั้นตอนออกตามต้องการ (คงฟังก์ชันว่างไว้ป้องกัน Error หากมีการเรียกใช้)"""
    pass


def render_form_header(title: str, badge: str, theme: str = "blue"):
    """แสดงหัวข้อของการ์ดฟอร์มกรอกข้อมูล"""
    if theme == "green":
        bg = "rgba(16, 185, 129, 0.18)"
        border = "rgba(52, 211, 153, 0.4)"
        color = "#6ee7b7"
    else:
        bg = "rgba(37, 99, 235, 0.2)"
        border = "rgba(96, 165, 250, 0.4)"
        color = "#93c5fd"

    html = (
        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">'
        f'<div style="font-size:17px; font-weight:700; color:#f8fafc;">{title}</div>'
        f'<span style="background:{bg}; border:1px solid {border}; color:{color};'
        f'padding:2px 10px; border-radius:12px; font-size:11.5px;">{badge}</span>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_project_summary_card(
    num_rooms: int,
    num_appliances: int,
    connected_va: float,
    demand_amp: float,
    bar_items: list[tuple[str, float]],
):
    """แสดงการ์ด KPI 4 ใบ และกราฟแท่งโหลดตามโซนห้อง"""
    st.markdown(
        '<div style="font-size:17px; font-weight:700; color:#f8fafc; margin-bottom:12px;">📊 สรุปข้อมูลโครงการ</div>',
        unsafe_allow_html=True,
    )

    kpi_html = (
        '<div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:10px; margin-bottom:16px;">'
        '<div style="background:linear-gradient(145deg, rgba(37,99,235,0.35), rgba(29,78,216,0.18));'
        'border:1px solid rgba(96,165,250,0.45); border-radius:12px; padding:12px 8px; text-align:center;">'
        '<div style="font-size:20px;">🏠</div>'
        '<div style="font-size:11.5px; color:#cbd5e1; margin-top:2px;">จำนวนห้อง</div>'
        f'<div style="font-size:18px; font-weight:700; color:#60a5fa;">{num_rooms} ห้อง</div>'
        '</div>'
        '<div style="background:linear-gradient(145deg, rgba(16,185,129,0.32), rgba(5,150,105,0.16));'
        'border:1px solid rgba(52,211,153,0.45); border-radius:12px; padding:12px 8px; text-align:center;">'
        '<div style="font-size:20px;">🔌</div>'
        '<div style="font-size:11.5px; color:#cbd5e1; margin-top:2px;">เครื่องใช้ไฟฟ้า</div>'
        f'<div style="font-size:18px; font-weight:700; color:#34d399;">{num_appliances} รายการ</div>'
        '</div>'
        '<div style="background:linear-gradient(145deg, rgba(245,158,11,0.32), rgba(217,119,6,0.16));'
        'border:1px solid rgba(251,191,36,0.45); border-radius:12px; padding:12px 8px; text-align:center;">'
        '<div style="font-size:20px;">⚡</div>'
        '<div style="font-size:11.5px; color:#cbd5e1; margin-top:2px;">โหลดติดตั้งรวม</div>'
        f'<div style="font-size:17px; font-weight:700; color:#fbbf24;">{connected_va:,.0f} VA</div>'
        '</div>'
        '<div style="background:linear-gradient(145deg, rgba(139,92,246,0.35), rgba(109,40,217,0.18));'
        'border:1px solid rgba(167,139,250,0.45); border-radius:12px; padding:12px 8px; text-align:center;">'
        '<div style="font-size:20px;">🧭</div>'
        '<div style="font-size:11.5px; color:#cbd5e1; margin-top:2px;">กระแสใช้งาน (DF)</div>'
        f'<div style="font-size:18px; font-weight:700; color:#c4b5fd;">{demand_amp:.1f} A</div>'
        '</div></div>'
    )
    st.markdown(kpi_html, unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:13.5px; font-weight:600; color:#e2e8f0; margin-bottom:8px;">📶 โหลดตามโซนห้อง (VA)</div>',
        unsafe_allow_html=True,
    )

    max_va = max([v for _, v in bar_items], default=1)
    bar_colors = [
        "linear-gradient(180deg, #60a5fa 0%, #2563eb 100%)",
        "linear-gradient(180deg, #34d399 0%, #059669 100%)",
        "linear-gradient(180deg, #fbbf24 0%, #d97706 100%)",
        "linear-gradient(180deg, #a78bfa 0%, #7c3aed 100%)",
        "linear-gradient(180deg, #38bdf8 0%, #0284c7 100%)",
    ]

    bars_html = ""
    for idx, (label, val) in enumerate(bar_items):
        pct = max(14, int((val / max_va) * 100))
        bg = bar_colors[idx % len(bar_colors)]
        bars_html += (
            '<div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-end; height:125px;">'
            f'<div style="font-size:11.5px; font-weight:600; color:#f8fafc; margin-bottom:4px;">{val:,.0f}</div>'
            f'<div style="width:52%; max-width:48px; height:{pct}%; background:{bg}; border-radius:7px 7px 3px 3px; box-shadow:0 4px 12px rgba(0,0,0,0.35);"></div>'
            f'<div style="font-size:11.5px; color:#cbd5e1; margin-top:6px; text-align:center; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:95px;">{label}</div>'
            '</div>'
        )

    chart_html = (
        '<div style="background:rgba(8, 16, 33, 0.65); border:1px solid rgba(51, 65, 85, 0.6);'
        'border-radius:12px; padding:12px 10px 8px 10px; display:flex; align-items:flex-end; gap:6px;">'
        f'{bars_html}</div>'
    )
    st.markdown(chart_html, unsafe_allow_html=True)


def render_sld_card(circuits: list, meter_str: str, main_cb_str: str, recommended_cu: int):
    """วาดแผนผังระบบไฟฟ้าเส้นเดี่ยว (Single-Line Diagram SVG) แบบเรียลไทม์"""
    header_html = (
        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">'
        '<div style="font-size:17px; font-weight:700; color:#f8fafc;">📐 แบบจำลองระบบไฟฟ้า (Single-Line)</div>'
        '<span style="font-size:11.5px; color:#60a5fa;">อัปเดตอัตโนมัติ</span>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)

    total_circuits = len(circuits)
    shown_circuits = circuits[:5]
    n_show = len(shown_circuits)
    svg_w = 500
    svg_h = 248
    meter_txt = meter_str.split("(")[0].strip() + "A"
    main_cb_txt = main_cb_str.split("(")[0].strip()

    branches_svg = ""
    if n_show > 0:
        margin_x = 55
        step_x = (svg_w - 2 * margin_x) / max(1, n_show - 1) if n_show > 1 else 0
        first_x = margin_x if n_show > 1 else svg_w / 2
        last_x = svg_w - margin_x if n_show > 1 else svg_w / 2

        branches_svg += f'<line x1="{first_x}" y1="112" x2="{last_x}" y2="112" stroke="#60a5fa" stroke-width="2"/>'

        for i, c in enumerate(shown_circuits):
            cx = first_x + i * step_x
            cb_short = c["เบรกเกอร์"].replace(" ", "")
            is_rcd = "RCBO" in c["ชนิดป้องกัน"]
            cb_border = "#f87171" if is_rcd else "#60a5fa"
            prot_color = "#fca5a5" if is_rcd else "#93c5fd"
            prot_lbl = "RCBO" if is_rcd else "MCB"
            lbl = c["short_label"][:11]

            branches_svg += (
                f'<line x1="{cx}" y1="112" x2="{cx}" y2="132" stroke="#60a5fa" stroke-width="1.6"/>'
                f'<rect x="{cx - 26}" y="132" width="52" height="34" rx="6" fill="#0f1e3d" stroke="{cb_border}" stroke-width="1.5"/>'
                f'<text x="{cx}" y="147" fill="#f8fafc" font-size="10.5" font-weight="600" text-anchor="middle">{cb_short}</text>'
                f'<text x="{cx}" y="160" fill="{prot_color}" font-size="8.5" text-anchor="middle">{prot_lbl}</text>'
                f'<line x1="{cx}" y1="166" x2="{cx}" y2="188" stroke="#60a5fa" stroke-width="1.6"/>'
                f'<circle cx="{cx}" cy="177" r="2.5" fill="#38bdf8"/>'
                f'<rect x="{cx - 38}" y="188" width="76" height="32" rx="7" fill="#13254b" stroke="#3b82f6" stroke-width="1.3"/>'
                f'<text x="{cx}" y="208" fill="#e2e8f0" font-size="10" text-anchor="middle">{lbl}</text>'
            )

    extra_note = f"แสดง {n_show} จากทั้งหมด {total_circuits} วงจร" if total_circuits > n_show else f"ครบทั้ง {total_circuits} วงจร"
    sld_html = (
        '<div style="background-color:#091326;'
        'background-image:linear-gradient(rgba(59,130,246,0.12) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.12) 1px, transparent 1px);'
        'background-size:20px 20px;'
        'border:1px solid rgba(59,130,246,0.28); border-radius:12px; padding:8px; text-align:center;">'
        f'<svg viewBox="0 0 {svg_w} {svg_h}" width="100%" style="max-height:245px;">'
        '<rect x="195" y="10" width="110" height="32" rx="8" fill="#172b56" stroke="#60a5fa" stroke-width="1.6"/>'
        f'<text x="250" y="30" fill="#ffffff" font-size="12" font-weight="700" text-anchor="middle">มิเตอร์ {meter_txt}</text>'
        '<line x1="250" y1="42" x2="250" y2="62" stroke="#60a5fa" stroke-width="2"/>'
        '<circle cx="250" cy="52" r="3" fill="#38bdf8"/>'
        '<rect x="190" y="62" width="120" height="30" rx="7" fill="#0f2942" stroke="#34d399" stroke-width="1.6"/>'
        f'<text x="250" y="81" fill="#6ee7b7" font-size="11" font-weight="700" text-anchor="middle">Main {main_cb_txt}</text>'
        '<line x1="250" y1="92" x2="250" y2="112" stroke="#60a5fa" stroke-width="2"/>'
        f'{branches_svg}'
        f'<text x="250" y="240" fill="#64748b" font-size="10" text-anchor="middle">ตู้ Consumer Unit แนะนำ {recommended_cu} ช่อง ({extra_note})</text>'
        '</svg></div>'
    )
    st.markdown(sld_html, unsafe_allow_html=True)


def style_schedule_table(df_in: pd.DataFrame):
    """จัดสีตาราง Load Schedule ให้อ่านง่าย"""
    def highlight_protection(val):
        if "RCBO" in str(val):
            return "background-color: rgba(239, 68, 68, 0.2); color: #fca5a5; font-weight: 600;"
        return "color: #93c5fd;"

    def highlight_vd(val):
        if "อัปไซส์" in str(val):
            return "background-color: rgba(59, 130, 246, 0.22); color: #93c5fd; font-weight: 600;"
        return ""

    return (
        df_in.style
        .map(highlight_protection, subset=["ชนิดป้องกัน"])
        .map(highlight_vd, subset=["แรงดันตก (%VD)"])
        .format({"โหลด (VA)": "{:,.0f}", "กระแส (A)": "{:.2f}"})
    )


def render_footer_warning():
    """แสดงแถบแจ้งเตือนมาตรฐานด้านล่างสุด"""
    html = (
        '<div style="margin-top:12px; padding:12px 18px; border-radius:12px;'
        'background:rgba(120, 53, 15, 0.25); border:1px solid rgba(245, 158, 11, 0.45);'
        'color:#fbbf24; font-size:13px; display:flex; align-items:center; gap:10px;">'
        '<span style="font-size:18px;">⚠️</span>'
        '<span>กรุณาตรวจสอบการคำนวณและการติดตั้งให้เป็นไปตามมาตรฐานการติดตั้งทางไฟฟ้าสำหรับประเทศไทย (วสท. พ.ศ. 2564) อย่างเคร่งครัด</span>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)