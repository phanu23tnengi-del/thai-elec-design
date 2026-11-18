# standards.py
# ฐานข้อมูลและตรรกะการออกแบบระบบไฟฟ้าสำหรับบ้านพักอยู่อาศัย ตามมาตรฐาน วสท. พ.ศ. 2564

NOMINAL_VOLTAGE = 230  # แรงดันไฟฟ้าระบุ 1 เฟส ของประเทศไทย (ข้อ 1.92)
STANDARD_BREAKERS = [16, 20, 25, 32, 40, 50]  # พิกัดเบรกเกอร์ลูกย่อยไม่เกิน 50A (ข้อ 3.1.2)

# พิกัดกระแสสายทองแดง หุ้มฉนวน PVC 70°C 1 เฟส 2 ตัวนำกระแส แยกตามกลุ่มการติดตั้ง (ตารางที่ 5-20 และ 5-27)
# หน่วย: {ขนาดสาย (ตร.มม.): พิกัดกระแส (แอมแปร์)}
CABLE_AMPACITY_TABLES = {
    "กลุ่มที่ 2: เดินในช่องเดินสายหรือท่อเกาะผนัง/ฝ้า/ในผนังคอนกรีต": {
        2.5: 21,
        4.0: 28,
        6.0: 36,
        10.0: 49,
        16.0: 66,
        25.0: 86,
        35.0: 106,
        50.0: 128,
    },
    "กลุ่มที่ 1: เดินสายในช่องเดินสาย/ท่อ ภายในผนังหรือเพดานที่เป็นฉนวนความร้อน": {
        2.5: 17,
        4.0: 23,
        6.0: 30,
        10.0: 40,
        16.0: 53,
        25.0: 70,
        35.0: 86,
        50.0: 104,
    },
    "กลุ่มที่ 3: เดินเกาะผนังหรือเดินในอากาศชิดผนัง": {
        2.5: 24,
        4.0: 32,
        6.0: 41,
        10.0: 56,
        16.0: 74,
        25.0: 96,
        35.0: 119,
        50.0: 144,
    },
    "กลุ่มที่ 4 (ลูกถ้วยแนวนอน): สายแกนเดี่ยววางเรียงบนลูกถ้วย แนวนอน": {
        2.5: 29,
        4.0: 39,
        6.0: 50,
        10.0: 70,
        16.0: 93,
        25.0: 120,
        35.0: 149,
        50.0: 182,
    },
    "กลุ่มที่ 4 (ลูกถ้วยแนวตั้ง): สายแกนเดี่ยววางเรียงบนลูกถ้วย แนวตั้ง": {
        2.5: 26,
        4.0: 35,
        6.0: 45,
        10.0: 63,
        16.0: 84,
        25.0: 108,
        35.0: 134,
        50.0: 164,
    },
    "กลุ่มที่ 5: เดินในท่อหรือรางใต้ดิน (ตารางที่ 5-27)": {
        2.5: 24,
        4.0: 32,
        6.0: 40,
        10.0: 54,
        16.0: 71,
        25.0: 91,
        35.0: 110,
        50.0: 131,
    },
}

# ค่าความต้านทานไฟฟ้ากระแสสลับของสายทองแดงที่ 70°C (โอห์ม/กม.) สำหรับคำนวณแรงดันตก (ข้อ 3.6)
CABLE_RESISTANCE_OHM_KM = {
    2.5: 8.87,
    4.0: 5.52,
    6.0: 3.69,
    10.0: 2.19,
    16.0: 1.38,
    25.0: 0.87,
    35.0: 0.63,
    50.0: 0.47,
}

# ตัวคูณปรับค่าขนาดกระแสเมื่อเดินสายหลายวงจรในท่อเดียวกัน (ตารางที่ 5-8)
DERATING_FACTORS = {
    "1 วงจรในท่อ (ปกติ)": 1.00,
    "2 วงจรในท่อเดียวกัน": 0.80,
    "3 วงจรในท่อเดียวกัน": 0.70,
    "4-5 วงจรในท่อเดียวกัน": 0.65,
}

