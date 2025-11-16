import re
import json
from collections import Counter

# ชื่อไฟล์รายชื่อไอดี (1 บรรทัด = 1 คอมโบนักเตะ)
NAMES_FILE = "names.txt"  # ถ้าไฟล์ชื่ออย่างอื่นก็เปลี่ยนตรงนี้

# ====== โหลดข้อมูลจาก names.txt ======
with open(NAMES_FILE, "r", encoding="utf-8") as f:
    lines = [l.strip() for l in f if l.strip()]

# ตัด (1) (2) (3) ท้ายบรรทัดออก เพื่อรวมเป็น "ไอดีเดียว" แล้วนับจำนวน
# เช่น "Adiano+Forlan (1)" "Adiano+Forlan (2)" → key เดียวคือ "Adiano+Forlan"
bases = [re.sub(r"\s*\(\d+\)$", "", line) for line in lines]
count_by_base = Counter(bases)

# mapping ชื่ออังกฤษ → ไทย (เฉพาะที่กูมั่นใจ)
mapping = {
    "Adiano": "อาเดรียโน่",
    "Alonso": "อลอนโซ่",
    "Baggio": "บาจโจ้",
    "Bale": "เบล",
    "Bebeto": "เบเบโต้",
    "Caceres": "คาเซเรส",
    "Cannavaro": "คันนาวาโร่",
    "Cannavaro(Old)": "คันนาวาโร่ (Old)",
    "CannavaroN": "คันนาวาโร่ N",
    "Casillas": "กาซิยาส",
    "Cole": "โคล",
    "Cunha": "คุนญ่า",
    "De jong": "เดอ ยอง",
    "Denilson": "เดนิลสัน",
    "Diaz": "ดิอาซ",
    "Doku": "ด็อกู",
    "Donnarumma": "ดอนนารุมม่า",
    "Ferdinand": "เฟอร์ดินานด์",
    "Fletcher": "เฟล็ทเชอร์",
    "Forlan": "ฟอร์ลัน",
    "Fotlan": "ฟอร์ลัน",
    "Guti": "กูตี",
    "Gyokeres": "กียอเคเรส",
    "Iniesta": "อิเนียสต้า",
    "Isak": "อีซัค",
    "Jude": "จู๊ด",
    "Juninho": "จูนินโญ่",
    "Kahn": "คาห์น",
    "Kaka": "กาก้า",
    "Lahm": "ลาห์ม",
    "Maicon": "ไมคอน",
    "Maldini": "มัลดินี่",
    "Mendes": "เมนเดส",
    "Morentes": "โมริเอนเตส",
    "Nakamura": "นากามูระ",
    "Nakata": "นากาตะ",
    "Olise": "โอลิเซ่",
    "Oshimen": "โอซิมเฮน",
    "Pedri": "เปดรี",
    "Pepe": "เปเป้",
    "Pique": "ปิเก้",
    "Puskat": "ปุสกัส",
    "Puyol": "ปูโยล",
    "Rafa": "ราฟา",
    "Raphin": "ราฟินญ่า",
    "Reus": "รอยส์",
    "Ronaldo": "โรนัลโด้",
    "Rooney": "รูนีย์",
    "Sanchez": "ซานเชซ",
    "Sedof": "ซีดอร์ฟ",
    "Silva": "ซิลวา",
    "Supanat": "สุภณัฐ",
    "Vandijk": "ฟานไดจ์ค",
    "Vieri": "วีเอรี",
    "Yaya": "ยาย่า",
    "Yuki": "ยูกิ",
    "Zico": "ซิโก้",
    "rooney": "รูนีย์",
    "yuki": "ยูกิ",
}

def token_to_th(token: str) -> str:
    """
    แปลงชื่อแต่ละตัวเป็นไทย ถ้ามั่นใจ + handle แบบมีเลขต่อท้าย
    เช่น Supanat2 → สุภณัฐ2, Supanat 5 → สุภณัฐ 5
    ที่ไม่รู้จักจะปล่อยไว้เป็นแบบเดิม
    """
    t = token.strip()

    # exact match
    if t in mapping:
        return mapping[t]

    # base+เลข ติดกัน เช่น Supanat2, Guti3
    m = re.match(r"^(.*?)(\d+)$", t)
    if m:
        base, num = m.group(1).strip(), m.group(2)
        if base in mapping:
            return f"{mapping[base]}{num}"

    # base + เว้นวรรค + เลข เช่น Supanat 5, Morentes 2
    m2 = re.match(r"^(.*?)[ ]+(\d+)$", t)
    if m2:
        base, num = m2.group(1).strip(), m2.group(2)
        if base in mapping:
            return f"{mapping[base]} {num}"

    # ไม่ชัวร์ → คืนค่าเดิม (อังกฤษเดิม)
    return t

accounts = []
idx = 1

for base in sorted(count_by_base.keys()):
    # ตัดแถวพิเศษที่ไม่ใช่ไอดีจริง
    if base == "names":
        continue

    qty = count_by_base[base]
    parts = [p.strip() for p in base.split("+")]

    # อังกฤษล้วน (เอาไว้ใช้คู่กับหน้า template นักเตะ)
    players_en = parts[:]  # copy list

    # ภาษาไทย (แปลเท่าที่ mapping มี)
    players_th = [token_to_th(p) for p in parts]

    display_name_th = " + ".join(players_th)
    display_name_en = " + ".join(players_en)

    acc = {
        "id": idx,
        "code": base,             # เก็บชื่อดิบๆ ไว้ด้วย (เผื่อใช้ทีหลัง)
        "name": display_name_th,  # default เอาไทยไว้โชว์บนการ์ด
        "name_en": display_name_en,
        "players": players_th,    # ใช้ filter แบบไทย
        "players_en": players_en, # ใช้ filter / ผูกกับ key อังกฤษ
        "quantity": qty,          # จำนวน "เหลือ"
        "price": 0,               # ราคา default = 0 (มึงไปแก้ทีหลัง)
        "image": ""               # path รูป (ตอนนี้เว้นว่างไว้ก่อน)
    }
    accounts.append(acc)
    idx += 1

# พ่นเป็น JavaScript พร้อมวางใน index.html
js = "const accounts = " + json.dumps(accounts, ensure_ascii=False, separators=(',', ':')) + ";"
print(js)
