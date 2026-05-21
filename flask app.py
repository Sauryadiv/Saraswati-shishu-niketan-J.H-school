
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "ssn_secret_cloud_key_2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
master_file = os.path.join(BASE_DIR, "students_master.csv")

def read_students():
    if not os.path.exists(master_file) or os.path.getsize(master_file) == 0:
        with open(master_file, "w") as f:
            f.write("Name,Father,Mother,DOB,Total,Paid,Balance\n")
        return []
    try:
        with open(master_file, "r") as f:
            lines = f.readlines()
            return [line.strip().split(",") for line in lines if line.strip() and not line.startswith("Name")]
    except Exception:
        return []

# COMMON BASE LAYOUT
BASE_CSS = """
:root {
    --primary: #ff9933;
    --secondary: #138808;
    --dark: #0f2347;
    --bg: #f4f7f6;
    --accent: #e11d48;
    --link-bg: #fff1f2;
    --link-border: #ffe4e6;
    --link-text: #9f1239;
}
body { font-family: 'Segoe UI', Arial, sans-serif; background: var(--bg); margin: 0; padding: 0; color: #333; display: flex; flex-direction: column; min-height: 100vh; }
.school-header {
    background: linear-gradient(135deg, #0f2347 0%, #1e3a8a 100%);
    color: white; padding: 30px 25px; border-bottom: 6px solid var(--primary);
    display: flex; flex-direction: row; align-items: center; position: relative;
}
.logo-box { flex-shrink: 0; }
.logo-box img {
    width: 100px; height: 100px; border-radius: 50%;
    border: 4px solid #ff9933; box-shadow: 0 4px 15px rgba(0,0,0,0.5); object-fit: cover;
}
.title-box { display: flex; flex-direction: column; align-items: center; text-align: center; flex-grow: 1; margin-right: 100px; }
.school-header h1 { margin: 0; font-size: clamp(20px, 2.8vw, 36px); font-weight: 800; color: #ffffff; text-shadow: 2px 2px 5px rgba(0,0,0,0.8); }
.school-header p { margin: 8px 0 0 0; font-size: clamp(13px, 1.6vw, 18px); color: #ffffff; font-weight: 700; background: rgba(255, 153, 51, 0.25); padding: 4px 18px; border-radius: 6px; display: inline-block; }
@media (max-width: 768px) {
    .title-box { margin-right: 0; }
    .logo-box img { width: 70px; height: 70px; }
    .school-header { padding: 15px 10px; }
}
.marquee-ticker {
    background: #cbd5e1; color: #0f2347; font-weight: bold; font-size: 13px;
    padding: 6px 0; border-bottom: 2px solid #cbd5e1; display: flex; align-items: center;
}
.marquee-tag { background: var(--accent); color: white; padding: 2px 10px; font-size: 11px; font-weight: 800; border-radius: 3px; margin-left: 10px; z-index: 10; text-transform: uppercase; }
.custom-navbar {
    background: #ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    display: flex; overflow-x: auto; white-space: nowrap; position: sticky; top: 0; z-index: 1000; border-bottom: 2px solid #e5e7eb;
}
.custom-navbar::-webkit-scrollbar { display: none; }
.nav-link { display: inline-block; padding: 16px 22px; color: #374151; text-decoration: none; font-size: 15px; font-weight: 600; border-bottom: 4px solid transparent; }
.nav-link i { margin-right: 8px; color: #4b5563; }
.container { padding: 20px; max-width: 1200px; margin: 0 auto; flex: 1; }
.hero-section-wrapper { display: flex; gap: 20px; margin-bottom: 25px; }
.hero-banner { flex: 1; background: linear-gradient(135deg, #1e3a8a 0%, #0f2347 100%); color: white; padding: 25px 20px; border-radius: 12px; display: flex; flex-direction: column; justify-content: center; }
.hero-banner h2 { margin: 0; font-size: 24px; color: var(--primary); }
.hero-banner p { margin: 8px 0 0 0; font-size: 14px; color: #cbd5e1; line-height: 1.5; }
.right-video-box {
    width: 380px; max-width: 100%; height: auto;
    aspect-ratio: 16 / 9; overflow: hidden; border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 3px solid white; flex-shrink: 0; position: relative;
}
.right-video-box video { width: 100%; height: 100%; object-fit: cover; display: block; transform: scale(1.35); }
.notice-board-card {
    background: #ffffff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 6px solid var(--accent); margin-bottom: 25px; padding: 20px;
}
.notice-board-header { display: flex; align-items: center; gap: 10px; margin-bottom: 15px; border-bottom: 2px solid #f3f4f6; padding-bottom: 10px; }
.notice-board-header h3 { margin: 0; color: var(--dark); font-size: 18px; font-weight: 700; }
.notice-board-header i { color: var(--accent); font-size: 20px; }
.notice-links-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }
.notice-item {
    display: flex; align-items: center; gap: 12px; background: var(--link-bg); padding: 12px 15px; border-radius: 8px; text-decoration: none; color: var(--link-text); font-weight: 600; font-size: 14px; border: 1px solid var(--link-border); transition: all 0.2s ease;
}
.notice-item:hover { background: #ffe4e6; transform: translateX(3px); }
.notice-item i { font-size: 16px; color: var(--accent); width: 20px; text-align: center; }
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }
.stat-card { background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.04); border-bottom: 4px solid var(--secondary); }
.stat-card h4 { margin: 0; font-size: 24px; color: var(--dark); }
.stat-card p { margin: 4px 0 0 0; font-size: 12px; color: #6b7280; font-weight: bold; }
.action-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
.action-tile { background: #ffffff; padding: 18px 5px; border-radius: 10px; text-align: center; text-decoration: none; color: var(--dark); font-weight: 700; font-size: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.04); border-top: 4px solid var(--primary); transition: transform 0.2s; }
.action-tile i { font-size: 26px; color: var(--primary); margin-bottom: 8px; display: block; }
.card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-top: 4px solid var(--dark); margin-bottom: 20px; }
.placeholder-box { text-align: center; padding: 40px 10px; color: #6b7280; }
.school-footer { background: #0f2347; color: #cbd5e1; padding: 30px 20px; border-top: 5px solid var(--primary); font-size: 14px; text-align: center; margin-top: auto; }
.footer-bottom p { margin: 5px 0; }
@media (max-width: 768px) {
    .hero-section-wrapper { flex-direction: column; }
    .right-video-box { width: 100%; }
    .action-grid { grid-template-columns: repeat(2, 1fr); }
    .stats-grid { grid-template-columns: 1fr; gap: 10px; }
}
"""

