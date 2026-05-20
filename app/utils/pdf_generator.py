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
    
    # --- COLORES ---
    bg_color = HexColor("#FCF8F2")
    dark_brown = HexColor("#3E2723")
    light_brown = HexColor("#EFEBE4")
    accent_brown = HexColor("#8D6E63")
    bone_color = HexColor("#EAE0C8")
    
    # 1. Fondo de la página
    c.setFillColor(bg_color)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    
    bg_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static', 'img', 'plantilla_recibo.png')
    if os.path.exists(bg_path):
        c.drawImage(bg_path, 0, 0, width=width, height=height, preserveAspectRatio=False)

    
    # 2. LOGO / TÍTULO PRINCIPAL
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width / 2.0, height - 80, "MARICHUY")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(accent_brown)
    c.drawCentredString(width / 2.0, height - 100, "CHOCOLATES QUE ENAMORAN")
    
    # Línea decorativa
    c.setStrokeColor(accent_brown)
    c.setLineWidth(1)
    c.line(100, height - 130, width - 100, height - 130)
    
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 150, "RECIBO DE COMPRA")
    
    # 3. INFORMACIÓN DEL CLIENTE Y MÉTODO DE PAGO
    y_info = height - 200
    
    # Columna Izquierda (Cliente)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_info, "Información del cliente")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, y_info - 25, "Nombre:")
    c.drawString(120, y_info - 25, str(order.customer_name or order.customer.username))
    
    c.drawString(50, y_info - 45, "Correo:")
    c.drawString(120, y_info - 45, str(order.customer_email or order.customer.email))
    
    c.drawString(50, y_info - 65, "Fecha:")
    c.drawString(120, y_info - 65, format_datetime(order.created_at))
    
    c.drawString(50, y_info - 85, "N° de pedido:")
    c.drawString(120, y_info - 85, f"#MC-{format_datetime(order.created_at, '%Y%m%d')}-{order.id:03d}")
    
    # Columna Derecha (Método de Pago) - Caja con fondo
    c.setFillColor(light_brown)
    c.setStrokeColor(accent_brown)
    c.roundRect(width - 250, y_info - 95, 200, 110, 10, fill=1, stroke=1)
    
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(width - 230, y_info - 15, "Método de pago")
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(width - 230, y_info - 40, order.payment_method.capitalize())
    
    c.setFont("Helvetica", 10)
    c.drawString(width - 230, y_info - 70, "Estado del pago:")
    c.setFillColor(HexColor("#B71C1C")) # Rojo para pendiente
    c.drawString(width - 130, y_info - 70, order.status)
    
    # 4. TABLA DE PRODUCTOS
    y_table = y_info - 140
    
    # Encabezado de la tabla
    c.setFillColor(dark_brown)
    c.rect(50, y_table - 20, width - 100, 25, fill=1, stroke=0)
    
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y_table - 13, "PRODUCTO")
    c.drawCentredString(320, y_table - 13, "CANTIDAD")
    c.drawCentredString(420, y_table - 13, "PRECIO UNITARIO")
    c.drawCentredString(520, y_table - 13, "TOTAL")
    
    # Filas de la tabla
    y = y_table - 45
    c.setFillColor(dark_brown)
    c.setFont("Helvetica", 10)
    c.setStrokeColor(HexColor("#E0E0E0"))
    
    for p_id, item in cart_items.items():
        c.drawString(60, y, str(item['name'])[:40])
        c.drawCentredString(320, y, str(item['quantity']))
        c.drawCentredString(420, y, f"${item['price']:,.2f}")
        c.drawCentredString(520, y, f"${item['price'] * item['quantity']:,.2f}")
        
        # Línea separadora tenue
        c.line(50, y - 10, width - 50, y - 10)
        y -= 30
        
    # 5. TOTALES
    y -= 10
    c.drawString(380, y, "Subtotal")
    c.drawRightString(540, y, f"${order.total_amount:,.2f}")
    
    y -= 20
    c.drawString(380, y, "Envío")
    c.drawRightString(540, y, "$0.00")
    
    y -= 20
    # Caja de TOTAL
    c.setFillColor(light_brown)
    c.rect(370, y - 15, 180, 30, fill=1, stroke=0)
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(380, y - 5, "TOTAL")
    c.drawRightString(540, y - 5, f"${order.total_amount:,.2f}")
    
    # 6. FOOTER Y MENSAJES
    y_footer = y - 80
    
    # Caja de Agradecimiento
    c.setFillColor(light_brown)
    c.roundRect(50, y_footer - 60, width - 100, 70, 10, fill=1, stroke=1)
    
    c.setFillColor(dark_brown)
    c.setFont("Helvetica-Oblique", 14)
    c.drawString(70, y_footer - 20, "¡Gracias por tu compra!")
    c.setFont("Helvetica", 10)
    c.drawString(70, y_footer - 40, "En Marichuy agradecemos tu confianza y apoyo.")
    c.drawString(70, y_footer - 55, "Tu pedido será preparado con mucho amor.")
    
    # Cajas inferiores de contacto e instrucciones
    y_contact = y_footer - 150
    
    c.roundRect(50, y_contact, 200, 70, 10, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(60, y_contact + 50, "¿Necesitas ayuda?")
    c.setFont("Helvetica", 9)
    c.drawString(60, y_contact + 30, "Email: hola@marichuy.com")
    c.drawString(60, y_contact + 15, "IG: @marichuy.chocolates")
    
    c.roundRect(width - 250, y_contact, 200, 70, 10, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(width - 240, y_contact + 50, "Instrucciones de pago (Nequi)")
    c.setFont("Helvetica", 9)
    c.drawString(width - 240, y_contact + 30, "Por favor envía el comprobante a nuestro")
    c.drawString(width - 240, y_contact + 15, "contacto para confirmar tu pedido.")
    
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
