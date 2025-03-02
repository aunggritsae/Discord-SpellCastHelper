# Discord-SpellCastHelper
ตัวช่วยในการเล่น SpellCast บน Discord 

## requirements

- Python 3.6 หรือใหม่กว่า
- Tkinter (ปกติรวมอยู่กับ Python อยู่แล้ว)
- 
## การติดตั้ง

1. โคลน repository นี้: git clone https://github.com/aunggritsae/Discord-SpellCastHelper
   
2. ตรวจสอบให้แน่ใจว่ามี Python 3.6 หรือใหม่กว่า และมี Tkinter (มักรวมมากับ Python อยู่แล้ว)

3. รัน file spellcast-helper.py

## วิธีใช้งาน

1. ป้อนตัวอักษรจากเกม Spellcast ลงในตาราง 5x5:
- พิมพ์ตัวอักษรและใช้ Tab หรือลูกศรเพื่อเลื่อนระหว่างช่อง
- ช่องว่างสามารถปล่อยไว้เป็นช่องว่างหรือใส่จุด (.)

2. คลิกปุ่ม "Find Best Words" เพื่อวิเคราะห์กระดาน

3. ผลลัพธ์จะแสดงคำที่ดีที่สุดสำหรับแต่ละจำนวนการสลับ (0, 1, 2 ตัว)

4. เลื่อนเมาส์ไปยังคำในผลลัพธ์เพื่อดูเส้นทางบนกระดาน:
- สีน้ำเงิน: เส้นทางปกติ
- สีแดง: ตัวอักษรที่ต้องสลับ

5. ใช้ปุ่ม "Clear Grid" เพื่อรีเซ็ตอินเตอร์เฟซสำหรับเกมใหม่

## กฎของเกม Spellcast

ในเกม Spellcast:
- คำต้องสร้างจากตัวอักษรที่อยู่ติดกัน (รวมถึงแนวทแยง)
- แต่ละตัวอักษรบนกระดานสามารถใช้ได้เพียงครั้งเดียวต่อคำ
- คำมีคะแนนตามค่าของตัวอักษร
- คำที่ยาว (7+ ตัวอักษร) จะได้รับโบนัส
- ตัวอักษรบางตัวมีค่าคะแนนสูงกว่าตัวอื่น

## ค่าคะแนนตัวอักษร

| ตัวอักษร | คะแนน | 
|---------|-------|
| A, E, I, O | 1 |
| N | 2 |
| D, G, K, L, R, S, T | 2-3 | 
B, H, M, P | 4 | J | 7 |
C, F, V, W, Y | 5 | Q, Z | 8 |
X | 7 | | |
## ไฟล์พจนานุกรม

- โปรแกรมจะดาวน์โหลดหรือสร้างไฟล์พจนานุกรมโดยอัตโนมัติเมื่อใช้งานครั้งแรก (Credit to : https://github.com/dwyl/english-words/blob/master/words_alpha.txt)

- หากต้องการใช้พจนานุกรมที่กำหนดเอง ให้แทนที่ไฟล์ `dictionary.txt` ด้วยรายการคำของคุณเอง (หนึ่งคำต่อบรรทัด)
