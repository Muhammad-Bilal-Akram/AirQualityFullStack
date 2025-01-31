import React, { useState, useEffect } from 'react';
import { getPM25Averages, postPM25Averages } from '../services/averagesService';
import {
    Button,
    TextField,
    Typography,
    Box,
    CircularProgress,
    Table,
    TableHead,
    TableBody,
    TableRow,
    TableCell,
    Grid2,
} from '@mui/material';


const AverageAirQuality = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [data, setData] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);
  
    const [pm25Data, setPm25Data] = useState(null);
    const [pm25Loading, setPm25Loading] = useState(false);
    const [pm25Error, setPm25Error] = useState(null);
  
    const [x, setX] = useState('');
    const [y, setY] = useState('');
    const [week, setWeek] = useState('');
    const [month, setMonth] = useState('');
    const [year, setYear] = useState('');

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await getPM25Averages();
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
            const result = await postPM25Averages(
                parseFloat(x),
                parseFloat(y),
                parseInt(week),
                parseInt(month),
                parseInt(year)
            );
    
            if (typeof result !== 'string') {
                setData(result);
                setPm25Data(null);
            } else {
                setPm25Data(result);
            }
        } catch (err) {
            setPm25Data(err.message);
        } finally {
            setPm25Loading(false);
        }
    };

    return (
        <Box sx={{ padding: '20px' }}>
            <Box sx={{
                border: '2px solid gray',
                padding: '20px',
                borderRadius: '20px',
                width: '50%',
                mx: 'auto',
                minWidth: '990px',
                boxShadow: 2,
                backgroundColor: '#fff',
            }}
            >
                <Typography variant="h6" align="center" gutterBottom>
                    PM2.5 Averages: Weekly, Monthly, Yearly
                </Typography>

                <Box sx={{
                    marginTop: '20px',
                    padding: '20px',
                    border: '1px solid gray',
                    borderRadius: '10px',
                    backgroundColor: '#f9f9f9',
                }}
                >
                    <Typography variant="h6" align="center" gutterBottom>
                        Track PM2.5 Levels for Your Location by Week, Month, and Year
                    </Typography>
                    <Typography variant="body2" color="textSecondary" align="center" sx={{ marginBottom: '10px' }}>
                        * Year, Month, and Week are required fields.
                    </Typography>

                    <Grid2 container spacing={2} alignItems="center" justifyContent="center">
                        {[
                            { label: 'Year *', value: year, setter: setYear },
                            { label: 'Week *', value: week, setter: setWeek },
                            { label: 'Month *', value: month, setter: setMonth },
                            { label: 'Point X', value: x, setter: setX },
                            { label: 'Point Y', value: y, setter: setY },
                        ].map((field, index) => (
                        <Grid2 item key={index}>
                            <TextField
                                label={field.label}
                                type="number"
                                value={field.value}
                                onChange={(e) => field.setter(e.target.value)}
                                margin="normal"
                                sx={{ width: '140px' }}
                            />
                        </Grid2>
                        ))}
                        <Grid2 item>
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={fetchPM25Averages}
                                sx={{ height: '56px', marginTop: '8px' }}
                            >
                                Submit
                            </Button>
                        </Grid2>
                    </Grid2>

                    {pm25Loading && <CircularProgress sx={{ marginTop: '10px', display: 'block', mx: 'auto' }} />}
                    {pm25Error && <Typography color="error">{pm25Error}</Typography>}
                    {pm25Data && (
                        <Box sx={{
                            marginTop: '10px',
                            padding: '10px',
                            backgroundColor: '#f8d7da',
                            borderRadius: '10px',
                        }}
                        >
                            <Typography variant="h6">
                                Error:
                            </Typography>
                            <Typography variant="body1">{JSON.stringify(pm25Data, null, 2)}</Typography>
                        
                        </Box>
                    )}
                </Box>

                {loading && <CircularProgress sx={{ marginTop: '20px', display: 'block', mx: 'auto' }} />}
                {error && <Typography color="error">{error}</Typography>}

                {!loading && !error && data && (
                    <Box sx={{
                        marginTop: '20px',
                        padding: '20px',
                        borderRadius: '10px',
                        backgroundColor: '#f9f9f9',
                        }}
                    >
                        <Typography variant="h6" align="center">
                            PM2.5 Averages
                        </Typography>

                        <Table sx={{ width: '100%', mt: 2, border: '1px solid gray' }}>
                            <TableHead>
                                <TableRow>
                                    <TableCell>
                                        <strong>Week/Month/Year</strong>
                                    </TableCell>
                                    <TableCell>
                                        <strong>Average PM2.5</strong>
                                    </TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {data.map((row, index) => (
                                    <TableRow key={index}>
                                        <TableCell>{row.Average_week_month_year}</TableCell>
                                        <TableCell>{row.Average_PM2.toFixed(2)}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </Box>
                )}

                {lastUpdated && (
                    <Box sx={{ marginTop: '10px' }}>
                        <Typography variant="body2" color="textSecondary" align="center">
                            Last Updated: {lastUpdated}
                        </Typography>
                    </Box>
                )}
            </Box>
        </Box>
    );
};


export default AverageAirQuality;