import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from app.utils.timezone import format_datetime

def generate_receipt(order, cart_items):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    center_x = width / 2.0
    
    # --- COLORES ---
    bg_color = HexColor("#FCF8F2")
    dark_brown = HexColor("#3E2723")
    light_brown = HexColor("#EFEBE4")
    accent_brown = HexColor("#8D6E63")
    bone_color = HexColor("#EAE0C8")
    gold = HexColor("#d4af37")
    
    # ──────────────────────────────────────────────
    # 1. FONDO DE LA PÁGINA
    # ──────────────────────────────────────────────
    c.setFillColor(bg_color)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    bg_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static', 'img', 'plantilla_recibo.png')
    if os.path.exists(bg_path):
        c.drawImage(bg_path, 0, 0, width=width, height=height, preserveAspectRatio=False)

    # ──────────────────────────────────────────────
    # 2. ENCABEZADO CENTRADO
    # ──────────────────────────────────────────────
    # Logo / Marca
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(center_x, height - 75, "MARICHUY")
    
    c.setFont("Helvetica", 11)
    c.setFillColor(accent_brown)
    c.drawCentredString(center_x, height - 95, "CHOCOLATES QUE ENAMORAN")
    
    # Líneas decorativas simétricas
    c.setStrokeColor(gold)
    c.setLineWidth(1.5)
    c.line(80, height - 115, width - 80, height - 115)
    c.setStrokeColor(accent_brown)
    c.setLineWidth(0.5)
    c.line(80, height - 118, width - 80, height - 118)
    
    # Título del documento
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(center_x, height - 145, "RECIBO DE COMPRA")

    # ──────────────────────────────────────────────
    # 3. INFORMACIÓN DEL CLIENTE Y MÉTODO DE PAGO
    #    Distribuidos simétricamente
    # ──────────────────────────────────────────────
    y_info = height - 190
    
    # Márgenes simétricos
    left_margin = 60
    right_box_x = center_x + 20
    
    # ── Columna Izquierda: Datos del Cliente ──
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_margin, y_info, "Información del cliente")
    
    c.setFont("Helvetica", 10)
    labels_left = left_margin
    values_left = left_margin + 85
    
    c.setFillColor(accent_brown)
    c.drawString(labels_left, y_info - 25, "Nombre:")
    c.setFillColor(dark_brown)
    c.drawString(values_left, y_info - 25, str(order.customer_name or order.customer.username))
    
    c.setFillColor(accent_brown)
    c.drawString(labels_left, y_info - 45, "Correo:")
    c.setFillColor(dark_brown)
    email_text = str(order.customer_email or order.customer.email)
    # Truncar email si es muy largo
    if len(email_text) > 30:
        email_text = email_text[:28] + "..."
    c.drawString(values_left, y_info - 45, email_text)
    
    c.setFillColor(accent_brown)
    c.drawString(labels_left, y_info - 65, "Fecha:")
    c.setFillColor(dark_brown)
    c.drawString(values_left, y_info - 65, format_datetime(order.created_at))
    
    c.setFillColor(accent_brown)
    c.drawString(labels_left, y_info - 85, "N° de pedido:")
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(values_left + 30, y_info - 85, f"#MC-{format_datetime(order.created_at, '%Y%m%d')}-{order.id:03d}")
    
    # ── Columna Derecha: Método de Pago (caja centrada) ──
    box_width = 200
    box_height = 100
    box_x = right_box_x + 10
    box_y = y_info - 90
    
    c.setFillColor(light_brown)
    c.setStrokeColor(accent_brown)
    c.setLineWidth(1)
    c.roundRect(box_x, box_y, box_width, box_height, 10, fill=1, stroke=1)
    
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(box_x + box_width / 2, box_y + box_height - 22, "Método de pago")
    
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(accent_brown)
    c.drawCentredString(box_x + box_width / 2, box_y + box_height - 48, order.payment_method.capitalize())
    
    c.setFont("Helvetica", 10)
    c.setFillColor(dark_brown)
    c.drawCentredString(box_x + box_width / 2, box_y + box_height - 72, "Estado del pago:")
    
    # Color del estado (igual a las otras letras)
    status_color = dark_brown
    
    c.setFillColor(status_color)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(box_x + box_width / 2, box_y + box_height - 88, order.status)

    # ──────────────────────────────────────────────
    # 4. TABLA DE PRODUCTOS (centrada y equilibrada)
    # ──────────────────────────────────────────────
    table_margin = 50
    table_width = width - (table_margin * 2)
    y_table = y_info - 130
    
    # Columnas distribuidas proporcionalmente
    col_product_x = table_margin + 10
    col_qty_x = table_margin + (table_width * 0.55)
    col_unit_x = table_margin + (table_width * 0.72)
    col_total_x = table_margin + (table_width * 0.90)
    
    # Encabezado de la tabla
    c.setFillColor(dark_brown)
    c.rect(table_margin, y_table - 20, table_width, 28, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col_product_x, y_table - 13, "PRODUCTO")
    c.drawCentredString(col_qty_x, y_table - 13, "CANT.")
    c.drawCentredString(col_unit_x, y_table - 13, "P. UNITARIO")
    c.drawCentredString(col_total_x, y_table - 13, "TOTAL")
    
    # Filas de la tabla
    y = y_table - 45
    c.setStrokeColor(HexColor("#E0E0E0"))
    c.setLineWidth(0.5)
    
    for p_id, item in cart_items.items():
        # Fondo alternado sutil
        c.setFillColor(dark_brown)
        c.setFont("Helvetica", 10)
        
        # Truncar nombre si es muy largo
        product_name = str(item['name'])
        if len(product_name) > 40:
            product_name = product_name[:38] + "..."
        
        c.drawString(col_product_x, y, product_name)
        c.drawCentredString(col_qty_x, y, str(item['quantity']))
        c.drawCentredString(col_unit_x, y, f"${item['price']:,.2f}")
        c.drawCentredString(col_total_x, y, f"${item['price'] * item['quantity']:,.2f}")
        
        # Línea separadora tenue
        c.line(table_margin, y - 10, table_margin + table_width, y - 10)
        y -= 30

    # ──────────────────────────────────────────────
    # 5. TOTALES (centrados a la derecha)
    # ──────────────────────────────────────────────
    y -= 10
    totals_label_x = col_unit_x - 20
    totals_value_x = table_margin + table_width - 10
    
    c.setFillColor(dark_brown)
    c.setFont("Helvetica", 11)
    c.drawRightString(totals_label_x + 40, y, "Subtotal")
    c.drawRightString(totals_value_x, y, f"${order.total_amount:,.2f}")
    
    y -= 22
    c.drawRightString(totals_label_x + 40, y, "Envío")
    c.drawRightString(totals_value_x, y, "$0.00")
    
    y -= 25
    # Caja de TOTAL centrada
    total_box_width = 220
    total_box_x = totals_value_x - total_box_width + 10
    c.setFillColor(dark_brown)
    c.roundRect(total_box_x, y - 15, total_box_width, 32, 6, fill=1, stroke=0)
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(total_box_x + 15, y - 5, "TOTAL")
    c.setFillColor(HexColor("#FFFFFF"))
    c.drawRightString(total_box_x + total_box_width - 15, y - 5, f"${order.total_amount:,.2f}")

    # ──────────────────────────────────────────────
    # 6. FOOTER CENTRADO
    # ──────────────────────────────────────────────
    y_footer = y - 60
    
    # Caja de Agradecimiento (centrada)
    thanks_width = width - 100
    thanks_x = (width - thanks_width) / 2
    c.setFillColor(light_brown)
    c.setStrokeColor(accent_brown)
    c.roundRect(thanks_x, y_footer - 55, thanks_width, 65, 10, fill=1, stroke=1)
    
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Oblique", 15)
    c.drawCentredString(center_x, y_footer - 10, "¡Gracias por tu compra!")
    c.setFont("Helvetica", 10)
    c.drawCentredString(center_x, y_footer - 30, "En Marichuy agradecemos tu confianza y apoyo.")
    c.drawCentredString(center_x, y_footer - 45, "Tu pedido será preparado con mucho amor. 🍫")
    
    # Caja de Contacto (centrada)
    y_contact = y_footer - 130
    contact_box_width = 260
    box_x = center_x - (contact_box_width / 2)
    
    c.setFillColor(light_brown)
    c.roundRect(box_x, y_contact - 15, contact_box_width, 65, 10, fill=1, stroke=0)
    
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(center_x, y_contact + 32, "¿Necesitas ayuda?")
    c.setFont("Helvetica", 10)
    c.drawCentredString(center_x, y_contact + 12, "WhatsApp: 3186713936")
    c.drawCentredString(center_x, y_contact - 3, "Email: marichuyy.m.a@gmail.com")
    
    # Guardar
    c.showPage()
    c.save()
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    # Guardar copia física temporal
    receipts_dir = os.path.join('instance', 'receipts')
    os.makedirs(receipts_dir, exist_ok=True)
    pdf_path = os.path.join(receipts_dir, f'recibo_{order.id}.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(pdf_bytes)
        
    return pdf_bytes, pdf_path
