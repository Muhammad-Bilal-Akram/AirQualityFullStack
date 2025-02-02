import { getCurrentAirQualityPM25Indicator, postCurrentAirQualityPM25Indicator } from "../services/indicatorService";
import api from "../api";

jest.mock("../api", () => ({
    get: jest.fn(),
    post: jest.fn(),
}));

describe('Air Quality PM2.5 Indicator Functions', () => {

    it('should return data when API call is successful for getCurrentAirQualityPM25Indicator', async () => {
        const mockResponse = { data: [{
            "Current_day_week_year": 2, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 1}, {
            "Current_day_week_year": 5, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 1}, {
            "Current_day_week_year": 2025, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 0.0}] };
        api.get.mockResolvedValue(mockResponse);
        const result = await getCurrentAirQualityPM25Indicator();

        expect(result).toEqual(mockResponse.data);
        expect(api.get).toHaveBeenCalledWith('/pm25/indicator');
    });

    it('should throw an error when API call fails for getCurrentAirQualityPM25Indicator', async () => {
        const mockError = {
        response: {
            data: {
            detail: 'Precomputing PM2.5 indicator, try again later.',
            },
        },
        };
        api.get.mockRejectedValue(mockError);

        await expect(getCurrentAirQualityPM25Indicator()).rejects.toThrow('Precomputing PM2.5 indicator, try again later.');
        expect(api.get).toHaveBeenCalledWith('/pm25/indicator'); 
    });

    it('should throw a default error message if no error detail is provided for getCurrentAirQualityPM25Indicator', async () => {
        const mockError = {
        response: {
            data: {},
        },
        };
        api.get.mockRejectedValue(mockError);

        await expect(getCurrentAirQualityPM25Indicator()).rejects.toThrow('Computing, try again later.');
        expect(api.get).toHaveBeenCalledWith('/pm25/indicator');
    });


    it('should return data when API call is successful for postCurrentAirQualityPM25Indicator', async () => {
        const mockResponse = { data: [{
            "Current_day_week_year": 2, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 1}, {
            "Current_day_week_year": 5, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 1}, {
            "Current_day_week_year": 2025, "Average_PM2.5": 1, "Air_quality_indicator_yearly_comparison": 0.0}] };
        api.post.mockResolvedValue(mockResponse);

        const result = await postCurrentAirQualityPM25Indicator(10, 20);
        expect(result).toEqual(mockResponse.data);
        expect(api.post).toHaveBeenCalledWith('/pm25/indicator', { point_x: 10, point_y: 20 });
    });

    it('should throw an error when API call fails for postCurrentAirQualityPM25Indicator', async () => {
        const mockError = {
        response: {
            data: {
            detail: 'Error message from the server',
            },
        },
        };
        api.post.mockRejectedValue(mockError);

        await expect(postCurrentAirQualityPM25Indicator(10, 20)).rejects.toThrow('Error message from the server');
        expect(api.post).toHaveBeenCalledWith('/pm25/indicator', { point_x: 10, point_y: 20 });
    });

    it('should throw a default error message if no error detail is provided for postCurrentAirQualityPM25Indicator', async () => {
        const mockError = {
        response: {
            data: {},
        },
        };
        api.post.mockRejectedValue(mockError);

        await expect(postCurrentAirQualityPM25Indicator(10, 20)).rejects.toThrow('Failed to post air quality pm25 indicator data.');
        expect(api.post).toHaveBeenCalledWith('/pm25/indicator', { point_x: 10, point_y: 20 });
    });
});
