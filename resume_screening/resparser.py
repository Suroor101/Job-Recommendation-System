from resume_parser import resumeparse
from pyresparser import ResumeParser

def reparse(resume_file):
    data = resumeparse.read_file(resume_file)
    resume = data['skills']
    return resume

def extract_skills_from_resume(resume_path):
    data = ResumeParser(resume_path).get_extracted_data()
    return data["skills"]

def skill(resume_file):
    user_skills1 = reparse(resume_file)
    user_skills2 = extract_skills_from_resume(resume_file)
    user_skills = user_skills1 + user_skills2
    user_skills = [skill.lower() for skill in user_skills]
    user_skills = list(set(user_skills))
    return user_skills
