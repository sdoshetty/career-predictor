# career-predictor

🌟 Resume-Based Career Recommendation System

Transform your resume into career insights! This tool analyzes your resume, identifies your skills, and recommends the best-fit career paths. It also highlights missing skills so you know what to learn next.

🎯 Features
✅ Upload resumes in PDF, DOCX, or TXT formats
✅ Detects Technical Skills & Soft Skills automatically
✅ Recommends Top 5 Career Options based on your profile
✅ Shows missing skills required for your top career choice
✅ Built using Python, TF-IDF, and Logistic Regression
🛠 Technologies Used
Technology	Purpose
Python 3	Core programming language
pandas	Data handling
PyPDF2	Extract text from PDF
python-docx	Extract text from DOCX
re	Text preprocessing & cleaning
scikit-learn	TF-IDF & Logistic Regression
Google Colab	Resume upload & interactive environment
🚀 How It Works
Upload Resume – Supports .pdf, .docx, .txt
Extract Text – Reads all content from your resume
Detect Skills – Matches your resume against technical and soft skills lists
Predict Careers – Uses machine learning to suggest the top 5 careers
Identify Missing Skills – Compares your skills with what’s required for your top career
🎓 Predefined Careers

Some of the careers included:

Data Scientist
Data Analyst
Frontend Developer
Backend Developer / Java Backend Developer
Machine Learning Engineer / NLP Engineer
Full Stack Developer
Software Engineer
DevOps Engineer
Cybersecurity Engineer
Mobile App Developer
Blockchain Developer
Game Developer
IoT Engineer

Each career comes with a required skill set for both technical and soft skills.

📈 Example Output
Name: John Doe

Technical Skills detected: ['python', 'machine learning', 'pandas']
Soft Skills detected: ['problem solving', 'analytical thinking']

Top 5 Career Recommendations:
- Data Scientist
- Machine Learning Engineer
- Data Analyst
- NLP Engineer
- Software Engineer

Missing Technical Skills: ['numpy']
Missing Soft Skills: ['critical thinking']
