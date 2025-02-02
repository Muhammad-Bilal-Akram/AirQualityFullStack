
# Technical Challenge:

## Part 1: Backend

### Data Processing
1. **Data Acquisition**: Downloaded and processed weekly, monthly, and yearly averages of PM2.5 levels.
2. **Data Comparison**: Compared current values (daily/weekly averages) with yearly averages to identify trends.
3. **Preprocessing for Performance**: Implemented optional preprocessing for GET requests to improve performance.

### API Development
Developed multiple endpoints for retrieving and posting PM2.5 data:
- **/pm25/averages**: 
  - `GET`: Retrieves average PM2.5 values.
  - `POST`: Allows submission of data (coordinates) to calculate/view PM2.5 data.
- **/pm25/indicator**: 
  - `GET`: Retrieves PM2.5 indicator data.
  - `POST`: Allows submission of data (coordinates) to calculate/view indicator data.
- **/pm25/map-data**: 
  - `GET`: Fetches map data for PM2.5 visualization.
  - `POST`: Allows submission of data (time-scale) to get/view map-related data.
- **/hamburg/map-data**: Created an additional endpoint specifically for rendering the map of Hamburg.

## Part 2: Frontend

### Key Features Implemented
1. **Hamburg Map**: Integrated Mapbox GL JS to render an interactive map of Hamburg.
2. **PM2.5 Overlay**: Added overlay functionality to display PM2.5 levels on the map.
3. **Interactive Map Features**: Enabled map interaction features like zoom, pan, and view details on click.
4. **PM2.5 Display**: Displayed PM2.5 data in an intuitive format.
5. **Indicator Display**: Showed indicators comparing current PM2.5 values (daily, weekly) to yearly averages.

## Optional Enhancements

### Features Implemented
1. **Heatmap with Time Range**: Implemented the ability to select a time range for the heatmap and included a feature for users to insert their coordinates to calculate current and average PM2.5 values for their area.
2. **Search Bar**: Added a search bar for easier navigation and data retrieval.
3. **Testing**: Testing was not implemented for both backend and frontend.

### Features Postponed or Planned
1. **Machine Learning**: While not implemented, machine learning is a future enhancement, using a combination of several gases for PM2.5 prediction.

## Tools and Approach

- **API Development**: FastAPI was chosen for its speed and ease of use in building RESTful APIs.
- **Frontend**: React.js with Material UI was used for building the interactive UI.
- **Data Downloading**: Google Earth Engine combined with the Geemap library was used to download the necessary environmental data.
- **Data Processing**: Utilized geospatial libraries like `rasterio`, `shapely`, `geopandas`, etc., for data processing and analysis.
- **Testing**: Pytest for backend, jest for frontend.

## Challenges Faced

1. **PM2.5 Calculation with Sentinel-5P**:
   - The primary challenge was the lack of direct PM2.5 data from Sentinel-5P. 
   - Extensive research was conducted to find a method to calculate PM2.5 using available data.
   - After exploring various combinations of gases, the following approaches were tested:
     - **NO2 + CO**: This combination initially provided poor results. After converting NO2 values from mol/m² to µg/m³, the results were acceptable, but the CO values were far out of range.
     - **NO2 + SO2 + O2**: Similar results to the NO2 + CO combination.
     - **NO2 + AAI (Absorbed Aerosol Index)**: This combination produced the best results. The formula to calculate PM2.5 is:
       \[
       \text{PM2.5} = (\alpha \times \text{NO2 (converted to µg/m³)}) + (\beta \times \text{AAI})
       \]
       Where (these were assumptions):
       - \(\alpha = 5\) for NO2
       - \(\beta = 30\) for AAI

## Potential Improvements

1. **Improved PM2.5 Calculation**: 
   - Investigate better proxies for calculating PM2.5, potentially incorporating ground truth data.
   - Merge data from other satellite sources (e.g., MODIS for AOD band data) to improve accuracy.
2. **Refining Coefficients**: 
   - Further research into more accurate coefficients for the PM2.5 calculation formula could improve prediction accuracy.