# ขนาดต่ำสุดของสายดินบริภัณฑ์ไฟฟ้าตามพิกัดเบรกเกอร์ (ตารางที่ 4-2)
GROUND_WIRE_TABLE = [
    (16, 1.5),
    (20, 2.5),
    (40, 4.0),
    (70, 6.0),
    (100, 10.0),
]

# ขนาดท่อร้อยสายไฟแนะนำสำหรับวงจรย่อย 1 วงจร (สาย L, N + สายดิน G รวม 3 เส้น, พื้นที่หน้าตัดไม่เกิน 40% ตารางที่ 5-3)
CONDUIT_SIZE_BY_WIRE = {
    2.5: '1/2" (15 มม.)',
    4.0: '1/2" (15 มม.)',
    6.0: '3/4" (20 มม.)',
    10.0: '3/4" (20 มม.)',
    16.0: '1" (25 มม.)',
    25.0: '1-1/4" (32 มม.)',
}

RCD_REQUIRED_ZONES = ["ห้องครัว", "ห้องน้ำ", "โรงจอดรถ", "ภายนอกอาคาร"]

# ชนิดหลอดไฟในบ้านพักอาศัย
LAMP_TYPES = {
    "หลอด LED (ดาวน์ไลท์/หลอดกลม)": {"default_w": 12, "ballast_w": 0, "ballast_ratio": 0.0, "pf": 0.90},
    "หลอดยาว LED T8": {"default_w": 18, "ballast_w": 0, "ballast_ratio": 0.0, "pf": 0.90},
    "หลอดผอม T5": {"default_w": 28, "ballast_w": 3, "ballast_ratio": 0.0, "pf": 0.95},
    "หลอดประหยัดไฟ (CFL)": {"default_w": 15, "ballast_w": 0, "ballast_ratio": 0.0, "pf": 0.55},
    "หลอดฟลูออเรสเซนต์ + LPF บัลลาสต์": {"default_w": 36, "ballast_w": 10, "ballast_ratio": 0.0, "pf": 0.50},
    "หลอดฟลูออเรสเซนต์ + HPF บัลลาสต์": {"default_w": 36, "ballast_w": 10, "ballast_ratio": 0.0, "pf": 0.85},
    "หลอด HID (ไฟสนาม/โรงรถ) + LPF": {"default_w": 250, "ballast_w": 0, "ballast_ratio": 0.15, "pf": 0.50},
    "หลอด HID (ไฟสนาม/โรงรถ) + HPF": {"default_w": 250, "ballast_w": 0, "ballast_ratio": 0.15, "pf": 0.85},
}

# Preset เครื่องใช้ไฟฟ้าเฉพาะทางในบ้านพักอาศัย
RESIDENTIAL_APPLIANCES = {
    "เครื่องปรับอากาศ 9,000 BTU": {"va": 900, "category": "ac", "zone": "ห้องนอน/ห้องนั่งเล่น", "rcd": False},
    "เครื่องปรับอากาศ 12,000 BTU": {"va": 1200, "category": "ac", "zone": "ห้องนอน/ห้องนั่งเล่น", "rcd": False},
    "เครื่องปรับอากาศ 18,000 BTU": {"va": 1800, "category": "ac", "zone": "ห้องนอน/ห้องนั่งเล่น", "rcd": False},
    "เครื่องปรับอากาศ 24,000 BTU": {"va": 2400, "category": "ac", "zone": "ห้องนอน/ห้องนั่งเล่น", "rcd": False},
    "เครื่องทำน้ำอุ่น 3,500 W": {"va": 3500, "category": "heater_cooking", "zone": "ห้องน้ำ", "rcd": True},
    "เครื่องทำน้ำอุ่น 4,500 W": {"va": 4500, "category": "heater_cooking", "zone": "ห้องน้ำ", "rcd": True},
    "เครื่องทำน้ำร้อน 6,000 W": {"va": 6000, "category": "heater_cooking", "zone": "ห้องน้ำ", "rcd": True},
    "เตาแม่เหล็กไฟฟ้า / เตาอบครัว": {"va": 3000, "category": "heater_cooking", "zone": "ห้องครัว", "rcd": True},
    "ปั๊มน้ำอัตโนมัติ 300 W (รวมกระแสสตาร์ท)": {"va": 800, "category": "other", "zone": "ภายนอกอาคาร", "rcd": True},
    "เครื่องซักผ้า / เครื่องอบผ้า": {"va": 2200, "category": "other", "zone": "ห้องครัว", "rcd": True},
    "เครื่องชาร์จรถยนต์ไฟฟ้า EV Charger 7.4 kW (32A)": {"va": 7400, "category": "other", "zone": "โรงจอดรถ", "rcd": True},
    "กรอกค่ากำลังไฟฟ้าเอง (Custom)": {"va": 1500, "category": "other", "zone": "ห้องนอน/ห้องนั่งเล่น", "rcd": False},
}


