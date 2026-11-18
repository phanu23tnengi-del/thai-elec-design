# app.py
# ไฟล์ควบคุมหลักของแพลตฟอร์มออกแบบไฟฟ้าบ้านพักอาศัย (เชื่อมต่อ Logic จาก standards.py และ UI จาก ui_theme.py)

import math
import pandas as pd
import streamlit as st

from standards import (
    CABLE_AMPACITY_TABLES,
    DERATING_FACTORS,
    LAMP_TYPES,
    RCD_REQUIRED_ZONES,
    RESIDENTIAL_APPLIANCES,
    calculate_lamp_va,
    calculate_whole_house_demand,
    select_circuit_components,
    select_main_service,
)
from ui_theme import (
    apply_custom_theme,
    render_footer_warning,
    render_form_header,
    render_hero_banner,
    render_project_summary_card,
    render_sidebar_brand,
    render_sidebar_version,
    render_sld_card,
    style_schedule_table,
)

try:
    from pdf_exporter import generate_pdf_report
    HAS_PDF_EXPORTER = True
except ImportError:
    HAS_PDF_EXPORTER = False

# --- ตั้งค่าหน้าเว็บและโหลดธีมจาก ui_theme.py ---
st.set_page_config(
    page_title="ระบบออกแบบไฟฟ้าบ้านพักอาศัย วสท. 2564",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_custom_theme()

# --- ข้อมูลเริ่มต้นใน Session State ---
if "zones" not in st.session_state:
    st.session_state.zones = [
        {"zone_name": "ห้องนอน 1", "zone_type": "ห้องนอน/ห้องนั่งเล่น", "floor": "ชั้น 1 (ชั้นล่าง)", "outlets": 3, "lamp_type": "หลอด LED (ดาวน์ไลท์/หลอดกลม)", "lights": 4, "watt_per_light": 12, "length_m": 15},
        {"zone_name": "ห้องนอน 2", "zone_type": "ห้องนอน/ห้องนั่งเล่น", "floor": "ชั้น 2 ขึ้นไป", "outlets": 3, "lamp_type": "หลอด LED (ดาวน์ไลท์/หลอดกลม)", "lights": 4, "watt_per_light": 12, "length_m": 20},
        {"zone_name": "ห้องรับแขก", "zone_type": "ห้องนอน/ห้องนั่งเล่น", "floor": "ชั้น 1 (ชั้นล่าง)", "outlets": 6, "lamp_type": "หลอด LED (ดาวน์ไลท์/หลอดกลม)", "lights": 6, "watt_per_light": 12, "length_m": 15},
        {"zone_name": "ห้องครัว", "zone_type": "ห้องครัว", "floor": "ชั้น 1 (ชั้นล่าง)", "outlets": 4, "lamp_type": "หลอดยาว LED T8", "lights": 2, "watt_per_light": 18, "length_m": 20},
    ]

if "dedicated_loads" not in st.session_state:
    st.session_state.dedicated_loads = [
        {"name": "เครื่องปรับอากาศ 12,000 BTU", "category": "ac", "zone_type": "ห้องนอน/ห้องนั่งเล่น", "floor": "ชั้น 2 ขึ้นไป", "va": 1200, "length_m": 25, "force_rcd": False},
        {"name": "เครื่องทำน้ำอุ่น 4,500 W", "category": "heater_cooking", "zone_type": "ห้องน้ำ", "floor": "ชั้น 2 ขึ้นไป", "va": 4500, "length_m": 25, "force_rcd": True},
        {"name": "ปั๊มน้ำอัตโนมัติ 300 W", "category": "other", "zone_type": "ภายนอกอาคาร", "floor": "ชั้น 1 (ชั้นล่าง)", "va": 800, "length_m": 30, "force_rcd": True},
    ]

if "status_msg" not in st.session_state:
    st.session_state.status_msg = ""

# --- แถบเมนูและการตั้งค่าด้านซ้าย (Sidebar) ---
with st.sidebar:
    render_sidebar_brand()

    nav_page = st.radio(
        "เมนูหลัก",
        options=["🏠 หน้าภาพรวม", "📋 ตารางโหลด & มิเตอร์", "📕 รายงานผล & Export PDF"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("##### 📝 ข้อมูลโครงการ")
    project_name = st.text_input("ชื่อบ้าน / โครงการ", value="บ้านพักอาศัย 2 ชั้น")
    designer_name = st.text_input("ชื่อผู้ออกแบบ", value="นักศึกษาวิศวกรรมไฟฟ้า")

    st.markdown("##### ⚙️ ตั้งค่าโครงสร้างบ้าน")
    utility = st.radio(
        "เขตพื้นที่การไฟฟ้าฯ",
        options=["การไฟฟ้านครหลวง (MEA - ตารางที่ 3-4)", "การไฟฟ้าส่วนภูมิภาค (PEA - ตารางที่ 3-5)"],
    )
    install_method = st.selectbox("วิธีการเดินสายหลักในบ้าน", options=list(CABLE_AMPACITY_TABLES.keys()))
    grouping_label = st.selectbox("จำนวนวงจรในท่อเดียวกัน (ตารางที่ 5-8)", options=list(DERATING_FACTORS.keys()))
    derating_val = DERATING_FACTORS[grouping_label]

    st.divider()
    if st.button("🗑️ ล้างข้อมูลเริ่มออกแบบใหม่", use_container_width=True):
        st.session_state.zones = []
        st.session_state.dedicated_loads = []
        st.session_state.status_msg = "ล้างข้อมูลทั้งหมดเรียบร้อยแล้ว"
        st.rerun()

    render_sidebar_version()

# --- แสดงแบนเนอร์ด้านบน ---
render_hero_banner(project_name, designer_name)

if st.session_state.status_msg:
    st.success(st.session_state.status_msg)
    st.session_state.status_msg = ""

# --- ส่วนรับข้อมูลโซนห้องและเครื่องใช้ไฟฟ้า (แสดงในหน้าภาพรวม) ---
if nav_page == "🏠 หน้าภาพรวม":
    col1, col2 = st.columns(2)

    with col1:
        with st.form("add_zone_form", clear_on_submit=False):
            render_form_header("🏠 เพิ่มโซนห้องในบ้าน", "ℹ️ เต้ารับ & แสงสว่าง", theme="blue")
            z_name = st.text_input("ชื่อห้อง / บริเวณ", placeholder="เช่น ห้องนอน 1, ห้องรับแขก, โรงจอดรถ")
            c1, c2 = st.columns(2)
            z_type = c1.selectbox("ประเภทพื้นที่", ["ห้องนอน/ห้องนั่งเล่น", "ห้องครัว", "ห้องน้ำ", "โรงจอดรถ", "ภายนอกอาคาร"])
            z_floor = c2.selectbox("ชั้น", ["ชั้น 1 (ชั้นล่าง)", "ชั้น 2 ขึ้นไป"])
            lamp_choice = st.selectbox("ชนิดหลอดไฟ", options=list(LAMP_TYPES.keys()))

            c3, c4, c5, c6 = st.columns(4)
            n_outlets = c3.number_input("เต้ารับ (จุด)", min_value=0, value=4, step=1)
            n_lights = c4.number_input("หลอดไฟ (ดวง)", min_value=0, value=2, step=1)
            w_light = c5.number_input("วัตต์/ดวง", min_value=1, value=12, step=1)
            z_len = c6.number_input("ระยะสาย (ม.)", min_value=5, value=15, step=5)

            if st.form_submit_button("➕ เพิ่มห้องเข้าสู่แบบบ้าน", type="primary", use_container_width=True):
                if z_name.strip():
                    st.session_state.zones.append({
                        "zone_name": z_name.strip(),
                        "zone_type": z_type,
                        "floor": z_floor,
                        "outlets": n_outlets,
                        "lamp_type": lamp_choice,
                        "lights": n_lights,
                        "watt_per_light": w_light,
                        "length_m": z_len,
                    })
                    st.session_state.status_msg = f"✅ เพิ่มโซน '{z_name.strip()}' (ระยะสาย {z_len} ม.) เรียบร้อยแล้ว"
                    st.rerun()
                else:
                    st.warning("กรุณากรอก 'ชื่อห้อง / บริเวณ' ก่อนกดเพิ่มครับ")

    with col2:
        with st.form("add_special_form", clear_on_submit=False):
            render_form_header("🔌 เพิ่มเครื่องใช้ไฟฟ้าเฉพาะวงจร", "⚡ วงจรเฉพาะ", theme="green")
            preset_choice = st.selectbox("เลือกเครื่องใช้ไฟฟ้ามาตรฐานในบ้าน", options=list(RESIDENTIAL_APPLIANCES.keys()))
            preset_data = RESIDENTIAL_APPLIANCES[preset_choice]

            default_title = "" if "Custom" in preset_choice else preset_choice
            d_name = st.text_input("ชื่อเรียกในตู้ไฟ (Load Label)", value=default_title, placeholder="ระบุชื่ออุปกรณ์และห้องที่ติดตั้ง")

            c1, c2, c3, c4 = st.columns(4)
            d_type = c1.selectbox(
                "พื้นที่ติดตั้ง",
                ["ห้องนอน/ห้องนั่งเล่น", "ห้องครัว", "ห้องน้ำ", "โรงจอดรถ", "ภายนอกอาคาร"],
                index=["ห้องนอน/ห้องนั่งเล่น", "ห้องครัว", "ห้องน้ำ", "โรงจอดรถ", "ภายนอกอาคาร"].index(preset_data["zone"]),
            )
            d_floor = c2.selectbox("ชั้นที่ติดตั้ง", ["ชั้น 1 (ชั้นล่าง)", "ชั้น 2 ขึ้นไป"])
            d_va = c3.number_input("กำลังไฟ (VA/W)", min_value=100, value=preset_data["va"], step=100)
            d_len = c4.number_input("ระยะสาย (ม.)", min_value=5, value=20, step=5)

            if st.form_submit_button("➕ เพิ่มวงจรเครื่องใช้ไฟฟ้า", type="secondary", use_container_width=True):
                if d_name.strip():
                    st.session_state.dedicated_loads.append({
                        "name": d_name.strip(),
                        "category": preset_data["category"],
                        "zone_type": d_type,
                        "floor": d_floor,
                        "va": d_va,
                        "length_m": d_len,
                        "force_rcd": preset_data["rcd"],
                    })
                    st.session_state.status_msg = f"✅ เพิ่มวงจร '{d_name.strip()}' (ระยะสาย {d_len} ม.) เรียบร้อยแล้ว"
                    st.rerun()
                else:
                    st.warning("กรุณากรอก 'ชื่อเรียกในตู้ไฟ' ก่อนกดเพิ่มครับ")

    with st.expander("🛠️ จัดการ / ลบรายการห้องหรือเครื่องใช้ไฟฟ้าที่เพิ่มไว้", expanded=False):
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.markdown("**รายการโซนห้อง:**")
            for i, z in enumerate(st.session_state.zones):
                r1, r2 = st.columns([4, 1])
                r1.write(f"• {z['zone_name']} ({z['floor']}, {z['length_m']} ม.)")
                if r2.button("ลบ", key=f"del_z_{i}"):
                    st.session_state.zones.pop(i)
                    st.rerun()
        with m_col2:
            st.markdown("**รายการเครื่องใช้ไฟฟ้าเฉพาะ:**")
            for i, d in enumerate(st.session_state.dedicated_loads):
                r1, r2 = st.columns([4, 1])
                r1.write(f"• {d['name']} ({d['va']} VA, {d['length_m']} ม.)")
                if r2.button("ลบ", key=f"del_d_{i}"):
                    st.session_state.dedicated_loads.pop(i)
                    st.rerun()

# --- ประมวลผลวงจรย่อยตามมาตรฐาน วสท. 2564 (เรียกใช้ standards.py) ---
circuits = []
zone_va_map = {}
circuit_no = 1

for z in st.session_state.zones:
    z_total_va = 0.0
    if z["outlets"] > 0:
        outlet_va = z["outlets"] * 180
        z_total_va += outlet_va
        spec = select_circuit_components(outlet_va, install_method, z["length_m"], derating_val)
        need_rcd = (z["zone_type"] in RCD_REQUIRED_ZONES) or ("ชั้น 1" in z["floor"])
        circuits.append({
            "category": "receptacle",
            "short_label": z["zone_name"],
            "วงจรที่": f"C-{circuit_no:02d}",
            "ป้ายชื่อวงจร (ตู้ไฟ)": f"เต้ารับ - {z['zone_name']} ({z['floor']})",
            "รายละเอียดโหลด": f"{z['outlets']} จุด (180 VA/จุด)",
            "โหลด (VA)": outlet_va,
            "กระแส (A)": spec["i_load"],
            "เบรกเกอร์": spec["cb"],
            "ชนิดป้องกัน": "RCBO กันดูด 30mA" if need_rcd else "MCB ลูกย่อย",
            "สายไฟ (L, N)": spec["wire"],
            "สายดิน (G)": spec["ground"],
            "ท่อร้อยสาย": spec["conduit"],
            "แรงดันตก (%VD)": f"{spec['vd_pct']}% (อัปไซส์)" if spec["upsized_by_vd"] else f"{spec['vd_pct']}%",
        })
        circuit_no += 1

    if z["lights"] > 0:
        l_type = z.get("lamp_type", "หลอด LED (ดาวน์ไลท์/หลอดกลม)")
        light_va = calculate_lamp_va(l_type, z["watt_per_light"], z["lights"])
        z_total_va += light_va
        spec = select_circuit_components(light_va, install_method, z["length_m"], derating_val)
        need_rcd = z["zone_type"] == "ภายนอกอาคาร"
        circuits.append({
            "category": "lighting",
            "short_label": f"ไฟ {z['zone_name']}",
            "วงจรที่": f"C-{circuit_no:02d}",
            "ป้ายชื่อวงจร (ตู้ไฟ)": f"แสงสว่าง - {z['zone_name']} ({z['floor']})",
            "รายละเอียดโหลด": f"{z['lights']} ดวง ({l_type} {z['watt_per_light']}W)",
            "โหลด (VA)": light_va,
            "กระแส (A)": spec["i_load"],
            "เบรกเกอร์": spec["cb"],
            "ชนิดป้องกัน": "RCBO กันดูด 30mA" if need_rcd else "MCB ลูกย่อย",
            "สายไฟ (L, N)": spec["wire"],
            "สายดิน (G)": spec["ground"],
            "ท่อร้อยสาย": spec["conduit"],
            "แรงดันตก (%VD)": f"{spec['vd_pct']}% (อัปไซส์)" if spec["upsized_by_vd"] else f"{spec['vd_pct']}%",
        })
        circuit_no += 1

    if z_total_va > 0:
        zone_va_map[z["zone_name"]] = zone_va_map.get(z["zone_name"], 0.0) + z_total_va

for d in st.session_state.dedicated_loads:
    spec = select_circuit_components(d["va"], install_method, d["length_m"], derating_val)
    need_rcd = d.get("force_rcd", False) or (d["zone_type"] in ["ห้องน้ำ", "ภายนอกอาคาร", "ห้องครัว"])
    circuits.append({
        "category": d["category"],
        "short_label": d["name"].split("(")[0].strip()[:16],
        "วงจรที่": f"C-{circuit_no:02d}",
        "ป้ายชื่อวงจร (ตู้ไฟ)": f"{d['name']} ({d['floor']})",
        "รายละเอียดโหลด": "วงจรเฉพาะ 1 เครื่อง",
        "โหลด (VA)": d["va"],
        "กระแส (A)": spec["i_load"],
        "เบรกเกอร์": spec["cb"],
        "ชนิดป้องกัน": "RCBO กันดูด 30mA" if need_rcd else "MCB ลูกย่อย",
        "สายไฟ (L, N)": spec["wire"],
        "สายดิน (G)": spec["ground"],
        "ท่อร้อยสาย": spec["conduit"],
        "แรงดันตก (%VD)": f"{spec['vd_pct']}% (อัปไซส์)" if spec["upsized_by_vd"] else f"{spec['vd_pct']}%",
    })
    circuit_no += 1

# --- แสดงผลลัพธ์ผ่านคอมโพเนนต์ใน ui_theme.py ---
if circuits:
    calc_input = [{"category": c["category"], "โหลดรวม (VA)": c["โหลด (VA)"]} for c in circuits]
    demand_res = calculate_whole_house_demand(calc_input)
    main_res = select_main_service(demand_res["demand_amp"], utility)

    total_circuits = len(circuits)
    required_slots = math.ceil(total_circuits * 1.2)
    recommended_cu = next((s for s in [4, 6, 8, 10, 12, 14, 16, 18, 24] if s >= required_slots), 24)

    # 1. แสดงกราฟและแผนผัง SLD
    if nav_page in ["🏠 หน้าภาพรวม", "📋 ตารางโหลด & มิเตอร์"]:
        dash_left, dash_right = st.columns([1.15, 1])
        bar_items = list(zone_va_map.items())[:5] or [(c["short_label"], c["โหลด (VA)"]) for c in circuits[:5]]

        with dash_left:
            with st.container(border=True):
                render_project_summary_card(
                    num_rooms=len(st.session_state.zones),
                    num_appliances=len(st.session_state.dedicated_loads),
                    connected_va=demand_res["connected_va"],
                    demand_amp=demand_res["demand_amp"],
                    bar_items=bar_items,
                )
        with dash_right:
            with st.container(border=True):
                render_sld_card(circuits, main_res["meter"], main_res["main_cb"], recommended_cu)

    # 2. แสดงสรุประบบประธานและมิเตอร์
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("#### ⚡ สรุประบบประธาน เครื่องวัดหน่วยไฟฟ้า และตู้คอนซูเมอร์ยูนิต")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("ขนาดมิเตอร์ที่แนะนำ", main_res["meter"])
        m2.metric("เมนเบรกเกอร์ (Main CB)", main_res["main_cb"])
        m3.metric("ขนาดตู้ Consumer Unit", f"{recommended_cu} ช่อง", delta=f"ใช้งานจริง {total_circuits} วงจร", delta_color="off")
        m4.metric("โหลดใช้งานสูงสุด (Demand)", f"{demand_res['demand_va']:,.0f} VA", delta=f"{demand_res['demand_amp']} A", delta_color="off")
        st.info(f"**สเปกสายเมนเข้าตู้ Consumer Unit ({main_res['ref']}):** {main_res['main_wire']}")

        c_left, c_right = st.columns([1.2, 1])
        with c_left:
            with st.expander("📊 รายละเอียดการคิด Demand Factor (ตารางที่ 3-1 และ 3-3)", expanded=False):
                for k, v in demand_res["breakdown"].items():
                    st.write(f"- **{k}:** {v}")
        with c_right:
            with st.expander("✅ รายการตรวจสอบความปลอดภัยหน้างาน (วสท. 2564)", expanded=False):
                st.write("- **พิกัดตัดกระแสลัดวงจร (IC):** เมนเบรกเกอร์ต้องไม่ต่ำกว่า **10 kA** (ข้อ 3.5.2.3)")
                st.write("- **ระบบหลักดิน:** ปักแท่งทองแดงขนาด **5/8 นิ้ว (14.2 มม.)** และต่อฝาก N-G ที่ตู้เมนเท่านั้น (ข้อ 2.4.7, 4.3.1)")
                st.write("- **การแยกวงจร:** แยกแสงสว่าง เต้ารับ และไฟนอกบ้านออกจากกันเรียบร้อยแล้ว (ข้อ 3.1.4.1)")

    # 3. แสดงตาราง Load Schedule และปุ่ม Export PDF / Excel
    with st.container(border=True):
        st.markdown("#### 📋 ตารางโหลดและรายการอุปกรณ์วงจรย่อย (Residential Load Schedule)")
        df_export = pd.DataFrame(circuits).drop(columns=["category", "short_label"])
        st.dataframe(
            style_schedule_table(df_export),
            use_container_width=True,
            hide_index=True,
            column_config={
                "วงจรที่": st.column_config.TextColumn(width="small"),
                "ป้ายชื่อวงจร (ตู้ไฟ)": st.column_config.TextColumn(width="large"),
                "รายละเอียดโหลด": st.column_config.TextColumn(width="medium"),
            },
        )

        dl1, dl2 = st.columns(2)
        with dl1:
            if HAS_PDF_EXPORTER:
                pdf_bytes = generate_pdf_report(
                    project_name=project_name,
                    designer_name=designer_name,
                    utility=utility,
                    install_method=install_method,
                    demand_res=demand_res,
                    main_res=main_res,
                    cu_slots=recommended_cu,
                    circuits=circuits,
                )
                st.download_button(
                    label="📕 ดาวน์โหลดรายงานการออกแบบ (ไฟล์ PDF ขนาด A4)",
                    data=pdf_bytes,
                    file_name="Residential_Electrical_Design_EIT2564.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )
            else:
                st.info("💡 ตรวจสอบไฟล์ `pdf_exporter.py` เพื่อเปิดใช้งานปุ่มดาวน์โหลด PDF")
        with dl2:
            csv_data = df_export.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="📗 ดาวน์โหลดตาราง Load Schedule (ไฟล์ Excel / CSV)",
                data=csv_data,
                file_name="Residential_Load_Schedule_EIT2564.csv",
                mime="text/csv",
                use_container_width=True,
            )

    render_footer_warning()
else:
    st.warning("ยังไม่มีข้อมูลห้องในบ้าน กรุณาเพิ่มโซนห้องหรือเครื่องใช้ไฟฟ้าด้านบนครับ")