import api from '../api';

/**
 * Fetches Current PM2.5 Air Quality Indicator data.
 * @returns {Promise<Object>}
 */
export const getCurrentAirQualityPM25Indicator = async () => {
    try {
        const response = await api.get('/pm25/indicator');
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to fetch air quality pm25 indicator data.')
    }
};


/**
 * Fetches Current PM2.5 Air Quality Indicator for given points (x,y).
 * @param {number} point_x - Longitude
 * @param {number} point_y - Latitude
 * @returns {Promise<object>}
 */
export const postCurrentAirQualityPM25Indicator = async (point_x, point_y) => {
    try {
        const response = await api.post('/pm25/indicator', {
            point_x,
            point_y
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to post air quality pm25 indicator data.')
    }
};