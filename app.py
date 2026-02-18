import os
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from flask_mail import Mail, Message
from bytez import Bytez

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pushpendra_portfolio_key')

# --- AI CONFIGURATION ---
key = os.environ.get("BYTEZ_KEY", "3f111f6b8edb9dbf37694dbceab79386")
sdk = Bytez(key)
model = sdk.model("inference-net/Schematron-3B")

# Context for the AI
MY_CONTEXT = """
Pushpendra Sachan is an AI/ML Engineer pursuing MCA from Manipal University Jaipur.
Skills: Python, Flask, Django, Deep Learning, Computer Vision, SQL.
Experience: Technical Support Engineer at Wayinfotech Solutions.
Projects: AI Chatbot, NLP Sentiment Analysis, Object Detection.
"""

# --- MAIL CONFIGURATION ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'testingpushpendra@gmail.com' 
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'testingpushpendra@gmail.com' 

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

# --- YOUR PERSONAL DATA ---
# Edit this section to add more details about your projects or hobbies
MY_INFO = """
You are the personal AI assistant for Pushpendra Sachan. 
Here is his background:
- Role: AI/ML Engineer.
- Education: Pursuing MCA (AI specialization) from Manipal University Jaipur (3rd Semester).
- Technical Skills: Python, Flask, Django, Deep Learning, Computer Vision, SQL, RFID Technology.
- Previous Experience: Technical Support Engineer at Zeel Infotech (Bharti Airtel nodal office).
- Key Projects: 
    1. Automated Attendance System using Face Recognition (for 50 employees).
    2. Restaurant Management App with WhatsApp ordering integration.
    3. AI Chatbot using Bytez SDK.
    4. NLP Sentiment Analysis.
- Goals: He is passionate about building scalable AI solutions.
"""
MY_INFO = """
Name: Pushpendra Sachan.
Role: AI/ML Engineer.
Education: MCA in AI, Manipal University Jaipur (3rd Sem).
Skills: Python, Flask, Django, CV, NLP, RFID.
Projects: Face Recognition Attendance, WhatsApp Restaurant App.
"""
MY_CONTEXT = """
You are the personal AI Assistant of Pushpendra Sachan. 
Pushpendra Sachan is an AI/ML Engineer pursuing MCA from Manipal University Jaipur.
Your job is to provide information about Pushpendra's skills, projects, and experience to recruiters and visitors.
"""
MY_CONTEXT = """
Subject: Pushpendra Sachan
Role: Technical Support Engineer & AI/ML Aspirant
Contact: sachanpushpendra03@gmail.com | +91-6388098635
Location: Kanpur, Uttar Pradesh
LinkedIn: linkedin.com/in/pushpendra-sachan-942095252

Current Experience: Technical Support Engineer at POXO RFID AUTOMATION (Oct 2023 - Present). 
Key Achievements: 96% first-contact resolution rate, reduced deployment timelines by 38% using SCCM.

Expertise: 
- Infrastructure: Active Directory, TCP/IP, LAN/WAN, DNS/DHCP, Firewalls.
- Systems: SCCM, Windows Server, PowerShell Scripting, OS Imaging (WDS/MDT).
- Specialized: RFID Automation, CCTV, Access Control.
- Cloud/Virtualization: VMware, Hyper-V, AWS EC2, Azure VMs.
- Databases: MS SQL Server (T-SQL).

Education:
- MCA in AI (2024 - Present) from Manipal University Jaipur.
- B.Sc. in Mathematics (2022).
"""
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        user_message = data.get("message")
        
        # Aggressive Language Instruction
        prompt = f"""
        [STRICT RULE: RESPOND IN THE SAME LANGUAGE AS THE USER]
        If user asks in English, reply in English.
        If user asks in Hindi, reply in English.
        Identity: You are the AI Assistant for Pushpendra Sachan's Portfolio.
        Personal Data: {MY_CONTEXT}
        
        STRICT RULES:
        1. If the user asks about Pushpendra (Who is he? Skills? Work? Education?), ONLY use the 'Personal Data' above. 
        2. If the user asks general questions (e.g., "What is Python?", "How to fix a slow PC?"), use your general AI knowledge to answer.
        3. Keep all answers VERY CONCISE (maximum 2-3 sentences).
        4. Match the user's language (Hindi, English, or Hinglish).
        5. Do not talk about things not present in the data if the question is about Pushpendra.
        
        Developer Info: {MY_INFO}
        Identity: You are Pushpendra Sachan's AI Assistant. Do NOT say "I am Pushpendra". 
        Always say "I am Pushpendra's AI Assistant" or "Pushpendra is an AI/ML Engineer".
        
        Context: {MY_CONTEXT}
        
        User Question: {user_message}
        Assistant Answer:"""
        

        results = model.run([{"role": "user", "content": prompt}])
        
        ai_data = results.output
        if isinstance(ai_data, dict) and 'content' in ai_data:
            final_reply = ai_data['content']
        elif isinstance(ai_data, list) and len(ai_data) > 0:
            final_reply = ai_data[0].get('content', str(ai_data[0]))
        else:
            final_reply = str(ai_data)

        # Cleanup: Agar model 'Assistant Answer:' prefix bhej raha ho
        final_reply = final_reply.replace("Assistant Answer:", "").strip()

        return jsonify({"reply": final_reply.replace("\n", "<br>")})

    except Exception as e:
        return jsonify({"reply": "Error connecting to AI."}), 500
@app.route('/send_message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message_body = request.form.get('message')

    msg = Message(
        subject=f"Portfolio Contact: {subject}",
        sender=app.config['MAIL_USERNAME'],
        recipients=['testingpushpendra@gmail.com'],
        body=f"Owner, naya message aaya hai!\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message_body}"
    )
    try:
        mail.send(msg)
        flash("Success! Your message has been sent.", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
    return redirect(url_for('index'))

@app.route('/download-resume')
def download_resume():
    resume_path = os.path.join(app.root_path, 'static')
    try:
        return send_from_directory(directory=resume_path, path='resume.pdf', as_attachment=True)
    except FileNotFoundError:
        return "Error: File 'resume.pdf' not found!", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)