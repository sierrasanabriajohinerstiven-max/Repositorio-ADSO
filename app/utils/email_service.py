# pyrefly: ignore [missing-import]
from flask_mail import Message
from app import mail
from flask import current_app, url_for
import traceback
from app.utils.timezone import format_datetime

def get_email_template(title, heading, content, footer_msg="", order_details=""):
    """
    Genera el HTML base para todos los correos usando la plantilla con fondo y centrado.
    """
    try:
        # Intentar obtener la URL absoluta de la imagen de fondo.
        # Usaremos plantilla_recibo.png asumiendo que es la imagen compartida con hojas de cacao.
        bg_img_url = url_for('static', filename='img/plantilla_recibo.png', _external=True)
    except Exception:
        # Fallback si se llama fuera del contexto
        bg_img_url = "https://marichuy.newonline.digital/static/img/plantilla_recibo.png"
        
    # Usamos diseño basado en tablas para máxima compatibilidad con clientes de correo
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background-color: #F5F1E7; font-family: 'Segoe UI', Arial, sans-serif;">
        
        <!-- Tabla principal de fondo -->
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #F5F1E7;">
            <tr>
                <td align="center" valign="top" background="{bg_img_url}" style="background-image: url('{bg_img_url}'); background-size: cover; background-position: center top; padding: 50px 20px;">
                    
                    <!-- Tarjeta central con contenido -->
                    <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: rgba(255, 255, 255, 0.95); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.15); margin: 0 auto;">
                        
                        <!-- Header de la tarjeta -->
                        <tr>
                            <td align="center" style="padding: 40px 30px 20px 30px;">
                                <h1 style="color: #3E2723; margin: 0; font-size: 32px; letter-spacing: 4px; font-weight: bold;">MARICHUY</h1>
                                <p style="color: #8D6E63; margin: 8px 0 0 0; font-size: 13px; letter-spacing: 2px; text-transform: uppercase;">Chocolates Premium</p>
                                <div style="height: 2px; width: 60px; background-color: #d4af37; margin: 20px auto 0 auto;"></div>
                            </td>
                        </tr>

                        <!-- Contenido Principal -->
                        <tr>
                            <td align="center" style="padding: 10px 40px 30px 40px;">
                                <h2 style="color: #3E2723; margin: 0 0 20px 0; font-size: 22px;">{heading}</h2>
                                <div style="color: #555; font-size: 15px; line-height: 1.6; text-align: center;">
                                    {content}
                                </div>
                                {order_details}
                                <p style="color: #8D6E63; font-size: 14px; text-align: center; font-style: italic; margin-top: 25px;">{footer_msg}</p>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td align="center" style="background-color: #3E2723; padding: 25px 20px;">
                                <p style="color: #d4af37; margin: 0 0 5px 0; font-size: 14px; font-weight: bold; letter-spacing: 1px;">MARICHUY CHOCOLATES</p>
                                <p style="color: #EFEBE4; margin: 0 0 10px 0; font-size: 12px;">Elaboramos cada chocolate con pasión y excelencia.</p>
                                <p style="color: #999; margin: 0; font-size: 10px;">© 2026 Marichuy. Todos los derechos reservados.</p>
                                <p style="color: #777; margin: 5px 0 0 0; font-size: 10px;">Este es un correo automático, por favor no respondas a esta dirección.</p>
                            </td>
                        </tr>

                    </table>
                    
                </td>
            </tr>
        </table>
        
    </body>
    </html>
    """
    return html

def send_nequi_confirmation(email, name, total, products, pdf_path=None):
    try:
        subject = "Confirmación de tu pedido en Marichuy"
        
        products_html = ""
        for item in products:
            product_total = item['price'] * item['quantity']
            products_html += f"<tr><td style='padding: 8px 0; border-bottom: 1px solid #eee; text-align: left;'><b>{item['quantity']}x {item['name']}</b></td><td style='padding: 8px 0; border-bottom: 1px solid #eee; text-align: right;'>${product_total:,.2f}</td></tr>"
            
        content = f"""
        <p>Hola <strong style="color: #3E2723;">{name}</strong>,</p>
        <p>¡Gracias por tu compra en Marichuy y por enviarnos tu comprobante de pago!</p>
        <p>Hemos recibido tu comprobante y actualmente lo estamos validando. Una vez confirmado, procederemos con la preparación y envío de tu pedido.</p>
        <p>Adjunto a este correo encontrarás el <b>recibo oficial</b> de tu pedido en formato PDF.</p>
        """

        order_details = f"""
        <div style="background-color: #FAF8F5; border: 1px solid #EAE0C8; border-radius: 10px; padding: 25px; margin: 25px 0; text-align: center;">
            <h3 style="color: #3E2723; margin: 0 0 15px 0; font-size: 16px; text-transform: uppercase; letter-spacing: 1px;">Resumen de tu pedido</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px; color: #555;">
                {products_html}
                <tr>
                    <td style="padding: 15px 0 0 0; text-align: right; color: #3E2723; font-weight: bold;">TOTAL:</td>
                    <td style="padding: 15px 0 0 0; text-align: right; color: #d4af37; font-size: 18px; font-weight: bold;">${total:,.2f}</td>
                </tr>
            </table>
        </div>
        """

        html_body = get_email_template(
            title=subject,
            heading="¡Recibimos tu comprobante!",
            content=content,
            footer_msg="¡Esperamos que disfrutes de nuestro chocolate 100% natural y premium!",
            order_details=order_details
        )

        sender_email = current_app.config.get('MAIL_DEFAULT_SENDER', 'marichuyy.m.a@gmail.com')
        msg = Message(
            subject=subject,
            sender=("Marichuy Chocolates", sender_email),
            recipients=[email],
            html=html_body
        )
        
        if pdf_path:
            with open(pdf_path, 'rb') as fp:
                msg.attach(filename="recibo.pdf", content_type="application/pdf", data=fp.read())
        
        mail.send(msg)
        return True
    except Exception as e:
        print("Error enviando el correo de recibo:", e)
        return False

def send_status_email(order, new_status, customer_email, customer_name):
    try:
        status_config = {
            'Verificando pedido': {
                'subject': f'Estamos verificando tu pedido #{order.id}',
                'heading': 'Verificando pedido',
                'message': 'Hemos recibido tu solicitud y actualmente estamos verificando los detalles y el pago. Pronto comenzaremos a prepararlo.',
                'color': '#17a2b8'
            },
            'Preparando tu pedido': {
                'subject': f'Tu pedido #{order.id} está en preparación',
                'heading': '¡Tu pedido está en preparación!',
                'message': 'Nuestro equipo ya está trabajando con amor y dedicación en tu pedido. Cada chocolate es elaborado con los mejores ingredientes para garantizarte una experiencia única.',
                'color': '#17a2b8'
            },
            'Pedido en camino': {
                'subject': f'Tu pedido #{order.id} va en camino',
                'heading': '¡Tu pedido ha sido enviado!',
                'message': 'Tu pedido ya salió de nuestras instalaciones y va en camino hacia ti. Muy pronto podrás disfrutar de nuestro chocolate premium.',
                'color': '#ffc107'
            },
            'Pedido entregado': {
                'subject': f'Tu pedido #{order.id} ha sido entregado',
                'heading': '¡Tu pedido fue entregado!',
                'message': '¡Esperamos que disfrutes al máximo de nuestro chocolate artesanal! Tu satisfacción es nuestra mayor recompensa.',
                'color': '#28a745'
            },
            'Cancelado': {
                'subject': f'Tu pedido #{order.id} ha sido cancelado',
                'heading': 'Pedido cancelado',
                'message': 'Lamentamos informarte que tu pedido ha sido cancelado. Si tienes alguna duda o deseas realizar un nuevo pedido, no dudes en contactarnos.',
                'color': '#dc3545'
            }
        }

        config = status_config.get(new_status)
        if not config:
            return False

        payment_display = order.payment_method.capitalize() if order.payment_method else 'No especificado'
        order_date = format_datetime(order.created_at, '%d de %B de %Y')

        content = f"""
        <p>Hola <strong style="color: #3E2723;">{customer_name}</strong>,</p>
        <p>{config['message']}</p>
        """

        order_details = f"""
        <div style="background-color: #FAF8F5; border: 1px solid #EAE0C8; border-radius: 10px; padding: 25px; margin: 25px 0; text-align: center;">
            <h3 style="color: #3E2723; margin: 0 0 15px 0; font-size: 16px; text-transform: uppercase; letter-spacing: 1px;">Detalles del pedido</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px; color: #555; text-align: left;">
                <tr>
                    <td style="padding: 6px 0; color: #888;">N° de pedido</td>
                    <td style="padding: 6px 0; text-align: right; font-weight: bold; color: #3E2723;">#{order.id}</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; color: #888;">Fecha</td>
                    <td style="padding: 6px 0; text-align: right; color: #3E2723;">{order_date}</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; color: #888;">Método de pago</td>
                    <td style="padding: 6px 0; text-align: right; color: #3E2723;">{payment_display}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 0 0 0; color: #888; border-top: 1px solid #eee;">Total</td>
                    <td style="padding: 10px 0 0 0; text-align: right; color: #d4af37; font-weight: bold; font-size: 16px; border-top: 1px solid #eee;">${order.total_amount:,.2f}</td>
                </tr>
            </table>
            <div style="margin-top: 20px;">
                <span style="background-color: {config['color']}; color: #fff; padding: 8px 20px; border-radius: 20px; font-size: 13px; font-weight: bold; letter-spacing: 1px;">
                    {new_status.upper()}
                </span>
            </div>
        </div>
        """

        html_body = get_email_template(
            title=config['subject'],
            heading=config['heading'],
            content=content,
            footer_msg="¡Gracias por ser parte de la familia Marichuy!",
            order_details=order_details
        )

        sender_email = current_app.config.get('MAIL_DEFAULT_SENDER', 'marichuyy.m.a@gmail.com')
        msg = Message(
            subject=config['subject'],
            sender=("Marichuy Chocolates", sender_email),
            recipients=[customer_email],
            html=html_body
        )

        mail.send(msg)
        return True

    except Exception as e:
        print(f"Error enviando correo de estado: {e}")
        return False

def send_verification_confirmed_email(order, customer_email, customer_name):
    try:
        order_date = format_datetime(order.created_at, '%d de %B de %Y')
        payment_display = order.payment_method.capitalize() if order.payment_method else 'No especificado'

        content = f"""
        <p>Hola <strong style="color: #3E2723;">{customer_name}</strong>,</p>
        <p>Hemos verificado exitosamente tu comprobante de pago para el pedido <strong style="color: #d4af37;">#{order.id}</strong>.</p>
        <p>Tu pago ha sido confirmado y comenzaremos a preparar tu pedido muy pronto.</p>
        """

        order_details = f"""
        <div style="background-color: #FAF8F5; border: 1px solid #EAE0C8; border-radius: 10px; padding: 25px; margin: 25px 0; text-align: center;">
            <h3 style="color: #3E2723; margin: 0 0 15px 0; font-size: 16px; text-transform: uppercase; letter-spacing: 1px;">Detalles del pedido</h3>
            <table style="width: 100%; border-collapse: collapse; font-size: 14px; color: #555; text-align: left;">
                <tr>
                    <td style="padding: 6px 0; color: #888;">N° de pedido</td>
                    <td style="padding: 6px 0; text-align: right; font-weight: bold; color: #3E2723;">#{order.id}</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; color: #888;">Fecha</td>
                    <td style="padding: 6px 0; text-align: right; color: #3E2723;">{order_date}</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; color: #888;">Total</td>
                    <td style="padding: 6px 0; text-align: right; color: #d4af37; font-weight: bold;">${order.total_amount:,.2f}</td>
                </tr>
            </table>
            <div style="margin-top: 20px;">
                <span style="background-color: #28a745; color: #fff; padding: 8px 20px; border-radius: 20px; font-size: 13px; font-weight: bold; letter-spacing: 1px;">
                    PAGO VERIFICADO ✓
                </span>
            </div>
        </div>
        """

        html_body = get_email_template(
            title=f'Comprobante verificado - Pedido #{order.id}',
            heading="¡Pago Confirmado!",
            content=content,
            footer_msg="🍫 Elaboramos cada chocolate con pasión y excelencia.",
            order_details=order_details
        )

        sender_email = current_app.config.get('MAIL_DEFAULT_SENDER', 'marichuyy.m.a@gmail.com')
        msg = Message(
            subject=f'✅ Comprobante verificado - Pedido #{order.id}',
            sender=("Marichuy Chocolates", sender_email),
            recipients=[customer_email],
            html=html_body
        )

        mail.send(msg)
        return True

    except Exception as e:
        print(f"Error enviando correo de verificación: {e}")
        return False
