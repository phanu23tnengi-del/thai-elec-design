# pdf_exporter.py
import os
import urllib.request
from datetime import datetime
from fpdf import FPDF


def _prepare_thai_fonts():
    """เตรียมฟอนต์ภาษาไทยที่อ่านง่ายสบายตา (Sarabun -> Leelawadee UI -> Tahoma)"""
    os.makedirs("fonts", exist_ok=True)
    sarabun_reg = os.path.join("fonts", "Sarabun-Regular.ttf")
    sarabun_bold = os.path.join("fonts", "Sarabun-Bold.ttf")

    # ดาวน์โหลดฟอนต์ Sarabun (ฟอนต์มาตรฐานเอกสารไทย อ่านง่าย วรรณยุกต์ไม่ขาด) หากยังไม่มีในเครื่อง
    if not os.path.exists(sarabun_reg):
        try:
            urllib.request.urlretrieve(
                "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Regular.ttf",
                sarabun_reg,
            )
            urllib.request.urlretrieve(
                "https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Bold.ttf",
                sarabun_bold,
            )
        except Exception:
            pass

    candidates = [
        (sarabun_reg, sarabun_bold),
        (r"C:\Windows\Fonts\leelawui.ttf", r"C:\Windows\Fonts\leelauib.ttf"),
        (r"C:\Windows\Fonts\tahoma.ttf", r"C:\Windows\Fonts\tahomabd.ttf"),
    ]
    for reg, bold in candidates:
        if os.path.exists(reg):
            return reg, bold if os.path.exists(bold) else reg
    return None, None


def _wrap_text_lines(pdf: FPDF, text: str, max_width: float) -> list[str]:
    """ตัดข้อความยาวให้ขึ้นบรรทัดใหม่พอดีกับความกว้างคอลัมน์ โดยไม่ตัดตัวอักษรทิ้ง"""
    text = str(text)
    if pdf.get_string_width(text) <= max_width:
        return [text]

    lines = []
    current_line = ""
    for ch in text:
        test_line = current_line + ch
        if pdf.get_string_width(test_line) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = ch
    if current_line:
        lines.append(current_line.strip())
    return lines if lines else [""]


class ResidentialElectricalPDF(FPDF):
    def __init__(self, project_name: str, designer_name: str):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=16)
        self.project_name = project_name
        self.designer_name = designer_name
        self.reg_font, self.bold_font = _prepare_thai_fonts()

        if self.reg_font:
            self.add_font("ThaiFont", "", self.reg_font)
            self.add_font("ThaiFont", "B", self.bold_font)
            self.font_family_name = "ThaiFont"
        else:
            self.font_family_name = "Helvetica"

    def header(self):
        self.set_font(self.font_family_name, "B", 15)
        self.set_text_color(20, 40, 75)
        self.cell(0, 8, "รายการคำนวณและตารางโหลดระบบไฟฟ้าบ้านพักอยู่อาศัย (RESIDENTIAL LOAD SCHEDULE)", ln=True, align="C")

        self.set_font(self.font_family_name, "", 10)
        self.set_text_color(70, 80, 95)
        today_str = datetime.now().strftime("%d/%m/%Y")
        info_line = f"โครงการ: {self.project_name}   |   ผู้ออกแบบ: {self.designer_name}   |   วันที่: {today_str}   |   อ้างอิง: มาตรฐาน วสท. พ.ศ. 2564"
        self.cell(0, 6, info_line, ln=True, align="C")
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font(self.font_family_name, "", 8.5)
        self.set_text_color(110, 115, 125)
        self.cell(
            0,
            6,
            f"หมายเหตุ: ใช้สำหรับการออกแบบและประเมินเบื้องต้นตามมาตรฐาน วสท. พ.ศ. 2564 เท่านั้น  |  หน้า {self.page_no()}/{{nb}}",
            align="C",
        )