def calculate_lamp_va(lamp_type: str, watt_per_lamp: float, quantity: int) -> float:
    spec = LAMP_TYPES[lamp_type]
    loss = spec["ballast_w"] + (watt_per_lamp * spec["ballast_ratio"])
    va_per_lamp = (watt_per_lamp + loss) / spec["pf"]
    return round(va_per_lamp * quantity, 2)


def calculate_voltage_drop_pct(i_load: float, length_m: float, wire_size: float) -> float:
    """คำนวณเปอร์เซ็นต์แรงดันตกสำหรับระบบ 1 เฟส 230V"""
    r_ohm_km = CABLE_RESISTANCE_OHM_KM.get(wire_size, 8.87)
    vd_volt = (2 * i_load * length_m * r_ohm_km) / 1000.0
    return round((vd_volt / NOMINAL_VOLTAGE) * 100.0, 2)


def select_circuit_components(
    load_va: float,
    install_method: str,
    length_m: float = 15.0,
    derating_factor: float = 1.0,
    max_branch_vd_pct: float = 3.0,
) -> dict:
    """คำนวณกระแส เลือกเบรกเกอร์ ขนาดสายไฟ (รวม Derating & Voltage Drop) สายดิน และท่อร้อยสาย"""
    i_load = load_va / NOMINAL_VOLTAGE

    # 1. เลือกขนาดเบรกเกอร์ (ต้องไม่ต่ำกว่าโหลดสูงสุด - ข้อ 3.1.4.2)
    selected_cb = None
    for cb in STANDARD_BREAKERS:
        if cb >= i_load:
            selected_cb = cb
            break

    if selected_cb is None:
        return {
            "i_load": round(i_load, 2),
            "cb": "เกิน 50A (แยกวงจร)",
            "wire": "-",
            "wire_num": 0,
            "derated_amp": "-",
            "vd_pct": 0.0,
            "upsized_by_vd": False,
            "ground": "-",
            "conduit": "-",
        }

    # 2. เลือกขนาดสายไฟตามพิกัดกระแสสุทธิ (หลังคูณ Derating Factor)
    ampacity_table = CABLE_AMPACITY_TABLES[install_method]
    selected_wire = None
    effective_ampacity = 0.0

    for wire_size, base_amp in ampacity_table.items():
        derated_amp = base_amp * derating_factor
        if wire_size >= 2.5 and derated_amp >= selected_cb:
            selected_wire = wire_size
            effective_ampacity = derated_amp
            break

    # 3. ตรวจสอบแรงดันตก (คุมวงจรย่อย <= 3% เพื่อไม่ให้รวมทั้งระบบเกิน 5% ตามข้อ 3.6.1)
    upsized_by_vd = False
    vd_pct = calculate_voltage_drop_pct(i_load, length_m, selected_wire)

    if vd_pct > max_branch_vd_pct:
        for wire_size, base_amp in ampacity_table.items():
            if wire_size > selected_wire:
                test_vd = calculate_voltage_drop_pct(i_load, length_m, wire_size)
                if test_vd <= max_branch_vd_pct:
                    selected_wire = wire_size
                    effective_ampacity = base_amp * derating_factor
                    vd_pct = test_vd
                    upsized_by_vd = True
                    break

    # 4. เลือกขนาดสายดิน (ตารางที่ 4-2) และระบุรูปแบบท่อร้อยสายตามกลุ่มการติดตั้ง
    selected_ground = 2.5
    for max_cb, g_size in GROUND_WIRE_TABLE:
        if selected_cb <= max_cb:
            selected_ground = g_size
            break

    base_conduit = CONDUIT_SIZE_BY_WIRE.get(selected_wire, '1-1/2" (40 มม.)')
    if "กลุ่มที่ 3" in install_method:
        conduit_str = "เดินเกาะผนัง (ไม่ใช้ท่อ)"
    elif "กลุ่มที่ 4" in install_method:
        conduit_str = "เดินบนลูกถ้วย (ไม่ใช้ท่อ)"
    elif "กลุ่มที่ 5" in install_method:
        conduit_str = f"{base_conduit} (ท่อฝังดิน)"
    else:
        conduit_str = base_conduit

    return {
        "i_load": round(i_load, 2),
        "cb": f"{selected_cb} AT",
        "wire": f"2 x {selected_wire:g} ตร.มม.",
        "wire_num": selected_wire,
        "derated_amp": f"{effective_ampacity:.1f} A",
        "vd_pct": vd_pct,
        "upsized_by_vd": upsized_by_vd,
        "ground": f"G - {selected_ground:g} ตร.มม.",
        "conduit": conduit_str,
    }


