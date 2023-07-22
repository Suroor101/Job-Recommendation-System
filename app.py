import os
from flask import Flask, render_template, request
from resume_screening.resparser import skill
from resume_screening.match import recommend_jobs, extract_skills_for_job

app = Flask(__name__)

os.makedirs(os.path.join(app.instance_path, 'resume_files'), exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    job_name = request.form["job_name"]

    # Save the uploaded file to a temporary location
    file = request.files['userfile']
    file_path = os.path.join(app.instance_path, 'resume_files', file.filename)
    file.save(file_path)

    #os.remove(file_path)

    # Step 1: Extract skills from the resume
    user_skills = skill(file_path)
    user_skills_str = ", ".join(user_skills)  # Convert user_skills to a string

    # Step 2: Get recommended jobs
    recommended_jobs = recommend_jobs(user_skills_str)

    # Step 3: Get missing skills for the specified job
    missing_skills = extract_skills_for_job(user_skills, job_name)

    # Prepare data for rendering in the template
    column_names = recommended_jobs.columns.values
    row_data = recommended_jobs.values.tolist()
    link_column = "link"

    

    return render_template(
        "index.html",
        column_names=column_names,
        row_data=row_data,
        link_column=link_column,
        show_missing_skills=bool(missing_skills),  # Pass the show_missing_skills variable to the template
        missing_skills=missing_skills,  # Pass the missing skills to the template
        zip=zip
    )


if __name__ == "__main__":
    app.run()
