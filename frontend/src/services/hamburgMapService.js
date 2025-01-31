import api from '../api';


/**
 * Fetches Hamburg vector file from the backend.
 * @returns {Promise<Object>}
 */
export const getHamburgMap = async () => {
    try {
        const response = await api.get('/hamburg/map-data');
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.detail || 'Failed to fetch Map of Hamburg');
    }
};
  