def calculate_whole_house_demand(circuits: list) -> dict:
    """คำนวณโหลดสูงสุดของบ้านพักอาศัยหลังคูณ Demand Factor (ตารางที่ 3-1 และ 3-3)"""
    lighting_va = sum(c["โหลดรวม (VA)"] for c in circuits if c["category"] == "lighting")
    receptacle_va = sum(c["โหลดรวม (VA)"] for c in circuits if c["category"] == "receptacle")
    ac_va = sum(c["โหลดรวม (VA)"] for c in circuits if c["category"] == "ac")
    heater_cooking_va = sum(c["โหลดรวม (VA)"] for c in circuits if c["category"] == "heater_cooking")
    other_va = sum(c["โหลดรวม (VA)"] for c in circuits if c["category"] == "other")

    # แสงสว่างที่พักอาศัย (ตารางที่ 3-1)
    if lighting_va <= 3000:
        demand_lighting = lighting_va
    elif lighting_va <= 120000:
        demand_lighting = 3000 + (lighting_va - 3000) * 0.35
    else:
        demand_lighting = 3000 + (117000 * 0.35) + (lighting_va - 120000) * 0.25

    # เครื่องทำน้ำร้อน / เครื่องหุงต้ม (ตารางที่ 3-3: 10 A แรก 100% + 30% ของส่วนเกิน 10 A)
    heater_amp = heater_cooking_va / NOMINAL_VOLTAGE
    demand_heater_amp = heater_amp if heater_amp <= 10 else 10 + (heater_amp - 10) * 0.30
    demand_heater_va = demand_heater_amp * NOMINAL_VOLTAGE

    total_connected_va = lighting_va + receptacle_va + ac_va + heater_cooking_va + other_va
    total_demand_va = demand_lighting + receptacle_va + ac_va + demand_heater_va + other_va
    total_demand_amp = total_demand_va / NOMINAL_VOLTAGE

    return {
        "connected_va": round(total_connected_va, 2),
        "demand_va": round(total_demand_va, 2),
        "demand_amp": round(total_demand_amp, 2),
        "breakdown": {
            "1. แสงสว่าง (ตารางที่ 3-1)": f"{demand_lighting:,.0f} VA (จาก {lighting_va:,.0f} VA)",
            "2. เต้ารับทั่วไป (100%)": f"{receptacle_va:,.0f} VA",
            "3. เครื่องปรับอากาศ (ตารางที่ 3-3: 100%)": f"{ac_va:,.0f} VA",
            "4. น้ำอุ่น/หุงต้ม (ตารางที่ 3-3: 10A+30%)": f"{demand_heater_va:,.0f} VA (จาก {heater_cooking_va:,.0f} VA)",
            "5. โหลดเฉพาะอื่นๆ เช่น ปั๊มน้ำ/EV (100%)": f"{other_va:,.0f} VA",
        },
    }


