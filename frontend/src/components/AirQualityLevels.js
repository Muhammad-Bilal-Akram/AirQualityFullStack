import React from 'react';
import { 
    Box, 
    Typography, 
    Table, 
    TableHead, 
    TableBody, 
    TableRow, 
    TableCell 
} from '@mui/material';


const AirQualityLevelsTable = () => {
    const levels = [
        { range: '0 - 50', level: 'Good' },
        { range: '51 - 100', level: 'Moderate' },
        { range: '101 - 150', level: 'Unhealthy for Sensitive Groups' },
        { range: '151 - 200', level: 'Unhealthy' },
        { range: '201 - 300', level: 'Very Unhealthy' },
        { range: '301 and higher', level: 'Hazardous' },
    ];
  
    return (
        <Box sx={{ 
            padding: 2, 
            border: '1px solid #ccc', 
            borderRadius: 2, 
            boxShadow: 1 
            }}>
            <Typography variant="h5" component="h2" sx={{ fontWeight: 'bold', marginBottom: 2 }}>
                Air Quality Levels
            </Typography>
            
            <Table sx={{ width: '100%' }}>
                <TableHead>
                    <TableRow>
                        <TableCell sx={{ fontWeight: 'bold' }}>AQI Range</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>Level of Health Concern</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {levels.map(({ range, level }, index) => (
                        <TableRow key={index}>
                            <TableCell>{range}</TableCell>
                            <TableCell>{level}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </Box>
    );
};


export default AirQualityLevelsTable;