import { AppBar, Toolbar, Typography, styled } from '@mui/material'
import React from 'react'
import SatelliteAltIcon from '@mui/icons-material/SatelliteAlt';


const StyledToolBar = styled(Toolbar)({
    display: "flex",
    justifyContent: "space-between",
    backgroundColor: 'primary',
})

const NavBar = () => {
  return (
    <AppBar position='sticky'>
      <StyledToolBar sx={{minWidth: "1350px"}}>
        <Typography 
        variant='h6' 
        sx={{
          display: "flex",
          alignItems: "center",
          width: "30%",
          gap: 2,
          }}
          >
            <SatelliteAltIcon />
            Hamburg Air Quality DashBoard
        </Typography>
      </StyledToolBar>
    </AppBar>
  )
};

export default NavBar
