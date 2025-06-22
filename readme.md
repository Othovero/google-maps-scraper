# Google Maps Restaurant Scraper System

A comprehensive system for scraping restaurant data from Google Maps across multiple UK cities. This project includes strategic batching, session resumption, data conversion, and merging capabilities to efficiently collect restaurant information while avoiding rate limiting. (Can be used for other industries not just restaurants)

## Features

- **Multi-City Scraping**: Scrape restaurants from 82+ UK cities
- **Strategic Batching**: Distribute major cities across batches to optimize scraping
- **Session Resumption**: Resume interrupted scraping sessions
- **Anti-Detection**: Random delays and human-like behavior to avoid blocking
- **Multiple Output Formats**: JSON, CSV, and Excel outputs
- **Progress Tracking**: Save and resume progress automatically
- **Data Merging**: Combine all city results into a single Excel file
- **Duplicate Removal**: Automatic deduplication based on name and address

## 📋 Prerequisites

- Python 3.7+
- Chrome browser installed
- Stable internet connection

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd google-maps-restaurant-scraper
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Project Structure

```
google-maps-restaurant-scraper/
├── google_maps_scraper.py      # Main scraper application
├── create_location_batches.py  # Batch creation utility  
├── convert_to_csv.py          # JSON to CSV converter
├── merge_csvs_to_excel.py     # CSV merger to Excel
├── requirements.txt           # Python dependencies
├── location_batches/          # Pre-created location batches
│   ├── batch_1.txt           # First batch of cities
│   ├── batch_2.txt           # Second batch of cities
│   └── ...                   # Additional batches
├── scraper_progress.json      # Progress tracking (auto-generated)
├── restaurants_*.json         # Scraped data in JSON format
├── restaurants_*.csv          # Converted CSV files
└── all_restaurants.xlsx       # Final merged Excel file
```

## 🚦 Quick Start

### Option 1: Use Pre-created Batches (Recommended)

1. **Run the scraper**
   ```bash
   python google_maps_scraper.py
   ```

2. **Follow the prompts:**
   - Resume previous session? (n for first time)
   - Load locations from file? (y)
   - Enter filename: `location_batches/batch_1.txt`

3. **Wait for completion** (may take 30-60 minutes per batch)

4. **Convert results to CSV**
   ```bash
   python convert_to_csv.py
   ```

### Option 2: Create Custom Batches

1. **Create new batches**
   ```bash
   python create_location_batches.py
   ```
   - Enter batch size (recommended: 10-15 cities)
   - Choose strategic distribution (recommended: yes)

2. **Follow steps 1-4 from Option 1**

## 📖 Detailed Usage

### Creating Location Batches

The batch creation system strategically distributes major cities across batches to improve scraping success rates:

```bash
python create_location_batches.py
```

**Prompts:**
- **Batch size**: Number of cities per batch (10-15 recommended)
- **Strategic distribution**: Evenly distributes major cities across batches

**Output**: Creates `location_batches/` directory with:
- `batch_1.txt`, `batch_2.txt`, etc. - Individual batch files
- `all_locations.txt` - Complete list of all cities

### Running the Scraper

```bash
python google_maps_scraper.py
```

**Key Features:**
- **Session Resumption**: If interrupted, restart and choose "y" to resume
- **Progress Tracking**: Automatically saves progress to `scraper_progress.json`
- **Random Delays**: 45-120 seconds between cities to avoid detection
- **Detailed Logging**: Real-time progress updates and error handling

**Search Query**: Currently configured to search for "Caribbean restaurants in [city]"

### Data Conversion

**Convert single JSON file:**
```bash
python convert_to_csv.py path/to/restaurants_city_timestamp.json
```

**Convert all JSON files:**
```bash
python convert_to_csv.py --all
```

### Merging Results

Combine all CSV files into a single Excel file:
```bash
python merge_csvs_to_excel.py
```

**Features:**
- Automatically finds all `restaurants_*.csv` files
- Adds location column to each record
- Removes duplicates based on name and address
- Outputs to `all_restaurants.xlsx`

## 📊 Data Structure

### JSON Output Format
```json
{
  "location": "London",
  "scrape_date": "2024-04-14T10:30:00",
  "total_restaurants": 25,
  "restaurants": [
    {
      "name": "Restaurant Name",
      "website": "https://example.com",
      "phone": "+44 20 1234 5678", 
      "address": "123 Main St, London, UK"
    }
  ]
}
```

### CSV/Excel Columns
- `name`: Restaurant name
- `website`: Website URL (if available)
- `phone`: Phone number (if available)
- `address`: Full address (if available)
- `location`: City name (added during merging)

## ⚙️ Configuration

### Modifying Search Terms

Edit the search query in `google_maps_scraper.py`:

```python
# Line ~30 in search_restaurants method
params = {
    'tbm': 'lcl',
    'q': f"Caribbean restaurants in {location}"  # Modify this line
}
```

### Adjusting Delays

Modify delay settings in `google_maps_scraper.py`:

```python
# Between cities (line ~340)
delay = random.uniform(45, 120)  # 45-120 seconds

# Between actions (line ~18)
def random_delay(self, min_seconds=2, max_seconds=5):
```

### Adding/Removing Cities

Edit the `all_locations` list in `create_location_batches.py` to customize cities.

## 🎯 Best Practices

### Batch Processing Strategy
1. **Start with small batches** (8-10 cities) to test
2. **Space out batch runs** by several hours or days
3. **Monitor first few cities** in each batch for quality
4. **Use different times of day** for different batches

### Avoiding Detection
- **Don't run continuously** - space out batches
- **Monitor for blocking** - if data quality drops, increase delays
- **Use residential IP** if possible
- **Avoid peak hours** (9am-5pm UK time)

### Data Quality
- **Check results regularly** during first few cities
- **Verify address extraction** is working correctly
- **Monitor for empty results** which may indicate blocking

## 🔧 Troubleshooting

### Common Issues

**No restaurants found:**
- Check if Google Maps layout has changed
- Verify Chrome browser is up to date
- Try increasing wait times in the code

**Session interrupted:**
- Run scraper again and choose "y" to resume
- Check `scraper_progress.json` for current state

**Chrome driver issues:**
- Chrome driver auto-updates via webdriver-manager
- If issues persist, manually update Chrome browser

**Rate limiting/blocking:**
- Increase delays between cities
- Wait longer between batch runs
- Consider using proxy services

### Error Logs

Check `scraper.log` for detailed error information and debugging.

## 📈 Performance

### Expected Results
- **Time per city**: 2-10 minutes depending on restaurant count
- **Batch completion**: 30-90 minutes for 10-15 cities
- **Success rate**: 80-95% with proper delay settings
- **Restaurant yield**: 5-50 restaurants per city (varies greatly)

## 🤝 Contributing

When contributing to this project:

1. **Test thoroughly** with small batches first
2. **Update documentation** for any new features
3. **Follow existing code style** and error handling patterns
4. **Add logging** for new functionality

## ⚠️ Disclaimer

This tool is for educational and research purposes. Always respect website terms of service and implement appropriate delays to avoid overloading servers. Users are responsible for complying with applicable laws and website policies.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review error logs in `scraper.log`
3. Create an issue in the repository with detailed error information

---

**Happy Scraping! 🍽️** 