HEADER_NAV_HTML = """
<div class="school-header">
    <div class="logo-box"><img src="/logo_image" alt="SSN Logo"></div>
    <div class="title-box">
        <h1>SARASWATI SHISHU NIKETAN J.H. SCHOOL</h1>
        <p>Suhag Nagar, Firozabad</p>
    </div>
</div>
<div class="marquee-ticker">
    <span class="marquee-tag">Updates</span>
    <marquee behavior="scroll" direction="left" scrollamount="5">
        ✨ New Session Admissions Open 2026-27 !! &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; 📝 Class 6 to 8 Scholarship Registrations started !! &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; 💼 New Teacher Vacancies released, Apply inside !! &nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp; ⏰ Summer School Timings updated !!
    </marquee>
</div>
<div class="custom-navbar">
    <a class="nav-link" href="/"><i class="fa-solid fa-house"></i>Home</a>
    <a class="nav-link" href="/admission"><i class="fa-solid fa-file-signature"></i>Admission</a>
    <a class="nav-link" href="/gallery"><i class="fa-solid fa-images"></i>Gallery</a>
    <a class="nav-link" href="/notes"><i class="fa-solid fa-book-open"></i>Notes</a>
    <a class="nav-link" href="/tc"><i class="fa-solid fa-id-card-clip"></i>TC</a>
    <a class="nav-link" href="/about"><i class="fa-solid fa-circle-info"></i>About</a>
</div>
"""

FOOTER_HTML = """
<footer class="school-footer">
    <div class="footer-bottom">
        <p>© 2026 Saraswati Shishu Niketan J.H. School. All Rights Reserved.</p>
        <p style="font-size: 12px; color: #9ca3af;">Designed with ❤️ by Anoop</p>
    </div>
</footer>
"""

