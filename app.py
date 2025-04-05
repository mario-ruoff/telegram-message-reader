from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import pandas as pd
import io
import os

app = Flask(__name__)
app.secret_key = "secret-key"  # Replace with a secure key in production

FILTERED_CSV = "messages_filtered.csv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'messages_file' not in request.files or 'keywords_file' not in request.files:
        flash("Both files are required.")
        return redirect(url_for('index'))

    messages_file = request.files['messages_file']
    keywords_file = request.files['keywords_file']

    if messages_file.filename == '' or keywords_file.filename == '':
        flash("No file selected.")
        return redirect(url_for('index'))

    try:
        # Read CSV file
        df = pd.read_csv(messages_file)

        # Read keywords file and strip newlines
        keywords = [line.decode('utf-8').strip() for line in keywords_file.readlines() if line.strip()]

        # Filter DataFrame where 'message' column contains any keyword (case-insensitive)
        pattern = '|'.join(keywords)
        filtered_df = df[df['message'].str.contains(pattern, case=False, na=False)]

        # Save the filtered DataFrame to a CSV file on disk
        filtered_df.to_csv(FILTERED_CSV, index=False)

        # Convert DataFrame to HTML table with Bootstrap styling
        table_html = filtered_df.to_html(classes='table table-striped', index=False, border=0)

        return render_template('results.html', table_html=table_html, download_link=url_for('download'))
    except Exception as e:
        flash("Error processing files: " + str(e))
        return redirect(url_for('index'))

@app.route('/download')
def download():
    if os.path.exists(FILTERED_CSV):
        return send_file(FILTERED_CSV, as_attachment=True)
    else:
        flash("Filtered file not found.")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
