import React from 'react';
import { Box, Typography } from '@mui/material';

const PmInformation = ({ pollutant }) => {
    const pm25Description = {
        pm25: 'PM2.5 refers to fine particulate matter in the air that is less than 2.5 micrometers in diameter. These tiny particles are so small that they can easily be inhaled into the lungs and even enter the bloodstream. PM2.5 is often the result of combustion processes, such as vehicle emissions, industrial activities, and the burning of fossil fuels like coal and oil. It can also be produced by natural sources such as wildfires and volcanic activity. Due to their minuscule size, PM2.5 particles can travel deep into the respiratory system, causing serious health issues like asthma, bronchitis, heart disease, and even premature death. Long-term exposure to high levels of PM2.5 can significantly reduce air quality and have harmful effects on both human health and the environment, contributing to haze, reduced visibility, and the formation of smog. Reducing PM2.5 levels is essential for improving public health and mitigating the harmful impacts of air pollution.'
    };

    const description = pm25Description[pollutant] || 'No information available for the pollutant.';

    return (
        <Box sx={{
            marginBottom: 4,
            padding: 2,
            border: '1px solid #ccc',
            borderRadius: 2,
            boxShadow: 1
        }}>
            <Typography variant='body1' sx={{
                marginTop: 2,
                textAlign: 'justify'
            }}
            >
                {description}
            </Typography>
        </Box>
    );
};

export default PmInformation;