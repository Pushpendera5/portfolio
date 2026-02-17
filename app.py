import os
from flask import Flask, render_template, request, flash, redirect, url_for ,send_from_directory
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'pushpendra_portfolio_key'

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'testingpushpendra@gmail.com' # Apna Gmail yahan likhein
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')    # Apna 16-digit App Password yahan likhein

# YEH LINE ZAROORI HAI:
app.config['MAIL_DEFAULT_SENDER'] = 'testingpushpendra@gmail.com' 

mail = Mail(app)
@app.route('/send_message', methods=['POST'])
def send_message():
    # 1. Capture the form data
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message_body = request.form.get('message')

    # 2. Create the Email Message
    # We send it TO your testing email FROM the form user
    msg = Message(
        subject=f"Portfolio: {subject}",
        sender=app.config['MAIL_USERNAME'],
        recipients=['testingpushpendra@gmail.com'], # Where you want to RECEIVE the mail
        body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_body}"
    )

    try:
        # 3. Attempt to send
        mail.send(msg)
        # 4. Redirect back to home so the user doesn't see a blank error page
        return redirect(url_for('index')) 
    
    except Exception as e:
        # If SMTP fails (wrong password, etc.), this prints to Render logs
        print(f"Mail Error: {e}")
        return f"Error sending message: {e}", 500

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download-resume')
def download_resume():
    # Yeh line system ka absolute path nikal legi
    resume_path = os.path.join(app.root_path, 'static')
    
    try:
        return send_from_directory(
            directory=resume_path, 
            path='resume.pdf', 
            as_attachment=True
        )
    except FileNotFoundError:
        return "Error: File 'resume.pdf' not found in static folder!", 404

    # Message object mein 'sender' parameter add kar diya hai taaki error na aaye
    msg = Message(
        subject=f"Portfolio Contact: {subject}",
        sender=app.config['MAIL_USERNAME'], # Explicitly defining sender
        recipients=['sachanpushpendra03@gmai.com'], # Jahan aapko mail chahiye
        body=f"new chutiya send you a massage malik check kro isko:\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message_body}"
    )

    try:
        mail.send(msg)
        flash("Success! Your message has been sent.", "success")
    except Exception as e:
        # Debugging ke liye pura error dikhayega
        flash(f"Error: {str(e)}", "error")
    
    return redirect(url_for('index'))
if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=port)