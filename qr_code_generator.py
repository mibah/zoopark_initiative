import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

url = "https://mibah.github.io/zoopark_initiative/"

# Erstelle QR-Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Generiere QR-Code Bild
qr_img = qr.make_image(fill_color="black", back_color="white")
qr_img.save("qr_simple.png")

# Erstelle kompaktes PDF
c = canvas.Canvas("qr_framed.pdf", pagesize=A4)
width, height = A4

# Zentrierte Position
qr_size = 250
x_center = width / 2
y_center = height / 2 + 40

# Einfacher schwarzer Rahmen
c.setStrokeColorRGB(0, 0, 0)
c.setLineWidth(2)
c.rect(x_center - qr_size/2,
       y_center - qr_size/2,
       qr_size, qr_size,
       fill=0, stroke=1)

# "Zoopark Initiative" Text über dem Rahmen
c.setFillColorRGB(0, 0, 0)
c.setFont("Helvetica-Bold", 20)
title = "Zoopark Initiative"
title_width = c.stringWidth(title, "Helvetica-Bold", 20)
c.drawString(x_center - title_width/2,
             y_center + qr_size/2 + 15,
             title)

# QR-Code einfügen (mit minimalem Padding)
padding = 10
qr_img_size = qr_size - 2*padding
c.drawImage("qr_simple.png",
            x_center - qr_img_size/2,
            y_center - qr_img_size/2,
            width=qr_img_size,
            height=qr_img_size)

# "SCAN ME" Text direkt unter dem Rahmen (kompakt)
c.setFillColorRGB(0, 0, 0)
c.setFont("Helvetica-Bold", 24)
text = "SCAN ME"
text_width = c.stringWidth(text, "Helvetica-Bold", 24)
c.drawString(x_center - text_width/2,
             y_center - qr_size/2 - 35,
             text)

c.save()
print("✓ Kompakter QR-Code erstellt: qr_framed.pdf")

# PNG-Version
print("\nErstelle kompakte PNG-Version...")

# Kompaktes Canvas
canvas_size = 400
frame_img = Image.new('RGB', (canvas_size, canvas_size), 'white')
draw = ImageDraw.Draw(frame_img)

# Schwarzer Rahmen (kein Schatten)
frame_size = 300
frame_pos = (canvas_size - frame_size) // 2
draw.rectangle(
    [frame_pos, frame_pos, frame_pos + frame_size, frame_pos + frame_size],
    outline='black',
    width=3
)

# QR-Code in der Mitte
qr_pil = qr_img.resize((280, 280))
qr_pos = (canvas_size - 280) // 2
frame_img.paste(qr_pil, (qr_pos, qr_pos))

# Text hinzufügen (kompakt)
try:
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
except:
    font_large = ImageFont.load_default()
    font_title = ImageFont.load_default()

# "Zoopark Initiative" Text über dem Rahmen
title = "Zoopark Initiative"
bbox_title = draw.textbbox((0, 0), title, font=font_title)
title_width = bbox_title[2] - bbox_title[0]
title_x = (canvas_size - title_width) // 2
title_y = frame_pos - 40  # Über dem Rahmen
draw.text((title_x, title_y), title, fill='black', font=font_title)

# "SCAN ME" Text
text = "SCAN ME"
bbox = draw.textbbox((0, 0), text, font=font_large)
text_width = bbox[2] - bbox[0]
text_x = (canvas_size - text_width) // 2
text_y = frame_pos + frame_size + 15  # Minimaler Abstand
draw.text((text_x, text_y), text, fill='black', font=font_large)

frame_img.save("qr_framed.png")
print("✓ PNG-Version erstellt: qr_framed.png")

print("\n" + "="*50)
print("FERTIG!")
print("="*50)
print("\nDateien erstellt:")
print("  - qr_framed.pdf (Schwarz-Weiß, kompakt)")
print("  - qr_framed.png (Schwarz-Weiß, kompakt)")
print("  - qr_simple.png (Nur QR-Code)")