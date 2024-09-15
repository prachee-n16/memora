import React from "react";
import APP_NAME from "../config";

import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import { Link } from "react-router-dom";

import { SignedIn, SignedOut, UserButton } from "@clerk/clerk-react";

const Navbar = () => {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar
        position="fixed"
        sx={{
          bgcolor: "#fdfcf6",
          color: "black",
          width: "100%",
          zIndex: (theme) => theme.zIndex.drawer + 1, // Ensure Navbar is above Sidebar
        }}
        elevation={1}
      >
        <Toolbar>
          <Typography
            variant="h6"
            sx={{
              fontFamily: "Berkshire Swash",
              fontSize: "xx-large",
              fontWeight: "bold",
              marginLeft: "70px",
            }}
          >
            memora
          </Typography>
          <Stack
            spacing={2}
            direction="row"
            sx={{ justifyContent: "end", alignItems: "center", flexGrow: 2 }}
          >
            <SignedIn>
              <UserButton afterSignOutUrl="/sign-in" />
            </SignedIn>
            <SignedOut>
              <Button
                variant="contained"
                color="inherit"
                sx={{
                  bgcolor: "#ce5c29",
                  // color: "white",
                  textTransform: "none",
                  fontWeight: "bold",
                }}
                component={Link} // Pass the Link component directly
                to="/sign-in"
              >
                SIGN IN
              </Button>
            </SignedOut>
          </Stack>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Navbar;
