import api from '../api';

/**
 * Fetches PM2.5 averages without any filters.
 * @returns {Promise<Object>}
 */
export const getPM25Averages = async () => {
    try {
        const response = await api.get('/pm25/averages');
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Computing, try again later.');
    }
};


/**
 * Posts PM2.5 averages with optional filters.
 * @param {number} point_x - X coordinate
 * @param {number} point_y - Y coordinate
 * @param {number} week_number - Week filter (optional)
 * @param {number} month_number - Month filter (optional)
 * @param {number} year - Year filter
 * @returns {Promise<Object>}
 */
export const postPM25Averages = async (point_x, point_y, week_number, month_number, year) => {
    try {
        const response = await api.post('/pm25/averages', {
            point_x,
            point_y,
            week_number,
            month_number,
            year,
        });
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to post PM2.5 averages');
    }
};