def select_main_service(demand_amp: float, utility: str) -> dict:
    """เลือกขนาดมิเตอร์ เมนเบรกเกอร์ และสายเมนสำหรับบ้านพักอาศัย (ตารางที่ 3-4 และ 3-5)"""
    required_cb_amp = demand_amp * 1.25  # หมายเหตุ ตารางที่ 3-4

    if "MEA" in utility:
        mea_options = [
            {"meter": "5(15) A (1 เฟส)", "max_cb": 16, "max_load": 10, "wire": "สายทองแดง 4 ตร.มม. (เดินอากาศ) / 10 ตร.มม. (ฝังดิน ข้อ 3.4.2)"},
            {"meter": "15(45) A (1 เฟส)", "max_cb": 50, "max_load": 30, "wire": "สายทองแดง 16 ตร.มม. (ร้อยท่อในอากาศ ตารางที่ 5-20)"},
            {"meter": "30(100) A (1 เฟส)", "max_cb": 100, "max_load": 75, "wire": "สายทองแดง 50 ตร.มม. (ร้อยท่อในอากาศ ตารางที่ 5-20)"},
            {"meter": "50(150) A (1 เฟส)", "max_cb": 125, "max_load": 100, "wire": "สายทองแดง 70 ตร.มม. (ร้อยท่อในอากาศ ตารางที่ 5-20)"},
        ]
        for opt in mea_options:
            if opt["max_cb"] >= required_cb_amp and opt["max_load"] >= demand_amp:
                return {
                    "meter": opt["meter"],
                    "main_cb": f"{opt['max_cb']} AT (2P, IC ≥ 10kA)",
                    "main_wire": opt["wire"],
                    "req_cb_125": round(required_cb_amp, 2),
                    "ref": "ตารางที่ 3-4 (การไฟฟ้านครหลวง - MEA)",
                }
    else:
        pea_options = [
            {"meter": "5(15) A (1P)", "max_cb": 16, "wire": "สายทองแดง 4 ตร.มม. (เดินอากาศตารางที่ 3-5)"},
            {"meter": "15(45) A (1P)", "max_cb": 50, "wire": "สายทองแดง 10 ตร.มม. (เดินอากาศ) / 16 ตร.มม. (ร้อยท่อ)"},
            {"meter": "30(100) A (1P)", "max_cb": 100, "wire": "สายทองแดง 35 ตร.มม. (เดินอากาศ) / 50 ตร.มม. (ร้อยท่อ)"},
        ]
        for opt in pea_options:
            if opt["max_cb"] >= required_cb_amp:
                return {
                    "meter": opt["meter"],
                    "main_cb": f"{opt['max_cb']} AT (2P, IC ≥ 10kA)",
                    "main_wire": opt["wire"],
                    "req_cb_125": round(required_cb_amp, 2),
                    "ref": "ตารางที่ 3-5 (การไฟฟ้าส่วนภูมิภาค - PEA)",
                }

    return {
        "meter": "โหลดสูง แนะนำขอไฟ 3 เฟส 4 สาย (15(45)A 3P หรือ 30(100)A 3P)",
        "main_cb": f"ต้องการเมนเบรกเกอร์ ≥ {required_cb_amp:.1f} A",
        "main_wire": "คำนวณแยกเฟสสมดุลตามระบบ 3 เฟส 4 สาย",
        "req_cb_125": round(required_cb_amp, 2),
        "ref": "เกินพิกัดมิเตอร์ 1 เฟสมาตรฐาน",
    }