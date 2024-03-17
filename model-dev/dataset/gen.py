import pandas as pd
import numpy as np
import random
import faker
import datetime

# Initialize Faker to generate fake data
fake = faker.Faker()

# Number of users and entries per user
num_users = 30
entries_per_user = 100
past_liked_keywords = 10

# List to store generated data
data = {
    'user_id': [],
    'query': [],
    'search_link_clicked': [],
    'meta_data': [],
    'time_spent': [],
    'past_searches': [],
    'priority_score': [],
}

# Generate browsing history data for each user
for user_id in range(1, num_users + 1):
    for _ in range(entries_per_user):
        data['user_id'].append(user_id)
        
        # Generate fake search query
        search_query = fake.text(max_nb_chars=random.randint(5, 50))
        data['query'].append(search_query)
        
        # Generate fake search link clicked
        search_link_clicked = fake.uri()
        data['search_link_clicked'].append(search_link_clicked)
        
        # Generate fake meta data
        meta_data = fake.text(max_nb_chars=random.randint(50, 200))
        data['meta_data'].append(meta_data)
        
        # Generate fake time spent on site
        time_spent = random.randint(1, 600)  # Random time between 1 second and 10 minutes
        data['time_spent'].append(time_spent)

        # Add past liked keywords for the user
        keywords = fake.text(max_nb_chars=random.randint(20, 40))
        data['past_searches'].append(keywords)

        # Generate fake priority score
        priority_score = random.randint(1, 100) / 100.0
        data['priority_score'].append(priority_score)

# Create DataFrame from generated data
df = pd.DataFrame(data)

# Convert time spent to datetime format
df['time_spent'] = df['time_spent'].apply(lambda x: datetime.timedelta(seconds=x))

# Display first few rows of the generated dataset
print(df.head())

# Save dataset to CSV file
df.to_csv('browsing_history_dataset.csv', index=False)
