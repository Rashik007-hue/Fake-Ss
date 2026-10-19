from fastapi import FastAPI, Response, Query
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from zoneinfo import ZoneInfo
import io
import os

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)
FONT1 = os.path.join(BASE_DIR, "roboto.ttf")
FONT2 = os.path.join(BASE_DIR, "roboto2.ttf")

# draw_text ফাংশনে bold সাপোর্ট যোগ করা হলো
def draw_text(draw, text, x, y, size, font_path, color, align="left", bold=False):
    font = ImageFont.truetype(font_path, size)
    anchor = "ls" # left-baseline (PHP এর মতো)
    if align == "right":
        anchor = "rs" # right-baseline
    
    try:
        # bold=True হলে stroke_width দিয়ে লেখা মোটা করা হবে
        if bold:
            draw.text((x, y), text, font=font, fill=color, anchor=anchor, stroke_width=1, stroke_fill=color)
        else:
            draw.text((x, y), text, font=font, fill=color, anchor=anchor)
    except Exception:
        if align == "right":
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            draw.text((x - w, y - size), text, font=font, fill=color)
        else:
            draw.text((x, y - size), text, font=font, fill=color)

@app.get("/api/image")
def generate_image(
    type: str = Query("bkash"), 
    number: str = Query("01986833907"), 
    transaction: str = Query("730MGQG6GH"), 
    amount: int = Query(10000)
):
    try:
        # Asia/Dhaka Time
        now = datetime.now(ZoneInfo("Asia/Dhaka"))
        
        if type == "bkash":
            img_path = os.path.join(BASE_DIR, "bkash_bg.jpg")
            img = Image.open(img_path).convert("RGB")
            draw = ImageDraw.Draw(img)
            image_width = img.width
            
            black = (90, 90, 90)
            total = amount
            totalWithExtra = total + 17
            
            time_main = now.strftime("%I:%M %p").lstrip('0')
            dayMonthYear = now.strftime("%d/%m/%y")
            
            draw_text(draw, number, 400, 850, 65, FONT1, black)
            draw_text(draw, number, 410, 950, 55, FONT2, black)
            draw_text(draw, transaction, image_width - 384, 1430, 60, FONT1, black, "right")
            draw_text(draw, f"{total} +17.39", 175, 1880, 50, FONT2, black)
            draw_text(draw, str(totalWithExtra), 175, 1768, 60, FONT1, black)
            draw_text(draw, time_main, 135, 1421, 60, FONT1, black)
            draw_text(draw, dayMonthYear, 420, 1420, 60, FONT1, black)
            draw_text(draw, time_main, 50, 109, 47, FONT2, black)

        elif type == "nagad":
            img_path = os.path.join(BASE_DIR, "nagad_bg.jpg")
            img = Image.open(img_path).convert("RGB")
            draw = ImageDraw.Draw(img)
            
            grey = (128, 128, 128)
            white = (255, 255, 255)
            black = (0, 0, 0) # কালো রঙ ডিফাইন করা হলো
            charge = 5
            total = amount + charge
            
            time_main = now.strftime("%d %B %Y, %I:%M %p").lstrip('0')
            timeeee = now.strftime("%I:%M %p").lstrip('0')
            
            # এখানে bold=True যোগ করা হলো
            draw_text(draw, number, 1110, 999, 55, FONT2, black, "right", bold=True)
            draw_text(draw, transaction, 1790, 1280, 50, FONT1, grey, "right")
            draw_text(draw, str(amount), 1630, 1385, 50, FONT1, grey, "right")
            draw_text(draw, str(charge), 1630, 1505, 50, FONT1, grey, "right")
            draw_text(draw, str(total), 1630, 1620, 50, FONT1, grey, "right")
            draw_text(draw, time_main, 1790, 1740, 50, FONT1, grey, "right")
            draw_text(draw, timeeee, 370, 105, 47, FONT1, white, "right")

        else: # sendmoney
            img_path = os.path.join(BASE_DIR, "sendmoney_bg.jpg")
            img = Image.open(img_path).convert("RGB")
            draw = ImageDraw.Draw(img)
            image_width = img.width
            
            black = (90, 90, 90)
            white = (255, 255, 255)
            total = amount
            totalWithExtra = total + 5
            
            time_main = now.strftime("%I:%M %p").lstrip('0')
            time_top = now.strftime("%I:%M").lstrip('0')
            dayMonthYear = now.strftime("%d/%m/%y")
            header_time = f"{time_main} {dayMonthYear}"
            
            # 🔴 Send Money এর পজিশন ফিক্স করা হলো 🔴
            # নাম্বার
            draw_text(draw, number, 250, 750, 55, FONT1, black)
            draw_text(draw, number, 270, 830, 45, FONT2, black)
            
            # ট্রানজেকশন আইডি, টাইম এবং ডেট
            draw_text(draw, transaction, image_width - 365, 1168, 50, FONT1, black, "right")
            draw_text(draw, time_main, 80, 1130, 45, FONT1, black)
            draw_text(draw, dayMonthYear, 330, 1120, 40, FONT1, black)
            
            # উপরের সাদা পিলের ভেতরের টেক্সট
            draw_text(draw, header_time, 800, 120, 35, FONT1, black)
            
            # টোটাল এবং সাব-টোটাল
            draw_text(draw, str(totalWithExtra), 80, 1400, 40, FONT1, black)
            draw_text(draw, f"{total} + 5.0", 80, 1450, 40, FONT2, black)
            
            # স্ট্যাটাস বারের টাইম
            draw_text(draw, time_top, 100, 77, 37, FONT2, white)

        img_io = io.BytesIO()
        img.save(img_io, format="PNG")
        img_io.seek(0)
        
        return Response(content=img_io.getvalue(), media_type="image/png")

    except Exception as e:
        return Response(content=f"Error: {str(e)}".encode(), media_type="text/plain", status_code=500)
