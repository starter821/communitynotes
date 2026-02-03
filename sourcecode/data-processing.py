import pandas as pd
import os

"""
python data_engineer.py
"""

OUTPUT_DIR = "../../data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Download files
print("Downloading notes...")
notes_url = (
    "https://ton.twimg.com/birdwatch-public-data/2026/02/02/notes/"
    "notes-00000.zip"
)
notes = pd.read_csv(notes_url, sep='\t', low_memory=False)

print("Downloading ratings...")

ratings_parts = []

for i in range(2):  # 0 through n
    url = f"https://ton.twimg.com/birdwatch-public-data/2026/02/02/noteRatings/ratings-{i:05d}.zip"
    print(f"Downloading ratings-{i:05d}.zip...")

    df = pd.read_csv(url, sep='\t', compression='zip', low_memory=False)

    # Check the date range in this file
    df['date'] = pd.to_datetime(df['createdAtMillis'], unit='ms')
    min_date = df['date'].min()
    max_date = df['date'].max()
    print(f"  Date range: {min_date} to {max_date}")

    # Keep only data before Nov 1, 2023
    df_filtered = df[df['date'] <= '2023-10-31']

    if len(df_filtered) > 0:
        ratings_parts.append(df_filtered.drop(columns=['date']))
        print(f"  Kept {len(df_filtered)} rows")

    # If this file has NO data before Oct 2023, we're done
    if len(df_filtered) == 0:
        print(f"  No more data before Oct 2023, stopping at file {i}")
        break

ratings = pd.concat(ratings_parts, ignore_index=True)


print("Downloading note status history...")
status_url = (
    "https://ton.twimg.com/birdwatch-public-data/2026/02/02/"
    "noteStatusHistory/noteStatusHistory-00000.zip"
)
notes_status = pd.read_csv(status_url, sep='\t')

print("Downloading user enrollment...")
enrollment_url = (
    "https://ton.twimg.com/birdwatch-public-data/2026/02/02/"
    "userEnrollment/userEnrollment-00000.zip"
)
userEnrollment = pd.read_csv(enrollment_url, sep='\t')

# Filter by date
print("\nFiltering data...")
notes['date'] = pd.to_datetime(notes['createdAtMillis'], unit='ms')
notes = notes[notes['date'] <= '2023-10-31']

notes_status['date'] = pd.to_datetime(
    notes_status['createdAtMillis'], unit='ms')
notes_status = notes_status[notes_status['date'] <= '2023-10-31']

ratings['date'] = pd.to_datetime(ratings['createdAtMillis'], unit='ms')
ratings = ratings[ratings['date'] <= '2023-10-31']

# Drop temporary date columns
notes = notes.drop(columns=['date'])
notes_status = notes_status.drop(columns=['date'])
ratings = ratings.drop(columns=['date'])

# Remove the unnecessary column

# notes
if 'isCollaborativeNote' in notes.columns:
    notes = notes.drop(columns=['isCollaborativeNote'])
    print(f"  Removed 'isCollaborativeNote' column")

# ratings
if 'ratingSourceBucketed' in ratings.columns:
    ratings = ratings.drop(columns=['ratingSourceBucketed'])
    print(f"  Removed 'ratingSourceBucketed' column")

# note status
columns_to_remove = [
    'timestampMillisOfMostRecentStatusChange',
    'timestampMillisOfNmrDueToMinStableCrhTime',
    'currentMultiGroupStatus',
    'currentModelingMultiGroup',
    'timestampMinuteOfFinalScoringOutput',
    'timestampMillisOfFirstNmrDueToMinStableCrhTime'
]

for col in columns_to_remove:
    if col in notes_status.columns:
        notes_status = notes_status.drop(columns=[col])
        print(f"  Removed '{col}' column")

# user enrollment
if 'numberOfTimesEarnedOut' in userEnrollment.columns:
    userEnrollment = userEnrollment.drop(columns=['numberOfTimesEarnedOut'])
    print(f"  Removed 'numberOfTimesEarnedOut' column")


#  Save
print("\nSaving filtered files...")
notes.to_csv(f'{OUTPUT_DIR}/notes-00001.tsv', sep='\t', index=False)
notes_status.to_csv(f'{OUTPUT_DIR}/noteStatusHistory-00001.tsv',
                    sep='\t', index=False)
ratings.to_csv(f'{OUTPUT_DIR}/ratings-00001.tsv', sep='\t', index=False)
userEnrollment.to_csv(f'{OUTPUT_DIR}/userEnrollment-00001.tsv',
                      sep='\t', index=False)

print(f"\nFiltered files saved to '{OUTPUT_DIR}'")
print(f"Notes: {len(notes)} rows")
print(f"Ratings: {len(ratings)} rows")
print(f"Status: {len(notes_status)} rows")
print(f"User Enrollment: {len(userEnrollment)} rows")