# ---- 1. HOME TEMPLATE (CLEANED - REGISTER REMOVED) ----
HOME_HTML = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Saraswati Shishu Niketan</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>{BASE_CSS}</style>
</head>
<body>
    {HEADER_NAV_HTML}
    <div class="container">
        <div class="hero-section-wrapper">
            <div class="hero-banner">
                <h2>Welcome to Portal Dashboard</h2>
                <p>Saraswati Shishu Niketan, Firozabad ka digital portal bacchon ki shiksha, records, aur school activities ko up-to-date rakhne ke liye taiyar hai.</p>
            </div>
            <div class="right-video-box">
                <video autoplay loop muted playsinline><source src="/get_school_video" type="video/mp4"></video>
            </div>
        </div>

        <div class="notice-board-card">
            <div class="notice-board-header">
                <i class="fa-solid fa-bullhorn"></i><h3>School Notice Board & Important Links</h3>
            </div>
            <div class="notice-links-grid">
                <a href="/vacancy" class="notice-item"><i class="fa-solid fa-user-tie"></i> Teacher Vacancy Form 2026</a>
                <a href="/scholarship" class="notice-item"><i class="fa-solid fa-graduation-cap"></i> Scholarship Form (Class 6 to 8)</a>
                <a href="/exams" class="notice-item"><i class="fa-solid fa-file-pen"></i> Exam Date Sheet & Updates</a>
                <a href="/timings" class="notice-item"><i class="fa-solid fa-clock"></i> School New Timings Notice</a>
                <a href="/books_uniform" class="notice-item"><i class="fa-solid fa-shirt"></i> Books & Uniform Pattern List</a>
                <a href="/academic_calendar" class="notice-item"><i class="fa-solid fa-calendar-days"></i> Holiday Calendar 2026-27</a>
                <a href="/toppers" class="notice-item"><i class="fa-solid fa-trophy"></i> Toppers & Achievements Gallery</a>
                <a href="/syllabus" class="notice-item"><i class="fa-solid fa-book"></i> Class-wise Syllabus Details</a>
                <a href="/homework" class="notice-item"><i class="fa-solid fa-pencil"></i> Daily Homework Updates</a>
                <a href="/staff_directory" class="notice-item"><i class="fa-solid fa-users"></i> Our School Staff Directory</a>
                <a href="/staff_leave" class="notice-item"><i class="fa-solid fa-file-signature"></i> Staff Leave Application Form</a>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card"><h4>{{{{ total_students }}}}</h4><p>REGISTERED STUDENTS</p></div>
            <div class="stat-card" style="border-bottom-color: var(--primary);"><h4>12+</h4><p>ACTIVE TEACHERS</p></div>
            <div class="stat-card" style="border-bottom-color: #3b82f6;"><h4>100%</h4><p>SECURE DIGITAL PORTAL</p></div>
        </div>

        <div class="action-grid">
            <a href="/admission" class="action-tile"><i class="fa-solid fa-user-plus"></i>Admission</a>
            <a href="/gallery" class="action-tile"><i class="fa-solid fa-camera-retro"></i>Gallery</a>
            <a href="/notes" class="action-tile"><i class="fa-solid fa-file-arrow-down"></i>Notes</a>
            <a href="/tc" class="action-tile"><i class="fa-solid fa-print"></i>Print TC</a>
        </div>
    </div>
    {FOOTER_HTML}
</body>
</html>
"""

# ---- 2. GENERAL SUBPAGE BLANKET ----
def make_subpage(title, icon, text):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>{BASE_CSS}</style>
    </head>
    <body>
        {HEADER_NAV_HTML}
        <div class="container">
            <div class="card">
                <h3><i class="{icon}"></i> {title}</h3>
                <div class="placeholder-box"><p>{text}</p></div>
            </div>
        </div>
        {FOOTER_HTML}
    </body>
    </html>
    """

# ---- 3. ADMISSION FORM SPECIFIC TEMPLATE ----
ADMISSION_HTML = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admission Entry</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        {BASE_CSS}
        form label {{ display: block; font-weight: bold; margin-top: 12px; font-size: 14px; color: var(--dark); }}
        form input {{ width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }}
        form button {{ background: var(--secondary); color: white; border: none; padding: 12px 20px; font-weight: bold; border-radius: 6px; cursor: pointer; margin-top: 18px; width: 100%; font-size: 15px; }}
    </style>
</head>
<body>
    {HEADER_NAV_HTML}
    <div class="container">
        <div class="card">
            <h3><i class="fa-solid fa-feather"></i> Student Admission Entry</h3>
            <form action="/save_admission" method="POST">
                <label>Student Name</label><input type="text" name="name" required>
                <label>Father Name</label><input type="text" name="father">
                <label>Mother Name</label><input type="text" name="mother">
                <label>DOB (DD-MM-YYYY)</label><input type="text" name="dob" placeholder="Eg: 15-08-2016">
                <label>Total Course Fees (₹)</label><input type="number" name="total" value="0">
                <label>Initial Paid Fees (₹)</label><input type="number" name="paid" value="0">
                <button type="submit">💾 Save Student Record</button>
            </form>
        </div>
    </div>
    {FOOTER_HTML}
