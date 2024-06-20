import pandas as pd
import sqlite3
import cv2

def initialize_database(csv_path, db_path='images.db'):
    print(f"Reading CSV file from {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Initial dataframe shape: {df.shape}")
    print(f"First few rows of the dataframe:\n{df.head()}")

    # Drop rows where 'depth' is NaN
    df = df.dropna(subset=['depth'])
    print(f"Dataframe shape after dropping NaNs: {df.shape}")

    # Ensure 'depth' is of integer type
    df['depth'] = df['depth'].astype(int)

    # Extract pixel data and resize image
    image_data = df.iloc[:, 1:].values  # Exclude the 'depth' column to enable image resizing
    resized_image_data = cv2.resize(image_data, (150, image_data.shape[0]))
    print(f"Resized image data shape: {resized_image_data.shape}")

    # Save the resized image data back to a DataFrame
    resized_df = pd.DataFrame(resized_image_data)
    resized_df.insert(0, 'depth', df['depth'])  # Reinsert the 'depth' column

    # Connect to SQLite database (creates the database file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table
    c.execute('''
    CREATE TABLE IF NOT EXISTS image_frames (
        depth INTEGER PRIMARY KEY,
        pixel_data BLOB
    )
    ''')

    # Insert resized image data
    for _, row in resized_df.iterrows():
        pixel_data = row[1:].values.tobytes()  # Convert pixel data to bytes
        c.execute('INSERT OR REPLACE INTO image_frames (depth, pixel_data) VALUES (?, ?)', (row['depth'], pixel_data))

    conn.commit()
    conn.close()
    print("Database initialization completed.")
