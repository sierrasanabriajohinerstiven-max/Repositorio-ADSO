# pyrefly: ignore [missing-import]
from flask_mail import Message
from app import mail
from flask import current_app
import traceback

def send_nequi_confirmation(email, name, total, products, pdf_path=None):
    """
    Envía un correo electrónico de confirmación de compra por Nequi.
    
    :param email: Correo electrónico del cliente.
    :param name: Nombre del cliente.
    :param total: Total de la compra.
    :param products: Lista de diccionarios con la información de los productos (ej. name, quantity, price).
    :param pdf_path: Ruta al archivo PDF del recibo para adjuntarlo.
    """
    try:
        subject = "Confirmación de tu pedido en Marichuy"
        
        # Construir el resumen de productos
        products_summary = ""
        products_html = ""
        for item in products:
            product_total = item['price'] * item['quantity']
            products_summary += f"- {item['quantity']}x {item['name']} - ${product_total:,.2f}\n"
            products_html += f"<li><b>{item['quantity']}x {item['name']}</b>: ${product_total:,.2f}</li>"
            
        body = f"""Hola {name},

¡Gracias por tu compra en Marichuy y por enviarnos tu comprobante de pago!

Hemos recibido tu comprobante y actualmente estamos validando el pago. Una vez confirmado, procederemos con el envío de tu pedido.

Este es el resumen de tu pedido:
{products_summary}
Total de la compra: ${total:,.2f}

Adjunto a este correo encontrarás el recibo oficial de tu pedido en formato PDF.

¡Esperamos que disfrutes de nuestro chocolate premium!

Atentamente,
El equipo de Marichuy
"""

        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333; border: 1px solid #e0e0e0; border-radius: 10px; overflow: hidden;">
            <div style="background-color: #3E2723; padding: 20px; text-align: center;">
                <h1 style="color: #FFC107; margin: 0;">Marichuy</h1>
                <p style="color: #EFEBE4; margin: 5px 0 0 0; font-size: 14px;">Chocolates que enamoran</p>
            </div>
            <div style="padding: 30px;">
                <h2 style="color: #3E2723;">¡Hola, {name}!</h2>
                <p>¡Gracias por tu compra en <b>Marichuy</b> y por enviarnos tu comprobante de pago!</p>
                <p>Hemos recibido tu comprobante y actualmente lo estamos validando. Una vez confirmado, procederemos con la preparación y envío de tu pedido.</p>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #8D6E63;">Resumen de tu pedido:</h3>
                    <ul>
                        {products_html}
                    </ul>
                    <hr style="border: 0; border-top: 1px solid #ccc;">
                    <h3 style="text-align: right; color: #3E2723;">Total: ${total:,.2f}</h3>
                </div>
                
                <p>Adjunto a este correo encontrarás el <b>recibo oficial</b> de tu pedido en formato PDF.</p>
                <p>¡Esperamos que disfrutes de nuestro chocolate 100% natural y premium!</p>
                
                <p style="margin-top: 30px;">Atentamente,<br><b>El equipo de Marichuy</b></p>
            </div>
            <div style="background-color: #f1f1f1; padding: 15px; text-align: center; font-size: 12px; color: #777;">
                <p style="margin: 0;">© 2026 Marichuy Chocolates. Todos los derechos reservados.</p>
                <p style="margin: 5px 0 0 0;">Este es un correo automático, por favor no respondas a esta dirección.</p>
            </div>
        </div>
        """

        sender_email = current_app.config.get('MAIL_DEFAULT_SENDER', 'marichuyy.m.a@gmail.com')
        msg = Message(
            subject=subject,
            sender=("Marichuy Chocolates", sender_email),
            recipients=[email],
            body=body,
            html=html_body
        )
        
        if pdf_path:
            with open(pdf_path, 'rb') as fp:
                msg.attach(
                    filename=f"recibo.pdf",
                    content_type="application/pdf",
                    data=fp.read()
                )
        
        mail.send(msg)
        print(f"Correo de recibo con PDF enviado exitosamente a {email}")
        return True
        
    except Exception as e:
        print("Error enviando el correo de recibo:", e)
        traceback.print_exc()
        try:
            with open('error_log.txt', 'a') as f:
                f.write(f"ERROR ENVIANDO CORREO:\n{str(e)}\n{traceback.format_exc()}\n\n")
        except:
            pass
        return False
