import streamlit as st
import pandas as pd
import PyPDF2
import docx
import re
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ===================== PAGE CONFIG =====================
st.set_page_config(page_title="Career Predictor", layout="centered")

# ===================== CLEAN DARK UI =====================
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}
.card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 15px;
}
.title {
    font-size: 20px;
    font-weight: bold;
    color: #4CAF50;
}
.text {
    font-size: 17px;
    color: #E0E0E0;
}
.chip {
    display: inline-block;
    margin: 6px 6px 6px 0;
    padding: 4px 10px;
    border: 1px solid #888;
    border-radius: 6px;
    font-size: 15px;
    color: #E0E0E0;
}
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.title("Career Prediction & Skill Gap Analysis")
st.write("Upload your resume to get career recommendations")

# ===================== TAG FUNCTION =====================
def create_tags(skills):
    if skills == ["None"] or skills == "None":
        return "<span class='text'>None</span>"
    return " ".join([f"<span class='chip'>{skill}</span>" for skill in skills])

# ===================== SKILLS =====================
technical_skills = list(set([
"python","java","c","c++","c#","javascript","typescript","go","rust","kotlin","swift","r","matlab","scala","dart",
"html","css","react","angular","vue","nodejs","express","django","flask","spring boot","rest api","graphql",
"machine learning","deep learning","nlp","computer vision","data analysis","pandas","numpy","scikit-learn",
"tensorflow","pytorch",
"sql","mysql","postgresql","mongodb","cassandra","firebase","redis",
"aws","azure","gcp","docker","kubernetes","jenkins","terraform","linux","shell scripting",
"network security","ethical hacking","cryptography","penetration testing",
"android","ios","flutter","react native",
"data structures","algorithms","oops","system design","operating systems","computer networks",
"testing","selenium","junit","automation testing",
"blockchain","solidity","web3","unity","unreal engine","iot","robotics","embedded systems"
]))

soft_skills = list(set([
"communication","teamwork","leadership","problem solving","critical thinking",
"creativity","adaptability","decision making","time management","analytical thinking",
"attention to detail","multitasking","work ethic","accountability",
"debugging","research","collaboration","agile","scrum"
]))

# ===================== TRAIN DATA =====================
data = {
"skills":[
"python machine learning data analysis pandas numpy",
"python sql excel tableau power bi",
"html css javascript react angular",
"python flask django api database",
"java spring boot backend microservices",
"python tensorflow pytorch deep learning",
"aws docker kubernetes terraform linux",
"python nlp machine learning transformers",
"javascript nodejs react mongodb express",
"java c++ data structures algorithms",
"cybersecurity ethical hacking network security",
"android kotlin ios swift mobile development",
"blockchain solidity web3 ethereum",
"unity unreal engine game development",
"iot embedded systems robotics"
],
"career":[
"Data Scientist","Data Analyst","Frontend Developer","Backend Developer",
"Java Backend Developer","Machine Learning Engineer","DevOps Engineer",
"NLP Engineer","Full Stack Developer","Software Engineer",
"Cybersecurity Engineer","Mobile App Developer","Blockchain Developer",
"Game Developer","IoT Engineer"
]
}

df = pd.DataFrame(data)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["skills"])

model = LogisticRegression(max_iter=1000)
model.fit(X, df["career"])

# ===================== MAP =====================
career_required_skills = {
"Data Scientist":["python","machine learning","data analysis","pandas","numpy"],
"Data Analyst":["python","sql","excel","tableau"],
"Frontend Developer":["html","css","javascript","react"],
"Backend Developer":["python","api","database","django","flask"],
"Java Backend Developer":["java","spring boot","microservices"],
"Machine Learning Engineer":["python","machine learning","tensorflow","pytorch"],
"DevOps Engineer":["aws","docker","kubernetes","terraform"],
"NLP Engineer":["python","nlp","machine learning"],
"Full Stack Developer":["javascript","react","nodejs","html","css"],
"Software Engineer":["java","c++","data structures","algorithms"],
"Cybersecurity Engineer":["network security","ethical hacking","cryptography"],
"Mobile App Developer":["android","kotlin","ios","swift"],
"Blockchain Developer":["blockchain","solidity","web3"],
"Game Developer":["unity","unreal engine"],
"IoT Engineer":["iot","embedded systems","robotics"]
}

