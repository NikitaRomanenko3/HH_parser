from flask import Flask, request, render_template, redirect, send_file
from hh_parser import hh_extract_jobs
from exporter import save_to_csv

app = Flask('hh_parser')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/report')
def report():
    keyword = request.args.get('keyword')
    if keyword is not None:
        keyword = keyword.lower()
        jobs = hh_extract_jobs(keyword)
    else:
        return redirect('/')
    return render_template('report.html', keyword=keyword, jobs=jobs, job_counter=len(jobs))


@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        if keyword is not None:
            keyword = keyword.lower()
            jobs = hh_extract_jobs(keyword)
            save_to_csv(jobs)
            return send_file('jobs.csv')
    except:
        return redirect('/')


app.run()
