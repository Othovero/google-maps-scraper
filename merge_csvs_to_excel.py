import pandas as pd
import glob
import re
from pathlib import Path

def extract_location(filename):
    """Extract location from filename like 'restaurants_york_20250413_152951.csv'"""
    # Get the base filename without extension
    basename = Path(filename).stem
    
    # Extract location using regex - match after 'restaurants_' and before the date
    match = re.search(r'restaurants_([^_]+(?:_[^_]+)*)_\d+', basename)
    if match:
        # Replace underscores with spaces and title case the location
        location = match.group(1).replace('_', ' ').title()
        return location
    
    return "Unknown"

def merge_csv_files_to_excel():
    print("Starting to merge CSV files...")
    
    # Get all CSV files matching the pattern
    csv_files = glob.glob('restaurants_*.csv')
    
    if not csv_files:
        print("No CSV files found to merge!")
        return False
    
    print(f"Found {len(csv_files)} CSV files to merge")
    
    # Create empty list to store DataFrames
    all_dataframes = []
    
    # Process each CSV file
    for csv_file in csv_files:
        try:
            # Read the CSV file
            df = pd.read_csv(csv_file)
            
            # Add location column
            location = extract_location(csv_file)
            df['location'] = location
            
            # Add to the list of dataframes
            all_dataframes.append(df)
            print(f"Processed {csv_file} - {location} ({len(df)} restaurants)")
        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")
    
    if not all_dataframes:
        print("No data could be processed")
        return False
    
    # Combine all DataFrames
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    
    # Remove duplicates based on name and address
    original_count = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=['name', 'address'])
    duplicates_removed = original_count - len(combined_df)
    
    print(f"\nRemoved {duplicates_removed} duplicate entries")
    print(f"Final dataset has {len(combined_df)} unique restaurants")
    
    # Save to Excel file
    output_file = 'all_restaurants.xlsx'
    combined_df.to_excel(output_file, index=False)
    
    print(f"\nSuccessfully merged all CSV files into {output_file}")
    return True

if __name__ == "__main__":
    merge_csv_files_to_excel() 