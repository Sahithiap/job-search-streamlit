import streamlit as st
import requests
from bs4 import BeautifulSoup
import yagmail
import datetime

st.set_page_config(page_title="Daily Job Notifier", layout="centered")
st.title("🔍 Daily Job Finder for CSE Students")
st.markdown("Finds AI/ML and Software Engineering jobs with ₹12+ LPA package.")

def search_jobs():
    urls = [
        "https://www.linkedin.com/jobs/search/?keywords=Machine%20Learning%20Engineer%20Fresher",
        "https://www.naukri.com/machine-learning-jobs?k=machine+learning&fresher=true&ctcFilter=12to99",
        "https://www.instahyre.com/search/?q=software%20engineer%20freshers"
    ]

    jobs = []
    for url in urls:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        if "linkedin" in url:
            listings = soup.find_all("a", class_="base-card__full-link")
            for job in listings[:5]:
                jobs.append(job['href'])

        elif "naukri" in url:
            listings = soup.find_all("a", class_="title ellipsis")
            for job in listings[:5]:
                jobs.append(job['href'])

        elif "instahyre" in url:
            listings = soup.find_all("a", class_="job-title")
            for job in listings[:5]:
                jobs.append("https://www.instahyre.com" + job['href'])

    return jobs

def send_email(jobs, email, password):
    yag = yagmail.SMTP(email, password)
    subject = f"🧠 AI/ML/Software Jobs - {datetime.date.today()}"
    content = "\n\n".join(jobs)
    yag.send(to="sahithibhisetti4@gmail.com", subject=subject, contents=content)

st.subheader("🔍 Click to Search Jobs")
if st.button("Find Latest Jobs"):
    job_links = search_jobs()
    if job_links:
        st.success("Found jobs:")
        for link in job_links:
            st.markdown(f"[View Job Posting]({link})", unsafe_allow_html=True)
    else:
        st.warning("No jobs found right now.")

st.subheader("📬 Email Results")
sender_email = st.text_input("Your Gmail Address")
app_password = st.text_input("App Password", type="password")

if st.button("Send Email"):
    if sender_email and app_password:
        jobs = search_jobs()
        if jobs:
            send_email(jobs, sender_email, app_password)
            st.success("Email sent to sahithibhisetti4@gmail.com!")
        else:
            st.warning("No jobs found to send.")
    else:
        st.error("Please enter your email and app password.")
