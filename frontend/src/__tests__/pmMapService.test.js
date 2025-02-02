import api from '../api';
import { getPM25Map, postPM25Map } from '../services/pmMapService';


jest.mock('../api', () => ({
    get: jest.fn(),
    post: jest.fn(),
}));

describe('PM2.5 Map Functions', () => {

    it('should return data when API call is successful for getPM25Map', async () => {
        const mockResponse = { data: { mapData: [5, 10, 15] } };
        api.get.mockResolvedValue(mockResponse);

        const result = await getPM25Map();
        expect(result).toEqual(mockResponse.data);
        expect(api.get).toHaveBeenCalledWith('/pm25/map-data');
    });

    it('should throw an error when API call fails for getPM25Map', async () => {

        const mockError = {
        response: {
            data: {
            detail: 'Error message from the server',
            },
        },
        };
        api.get.mockRejectedValue(mockError); 

        await expect(getPM25Map()).rejects.toThrow('Error message from the server');
        expect(api.get).toHaveBeenCalledWith('/pm25/map-data');
    });

    it('should throw a default error message if no error detail is provided for getPM25Map', async () => {

        const mockError = {
        response: {
            data: {},
        },
        };
        api.get.mockRejectedValue(mockError);

        await expect(getPM25Map()).rejects.toThrow('Computing, try again later.');
        expect(api.get).toHaveBeenCalledWith('/pm25/map-data');
    });

    it('should return data when API call is successful for postPM25Map', async () => {

        const mockResponse = { data: { result: 'success' } };
        api.post.mockResolvedValue(mockResponse); 

        const result = await postPM25Map('2025-01-01', '2025-01-31');
        expect(result).toEqual(mockResponse.data);
        expect(api.post).toHaveBeenCalledWith('/pm25/map-data', {
        start_date: '2025-01-01',
        end_date: '2025-01-31',
        });
    });

    it('should throw an error when API call fails for postPM25Map', async () => {

        const mockError = {
        response: {
            data: {
            detail: 'Error message from the server',
            },
        },
        };
        api.post.mockRejectedValue(mockError);

        await expect(postPM25Map('2025-01-01', '2025-01-31')).rejects.toThrow('Error message from the server');
        expect(api.post).toHaveBeenCalledWith('/pm25/map-data', {
        start_date: '2025-01-01',
        end_date: '2025-01-31',
        });
    });

    it('should throw a default error message if no error detail is provided for postPM25Map', async () => {

        const mockError = {
        response: {
            data: {},
        },
        };
        api.post.mockRejectedValue(mockError);

        await expect(postPM25Map('2025-01-01', '2025-01-31')).rejects.toThrow('Failed to post Map PM2.5 averages');
        expect(api.post).toHaveBeenCalledWith('/pm25/map-data', {
        start_date: '2025-01-01',
        end_date: '2025-01-31',
        }); 
    });
});
