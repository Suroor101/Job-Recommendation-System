JOB RECOMMENDATION SYSTEM

Our project aims to streamline the resume screening process by leveraging natural language processing and machine learning techniques. With the increasing volume of job applications received by companies, it becomes challenging for recruiters to manually review each resume. Our solution automates this process by analyzing resumes and comparing them with job descriptions to identify the most qualified candidates.

Using advanced text processing algorithms, we extract key skills and qualifications from resumes and job descriptions. We then apply cosine similarity to calculate the match percentage between the skills mentioned in the resume and the required skills for a specific job. This helps recruiters quickly identify candidates who possess the necessary skills and qualifications for a particular role.

The system also provides a user-friendly web interface where job seekers can upload their resumes and specify the job they are applying for. The system analyzes the resume, generates a skills match report, and provides a list of job vacancies that best match the candidate's skills and qualifications.

Additionally, our project offers the feature of highlighting missing skills. If a candidate's resume lacks certain key skills required for a job, the system identifies those missing skills and alerts the candidate, enabling them to update their resume accordingly.

By automating the resume screening process and providing targeted job recommendations, our project saves time and effort for both recruiters and job seekers. It enhances the efficiency of the hiring process, improves the chances of finding the right candidates, and increases the overall effectiveness of talent acquisition for organizations.

Requirements:
- [Resume-Parser](https://pypi.org/project/resume-parser/)
- [en_core_web_sm==2.3.1](https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz)
