import api from '../api'; 
import { getPM25Averages, postPM25Averages } from '../services/averagesService';

jest.mock('../api', () => ({
    get: jest.fn(),
    post: jest.fn(),
}));

describe('PM2.5 Averages Functions', () => {

    it('should return data when API call is successful for getPM25Averages', async () => {
        const mockResponse = { data: [{
            "Current_day_week_year": 2, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 1}, {
            "Current_day_week_year": 5, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 1}, {
            "Current_day_week_year": 2025, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 0.0}] };
        api.get.mockResolvedValue(mockResponse);

        const result = await getPM25Averages();
        expect(result).toEqual(mockResponse.data);
        expect(api.get).toHaveBeenCalledWith('/pm25/averages');
    });

    it('should throw an error when API call fails for getPM25Averages', async () => {
        const mockError = {
        response: {
            data: {
            detail: 'Error message from the server',
            },
        },
        };
        api.get.mockRejectedValue(mockError);

        await expect(getPM25Averages()).rejects.toThrow('Error message from the server');
        expect(api.get).toHaveBeenCalledWith('/pm25/averages'); 
    });

    it('should throw a default error message if no error detail is provided for getPM25Averages', async () => {
        const mockError = {
        response: {
            data: {},
        },
        };
        api.get.mockRejectedValue(mockError);

        await expect(getPM25Averages()).rejects.toThrow('Computing, try again later.');
        expect(api.get).toHaveBeenCalledWith('/pm25/averages'); 
    });

    it('should return data when API call is successful for postPM25Averages', async () => {

        const mockResponse = { data: [{
            "Current_day_week_year": 2, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 1}, {
            "Current_day_week_year": 5, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 1}, {
            "Current_day_week_year": 2025, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 0.0}] };
        api.post.mockResolvedValue(mockResponse);

        const result = await postPM25Averages(10, 20, 5, 3, 2025);
        expect(result).toEqual(mockResponse.data);
        expect(api.post).toHaveBeenCalledWith('/pm25/averages', {
        point_x: 10,
        point_y: 20,
        week_number: 5,
        month_number: 3,
        year: 2025,
        });
    });

    it('should throw an error when API call fails for postPM25Averages', async () => {

        const mockError = {
        response: {
            data: {
            detail: 'Error message from the server',
            },
        },
        };
        api.post.mockRejectedValue(mockError); 

        await expect(postPM25Averages(10, 20, 5, 3, 2025)).rejects.toThrow('Error message from the server');
        expect(api.post).toHaveBeenCalledWith('/pm25/averages', {
        point_x: 10,
        point_y: 20,
        week_number: 5,
        month_number: 3,
        year: 2025,
        });
    });

    it('should throw a default error message if no error detail is provided for postPM25Averages', async () => {

        const mockError = {
        response: {
            data: {},
        },
        };
        api.post.mockRejectedValue(mockError);

        await expect(postPM25Averages(10, 20, 5, 3, 2025)).rejects.toThrow('Failed to post PM2.5 averages');
        expect(api.post).toHaveBeenCalledWith('/pm25/averages', {
        point_x: 10,
        point_y: 20,
        week_number: 5,
        month_number: 3,
        year: 2025,
        }); 
    });
});