</body>
</html>
"""


@app.route("/")
def index():
    st_list = read_students()
    return render_template_string(HOME_HTML, total_students=len(st_list))

@app.route("/admission")
def admission(): return render_template_string(ADMISSION_HTML)

# ALL 11 ROUTINGS LINKED WITH NOTICE BOARD PERFECTLY
@app.route("/vacancy")
def vacancy(): return make_subpage("Teacher Vacancy Recruitment Form", "fa-solid fa-user-tie", "Teacher job application form content will go here.")

@app.route("/scholarship")
def scholarship(): return make_subpage("Class 6 to 8 Scholarship Portal", "fa-solid fa-graduation-cap", "Scholarship registration and verification panel.")

@app.route("/exams")
def exams(): return make_subpage("Examination Notice & Time Table", "fa-solid fa-file-pen", "Date sheet PDFs and exam alerts.")

@app.route("/timings")
def timings(): return make_subpage("Official School Timings", "fa-solid fa-clock", "Summer/Winter official school hours details.")

@app.route("/books_uniform")
def books_uniform(): return make_subpage("Books & Uniform Pattern List", "fa-solid fa-shirt", "Class-wise books distributor list and uniform dress codes.")

@app.route("/academic_calendar")
def academic_calendar(): return make_subpage("Holiday Calendar 2026-27", "fa-solid fa-calendar-days", "List of official holidays, festival breaks and PTM updates.")

@app.route("/toppers")
def toppers(): return make_subpage("Toppers & Achievements Gallery", "fa-solid fa-trophy", "Photos and scores of outstanding student performances.")

@app.route("/syllabus")
def syllabus(): return make_subpage("Class-wise Syllabus Details", "fa-solid fa-book", "Detailed syllabus download links for session 2026-27.")

@app.route("/homework")
def homework(): return make_subpage("Daily Homework Updates", "fa-solid fa-pencil", "Class-wise daily homework blackboard for student logging.")

@app.route("/staff_directory")
def staff_directory(): return make_subpage("Our School Staff Directory", "fa-solid fa-users", "List of esteemed faculties and administration workers.")

@app.route("/staff_leave")
def staff_leave(): return make_subpage("Staff Leave Application Form", "fa-solid fa-file-signature", "Teacher digital leave request processing panel.")

@app.route("/gallery")
def gallery(): return make_subpage("Photo Gallery", "fa-solid fa-images", "School event photos album dashboard.")

@app.route("/notes")
def notes(): return make_subpage("Digital Notes", "fa-solid fa-file-pdf", "Class-wise study materials and PDF files.")

@app.route("/tc")
def tc(): return make_subpage("TC Generator", "fa-solid fa-print", "Transfer Certificate dynamic entry and printing system.")

@app.route("/about")
def about(): return make_subpage("About School", "fa-solid fa-school", "Saraswati Shishu Niketan school history and foundation details.")


@app.route("/logo_image")
def logo_image():
    if os.path.exists(os.path.join(BASE_DIR, "1778386153583.png")):
        return send_from_directory(BASE_DIR, "1778386153583.png")
    else:
        return redirect("https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=150")

@app.route("/get_school_video")
def get_school_video():
    if os.path.exists(os.path.join(BASE_DIR, "school.mp4")):
        return send_from_directory(BASE_DIR, "school.mp4")
    else:
        return redirect("https://assets.mixkit.co/videos/preview/mixkit-children-in-a-school-setting-with-masks-34241-large.mp4")

@app.route("/save_admission", methods=["POST"])
def save_admission():
    name = request.form.get("name", "").strip()
    father = request.form.get("father", "").strip()
    mother = request.form.get("mother", "").strip()
    dob = request.form.get("dob", "").strip()
    total = request.form.get("total", "0").strip()
    paid = request.form.get("paid", "0").strip()

    tot_val = int(total) if total.isdigit() else 0
    pd_val = int(paid) if paid.isdigit() else 0
    bal_val = tot_val - pd_val

    with open(master_file, "a") as f:
        f.write(f"{name},{father},{mother},{dob},{tot_val},{pd_val},{bal_val}\n")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