def generate_pdf_report(
    project_name: str,
    designer_name: str,
    utility: str,
    install_method: str,
    demand_res: dict,
    main_res: dict,
    cu_slots: int,
    circuits: list,
) -> bytes:
    """สร้างไฟล์ PDF รายงานการออกแบบไฟฟ้าแบบตารางขยายบรรทัดอัตโนมัติ (ข้อความครบไม่ขาด)"""
    pdf = ResidentialElectricalPDF(project_name, designer_name)
    pdf.alias_nb_pages()
    pdf.add_page()
    ff = pdf.font_family_name

    # --- ส่วนที่ 1: กล่องสรุประบบประธานและตู้ Consumer Unit ---
    pdf.set_fill_color(238, 244, 252)
    pdf.set_draw_color(185, 200, 220)
    pdf.set_text_color(20, 40, 75)
    pdf.set_font(ff, "B", 10.5)
    pdf.cell(0, 7.5, "  1. สรุปข้อมูลระบบประธาน เครื่องวัดหน่วยไฟฟ้า และตู้คอนซูเมอร์ยูนิต", border=1, ln=True, fill=True)

    pdf.set_text_color(30, 35, 45)
    pdf.set_font(ff, "", 9.5)
    col_w = 138.5  # ครึ่งหนึ่งของความกว้าง A4 แนวนอน (277 mm)
    pdf.cell(col_w, 6.5, f"  • เขตพื้นที่การไฟฟ้าฯ: {utility}", border="LR")
    pdf.cell(col_w, 6.5, f"  • ขนาดมิเตอร์ที่แนะนำ: {main_res['meter']}", border="R", ln=True)

    pdf.cell(col_w, 6.5, f"  • โหลดติดตั้งรวม (Connected Load): {demand_res['connected_va']:,.0f} VA", border="LR")
    pdf.cell(col_w, 6.5, f"  • พิกัดเมนเบรกเกอร์ (Main CB): {main_res['main_cb']}", border="R", ln=True)

    pdf.cell(col_w, 6.5, f"  • โหลดใช้งานสูงสุด (Demand Load): {demand_res['demand_va']:,.0f} VA ({demand_res['demand_amp']} A)", border="LR")
    pdf.cell(col_w, 6.5, f"  • ขนาดตู้ Consumer Unit แนะนำ: {cu_slots} ช่อง (รวมเผื่อ Spare ~20%)", border="R", ln=True)

    pdf.cell(0, 6.5, f"  • ข้อกำหนดสายเมน ({main_res['ref']}): {main_res['main_wire']}", border="LRB", ln=True)
    pdf.ln(4)

    # --- ส่วนที่ 2: ตาราง Load Schedule ---
    pdf.set_text_color(20, 40, 75)
    pdf.set_font(ff, "B", 10.5)
    pdf.cell(0, 7, "  2. ตารางรายละเอียดวงจรย่อย (Branch Circuit Schedule)", ln=True)

    # กำหนดความกว้างคอลัมน์รวม 277 mm (เผื่อพื้นที่ให้คอลัมน์ข้อความกว้างขึ้น)
    headers = [
        ("วงจร", 13),
        ("ป้ายชื่อวงจร (Load Label)", 56),
        ("รายละเอียดโหลด", 48),
        ("VA", 15),
        ("แอมป์", 13),
        ("เบรกเกอร์", 17),
        ("ชนิดป้องกัน", 29),
        ("สายไฟ (L,N)", 23),
        ("สายดิน", 19),
        ("ท่อร้อยสาย", 22),
        ("%VD", 22),
    ]

    def draw_table_header():
        pdf.set_fill_color(35, 65, 105)
        pdf.set_text_color(255, 255, 255)
        pdf.set_draw_color(180, 190, 205)
        pdf.set_font(ff, "B", 9)
        for title, w in headers:
            pdf.cell(w, 8, title, border=1, align="C", fill=True)
        pdf.ln()

    draw_table_header()

    line_h = 5.0
    pad_x = 1.8
    pad_y = 1.8

    for idx, c in enumerate(circuits):
        pdf.set_font(ff, "", 8.8)
        raw_values = [
            (c["วงจรที่"], "C"),
            (c["ป้ายชื่อวงจร (ตู้ไฟ)"], "L"),
            (c["รายละเอียดโหลด"], "L"),
            (f"{c['โหลด (VA)']:,.0f}", "R"),
            (f"{c['กระแส (A)']:.2f}", "R"),
            (c["เบรกเกอร์"], "C"),
            (c["ชนิดป้องกัน"], "C"),
            (c["สายไฟ (L, N)"], "C"),
            (c["สายดิน (G)"], "C"),
            (c["ท่อร้อยสาย"], "C"),
            (c["แรงดันตก (%VD)"], "C"),
        ]

        # คำนวณการตัดบรรทัดของแต่ละคอลัมน์ และหาความสูงสูงสุดของแถว
        wrapped_cols = []
        max_lines = 1
        for (val, align), (_, w) in zip(raw_values, headers):
            lines = _wrap_text_lines(pdf, val, w - (pad_x * 2))
            wrapped_cols.append((lines, align, w, val))
            if len(lines) > max_lines:
                max_lines = len(lines)

        row_h = (max_lines * line_h) + (pad_y * 2)

        # เช็กขึ้นหน้าใหม่พร้อมพิมพ์หัวตารางซ้ำหากใกล้สุดขอบกระดาษ
        if pdf.get_y() + row_h > pdf.page_break_trigger:
            pdf.add_page()
            draw_table_header()

        x_start = pdf.get_x()
        y_start = pdf.get_y()
        fill_color = (246, 249, 253) if idx % 2 == 1 else (255, 255, 255)
        pdf.set_draw_color(200, 208, 220)

        curr_x = x_start
        for lines, align, w, raw_val in wrapped_cols:
            # วาดพื้นหลังและกรอบเซลล์ให้สูงเท่ากันทั้งแถว
            pdf.set_fill_color(*fill_color)
            pdf.rect(curr_x, y_start, w, row_h, style="DF")

            # เน้นสีข้อความสำคัญให้อ่านง่ายไม่ลายตา
            if "RCBO" in str(raw_val):
                pdf.set_text_color(175, 35, 35)
                pdf.set_font(ff, "B", 8.8)
            elif "อัปไซส์" in str(raw_val):
                pdf.set_text_color(20, 90, 175)
                pdf.set_font(ff, "B", 8.8)
            else:
                pdf.set_text_color(30, 35, 45)
                pdf.set_font(ff, "", 8.8)

            # จัดกึ่งกลางแนวตั้งของข้อความในเซลล์
            text_block_h = len(lines) * line_h
            text_y = y_start + (row_h - text_block_h) / 2.0

            for line_i, line_txt in enumerate(lines):
                pdf.set_xy(curr_x + pad_x, text_y + (line_i * line_h))
                pdf.cell(w - (pad_x * 2), line_h, line_txt, border=0, align=align)

            curr_x += w

        pdf.set_xy(x_start, y_start + row_h)

    pdf.ln(4)

    # --- ส่วนที่ 3: ข้อกำหนดสำคัญหน้างาน ---
    if pdf.get_y() + 28 > pdf.page_break_trigger:
        pdf.add_page()

    pdf.set_text_color(20, 40, 75)
    pdf.set_font(ff, "B", 9.5)
    pdf.cell(0, 6, "3. ข้อกำหนดการติดตั้งและมาตรฐานความปลอดภัย (อ้างอิง วสท. พ.ศ. 2564):", ln=True)
    pdf.set_text_color(45, 50, 60)
    pdf.set_font(ff, "", 9)
    notes = [
        f"• วิธีการเดินสายวงจรย่อยหลัก: {install_method}",
        "• ระบบต่อลงดิน: ใช้หลักดินทองแดงขนาด 5/8 นิ้ว (14.2 มม.) ต่อฝากสาย N-G ที่ตู้เมนสวิตช์เพียงจุดเดียว (ข้อ 2.4.7 และ 4.3.1)",
        "• การป้องกันไฟดูด: วงจรเต้ารับชั้นล่าง ห้องครัว ห้องน้ำ โรงจอดรถ ภายนอกอาคาร และเครื่องทำน้ำอุ่น ต้องติดตั้งเครื่องตัดไฟรั่ว (RCBO) ขนาดไม่เกิน 30 mA (ข้อ 3.1.8)",
        "• การระบุป้ายวงจร: ให้พิมพ์ตาราง Load Schedule นี้ติดไว้ที่ฝาตู้คอนซูเมอร์ยูนิตอย่างถาวรเพื่อความสะดวกในการซ่อมบำรุง (ข้อ 3.3.11)",
    ]
    for n in notes:
        pdf.cell(0, 5.5, n, ln=True)

    return bytes(pdf.output())