career_soft_skills = {
"Data Scientist":["problem solving","critical thinking","analytical thinking"],
"Data Analyst":["communication","analytical thinking"],
"Frontend Developer":["creativity","teamwork"],
"Backend Developer":["problem solving","adaptability"],
"Java Backend Developer":["problem solving","teamwork"],
"Machine Learning Engineer":["critical thinking","problem solving"],
"NLP Engineer":["research","critical thinking"],
"DevOps Engineer":["teamwork","decision making"],
"Full Stack Developer":["teamwork","communication"],
"Software Engineer":["analytical thinking","problem solving"],
"Cybersecurity Engineer":["attention to detail","critical thinking"],
"Mobile App Developer":["creativity","problem solving"],
"Blockchain Developer":["analytical thinking","problem solving"],
"Game Developer":["creativity","teamwork"],
"IoT Engineer":["problem solving","research"]
}

# ===================== SKILL EXTRACTION =====================
def extract_skills(text, skill_list):
    text = text.lower()
    found = []
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            found.append(skill)
    return found or ["None"]

def get_missing_skills(required_skills, found_skills):
    missing = [s for s in required_skills if s not in found_skills]
    return missing or ["None"]

# ===================== FILE UPLOAD =====================
uploaded_file = st.file_uploader("Upload Resume", type=["pdf","docx","txt"])

if uploaded_file:
    with st.spinner("Analyzing Resume..."):
        time.sleep(1)

    resume_text = ""
    if uploaded_file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text + " "
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            resume_text += para.text + " "
    else:
        resume_text = uploaded_file.read().decode("utf-8")

    words = resume_text.split()
    name = (words[0] + " " + words[1]).title() if len(words) >= 2 else "Not Found"

    found_technical = extract_skills(resume_text, technical_skills)
    found_soft = extract_skills(resume_text, soft_skills)

    # ===================== PREDICT =====================
    user_skills_text = " ".join(found_technical)
    vector = vectorizer.transform([user_skills_text])
    probs = model.predict_proba(vector)[0]
    careers = model.classes_
    career_scores = sorted(zip(careers, probs), key=lambda x: x[1], reverse=True)
    top_5_careers = career_scores[:5]
    top_career = top_5_careers[0][0]

    # ===================== MISSING SKILLS =====================
    req_tech = career_required_skills.get(top_career, [])
    missing_technical = get_missing_skills(req_tech, found_technical)

    req_soft = career_soft_skills.get(top_career, [])
    missing_soft = get_missing_skills(req_soft, found_soft)

    # ===================== OUTPUT =====================
    st.markdown("## Analysis Report")

    st.markdown(f"""
    <div class="card">
    <span class="title">Name:</span><br>
    <span class="text">{name}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
    <span class="title">Technical Skills detected:</span><br>
    {create_tags(found_technical)}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
    <span class="title">Soft Skills detected:</span><br>
    {create_tags(found_soft)}
    </div>
    """, unsafe_allow_html=True)

    career_list = "<br>".join([f"- {c}" for c, _ in top_5_careers])
    st.markdown(f"""
    <div class="card">
    <span class="title">Top Career Recommendations:</span><br>
    <span class="text">{career_list}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
    <span class="title">Missing Technical Skills:</span><br>
    {create_tags(missing_technical)}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
    <span class="title">Missing Soft Skills:</span><br>
    {create_tags(missing_soft)}
    </div>
    """, unsafe_allow_html=True)