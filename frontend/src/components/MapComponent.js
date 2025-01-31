import React, { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import axios from "axios";
import { Box, Typography, TextField, Button } from "@mui/material";
import { getPM25Map, postPM25Map } from "../services/pmMapService"; 
import { getHamburgMap } from '../services/hamburgMapService';
import 'mapbox-gl/dist/mapbox-gl.css';
import RefreshIcon from '@mui/icons-material/Refresh'; 


const MapComponent = () => {
    const mapContainerRef = useRef(null);
    const [map, setMap] = useState(null);
    const [popup, setPopup] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [startDate, setStartDate] = useState('2025-01-01');
    const [endDate, setEndDate] = useState('2025-01-01');
    const [pm25Data, setPm25Data] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!mapContainerRef.current) return;

    mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_ACCESS_TOKEN;

    const mapInstance = new mapboxgl.Map({
        container: mapContainerRef.current,
        style: 'mapbox://styles/mapbox/light-v10',
        center: [10.0, 53.55], // Hamburg
        zoom: 12,
    });
    setMap(mapInstance);

    return () => mapInstance.remove();
    }, []);

    useEffect(() => {
        if (!map) return;

    map.on('load', async () => {
        try {
            const hamburgData = await getHamburgMap();
            map.addSource('hamburg-source', { type: 'geojson', data: hamburgData });
            map.addLayer({
                id: 'hamburg-layer',
                type: 'line',
                source: 'hamburg-source',
                paint: { 'line-color': '#000', 'line-width': 2 },
            });

        const pm25Data = await getPM25Map();
        map.addSource('pm25-source', { type: 'geojson', data: pm25Data });
        map.addLayer({
            id: 'heatmap-layer',
            type: 'heatmap',
            source: 'pm25-source',
            maxzoom: 15,
            paint: {
                'heatmap-weight': ['interpolate', ['linear'], ['get', 'PM2.5'], 0, 0, 50, 1],
                'heatmap-intensity': ['interpolate', ['linear'], ['zoom'], 0, 0.5, 10, 1, 15, 3],
                'heatmap-color': [
                'interpolate',
                ['linear'],
                ['heatmap-density'],
                0, 'rgba(33,102,172,0)',
                0.2, 'rgb(103,169,207)',
                0.4, 'rgb(209,229,240)',
                0.6, 'rgb(253,219,199)',
                0.8, 'rgb(239,138,98)',
                1, 'rgb(178,24,43)'
                ],
                'heatmap-radius': ['interpolate', ['linear'], ['zoom'], 0, 2, 10, 20, 15, 40],
                'heatmap-opacity': ['interpolate', ['linear'], ['zoom'], 0, 0.6, 10, 0.8, 15, 0.9],
            },
        });

        map.on('click', (event) => {
            const features = map.queryRenderedFeatures(event.point, { layers: ['heatmap-layer'] });
            if (!features || features.length === 0) return;

            const feature = features[0];
            const coordinates = feature.geometry.coordinates;
            const pmValue = parseFloat(feature.properties['PM2.5']).toFixed(2);
            const longitude = parseFloat(coordinates[0]).toFixed(2);
            const latitude = parseFloat(coordinates[1]).toFixed(2);

            if (popup) {
                popup.remove();
            }

            const newPopup = new mapboxgl.Popup()
                .setLngLat(coordinates)
                .setHTML(`
                <strong>PM2.5 Level:</strong> ${pmValue} <br/>
                <strong>Longitude (X):</strong> ${longitude} <br/>
                <strong>Latitude (Y):</strong> ${latitude}
                `)
                .addTo(map);
            setPopup(newPopup);
        });

        map.on('mouseenter', 'heatmap-layer', () => {
            map.getCanvas().style.cursor = 'pointer';
        });

        map.on('mouseleave', 'heatmap-layer', () => {
            map.getCanvas().style.cursor = '';
        });
        } catch (error) {
            console.error('Error loading map data:', error);
        }
        });
    }, [map]);


    const handleSearch = async (query) => {
        if (!query) {
        setSearchResults([]);
        return;
    }

    try {
        const response = await axios.get(
            `https://api.mapbox.com/geocoding/v5/mapbox.places/${query}.json?proximity=10.0,53.55&bbox=9.7,53.4,10.3,53.7&limit=5&access_token=${mapboxgl.accessToken}`
        );
        setSearchResults(response.data.features);
    } catch (error) {
        console.error('Error fetching search results:', error);
    }
    };


    const handleSelectLocation = (coordinates) => {
        if (map) {
        map.flyTo({ center: coordinates, zoom: 14 });
        }
        setSearchQuery('');
        setSearchResults([]);
    };


    const handlePostPM25Data = async () => {
        setLoading(true); 

    try {
        const newData = await postPM25Map(startDate, endDate); 
        setPm25Data(newData); 
  
        if (map && map.getSource('pm25-source')) {
            map.getSource('pm25-source').setData(newData);
        }
    } catch (error) {
        console.error('Error updating PM2.5 data:', error);
    } finally {
        setLoading(false);
    }
    };

    return (
    <Box sx={{
        border: '2px solid gray',
        padding: '20px',
        borderRadius: '20px',
        width: '90%',
        mx: 'auto',
        minWidth: '990px',
        boxShadow: 2,
        marginTop: '2px',
        backgroundColor: '#f9f9f9',
        position: 'relative',
        marginBottom: '50px'
    }}
    >
        <Typography variant="h6" sx={{ marginBottom: '20px', textAlign: 'center', fontWeight: 'bold' }}>
            Explore PM2.5 Heatmap: Search Locations, View PM25 Values, and Filter Data by Date Range
        </Typography>
  
        <Box sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            gap: 2,
            flexWrap: 'wrap',
            mb: 3,
            position: 'relative',
        }}
        >

        <Box sx={{ position: 'relative', width: '30%' }}>
            <TextField
                variant="outlined"
                label="Search location in Hamburg..."
                value={searchQuery}
                onChange={(e) => {
                    setSearchQuery(e.target.value);
                    handleSearch(e.target.value);
                }}
                sx={{ width: '100%' }}
            />
  

            {searchResults.length > 0 && (
            <Box sx={{
                position: 'absolute',
                top: '100%',
                left: 0,
                width: '100%',
                background: 'white',
                borderRadius: '8px',
                boxShadow: 3,
                zIndex: 10,
                maxHeight: '200px',
                overflowY: 'auto',
            }}
            >
                {searchResults.map((result) => (
                <Typography
                    key={result.id}
                    sx={{
                        padding: '12px',
                        cursor: 'pointer',
                        '&:hover': { background: '#f0f0f0' },
                        transition: 'background 0.3s ease',
                    }}
                    onClick={() => handleSelectLocation(result.center)}
                >
                    {result.place_name}
                </Typography>
              ))}
            </Box>
          )}
        </Box>
  
        <TextField
            variant="outlined"
            label="Start Date"
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            sx={{ width: '18%' }}
        />
  
        <TextField
            variant="outlined"
            label="End Date"
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            sx={{ width: '18%' }}
        />
  
        <Button
          variant="contained"
          onClick={handlePostPM25Data}
          sx={{
            backgroundColor: '#1976d2',
            color: 'white',
            fontWeight: 'bold',
            padding: '10px 20px',
            borderRadius: '8px',
            width: '20%',
            height: '56px',
            '&:hover': { backgroundColor: '#115293' },
            position: 'relative',
            }}
            disabled={loading} 
        >
            {loading ? (
            <RefreshIcon sx={{ animation: 'spin 2s linear infinite', mr: 2 }} />
            ) : (
                'Update PM2.5 HeatMap'
            )}
            {loading && 'Updating...'}
        </Button>
    </Box>
  

    <Box
        ref={mapContainerRef}
        sx={{
        width: '100%',
        height: '500px',
        mt: 3,
        borderRadius: '10px',
        overflow: 'hidden',
        boxShadow: 2,
        }}
    />
    </Box>
  );
};


export default MapComponent;

