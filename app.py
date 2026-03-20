import os
import socket
import smtplib
import json
from urllib import error as urlerror
from urllib import request as urlrequest
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from flask_mail import Mail, Message
from bytez import Bytez

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'pushpendra_portfolio_key')


def _get_bool_env(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _safe_flash(message, category="message"):
    try:
        text = str(message)
        max_len = 300
        if len(text) > max_len:
            text = text[: max_len - 3] + "..."
        flash(text, category)
    except Exception:
        app.logger.exception("Failed to write flash message")


def _check_smtp_connectivity(host, port, timeout_seconds=3):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout_seconds):
            return True, ""
    except Exception as exc:
        return False, str(exc)


def _send_via_resend(subject, text_body, reply_to=None):
    api_key = os.environ.get("RESEND_API_KEY", "").strip()
    from_email = os.environ.get("RESEND_FROM", "").strip()

    missing = []
    if not api_key:
        missing.append("RESEND_API_KEY")
    if not from_email:
        missing.append("RESEND_FROM")
    if not CONTACT_RECIPIENT:
        missing.append("CONTACT_RECIPIENT")
    if missing:
        raise ValueError(f"Missing Resend config: {', '.join(missing)}")

    payload = {
        "from": from_email,
        "to": [CONTACT_RECIPIENT],
        "subject": subject,
        "text": text_body,
    }
    if reply_to:
        payload["reply_to"] = reply_to

    req = urlrequest.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    timeout_seconds = float(os.environ.get("RESEND_TIMEOUT", "10"))
    try:
        with urlrequest.urlopen(req, timeout=timeout_seconds) as response:
            response.read()
    except urlerror.HTTPError as exc:
        error_body = exc.read().decode("utf-8", "replace")
        snippet = error_body[:200].replace("\n", " ").strip()
        raise RuntimeError(f"Resend API error {exc.code}: {snippet}") from exc
    except urlerror.URLError as exc:
        raise RuntimeError(f"Resend API network error: {exc.reason}") from exc


