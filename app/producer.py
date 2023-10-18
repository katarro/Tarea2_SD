from sendgrid.helpers.mail import Mail, From, To, Content, TemplateId
from flask import Flask, render_template, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from kafka import KafkaProducer
import json
import os


app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers=['kafka1:9092', 'kafka2:9093', 'kafka3:9094'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'address': request.form['address'],
            'phone': request.form['phone'],
            'type': request.form['type'],
            'password': request.form['password'],
            'email': request.form['email']
        }
        
        # Determinar a qué tópico enviar basado en si el mensaje está marcado como "Paid"
        topic = 'regular-topic'
        if data.get('type') == 'paid':
            topic = 'paid-topic'
        
        producer.send(topic, value=data)

        # Enviar correo electrónico con SendGrid
        message = send_email(data['email'], data['password'])

    return render_template('index.html', message=message)


def send_email(recipient_email, password):
    message = Mail(
        from_email='felipe.castro3@mail.udp.cl',
        to_emails=recipient_email,
        subject='Tus credenciales',
        html_content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 50px auto;
                        background-color: #fff;
                        padding: 20px 30px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 20px;
                    }}
                    .header img {{
                        max-width: 150px;
                    }}
                    .content {{
                        font-size: 16px;
                        line-height: 1.5;
                    }}
                    .credentials {{
                        background-color: #f9f9f9;
                        padding: 10px 15px;
                        border-radius: 5px;
                        margin: 20px 0;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        color: #888;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <img src="https://www.tipicochileno.cl/wp-content/uploads/2018/01/receta-mote-con-huesillo-576X205.jpg" alt="Your Logo"> 
                        <h2>Bienvenido a MAMOCHI</h2>  
                    </div>
                    <div class="content">
                        <p><strong>Hola,</strong></p>
                        <p>Gracias por registrarte en MAMOCHI. Aquí están tus credenciales:</p>
                        <div class="credentials">
                            <p><strong>Correo:</strong> {recipient_email}</p>
                            <p><strong>Contraseña:</strong> {password}</p>
                        </div>
                        <p>Por favor, guarda esta información en un lugar seguro.</p>
                    </div>
                    <div class="footer">
                        <p>Si tienes alguna pregunta, no dudes en <a href="mailto:support@your-service.com">contactarnos</a>.</p>  <!-- Replace with your support email -->
                    </div>
                </div>
            </body>
            </html>
            '''
        )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return f"Correo enviado con éxito. Código de respuesta: {response.status_code}"
    except Exception as e:
        return f"Error al enviar el correo: {str(e)}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
