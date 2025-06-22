import os
import math
import random

def create_batches(locations, batch_size=10, strategic=False):
    """Split locations into batches of specified size"""
    if not strategic:
        # Simple sequential batching
        num_batches = math.ceil(len(locations) / batch_size)
        batches = []
        
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = min(start_idx + batch_size, len(locations))
            batch = locations[start_idx:end_idx]
            batches.append(batch)
    else:
        # Strategic batching - distribute major cities
        # Mark major cities with * in the original list
        major_cities = [loc.replace("*", "").strip() for loc in locations if "*" in loc]
        other_cities = [loc.replace("*", "").strip() for loc in locations if "*" not in loc]
        
        # Ensure we have all cities without asterisks
        clean_locations = [loc.replace("*", "").strip() for loc in locations]
        
        # Shuffle both lists to randomize distribution
        random.shuffle(major_cities)
        random.shuffle(other_cities)
        
        # Calculate how many major cities per batch
        num_batches = math.ceil(len(clean_locations) / batch_size)
        major_per_batch = math.ceil(len(major_cities) / num_batches)
        
        # Create batches with mix of major and other cities
        batches = []
        major_idx = 0
        other_idx = 0
        
        for _ in range(num_batches):
            batch = []
            
            # Add major cities to this batch
            for _ in range(major_per_batch):
                if major_idx < len(major_cities):
                    batch.append(major_cities[major_idx])
                    major_idx += 1
                    
            # Fill the rest with other cities
            while len(batch) < batch_size and other_idx < len(other_cities):
                batch.append(other_cities[other_idx])
                other_idx += 1
                
            if batch:  # Only add non-empty batches
                batches.append(batch)
    
    return batches

def save_batches_to_files(batches, output_dir="location_batches"):
    """Save each batch to a separate file"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for i, batch in enumerate(batches):
        batch_filename = os.path.join(output_dir, f"batch_{i+1}.txt")
        with open(batch_filename, 'w', encoding='utf-8') as f:
            for location in batch:
                f.write(f"{location}\n")
        print(f"Saved batch {i+1} with {len(batch)} locations to {batch_filename}")

def save_all_locations(locations, output_dir="location_batches"):
    """Save the complete list of locations"""
    os.makedirs(output_dir, exist_ok=True)
    all_locations_file = os.path.join(output_dir, "all_locations.txt")
    
    with open(all_locations_file, 'w', encoding='utf-8') as f:
        for location in locations:
            f.write(f"{location.replace('*', '')}\n")
    
    print(f"Saved all {len(locations)} locations to {all_locations_file}")

def main():
    # The list of all locations (* marks major cities for strategic batching)
    all_locations = [
        "Bath",
        "Birmingham",
        "Bradford",
        "Brighton & Hove",
        "Bristol",
        "Cambridge",
        "Canterbury",
        "Carlisle",
        "Chelmsford",
        "Chester",
        "Chichester",
        "Colchester",
        "Coventry",
        "Derby",
        "Doncaster",
        "Durham",
        "Ely",
        "Exeter",
        "Gloucester",
        "Hereford",
        "Kingston-upon-Hull",
        "Lancaster",
        "Leeds",
        "Leicester",
        "Lichfield",
        "Lincoln",
        "Liverpool",
        "London",
        "Manchester",
        "Milton Keynes",
        "Newcastle-upon-Tyne",
        "Norwich",
        "Nottingham",
        "Oxford",
        "Peterborough",
        "Plymouth",
        "Portsmouth",
        "Preston",
        "Ripon",
        "Salford",
        "Salisbury",
        "Sheffield",
        "Southampton",
        "Southend-on-Sea",
        "St Albans",
        "Stoke on Trent",
        "Sunderland",
        "Truro",
        "Wakefield",
        "Wells",
        "Westminster",
        "Winchester",
        "Wolverhampton",
        "Worcester",
        "York",
        "Armagh",
        "Bangor",
        "Belfast",
        "Lisburn",
        "Londonderry",
        "Newry",
        "Aberdeen",
        "Dundee",
        "Dunfermline",
        "Edinburgh",
        "Glasgow",
        "Inverness",
        "Perth",
        "Stirling",
        "Bangor (Wales)",
        "Cardiff",
        "Newport",
        "St Asaph",
        "St Davids",
        "Swansea",
        "Wrexham",
        "Douglas",
        "Hamilton",
        "City of Gibraltar",
        "Stanley",
        "Jamestown"
    ]
    
    # Get batch size from user
    try:
        batch_size = int(input("Enter the number of locations per batch (recommended: 10-15): "))
        if batch_size <= 0:
            raise ValueError("Batch size must be positive")
    except ValueError:
        print("Invalid input. Using default batch size of 10.")
        batch_size = 10
    
    # Ask if user wants strategic batching
    strategic_input = input("Do you want to distribute major cities evenly across batches? (y/n): ").lower()
    strategic = strategic_input.startswith('y')
    
    # Create batches
    batches = create_batches(all_locations, batch_size, strategic)
    
    # Save all locations and batches
    save_all_locations(all_locations)
    save_batches_to_files(batches)
    
    print(f"\nCreated {len(batches)} batches with approximately {batch_size} locations per batch")
    print(f"Files are saved in the 'location_batches' directory")
    print("\nTo use these batches with the scraper:")
    print("1. Run the scraper: python google_maps_scraper.py")
    print("2. Choose to load locations from a file (y)")
    print(f"3. Enter the path to a batch file (e.g., location_batches/batch_1.txt)")
    
    # Print the first few batches as examples
    print("\nExample batches:")
    for i in range(min(3, len(batches))):
        print(f"Batch {i+1}: {', '.join(batches[i])}")

if __name__ == "__main__":
    main() 