def _send_via_formsubmit(name, email, subject, message_body):
    recipient = (CONTACT_RECIPIENT or "").strip()
    if not recipient:
        raise ValueError("Missing CONTACT_RECIPIENT for FormSubmit fallback")

    payload = {
        "name": name or "Website Visitor",
        "email": email or "not-provided@example.com",
        "subject": subject or "Portfolio Contact: No Subject",
        "message": message_body or "No message body",
        "_captcha": "false",
        "_template": "table",
    }

    req = urlrequest.Request(
        f"https://formsubmit.co/ajax/{recipient}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    timeout_seconds = float(os.environ.get("FORMSUBMIT_TIMEOUT", "10"))
    try:
        with urlrequest.urlopen(req, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8", "replace")
            data = json.loads(body) if body else {}
            if not data.get("success"):
                raise RuntimeError(f"FormSubmit response: {body}")
    except urlerror.HTTPError as exc:
        raise RuntimeError(f"FormSubmit error {exc.code}") from exc
    except urlerror.URLError as exc:
        raise RuntimeError(f"FormSubmit network error: {exc.reason}") from exc

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
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = _get_bool_env('MAIL_USE_TLS', True)
app.config['MAIL_USE_SSL'] = _get_bool_env('MAIL_USE_SSL', False)
app.config['MAIL_TIMEOUT'] = int(os.environ.get('MAIL_TIMEOUT', 10))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'testingpushpendra@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])
CONTACT_RECIPIENT = os.environ.get('CONTACT_RECIPIENT', app.config['MAIL_USERNAME'])

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/keepalive', methods=['GET', 'POST'])
def keepalive():
    """Keep-alive endpoint to prevent server/model timeout"""
    return jsonify({"status": "alive", "timestamp": str(__import__('datetime').datetime.now())})

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
*** IMPORTANT: This AI Chatbot is developed ONLY by Pushpendra Sachan as a solo project. No team involved. Pushpendra Sachan is the sole developer, creator, and owner. ***

Subject: Pushpendra Sachan
Role: Technical Support Engineer & AI/ML Aspirant
Contact: sachanpushpendra03@gmail.com | +91-6388098635
Location: Kanpur, Uttar Pradesh
LinkedIn: linkedin.com/in/pushpendra-sachan-942095252

PERSONAL INFORMATION:
- Name: Pushpendra Sachan
- Age: 27 years old
- Location: Kanpur, Uttar Pradesh, India
- Email: sachanpushpendra03@gmail.com
- Phone: +91-6388098635
- LinkedIn: linkedin.com/in/pushpendra-sachan-942095252

ABOUT:
Pushpendra Sachan is a Technical Support Engineer & AI/ML Aspirant based in Kanpur, Uttar Pradesh. Currently, he works at POXO RFID AUTOMATION since October 2023. In this role, he has achieved a remarkable 96% first-contact resolution rate and has successfully reduced deployment timelines by 38% using SCCM. He is passionate about building scalable AI/ML solutions and combining them with infrastructure expertise.

PASSION & GOALS:
- Passionate about both technical support and AI/ML
- Interested in building intelligent automation systems
- Goal: Combine RFID automation with AI for smart solutions
- Aspires to work on cutting-edge ML/AI projects

TECHNICAL EXPERTISE:

Infrastructure & Networking:
- Active Directory, TCP/IP, LAN/WAN, DNS/DHCP, Firewalls
- Network troubleshooting and optimization
- IT Infrastructure management

Systems Administration:
- SCCM (Systems Center Configuration Manager) - 38% deployment timeline reduction
- Windows Server administration
- PowerShell Scripting for automation
- OS Imaging (WDS/MDT)
- Group Policy management
- 96% first-contact resolution rate in current role

Specialized Technologies:
- RFID Automation & RFID Technology
- CCTV systems integration
- Access Control systems
- IoT device management

Cloud & Virtualization:
- VMware
- Hyper-V
- AWS EC2 instances
- Microsoft Azure VMs
- Cloud infrastructure optimization

Programming & Development:
- Python (AI/ML focus)
- Flask web framework
- Django web framework
- SQL & Database Management
- T-SQL (MS SQL Server)
- JavaScript
- HTML/CSS

AI/ML & Data Science:
- Deep Learning
- Computer Vision (Face Recognition, Object Detection)
- Natural Language Processing (NLP)
- Sentiment Analysis
- Machine Learning workflows

EDUCATION:
- MCA in Artificial Intelligence (2024 - Present) - Manipal University Jaipur, 3rd Semester
- B.Sc. in Mathematics (2022)
- 12th Grade: 88.8% from Vikas Vidhya Mandir
- 10th Grade: 85% from Vikas Vidhya Mandir

CURRENT EMPLOYMENT:
- Title: Technical Support Engineer
- Company: POXO RFID AUTOMATION
- Duration: October 2023 - Present
- Key Achievements:
  * 96% first-contact resolution rate
  * 38% reduction in deployment timelines using SCCM
  * Expert in RFID automation and infrastructure support

PREVIOUS EXPERIENCE:
- Technical Support Engineer at Zeel Infotech (Bharti Airtel nodal office) - Provided infrastructure and system support

KEY PROJECTS:
1. Automated Attendance System using Face Recognition
   - Built a face recognition system for employee attendance tracking
   - Supports 50+ employees
   - Real-time identification and logging

2. Restaurant Management App with WhatsApp Integration
   - Full-stack application with order management
   - WhatsApp API integration for ordering
   - Database-backed order tracking system

3. AI Chatbot using Bytez SDK
   - Conversational AI with memory system
   - Context-aware responses
   - Deployed on personal portfolio

4. NLP Sentiment Analysis
   - Analyzes text sentiment (positive/negative)
   - Applied to social media monitoring

5. Object Detection System
   - Computer vision based object identification
   - Real-time detection capabilities

INTERESTS & HOBBIES:
- AI and Machine Learning research
- Building end-to-end ML solutions
- Automation and systems optimization
- Open source contributions
- Technical writing and documentation

TECHNICAL SKILLS SUMMARY:
- Languages: Python, SQL, PowerShell, JavaScript, HTML/CSS
- Web Frameworks: Flask, Django
- AI/ML: Deep Learning, CV, NLP
- Cloud: AWS, Azure
- Virtualization: VMware, Hyper-V
- Tools: SCCM, Active Directory, Git

SOFT SKILLS:
- Problem-solving and troubleshooting
- 96% customer satisfaction (first-contact resolution)
- Leadership and teamwork
- Clear communication
- Ability to learn new technologies quickly

ACHIEVEMENTS:
- 38% improvement in deployment timelines
- 96% first-contact resolution rate
- Successfully completed multiple AI/ML projects
- Currently pursuing advanced degree in AI/ML

AVAILABILITY:
- Open to job opportunities in AI/ML, Data Science
- Available for freelance/consulting projects
- Willing to relocate for right opportunity

ABOUT THIS AI CHATBOT:
- **SOLE DEVELOPER**: Pushpendra Sachan (100% developed by him, no team)
- **OWNER**: Pushpendra Sachan
- **CREATOR**: Pushpendra Sachan  
- **MANAGER/BOSS**: Pushpendra Sachan (it's his project)
- **Purpose**: Intelligent assistant for the portfolio website
- **Built Entirely By**: Pushpendra Sachan (solo project)
- **Technologies Used**: Python, Flask, Bytez AI SDK, JavaScript
- **Features**: Conversation memory, context-aware responses, portfolio data
- **IMPORTANT**: When asked who created/developed/built/owns this chatbot - Answer ALWAYS: "Pushpendra Sachan is the sole developer and creator. He built this as a solo project."
- **NO TEAM, NO COMPANY** - This chatbot is entirely Pushpendra Sachan's creation
- This AI showcases Pushpendra's AI/ML development and engineering skills

LINKS & PORTFOLIO:
- Portfolio Website: (This website)
- GitHub: Available in portfolio
- LinkedIn: linkedin.com/in/pushpendra-sachan-942095252
- Email: sachanpushpendra03@gmail.com
"""
@app.route('/ask', methods=['POST'])
def ask():
    try:
        from datetime import datetime
        
        data = request.json
        user_message = data.get("message")
        conversation_history = data.get("conversation_history", [])
        
        # Clean up context by removing HTML tags
        clean_context = MY_CONTEXT.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
        
        # Build conversation context from history
        conversation_context = ""
        if conversation_history:
            conversation_context = "\n\nConversation History:\n"
            for msg in conversation_history:
                role = "User" if msg['role'] == 'user' else "Assistant"
                conversation_context += f"{role}: {msg['content']}\n"
        
        # Check if this is a REPEATED question (same question asked before)
        def is_similar_question(q1, q2, threshold=0.6):
            """Check if two questions are similar (70%+ word overlap)"""
            words1 = set(q1.lower().split())
            words2 = set(q2.lower().split())
            if not words1 or not words2:
                return False
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            similarity = intersection / union if union > 0 else 0
            return similarity >= threshold
        
        # Count how many times similar question was asked
        repeated_count = 0
        if conversation_history:
            for msg in conversation_history:
                if msg['role'] == 'user' and is_similar_question(user_message, msg['content']):
                    repeated_count += 1
        
        is_repeated_question = repeated_count > 0
        repeat_instruction = ""
        if is_repeated_question:
            repeat_instruction = f"\n\n**IMPORTANT**: This question (or similar) was asked {repeated_count} time(s) before. You provided an answer before. NOW give a DIFFERENT variation/rephrasing of that answer - same meaning, but different words and structure. Use different examples or explanations."
        
        # Detect if this is a greeting/casual message (NOT asking about Pushpendra)
        greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy', 'hola', 'namaste', 'how are you', 'whats up', 'wassup']
        user_lower = user_message.lower()
        is_greeting = any(keyword in user_lower for keyword in greeting_keywords)
        
        # Check if asking about Pushpendra (skills, projects, experience, etc)
        # NOTE: "tell me about" alone is too broad (e.g., "tell me about delhi").
        # It should count as Pushpendra-intent only when combined with self/profile references.
        pushpendra_keywords = [
            'pushpendra', 'your skills', 'your projects', 'your experience', 'your work',
            'what do you do', 'portfolio', 'your background', 'who are you',
            'what are your skills', 'about you', 'your expertise', 'yourself'
        ]
        tell_me_about_self_refs = [
            'pushpendra', 'you', 'yourself', 'your work', 'your skills',
            'your projects', 'your experience', 'your background', 'portfolio'
        ]
        is_tell_me_about_self = 'tell me about' in user_lower and any(
            ref in user_lower for ref in tell_me_about_self_refs
        )
        is_asking_about_pushpendra = any(keyword in user_lower for keyword in pushpendra_keywords) or is_tell_me_about_self
        
        # Detect if asking about this CHATBOT specifically (developer, creator, builder) - CHECK FIRST PRIORITY
        asking_about_chatbot_creator = any(kw in user_lower for kw in ['who created you', 'who built you', 'your developer', 'your creator', 'who made you', 'who developed you', 'who built this', 'your boss', 'your owner', 'who created this chatbot', 'who is behind this', 'who developed this chatbot', 'who is your boss', 'who is the boss', 'who is my boss', 'my boss', 'your boss', 'boss', 'owner', 'whos your boss', 'whats your boss', 'who made this', 'who developed this', 'who is behind', 'who developed me', 'who is my developer', 'who created me', 'developer', 'creator', 'built me', 'created me', 'made me', 'your creator'])
        
        # DEBUG: Log detection for chatbot creator questions
        print(f"[DEBUG] user_lower: '{user_lower}'")
        print(f"[DEBUG] asking_about_chatbot_creator: {asking_about_chatbot_creator}")
        
        # Detect WHAT specifically is being asked about Pushpendra
        asking_about_skills = any(kw in user_lower for kw in ['skill', 'expertise', 'what can you do', 'know', 'proficient'])
        asking_about_projects = any(kw in user_lower for kw in ['project', 'built', 'created', 'worked on'])
        asking_about_experience = any(kw in user_lower for kw in ['experience', 'background', 'worked', 'job', 'company'])
        asking_who = any(kw in user_lower for kw in ['who is', 'who are you', 'tell me about', 'about you', 'introduce'])
        
        # Get current time for greeting
        current_hour = datetime.now().hour
        if current_hour < 12:
            time_greeting = "Good morning"
        elif current_hour < 18:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"
        
        # Different prompts based on whether asking about Pushpendra
        if asking_about_chatbot_creator:
            # CHATBOT CREATOR MODE - ABSOLUTE PRIORITY - Clear answer: Pushpendra Sachan only
            prompt = f"""IMPORTANT: This is a SPECIAL QUESTION about THIS AI CHATBOT specifically.

**ABSOLUTE RULE - THIS IS NOT A GENERAL QUESTION:**
The user is asking about WHO CREATED/OWNS/RUNS THIS CHATBOT - Not about AI assistants in general.

**THE ANSWER IS ALWAYS:** Pushpendra Sachan

- "who is your boss?" → "Pushpendra Sachan is the boss of this chatbot. He's the sole developer who created me."
- "who created you?" → "Pushpendra Sachan created me using Python, Flask, and Bytez AI SDK."
- "who is the owner?" → "Pushpendra Sachan is the sole owner and developer of this chatbot."
- "boss?" → "Pushpendra Sachan is the boss. He built this chatbot."

**CRITICAL:**
- This is about THIS specific chatbot, not AI in general
- DO NOT say "I don't have a boss" or "AI assistants don't have bosses"
- ALWAYS answer: "Pushpendra Sachan"
- NEVER mention any company (except in context of HIS employment)
- NEVER say Pushpendra has a boss
- Pushpendra Sachan created this chatbot as a solo project - HE is the boss{repeat_instruction}

{clean_context}

PREVIOUS CONVERSATION:
{conversation_context if conversation_context else "(First message)"}

USER ASKED: {user_message}

ANSWER (MUST be about Pushpendra Sachan being the boss/creator of THIS chatbot - 1-2 sentences):"""
        elif is_asking_about_pushpendra:
            # SPECIFIC MODE - Answer ONLY what was asked, not everything
            context_hint = "ABOUT PUSHPENDRA:\n" + clean_context
            
            if asking_about_skills:
                prompt = f"""You are Pushpendra Sachan's AI Assistant. Answer about his skills in 1-2 sentences MAX.{repeat_instruction}

{context_hint}

PREVIOUS CONVERSATION:
{conversation_context if conversation_context else "(First message)"}

RULES:
- Answer from the portfolio data above
- Focus on Pushpendra's technical skills/expertise
- Be concise (1-2 sentences)
- NO labels like "Answer:" or "Response:"
- Mention specific technologies/tools

USER ASKED: {user_message}

ANSWER (1-2 sentences):"""
            elif asking_about_projects:
                prompt = f"""You are Pushpendra Sachan's AI Assistant. Answer about his projects in 1-2 sentences MAX.{repeat_instruction}

{context_hint}

PREVIOUS CONVERSATION:
{conversation_context if conversation_context else "(First message)"}

RULES:
- Answer from the portfolio data above
- Mention specific projects he has built
- Be concise (1-2 sentences)
- NO labels like "Answer:" or "Response:"
- If asked about a specific project, provide details

USER ASKED: {user_message}

ANSWER (1-2 sentences):"""
            elif asking_about_experience:
                prompt = f"""You are Pushpendra Sachan's AI Assistant. Answer about his experience/background in 1-2 sentences MAX.{repeat_instruction}

{context_hint}

PREVIOUS CONVERSATION:
{conversation_context if conversation_context else "(First message)"}

RULES:
- Answer from the portfolio data above
- Share his work experience and education
- Be concise (1-2 sentences)
- NO labels like "Answer:" or "Response:"
- Mention relevant achievements/milestones

USER ASKED: {user_message}

ANSWER (1-2 sentences):"""
            elif asking_who:
                prompt = f"""You are Pushpendra Sachan's AI Assistant. Give a brief intro in 1-2 sentences MAX.{repeat_instruction}

{context_hint}

PREVIOUS CONVERSATION:
{conversation_context if conversation_context else "(First message)"}

RULES:
- Give a brief intro with his role and expertise
- Be concise (1-2 sentences)
- NO labels like "Answer:" or "Response:"
- Make it friendly and informative
- Highlight what makes him unique

USER ASKED: {user_message}

BRIEF INTRO (1-2 sentences):"""
            else:
                # Generic Pushpendra question
                prompt = f"""You are Pushpendra Sachan's AI Assistant. Answer in 1-2 sentences MAX.{repeat_instruction}

{context_hint}

PREVIOUS CONVERSATION:
{conversation_context if conversation_context else "(First message)"}

RULES:
- Answer from the portfolio data above
- Be helpful and informative
- Be concise (1-2 sentences)
- NO labels like "Answer:", "Response:", etc
- Provide clear, direct answers
- Remember conversation context

USER ASKED: {user_message}

ANSWER (1-2 sentences):"""
        else:
            # GENERAL/CASUAL MODE - friendly replies with general knowledge
            prompt = f"""{time_greeting}! I'm Pushpendra's AI Assistant.{repeat_instruction}

PREVIOUS CONVERSATION:
{conversation_context if conversation_context else "(First message)"}

Answer the user's question in 1-2 sentences in a friendly, conversational way. You can provide general knowledge and helpful information for any topic. Be casual, fun, and helpful. Remember the previous conversation and respond naturally. If they ask about Pushpendra or his work specifically, mention he's an AI/ML engineer and invite them to ask more.

USER MESSAGE: {user_message}

FRIENDLY REPLY (1-2 sentences):"""
        

        results = model.run([{"role": "user", "content": prompt}])
        
        ai_data = results.output
        if isinstance(ai_data, dict) and 'content' in ai_data:
            final_reply = ai_data['content']
        elif isinstance(ai_data, list) and len(ai_data) > 0:
            final_reply = ai_data[0].get('content', str(ai_data[0]))
        else:
            final_reply = str(ai_data)

        # Aggressive cleanup: Remove leading assistant label when returned by the model
        final_reply = final_reply.replace("Assistant Answer:", "").replace("Assistant:", "").strip()
        
        # Remove the user's question if it appears at the start of the answer
        if user_message and final_reply.lower().startswith(user_message.lower()):
            final_reply = final_reply[len(user_message):].strip()
        
        # Remove any labels like "Answer:", "Response:", etc
        final_reply = final_reply.lstrip("Answer:").lstrip("Response:").lstrip("Reply:").lstrip("Brief Answer:").strip()
        
        # If response is too long (more than 3 sentences), truncate it
        sentences = final_reply.split('. ')
        if len(sentences) > 2:
            final_reply = '. '.join(sentences[:2]) + ('.' if not sentences[1].endswith('.') else '')

        return jsonify({"reply": final_reply.replace("\n", "<br>")})

    except Exception as e:
        return jsonify({"reply": "Error connecting to AI."}), 500
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        subject = (request.form.get("subject") or "").strip()
        message_body = (request.form.get("message") or "").strip()
        final_subject = f"Portfolio Contact: {subject or 'No Subject'}"
        final_body = (
            "Owner, you have a new message!\n\n"
            f"Name: {name or 'Not provided'}\n"
            f"Email: {email or 'Not provided'}\n\n"
            f"Message:\n{message_body or 'No message body'}"
        )

        provider = os.environ.get("MAIL_PROVIDER", "auto").strip().lower()
        formsubmit_enabled = _get_bool_env("FORMSUBMIT_ENABLE", False)
        use_resend = provider == "resend" or (
            provider == "auto" and bool(os.environ.get("RESEND_API_KEY"))
        )
        use_formsubmit_only = provider == "formsubmit"

        if use_resend:
            _send_via_resend(
                subject=final_subject,
                text_body=final_body,
                reply_to=email if email else None,
            )
            _safe_flash("Success! Your message has been sent.", "success")
            return redirect(url_for("index"))

        if use_formsubmit_only:
            _send_via_formsubmit(
                name=name,
                email=email,
                subject=final_subject,
                message_body=final_body,
            )
            _safe_flash("Success! Your message has been sent.", "success")
            return redirect(url_for("index"))

        required_config = {
            "MAIL_SERVER": app.config.get("MAIL_SERVER"),
            "MAIL_PORT": app.config.get("MAIL_PORT"),
            "MAIL_USERNAME": app.config.get("MAIL_USERNAME"),
            "MAIL_PASSWORD": app.config.get("MAIL_PASSWORD"),
            "CONTACT_RECIPIENT": CONTACT_RECIPIENT,
        }
        missing = [key for key, value in required_config.items() if not value]
        if missing:
            if provider == "auto" and formsubmit_enabled:
                _send_via_formsubmit(
                    name=name,
                    email=email,
                    subject=final_subject,
                    message_body=final_body,
                )
                _safe_flash("Success! Your message has been sent via backup service.", "success")
                return redirect(url_for("index"))
            _safe_flash(
                f"SMTP is not configured on server. Missing: {', '.join(missing)}.",
                "error",
            )
            return redirect(url_for("index"))

        preflight_enabled = _get_bool_env("SMTP_PREFLIGHT_CHECK", True)
        if preflight_enabled:
            preflight_timeout = float(os.environ.get("SMTP_PREFLIGHT_TIMEOUT", "3"))
            reachable, reason = _check_smtp_connectivity(
                app.config["MAIL_SERVER"],
                app.config["MAIL_PORT"],
                timeout_seconds=preflight_timeout,
            )
            if not reachable:
                if provider == "auto" and formsubmit_enabled:
                    _send_via_formsubmit(
                        name=name,
                        email=email,
                        subject=final_subject,
                        message_body=final_body,
                    )
                    _safe_flash("Success! Your message has been sent via backup service.", "success")
                    return redirect(url_for("index"))
                _safe_flash(
                    "SMTP server is unreachable from this host. "
                    "On Render free web services, outbound SMTP ports are blocked.",
                    "error",
                )
                app.logger.error(
                    "SMTP preflight failed for %s:%s (%s)",
                    app.config["MAIL_SERVER"],
                    app.config["MAIL_PORT"],
                    reason,
                )
                return redirect(url_for("index"))

        msg = Message(
            subject=final_subject,
            sender=app.config["MAIL_USERNAME"],
            recipients=[CONTACT_RECIPIENT],
            reply_to=email if email else None,
            body=final_body,
        )

        mail.send(msg)
        _safe_flash("Success! Your message has been sent.", "success")
    except (socket.timeout, TimeoutError):
        app.logger.exception("Contact form email timed out")
        if _get_bool_env("FORMSUBMIT_ENABLE", False):
            try:
                _send_via_formsubmit(
                    name=(request.form.get("name") or "").strip(),
                    email=(request.form.get("email") or "").strip(),
                    subject=f"Portfolio Contact: {(request.form.get('subject') or '').strip() or 'No Subject'}",
                    message_body=(
                        "Owner, you have a new message!\n\n"
                        f"Name: {(request.form.get('name') or '').strip() or 'Not provided'}\n"
                        f"Email: {(request.form.get('email') or '').strip() or 'Not provided'}\n\n"
                        f"Message:\n{(request.form.get('message') or '').strip() or 'No message body'}"
                    ),
                )
                _safe_flash("Success! Your message has been sent via backup service.", "success")
                return redirect(url_for("index"))
            except Exception:
                app.logger.exception("FormSubmit fallback failed after timeout")
        _safe_flash(
            "Email service timed out. Configure Resend on Render: MAIL_PROVIDER=resend, RESEND_API_KEY, RESEND_FROM, CONTACT_RECIPIENT.",
            "error",
        )
    except smtplib.SMTPException as e:
        app.logger.exception("Contact form SMTP error")
        if _get_bool_env("FORMSUBMIT_ENABLE", False):
            try:
                _send_via_formsubmit(
                    name=(request.form.get("name") or "").strip(),
                    email=(request.form.get("email") or "").strip(),
                    subject=f"Portfolio Contact: {(request.form.get('subject') or '').strip() or 'No Subject'}",
                    message_body=(
                        "Owner, you have a new message!\n\n"
                        f"Name: {(request.form.get('name') or '').strip() or 'Not provided'}\n"
                        f"Email: {(request.form.get('email') or '').strip() or 'Not provided'}\n\n"
                        f"Message:\n{(request.form.get('message') or '').strip() or 'No message body'}"
                    ),
                )
                _safe_flash("Success! Your message has been sent via backup service.", "success")
                return redirect(url_for("index"))
            except Exception:
                app.logger.exception("FormSubmit fallback failed after SMTP error")
        _safe_flash(
            "SMTP is unavailable on this host. Configure Resend API for delivery.",
            "error",
        )
    except Exception as e:
        app.logger.exception("Contact form email failed")
        _safe_flash(
            "Unable to send message right now. Configure Resend API and try again.",

            "error",
        )
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
