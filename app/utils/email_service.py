# pyrefly: ignore [missing-import]
from flask_mail import Message
from app import mail
from flask import current_app
import traceback
from app.utils.timezone import format_datetime

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


# ─────────────────────────────────────────────────────────────
# Correo automático según cambio de estado del pedido
# ─────────────────────────────────────────────────────────────
def send_status_email(order, new_status, customer_email, customer_name):
    """
    Envía un correo electrónico profesional al cliente cuando cambia el estado de su pedido.
    """
    try:
        # Configuración de mensajes por estado
        status_config = {
            'Preparando tu pedido': {
                'subject': f'🍫 Tu pedido #{order.id} está en preparación',
                'icon': '👨‍🍳',
                'color': '#17a2b8',
                'heading': '¡Tu pedido está siendo preparado!',
                'message': 'Nuestro equipo ya está trabajando con amor y dedicación en tu pedido. Cada chocolate es elaborado con los mejores ingredientes para garantizarte una experiencia única.',
                'footer_msg': 'Te notificaremos cuando tu pedido esté en camino.'
            },
            'Pedido en camino': {
                'subject': f'🚚 Tu pedido #{order.id} va en camino',
                'icon': '🚚',
                'color': '#ffc107',
                'heading': '¡Tu pedido ha sido enviado!',
                'message': 'Tu pedido ya salió de nuestras instalaciones y va en camino hacia ti. Muy pronto podrás disfrutar de nuestro chocolate premium.',
                'footer_msg': 'Te notificaremos cuando tu pedido sea entregado.'
            },
            'Pedido entregado': {
                'subject': f'✅ Tu pedido #{order.id} ha sido entregado',
                'icon': '🎉',
                'color': '#28a745',
                'heading': '¡Tu pedido fue entregado exitosamente!',
                'message': '¡Esperamos que disfrutes al máximo de nuestro chocolate artesanal! Tu satisfacción es nuestra mayor recompensa.',
                'footer_msg': '¡Gracias por ser parte de la familia Marichuy!'
            },
            'Cancelado': {
                'subject': f'❌ Tu pedido #{order.id} ha sido cancelado',
                'icon': '😔',
                'color': '#dc3545',
                'heading': 'Tu pedido ha sido cancelado',
                'message': 'Lamentamos informarte que tu pedido ha sido cancelado. Si tienes alguna duda o deseas realizar un nuevo pedido, no dudes en contactarnos.',
                'footer_msg': 'Estamos aquí para ayudarte en lo que necesites.'
            }
        }

        config = status_config.get(new_status)
        if not config:
            return False

        # Formatear método de pago
        payment_display = order.payment_method.capitalize() if order.payment_method else 'No especificado'
        order_date = format_datetime(order.created_at, '%d de %B de %Y a las %H:%M')

        html_body = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #3E2723 0%, #5D4037 100%); padding: 30px 20px; text-align: center;">
                <h1 style="color: #d4af37; margin: 0; font-size: 28px; letter-spacing: 3px;">🍫 MARICHUY</h1>
                <p style="color: #EFEBE4; margin: 8px 0 0 0; font-size: 13px; letter-spacing: 2px;">CHOCOLATES PREMIUM</p>
            </div>

            <!-- Status Icon -->
            <div style="text-align: center; padding: 25px 0 10px 0;">
                <div style="display: inline-block; width: 70px; height: 70px; border-radius: 50%; background-color: {config['color']}20; border: 3px solid {config['color']}; line-height: 70px; font-size: 32px;">
                    {config['icon']}
                </div>
            </div>

            <!-- Body -->
            <div style="padding: 20px 35px 30px 35px;">
                <h2 style="color: #d4af37; text-align: center; margin: 0 0 20px 0; font-size: 20px;">{config['heading']}</h2>
                
                <p style="color: #EFEBE4; font-size: 15px; line-height: 1.6;">Hola <strong style="color: #d4af37;">{customer_name}</strong>,</p>
                <p style="color: #ccc; font-size: 14px; line-height: 1.7;">{config['message']}</p>

                <!-- Order Details Box -->
                <div style="background-color: #2a2a2a; border: 1px solid #3E2723; border-radius: 10px; padding: 20px; margin: 25px 0;">
                    <h3 style="color: #d4af37; margin: 0 0 15px 0; font-size: 16px; border-bottom: 1px solid #444; padding-bottom: 10px;">📋 Detalles del pedido</h3>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="color: #999; padding: 8px 0; font-size: 13px;">N° de pedido</td>
                            <td style="color: #EFEBE4; padding: 8px 0; font-size: 13px; text-align: right; font-weight: bold;">#{order.id}</td>
                        </tr>
                        <tr>
                            <td style="color: #999; padding: 8px 0; font-size: 13px;">Fecha del pedido</td>
                            <td style="color: #EFEBE4; padding: 8px 0; font-size: 13px; text-align: right;">{order_date}</td>
                        </tr>
                        <tr>
                            <td style="color: #999; padding: 8px 0; font-size: 13px;">Método de pago</td>
                            <td style="color: #EFEBE4; padding: 8px 0; font-size: 13px; text-align: right;">{payment_display}</td>
                        </tr>
                        <tr>
                            <td style="color: #999; padding: 8px 0; font-size: 13px;">Total</td>
                            <td style="color: #d4af37; padding: 8px 0; font-size: 15px; text-align: right; font-weight: bold;">${order.total_amount:,.2f}</td>
                        </tr>
                    </table>

                    <!-- Status Badge -->
                    <div style="text-align: center; margin-top: 15px; padding-top: 15px; border-top: 1px solid #444;">
                        <span style="display: inline-block; background-color: {config['color']}; color: #fff; padding: 8px 20px; border-radius: 20px; font-size: 13px; font-weight: bold; letter-spacing: 1px;">
                            {new_status.upper()}
                        </span>
                    </div>
                </div>

                <p style="color: #8D6E63; font-size: 13px; text-align: center; font-style: italic;">{config['footer_msg']}</p>
            </div>

            <!-- Footer -->
            <div style="background-color: #111; padding: 20px; text-align: center; border-top: 2px solid #d4af37;">
                <p style="color: #d4af37; margin: 0 0 5px 0; font-size: 13px; font-weight: bold;">Marichuy Chocolates Premium</p>
                <p style="color: #666; margin: 0; font-size: 11px;">Elaboramos cada chocolate con pasión y excelencia.</p>
                <p style="color: #555; margin: 10px 0 0 0; font-size: 10px;">© 2026 Marichuy. Todos los derechos reservados.</p>
                <p style="color: #444; margin: 5px 0 0 0; font-size: 10px;">Este es un correo automático, por favor no respondas a esta dirección.</p>
            </div>
        </div>
        """

        body = (
            f"Hola {customer_name},\n\n"
            f"{config['message']}\n\n"
            f"Detalles del pedido:\n"
            f"- N° de pedido: #{order.id}\n"
            f"- Fecha: {order_date}\n"
            f"- Método de pago: {payment_display}\n"
            f"- Total: ${order.total_amount:,.2f}\n"
            f"- Estado actual: {new_status}\n\n"
            f"{config['footer_msg']}\n\n"
            f"Atentamente,\nEl equipo de Marichuy Chocolates Premium"
        )

        sender_email = current_app.config.get('MAIL_DEFAULT_SENDER', 'marichuyy.m.a@gmail.com')
        msg = Message(
            subject=config['subject'],
            sender=("Marichuy Chocolates", sender_email),
            recipients=[customer_email],
            body=body,
            html=html_body
        )

        mail.send(msg)
        print(f"Correo de estado '{new_status}' enviado exitosamente a {customer_email}")
        return True

    except Exception as e:
        print(f"Error enviando correo de estado: {e}")
        traceback.print_exc()
        return False


# ─────────────────────────────────────────────────────────────
# Correo de verificación de comprobante confirmada
# ─────────────────────────────────────────────────────────────
def send_verification_confirmed_email(order, customer_email, customer_name):
    """
    Envía un correo informando al cliente que su comprobante de pago fue verificado exitosamente.
    """
    try:
        order_date = format_datetime(order.created_at, '%d de %B de %Y a las %H:%M')
        payment_display = order.payment_method.capitalize() if order.payment_method else 'No especificado'

        html_body = f"""
        <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #1a1a1a; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #3E2723 0%, #5D4037 100%); padding: 30px 20px; text-align: center;">
                <h1 style="color: #d4af37; margin: 0; font-size: 28px; letter-spacing: 3px;">🍫 MARICHUY</h1>
                <p style="color: #EFEBE4; margin: 8px 0 0 0; font-size: 13px; letter-spacing: 2px;">CHOCOLATES PREMIUM</p>
            </div>

            <!-- Status Icon -->
            <div style="text-align: center; padding: 25px 0 10px 0;">
                <div style="display: inline-block; width: 70px; height: 70px; border-radius: 50%; background-color: rgba(40,167,69,0.15); border: 3px solid #28a745; line-height: 70px; font-size: 32px;">
                    ✅
                </div>
            </div>

            <!-- Body -->
            <div style="padding: 20px 35px 30px 35px;">
                <h2 style="color: #d4af37; text-align: center; margin: 0 0 20px 0; font-size: 20px;">¡Comprobante verificado exitosamente!</h2>
                
                <p style="color: #EFEBE4; font-size: 15px; line-height: 1.6;">Hola <strong style="color: #d4af37;">{customer_name}</strong>,</p>
                <p style="color: #ccc; font-size: 14px; line-height: 1.7;">Hemos verificado exitosamente tu comprobante de pago para el pedido <strong style="color: #d4af37;">#{order.id}</strong>.</p>
                <p style="color: #ccc; font-size: 14px; line-height: 1.7;">Tu pago ha sido confirmado y comenzaremos a preparar tu pedido muy pronto.</p>

                <!-- Order Details Box -->
                <div style="background-color: #2a2a2a; border: 1px solid #3E2723; border-radius: 10px; padding: 20px; margin: 25px 0;">
                    <h3 style="color: #d4af37; margin: 0 0 15px 0; font-size: 16px; border-bottom: 1px solid #444; padding-bottom: 10px;">📋 Detalles del pedido</h3>
                    
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="color: #999; padding: 8px 0; font-size: 13px;">N° de pedido</td>
                            <td style="color: #EFEBE4; padding: 8px 0; font-size: 13px; text-align: right; font-weight: bold;">#{order.id}</td>
                        </tr>
                        <tr>
                            <td style="color: #999; padding: 8px 0; font-size: 13px;">Fecha del pedido</td>
                            <td style="color: #EFEBE4; padding: 8px 0; font-size: 13px; text-align: right;">{order_date}</td>
                        </tr>
                        <tr>
                            <td style="color: #999; padding: 8px 0; font-size: 13px;">Método de pago</td>
                            <td style="color: #EFEBE4; padding: 8px 0; font-size: 13px; text-align: right;">{payment_display}</td>
                        </tr>
                        <tr>
                            <td style="color: #999; padding: 8px 0; font-size: 13px;">Total</td>
                            <td style="color: #d4af37; padding: 8px 0; font-size: 15px; text-align: right; font-weight: bold;">${order.total_amount:,.2f}</td>
                        </tr>
                    </table>

                    <!-- Status Badge -->
                    <div style="text-align: center; margin-top: 15px; padding-top: 15px; border-top: 1px solid #444;">
                        <span style="display: inline-block; background-color: #28a745; color: #fff; padding: 8px 20px; border-radius: 20px; font-size: 13px; font-weight: bold; letter-spacing: 1px;">
                            PAGO VERIFICADO ✓
                        </span>
                    </div>
                </div>

                <p style="color: #ccc; font-size: 14px; line-height: 1.7; text-align: center;">Gracias por confiar en <strong style="color: #d4af37;">Marichuy Chocolates Premium</strong>.</p>
                <p style="color: #8D6E63; font-size: 13px; text-align: center; font-style: italic;">🍫 Elaboramos cada chocolate con pasión y excelencia.</p>
            </div>

            <!-- Footer -->
            <div style="background-color: #111; padding: 20px; text-align: center; border-top: 2px solid #d4af37;">
                <p style="color: #d4af37; margin: 0 0 5px 0; font-size: 13px; font-weight: bold;">Marichuy Chocolates Premium</p>
                <p style="color: #666; margin: 0; font-size: 11px;">Elaboramos cada chocolate con pasión y excelencia.</p>
                <p style="color: #555; margin: 10px 0 0 0; font-size: 10px;">© 2026 Marichuy. Todos los derechos reservados.</p>
                <p style="color: #444; margin: 5px 0 0 0; font-size: 10px;">Este es un correo automático, por favor no respondas a esta dirección.</p>
            </div>
        </div>
        """

        body = (
            f"Hola {customer_name},\n\n"
            f"Hemos verificado exitosamente tu comprobante de pago para el pedido #{order.id}.\n\n"
            f"Tu pago ha sido confirmado y comenzaremos a preparar tu pedido muy pronto.\n\n"
            f"Detalles del pedido:\n"
            f"- N° de pedido: #{order.id}\n"
            f"- Fecha: {order_date}\n"
            f"- Método de pago: {payment_display}\n"
            f"- Total: ${order.total_amount:,.2f}\n\n"
            f"Gracias por confiar en Marichuy Chocolates Premium.\n\n"
            f"🍫 Elaboramos cada chocolate con pasión y excelencia.\n\n"
            f"Atentamente,\nEl equipo de Marichuy"
        )

        sender_email = current_app.config.get('MAIL_DEFAULT_SENDER', 'marichuyy.m.a@gmail.com')
        msg = Message(
            subject=f'✅ Comprobante verificado - Pedido #{order.id}',
            sender=("Marichuy Chocolates", sender_email),
            recipients=[customer_email],
            body=body,
            html=html_body
        )

        mail.send(msg)
        print(f"Correo de verificación confirmada enviado exitosamente a {customer_email}")
        return True

    except Exception as e:
        print(f"Error enviando correo de verificación: {e}")
        traceback.print_exc()
        return False
