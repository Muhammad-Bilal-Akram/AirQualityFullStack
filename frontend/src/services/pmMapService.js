import api from '../api';


/**
 * Fetches PM2.5 averages without any filters.
 * @returns {Promise<Object>}
 */
export const getPM25Map = async () => {
  try {
    const response = await api.get('/pm25/map-data');
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Computing, try again later.');
  }
};

/**
 * Posts PM2.5 averages with optional filters.
 * @param {string} start_date - Start date
 * @param {string} end_date - End date
 * @returns {Promise<Object>}
 */
export const postPM25Map = async (start_date, end_date) => {
    try {
      const response = await api.post('/pm25/map-data', {
        start_date,
        end_date,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to post Map PM2.5 averages');
    }
  };