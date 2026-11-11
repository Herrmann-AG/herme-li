import qrcode
from qrcode.image.svg import SvgImage
from base64 import b64encode
from io import BytesIO
from reportlab.lib.colors import CMYKColor
from reportlab.pdfgen import canvas
from io import BytesIO
import sqlite3

def lookForNull():
    print('Looking for null values')
    try:
        conn = sqlite3.connect('pygmy.db')
        cur = conn.cursor()
        cur.execute('SELECT id, qr_code, short_code FROM link')
        table = cur.fetchall()
        for row in table:
            qr_code = generateQrCode(row[2])
            print("Generated code, b64: %s" % qr_code)
            cur.execute("UPDATE link SET qr_code = '%s' WHERE link.id = %s" % (qr_code, row[0]))
        conn.commit()
        print('Affected rows ' + str(len(table)))
        conn.close()
    except Exception as e:
        print(e)


def generateQrCode(shorted):
    print('Generating the Qr-Code')
    box_size = 20
    border = 1
    # Generate qr code
    qr = qrcode.QRCode(
        version=None,
        box_size=box_size,
        border=border,
    )
    qr.add_data("https://herme.li/" + shorted)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    box_count = len(matrix)
    size = (box_count + 2 * border) * box_size

    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=(size, size))

    true_black = CMYKColor(0, 0, 0, 1)
    c.setFillColor(true_black)

    for row_idx, row in enumerate(matrix):
        for col_idx, is_black in enumerate(row):
            if is_black:
                x = (col_idx + border) * box_size
                # PDF origin is bottom-left, QR matrix is top-left
                y = size - (row_idx + 1 + border) * box_size
                c.rect(x, y, box_size, box_size, stroke=0, fill=1)

    c.showPage()
    c.save()

    # Convert bytes to base64 string
    pdf_buffer.seek(0)
    return b64encode(pdf_buffer.read()).decode("utf-8")

print('Updating Qr-Codes')
lookForNull()