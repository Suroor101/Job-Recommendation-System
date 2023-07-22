import re
import string
from ftfy import fix_text
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
from collections import Counter

def ngrams(string, n=3):
    string = fix_text(string) # fix text
    string = string.encode("ascii", errors="ignore").decode() # remove non ascii chars
    string = string.lower()
    chars_to_remove = [")","(",".","|","[","]","{","}","'"]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string)
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title() # normalize case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single
    string = ' '+ string +' ' # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]

def preprocess_text(text):
    text = re.sub(r'\.(?!\s)', ' ', text)  # remove dots
    text = re.sub(r',', ' ', text)  # remove commas
    text = re.sub(r'\d+', '', text)  # remove digits
    text = re.sub(r'#\w+', '', text)  # remove hashtags
    text = re.sub(r'\s+', ' ', text)  # remove extra white spaces
    text = text.replace('\n', ' ')  # replace new lines with spaces
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove all punctuations
    text = text.strip()  # remove leading/trailing spaces
    return text

def casefoldingText(text):
    text = text.lower() # Converting all the characters in a text into lower case
    return text

def recommend_jobs(user_skills):
    # Step 1: Load the dataset

    directory = 'C:/Users/LENOVO/Desktop/Job Recommendation System/resume_screening'
    file_path = os.path.join(directory, 'combined.csv')
    df = pd.read_csv(file_path)

    # Step 2: Preprocess the job descriptions
    df["processed_skills"] = df["skills"].apply(lambda x: preprocess_text(str(x)) if pd.notnull(x) else "")

    # Step 3: TF-IDF Vectorization
    vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams, lowercase=False)
    job_skills_matrix = vectorizer.fit_transform(df["processed_skills"])

    # Step 4: kNN for Job Recommendations
    k = 15  # Number of nearest neighbors
    nn_model = NearestNeighbors(n_neighbors=k, metric="cosine")
    nn_model.fit(job_skills_matrix)
    distances, indices = nn_model.kneighbors(vectorizer.transform([user_skills]))

    # Step 5: Generate Recommendations
    recommended_jobs = df.iloc[indices.flatten()][:15]

    # Step 6: Calculate Similarity Scores
    similarity_scores = (1 - distances.flatten()) * 100
    similarity_scores = [str(x)[:5] for x in similarity_scores] # converting each score to string to slice at 56.32
    recommended_jobs["skill_match"] = similarity_scores

    return recommended_jobs[["title", "company", "skill_match", "link"]]


def extract_skills_for_job(user_skills, job_name):
    # Step 1: Load the dataset
    directory = 'C:/Users/LENOVO/Desktop/Job Recommendation System/resume_screening'
    file_path = os.path.join(directory, 'combined.csv')
    df = pd.read_csv(file_path)

    # Step 2: Extract skills for job titles containing the keyword
    matching_jobs = df[df["title"].str.contains(job_name, case=False)]
    required_skills = []
    for skills in matching_jobs["skills"]:
        required_skills.extend(skills.lower().split(","))

    # Step 3: Count the frequency of each skill
    skill_frequency = Counter(required_skills)

    # Step 4: Handle similar skills and select the one with the highest frequency
    similar_skills = {}
    for skill in skill_frequency:
        similar_skill = None
        for existing_skill in similar_skills:
            if skill.lower() in existing_skill.lower() or existing_skill.lower() in skill.lower():
                if skill_frequency[skill] > skill_frequency[existing_skill]:
                    similar_skill = skill
                else:
                    similar_skill = existing_skill
                break
        if similar_skill:
            similar_skills[similar_skill] = skill
        else:
            similar_skills[skill] = skill

    # Step 5: Get the top 10 most frequent skills with similar skills handled
    top_skills = skill_frequency.most_common(10)
    top_skills_with_similar = []
    for skill, frequency in top_skills:
        if skill in similar_skills:
            similar_skill = similar_skills[skill]
            if similar_skill != skill:
                skill = f"{skill} ({similar_skill})"
        top_skills_with_similar.append(skill)

    # Step 6: Find the missing skills
    user_skills_lower = set([skill.lower() for skill in user_skills])
    missing_skills = [skill for skill in top_skills_with_similar if skill.lower() not in user_skills_lower]

    if len(missing_skills) == 0:
        return [f"You are qualified for the job '{job_name}'."]
    else:
        return missing_skills[:10]
