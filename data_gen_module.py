import pandas as pd
import random

def generate_mock_data():
    # Generate random data
    num_students = 20
    students = [f"Student {i}" for i in range(1, num_students + 1)]

    data = {
        'Student Name': students,
        'Engaged (%)': [random.randint(45, 100) for _ in range(num_students)],
        'Confused (%)': [random.randint(0, 20) for _ in range(num_students)],
        'Frustrated (%)': [random.randint(0, 20) for _ in range(num_students)],
        'Annoyed (%)': [random.randint(0, 15) for _ in range(num_students)]
    }

    df = pd.DataFrame(data)

    # Adjust the data to make sure the percentages add up to 100 or less
    for idx, row in df.iterrows():
        total = row['Engaged (%)'] + row['Confused (%)'] + row['Frustrated (%)'] + row['Annoyed (%)']
        if total > 100:
            diff = total - 100
            for emotion in ['Confused (%)', 'Frustrated (%)', 'Annoyed (%)']:
                if df.at[idx, emotion] >= diff:
                    df.at[idx, emotion] -= diff
                    break

    # Save to CSV
    df.to_csv('data.csv', index=False)
