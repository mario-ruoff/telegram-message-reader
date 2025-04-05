import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = 'messages_full.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(file_path)

# Display the full DataFrame
print(df)

# Load keywords from the text file
keywords_file = 'keywords.txt'  # Replace with the actual path to your keywords file
with open(keywords_file, 'r') as f:
    keywords = [line.strip() for line in f]
print(keywords)

# Filter the DataFrame based on the 'message' column containing any of the keywords
filtered_df = df[df['message'].str.contains('|'.join(keywords), case=False, na=False)]

# Count the occurrences of each keyword in the 'message' column
keyword_counts = {keyword: df['message'].str.contains(keyword, case=False, na=False).sum() for keyword in keywords}
keyword_counts_df = pd.DataFrame(list(keyword_counts.items()), columns=['Keyword', 'Occurrences'])
keyword_counts_df.to_csv('keyword_analysis.csv', index=False)

# Display the keyword counts
print("Keyword occurrences:")
for keyword, count in keyword_counts.items():
    print(f"{keyword}: {count}")

# Display the filtered DataFrame
print(filtered_df)

# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('messages_filtered.csv', index=False)
