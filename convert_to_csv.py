import json
import csv
import sys
from pathlib import Path
import glob

def convert_json_to_csv(json_file, csv_file):
    # Read JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get the restaurants array
        restaurants = data['restaurants']
        
        # Open CSV file for writing
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            # Create CSV writer
            writer = csv.DictWriter(f, fieldnames=['name', 'website', 'phone', 'address'])
            
            # Write header
            writer.writeheader()
            
            # Write each restaurant
            for restaurant in restaurants:
                writer.writerow(restaurant)
        
        print(f"Successfully converted {len(restaurants)} restaurants to CSV")
        print(f"Input JSON: {json_file}")
        print(f"Output CSV: {csv_file}")
        return True
    except FileNotFoundError:
        print(f"Error: Could not find the JSON file '{json_file}'")
        return False
    except json.JSONDecodeError:
        print(f"Error: '{json_file}' is not a valid JSON file")
        return False
    except KeyError:
        print(f"Error: JSON file does not have the expected 'restaurants' array")
        return False
    except Exception as e:
        print(f"Error: An unexpected error occurred: {str(e)}")
        return False

def convert_all_json_files():
    # Find all restaurant JSON files
    json_files = list(Path('.').glob('restaurants_*.json'))
    
    if not json_files:
        print("Error: No restaurant JSON files found in current directory")
        return False
    
    print(f"Found {len(json_files)} JSON files to convert")
    
    success_count = 0
    fail_count = 0
    
    for json_file in json_files:
        json_file_str = str(json_file)
        csv_file = json_file.stem + ".csv"
        
        if convert_json_to_csv(json_file_str, csv_file):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\nConversion Summary:")
    print(f"Total files processed: {len(json_files)}")
    print(f"Successfully converted: {success_count}")
    print(f"Failed conversions: {fail_count}")
    
    return success_count > 0

if __name__ == "__main__":
    # Check if user wants to process a single file or all files
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            print("Converting all JSON files...")
            if convert_all_json_files():
                print("Batch conversion completed")
            else:
                print("Batch conversion failed")
                sys.exit(1)
        else:
            # Process a single file provided by the user
            json_file = sys.argv[1]
            csv_file = Path(json_file).stem + ".csv"
            
            if convert_json_to_csv(json_file, csv_file):
                print("Conversion completed successfully")
    else:
        # Default behavior: convert all files
        print("Converting all JSON files...")
        if convert_all_json_files():
            print("Batch conversion completed")
        else:
            print("Batch conversion failed")
            sys.exit(1) 