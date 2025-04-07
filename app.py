from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")

FILTERED_CSV = "/tmp/messages_filtered.csv"
KEYWORDS_ANALYSIS_CSV = "/tmp/keyword_analysis.csv"

@app.route('/', methods=['GET', 'POST'])
def index():
    table_html = None
    download_link_filtered = None
    download_link_keywords = None

    if request.method == 'POST':
        if 'messages_file' not in request.files or 'keywords_file' not in request.files:
            flash("Both files are required.")
            return render_template('index.html')

        messages_file = request.files['messages_file']
        keywords_file = request.files['keywords_file']

        if messages_file.filename == '' or keywords_file.filename == '':
            flash("No file selected.")
            return render_template('index.html')

        try:
            # Read CSV file
            df = pd.read_csv(messages_file)

            # Read keywords file and strip newlines
            keywords = [line.decode('utf-8').strip() for line in keywords_file.readlines() if line.strip()]

            # Filter DataFrame where 'message' column contains any keyword (case-insensitive)
            pattern = '|'.join(keywords)
            filtered_df = df[df['message'].str.contains(pattern, case=False, na=False)]

            # Analyze Keyword Frequency
            keyword_counts = {keyword: df['message'].str.contains(keyword, case=False, na=False).sum() for keyword in keywords}
            keyword_counts_df = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Occurrences'])
            keyword_counts_df.to_csv(KEYWORDS_ANALYSIS_CSV, index=False)
            download_link_keywords = url_for('download_keywords')

            # Save the filtered DataFrame to a CSV file on disk
            filtered_df.to_csv(FILTERED_CSV, index=False)

            # Convert DataFrame to HTML table with Bootstrap styling
            table_html = filtered_df.to_html(classes='table table-striped', index=False, border=0)
            download_link_filtered = url_for('download_filtered')
        except Exception as e:
            flash("Error processing files: " + str(e))
    
    return render_template('index.html', table_html=table_html, download_link_filtered=download_link_filtered, download_link_keywords=download_link_keywords)

@app.route('/download_filtered')
def download_filtered():
    if os.path.exists(FILTERED_CSV):
        return send_file(FILTERED_CSV, as_attachment=True)
    else:
        flash("Filtered file not found.")
        return redirect(url_for('index'))
    
@app.route('/download_keywords')
def download_keywords():
    if os.path.exists(KEYWORDS_ANALYSIS_CSV):
        return send_file(KEYWORDS_ANALYSIS_CSV, as_attachment=True)
    else:
        flash("Keywords file not found.")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
