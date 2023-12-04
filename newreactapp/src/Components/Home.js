import React, { useState, useEffect, useRef } from 'react';
import L from 'leaflet';
import ReactDOMServer from 'react-dom/server';
import 'leaflet/dist/leaflet.css';
import 'leaflet/dist/images/marker-icon.png';
import 'leaflet/dist/images/marker-shadow.png';
import {
  Container,
  Typography,
  AppBar,
  Toolbar,
  InputBase,
  Button,
  Card,
  CardContent,
  CardMedia,
  List,
  ListItem,
  Pagination,
  IconButton,
  Grid,
  ToggleButton,
  ToggleButtonGroup,
  Skeleton
} from '@mui/material';
import { styled, alpha } from '@mui/material/styles';
import SearchIcon from '@mui/icons-material/Search';
import ViewListIcon from '@mui/icons-material/ViewList';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import ViewModuleIcon from '@mui/icons-material/ViewModule';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import Rating from '@mui/material/Rating'


const SearchResult = ({ property, isGrid}) => {

    if (isGrid) {
      return (
        <Grid item xs={12} sm={6} md={4}>
          <Card sx={{ height: 405 }}>
            <CardMedia component="img" height="140" image={property.photo} alt={property.name} />
            <CardContent>
              <Typography variant="h6" sx={{ overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical', maxWidth: '100%' }}>{property.name}</Typography>
              <Typography variant="body1" sx={{color:'gray', fontSize: '16px'}}>{property.subtext}</Typography>
              <Typography variant="subtitle1" sx={{fontSize: '14px'}}> {'\u2605'} {property.starRating} • {property.price} per night</Typography>
              <br />
              <Typography variant="body2" sx={{ overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', maxWidth: '100%' }}>{property.description}</Typography>
              <br />
              <Typography variant="subtitle2" sx={{ color: 'gray', fontWeight: 'normal'}}>📍 {property.location}</Typography>
              <br />
              <Button disableElevation variant="outlined" href={property.link} target="_blank" rel="noopener noreferrer" style={{
                        borderRadius: 5,
                        borderColor: "#FF5A5F",
                        color: "#FF5A5F",
                        fontSize: "12px",
                        top: '4px',
                        marginLeft: '0px',
                        minWidth: '20px',
                        alignItems: 'center'}}>                View Listing
              </Button>
            </CardContent>
          </Card>
        </Grid>
      );
    } else {
      return (
        <ListItem minWidth='100%' sx={{paddingRight:0, marginRight:0, marginLeft:0, paddingLeft:0, paddingTop:2}}>
            <Card sx={{ display: 'flex', width:'100%', marginLeft: 0, marginRight:0}}>
                <CardMedia sx={{ width: 300 }} component="img" image={property.photo} alt={property.name} />
                <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                <CardContent>
                <Typography variant="h6" sx={{ overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 1, WebkitBoxOrient: 'vertical', maxWidth: '100%' }}>{property.name}</Typography>
                    <Typography variant="body1" sx={{color:'gray'}}>{property.subtext}</Typography>
                    <Typography variant="subtitle1" sx={{fontSize: '14px'}}> {'\u2605'} {property.starRating} • {property.price} per night</Typography>
                    <br />
                    <Typography variant="body2" sx={{ overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 4, WebkitBoxOrient: 'vertical', maxWidth: '100%' }}>{property.description}</Typography>
                    <br />
                    <Typography variant="subtitle2" sx={{ color: 'gray', fontWeight: 'normal'}}> 📍 {property.location}</Typography>
                    <br />
                    <Button disableElevation variant="outlined" href={property.link} target="_blank" rel="noopener noreferrer" style={{
                        borderRadius: 5,
                        borderColor: "#FF5A5F",
                        color: "#FF5A5F",
                        fontSize: "12px",
                        top: '4px',
                        marginLeft: '0px',
                        minWidth: '20px',
                        alignItems: 'center'}}>  
                        View Listing
                    </Button>
                </CardContent>
                </Box>
            </Card>
        </ListItem>
      );
    }
  };

const MapView = ({ searchResults }) => {
  const mapRef = useRef(null);

  useEffect(() => {

    delete L.Icon.Default.prototype._getIconUrl;

    L.Icon.Default.mergeOptions({
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png')
    });

    // Check if map is already initialized
    if (!mapRef.current) {

      const bounds = L.latLngBounds(searchResults.map(result => [result.lat, result.long]));

      // Create a Leaflet map
      // const map = L.map('map').setView([37.7749, -122.4194], 13);
      const map = L.map('map').fitBounds(bounds);

      // Add a Tile Layer (you may need to replace the URL with your own)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
      }).addTo(map);

      // Save the map instance to the ref
      mapRef.current = map;

      // Add Markers to the map based on the searchResults data
        searchResults.forEach((result) => {
          const popupContent = (
            <div>
              <h3>{result.name}</h3>
              <Typography variant="subtitle1" sx={{fontSize: '14px'}}> {'\u2605'} {result.starRating} • {result.price} per night</Typography><img src={result.photo} alt={result.name} style={{ maxWidth: '100%', height: 'auto' }} />
              <p>
                <Button
                  disableElevation
                  variant="outlined"
                  href={result.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    borderRadius: 5,
                    borderColor: '#FF5A5F',
                    color: '#FF5A5F',
                    fontSize: '12px',
                    top: '4px',
                    marginLeft: '0px',
                    width: '100%',
                    alignItems: 'center',
                  }}
                >
                  View Listing
                </Button>
              </p>
            </div>
          );
  
          // Convert the React component to HTML string
          const popupHtml = ReactDOMServer.renderToString(popupContent);
  
        L.marker([result.lat, result.long])
          .addTo(map)
          .bindPopup(popupHtml);
      });
    }
  }, [searchResults]); // Empty dependency array ensures the useEffect runs only once

  return <div id="map" style={{ height: '650px', marginTop: '20px' }} />;
};

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [viewType, setViewType] = useState('grid');
  const [loading, setLoading] = useState(false);
  const [searchOn, setSearchOn] = useState(false);


  const handleViewTypeChange = (event, newViewType) => {
    setViewType(newViewType);
  };
  const fetchData = async () => {

    const encodedQuery = encodeURIComponent(query);
    const apiUrl = `https://xe77lom6bg.execute-api.us-east-2.amazonaws.com/demo?query=${encodedQuery}`;

    // const apiUrl = 'https://xe77lom6bg.execute-api.us-east-2.amazonaws.com/demo?query=house+long+beach';
  
    try {
        setLoading(true);
        const response = await fetch(apiUrl);

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
    
        const data = await response.json();

        setSearchResults(data)
        setSearchOn(true)

      } catch (error) {
        console.error('Error fetching data:', error.message);
        return null;
      } finally {
        setLoading(false);
      }
  }

  return (
    <div>
        <AppBar elevation={0} position="sticky" style={{backgroundColor: 'white', width: '100%', height: '75px', borderBottom: '1px solid lightgray'}}>
            <Container maxWidth="lg">
            <Toolbar disableGutters sx={{ display: 'flex', width:'100%', maxWidth: '800px'}}>
                <Box display='flex' sx={{marginTop: '10px'}}>
                    <Typography variant="h6" >
                        <img src="https://www.edigitalagency.com.au/wp-content/uploads/airbnb-logo-png-transparent-background.png" alt="Airbnb Logo" style={{ maxWidth: '100px'}} />
                    </Typography>
                </Box>
                <Box sx={{border: '1px solid lightgray', height:'45px',  borderRadius: '42px', marginLeft: '60px'}}>
                    <InputBase
                    placeholder="Search for experiences"
                    inputProps={{ 'aria-label': 'search'}}
                    sx={{ width: '450px', marginLeft: '18px',variant:'filled', top: '5px'}}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    
                    />
                    <Button disableElevation variant="contained" startIcon={<SearchIcon />} onClick={fetchData} style={{
                        borderRadius: 40,
                        backgroundColor: "#FF5A5F",
                        fontSize: "12px",
                        top: '4px',
                        marginRight: '6px',
                        minWidth: '20px',
                        alignItems: 'center'}}>
                        Search
                    </Button>
                </Box>


        </Toolbar>
        </Container>
      </AppBar>

    <Container>
    
      
    {searchOn && (
        <Box display='flex' sx={{height: '70px', width: '100%', marginRight: 0}}>
    
        <Typography variant="body1" sx={{color:'gray', fontSize: '22px', fontWeight: 'normal', marginTop: 2.5}}>Top search results</Typography>
        <ToggleButtonGroup
        value={viewType}
        exclusive
        onChange={handleViewTypeChange}
        sx={{marginTop: 3, marginLeft: 103, marginRight: 0}}
      >
        <ToggleButton value="grid">
          <ViewModuleIcon />
        </ToggleButton>
        <ToggleButton value="list">
          <ViewListIcon />
        </ToggleButton>
        <ToggleButton value="map">
          <LocationOnIcon />
        </ToggleButton>
      </ToggleButtonGroup>
    </Box>
    )}
    {loading && (
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <CircularProgress />
          <Typography variant="body1" style={{ marginTop: '10px' }}>
            Loading...
          </Typography>
        </div>
      )}
    
      {viewType === 'grid' ? (
        <Grid container spacing={3} sx={{ marginTop: 0 }}>
          {searchResults.map((property, index) => (
            <SearchResult key={index} property={property} isGrid={true} />
          ))}
        </Grid>
      ) : viewType === 'list' ? (
        <List sx={{ marginTop: 0 }}>
          {searchResults.map((property, index) => (
            <SearchResult key={index} property={property} isGrid={false}/>
          ))}
        </List>
        
      ) : (
        <MapView searchResults={searchResults}/>
        )
      }
</Container>
</div>
      
    
  );
};

export default SearchPage;
