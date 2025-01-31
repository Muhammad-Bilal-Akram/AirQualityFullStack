import React, { useState, useEffect} from "react";
import { 
    getCurrentAirQualityPM25Indicator, 
    postCurrentAirQualityPM25Indicator 
} from "../services/indicatorService";
import { 
    Box, 
    CircularProgress, 
    Typography, 
    Paper, 
    Button, 
    Grid2, 
    TextField 
} from "@mui/material";
import RefreshIcon from '@mui/icons-material/Refresh';
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import AirQualityLevelsTable from "./AirQualityLevels";
import PmInformation from "./PmInformation";


const CurrentAirQualityIndicator = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [data, setData] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);

    const [pm25Data, setPm25Data] = useState(null);
    const [pm25Loading, setPm25Loading] = useState(false);
    const [pm25Error, setPm25Error] = useState(null);

    const [lon, setLon] = useState('');
    const [lat, setLat] = useState('');

    useEffect(() => {
        fetchData();
    }, []);
    
    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getCurrentAirQualityPM25Indicator();
            setData(result);
            setLastUpdated(new Date().toLocaleString());
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const fetchPM25Averages = async () => {
        setPm25Loading(true);
        setPm25Error(null);
        try {
            const result = await postCurrentAirQualityPM25Indicator(parseFloat(lon), parseFloat(lat));
            if (typeof result !== 'string') {
                setData(result);
                setPm25Data(false);
            } else {
                setPm25Data(result);
            }
        } catch (err) {
            setPm25Error(err.message);
        } finally {
            setPm25Loading(false);
        }
    };

    return (
        <div>
            <Box sx={{ padding: '10px' }}></Box> 
            <Box sx={{ 
                border: '2px solid gray', 
                padding: '20px', 
                borderRadius: '20px', 
                width: '50%', 
                mx: 'auto', 
                minWidth: '990px', 
                boxShadow: 1 }}
                >
                    <Box sx={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        alignItems: 'center' 
                        }}
                        >
                            <Typography variant="h6">
                                Current Air Quality - PM2.5 Indicator (Daily/Weekly vs Yearly Averages)
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                <Button variant="contained" color="primary" sx={{ height: '50px' }} startIcon={<RefreshIcon />} onClick={fetchData}>Reload Hamburg Data</Button>
                            </Box>
                    </Box>

                    {/* Form for posting Air Quality Indicator */}
                    <Box sx={{ 
                        marginTop: '20px', 
                        padding: '20px', 
                        border: '1px solid gray', 
                        borderRadius: '10px', 
                        backgroundColor: '#f9f9f9' 
                        }}
                    >
                        <Typography variant="h6" sx={{ textAlign: 'center' }}>
                            Get Real-Time PM2.5 Air Quality Data for Your Location
                        </Typography>
                        <Typography variant="body2" color="textSecondary" sx={{ marginBottom: '10px', textAlign: 'center' }}>
                            * Longitude (Lon) and Latitude (Lat) are required.
                        </Typography>
                        <Grid2 container spacing={2} sx={{ marginTop: '16px' }} justifyContent="center">
                            <Grid2 item xs={12} sm={6} md={4}>
                                <TextField
                                label="Longitude (Lon)"
                                type="number"
                                value={lon}
                                onChange={(e) => setLon(e.target.value)}
                                fullWidth
                                variant="outlined"
                                />
                            </Grid2>
                            <Grid2 item xs={12} sm={6} md={4}>
                                <TextField
                                label="Latitude (Lat)"
                                type="number"
                                value={lat}
                                onChange={(e) => setLat(e.target.value)}
                                fullWidth
                                variant="outlined"
                                />
                            </Grid2>
                            <Grid2 item xs={12} sm={6} md={4}>
                                <Button
                                variant="contained"
                                color="primary"
                                onClick={fetchPM25Averages}
                                fullWidth
                                sx={{ height: '56px', width: '220px' }}
                                >
                                    Submit
                                </Button>
                            </Grid2>
                        </Grid2>

                        {pm25Loading && <CircularProgress sx={{ marginTop: '10px' }} />}
                        {pm25Error && <Typography color="error">{pm25Error}</Typography>}
                        {pm25Data && (
                            <Box sx={{ 
                                marginTop: '10px', 
                                padding: '10px', 
                                backgroundColor: '#f8d7da', 
                                borderRadius: '10px' 
                                }}
                            >
                                <Typography variant="h6">Error:</Typography>
                                <Typography variant="body1">{JSON.stringify(pm25Data, null, 2)}</Typography>
                            </Box>
                        )}
                    </Box>

                    {/* Existing Air Quality Indicator display */}
                    {loading && <CircularProgress sx={{ marginTop: '20px' }} />}
                    {error && <Typography color="error">{error}</Typography>}
                    {data && (
                        <Grid2 container spacing={2} sx={{ 
                            marginTop: '20px', 
                            display: 'flex', 
                            justifyContent: 'center', 
                            backgroundColor: '#f9f9f9', 
                            padding: '20px', 
                            borderRadius: '10px'
                            }}
                        >
                            {data.map((row, index) => {
                                const percentageChange = row['Air_quality_indicator_yearly_comparison'] === 0 ? 0 : row['Air_quality_indicator_yearly_comparison'] - 100;
                                return (
                                    <Grid2 item xs={4} key={index} sx={{ 
                                        display: 'flex', 
                                        justifyContent: index === 2 ? 'flex-end' : index === 1 ? 'center' : 'flex-start' 
                                        }}
                                    >
                                        <Paper sx={{ 
                                            padding: '20px', 
                                            borderRadius: '50px', 
                                            width: '250px',
                                            textAlign: "center",
                                            boxShadow: 1,
                                            backgroundColor: row['Air_quality_indicator_yearly_comparison'] === 0 ? '#ffffff' :
                                                            row['Air_quality_indicator_yearly_comparison'] > 100 ? '#ffcccc' : '#e0f7fa'
                                            }}
                                        >
                                            <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                                                {index === 0 ? 'Day' : index === 1 ? 'Week' : 'Year'}
                                            </Typography>
                                            <Typography variant="h4" sx={{ fontWeight: 'bold', marginTop: '10px' }}>
                                                {row['Average_PM2.5'].toFixed(2)}
                                            </Typography>
                                            {index !== 2 && (
                                                <Typography variant="body2" sx={{ marginTop: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                                    {row['Air_quality_indicator_yearly_comparison'].toFixed(2)}% 
                                                    {percentageChange > 0 ? <ArrowUpwardIcon color="error" sx={{ marginLeft: '5px' }} /> : <ArrowDownwardIcon color="success" sx={{ marginLeft: '5px' }} />}
                                                </Typography>
                                            )}
                                        </Paper>
                                    </Grid2>
                                );
                            })}
                        </Grid2>
                    )}

                <Typography variant="body2" color="textSecondary" sx={{ textAlign: 'center' }}>
                    Last Updated: {lastUpdated || 'Fetching...'}
                </Typography>

                {/* Pollutant Info Section */}
                <Box sx={{ marginTop: '5px' }}>
                    <Grid2 container spacing={2}>
                        <Grid2 item xs={12} sm={6}>
                            <PmInformation pollutant="pm25" />
                        </Grid2>
                    </Grid2>
                </Box>

                {/* Air Quality Levels Table Section */}
                <Box sx={{ marginTop: '1px' }}>
                    <AirQualityLevelsTable /> 
                </Box>
            </Box>
        </div>
    )
};

export default CurrentAirQualityIndicator;