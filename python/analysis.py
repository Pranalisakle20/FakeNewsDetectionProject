import pandas as pd
import matplotlib.pyplot as plt

fake = pd.read_csv("../data/Fake.csv")
real = pd.read_csv("../data/True.csv")

print(fake.head())
print(real.head())

fake['news_type'] = 'Fake'
real['news_type'] = 'Real'

df = pd.concat([fake, real])

print(df.head())

print(df['news_type'].value_counts())

df['news_type'].value_counts().plot(kind='bar')

plt.title("Fake vs Real News Count")
plt.xlabel("News Type")
plt.ylabel("Count")

plt.show()

fake_news = df[df['news_type'] == 'Fake']

print(fake_news['subject'].value_counts())

#categary or subject wise graph
fake_news['subject'].value_counts().plot(kind='bar')

plt.title("Fake News by Subject")
plt.xlabel("Subject")
plt.ylabel("Count")

plt.show()

#Clean date properly (VERY IMPORTANT)
df['date'] = df['date'].astype(str).str.strip()

# Convert to datetime
df['date'] = pd.to_datetime(df['date'], format='%B %d, %Y', errors='coerce')

df['month'] = df['date'].dt.month

df = df.dropna(subset=['month'])

df['month'] = df['month'].astype(int)

print(df[df['news_type'] == 'Real']['month'].value_counts())

monthly_trend = df.groupby('month').size()

print(monthly_trend)

#graph
monthly_trend.plot(kind='line', marker='o')

plt.title("News Trend Over Months")
plt.xlabel("Month")
plt.ylabel("Number of News")

plt.show()

# Separate Fake & Real trends
fake_trend = df[df['news_type'] == 'Fake'].groupby('month').size()
real_trend = df[df['news_type'] == 'Real'].groupby('month').size()

# Combine both into one dataframe
trend_df = pd.DataFrame({
    'Fake': fake_trend,
    'Real': real_trend
}).fillna(0)

# Plot
trend_df.plot(marker='o')

plt.title("Fake vs Real News Trend")
plt.xlabel("Month")
plt.ylabel("Count")

plt.show()

# for creating new_cleaned csv file
df.to_csv("cleaned_news.csv", index=False)

#for sql connection 

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="fakenewsdetectiondb"
)

cursor = conn.cursor()

# Clear old data
cursor.execute("DELETE FROM news_data")

# Prepare data
data = list(df[['title','text','subject','date','news_type']].itertuples(index=False, name=None))

# Insert in batches (VERY IMPORTANT)
batch_size = 500

for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    
    cursor.executemany("""
        INSERT INTO news_data (title, text, subject, date, news_type)
        VALUES (%s, %s, %s, %s, %s)
    """, batch)
    
    conn.commit()
    print(f"Inserted {i + len(batch)} rows")

conn.close()

print("All data inserted successfully")

print(df['news_type'].value_counts())