import pandas as pd

def load_data(filepath=None):
    if filepath:
        try:
            df = pd.read_csv(filepath)
            
            # Map your data columns to the expected columns
            df = df.rename(columns={
                'sold_price': 'Closing Price',  # Map sold_price to Closing Price
                'beds': 'Bedrooms',            # Map beds to Bedrooms
                'full_baths': 'Bathrooms',      # Map full_baths to Bathrooms
                'last_sold_date': 'Date',      # Map last_sold_date to Date
                'zip_code': 'ZIP Code',         # Map zip_code to ZIP Code
                'lot_sqft': 'Yard Size',        # Map lot_sqft to Yard Size
                'parking_garage': 'Garage',     # Map parking_garage to Garage
                'sqft': 'Sqft'                  # Map sqft to Sqft (if needed)
            })
            
            # Convert the 'Date' column to datetime
            df['Date'] = pd.to_datetime(df['Date'])
            
            return df
        except Exception as e:
            print(f"Error loading data from {filepath}: {e}")
            return None
    else:
        # Sample data for demonstration
        data = {
            'Closing Price': [350000, 420000, 315000],
            'Bedrooms': [3, 4, 2],
            'Bathrooms': [2, 3, 2],
            'Yard Size': [500, 600, 400],
            'Garage': [1, 2, 1],
            'Parking Spaces': [2, 3, 1],
            'ZIP Code': ['30301', '30302', '30303'],
            'Date': ['2024-01-15', '2024-03-22', '2024-05-10']
        }
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
