from flask import(
    Blueprint, render_template, request, redirect, url_for, current_app
)
import sendgrid
from sendgrid.helpers.mail import *
from flask.templating import render_template
bp = Blueprint('portfolio', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html')

@bp.route('/mail', methods=['GET','POST'])
def mail():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if request.method == 'POST':
        send_mail(name, email, message)
        return render_template('portfolio/sent_mail.html')

    return redirect(url_for('portfolio.index'))

def send_mail(name, email, message):  
    mi_email = 'tomassilvente10@gmail.com'
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])
    
    from_email = Email(mi_email)
    to_email = To('silventetomas@gmail.com', substitutions={
        "-name-": name,
        "-email-": email,
        "-message-": message,
    })

    html_content = """
            <p> Hola Tomas, tienes un nuevo contacto desde la web: </p>
            <p> Nombre: -name- </p>
            <p> Correo: -email- </p>
            <p> Mensaje: -message- </p>
    """
    mail = Mail(mi_email, to_email, 'Nuevo Contacto desde la web', html_content=html_content)
    response =  sg.client.mail.send.post(request_body=mail.get())