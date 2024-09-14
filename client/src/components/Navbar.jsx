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
        position="static"
        sx={{ bgcolor: "white", color: "black" }}
        elevation={0}
      >
        <Toolbar>
          <Stack direction="row" spacing={3} sx={{ flexGrow: 1 }}>
            <Typography variant="h6">Discover</Typography>
            <Typography variant="h6">Features</Typography>
            <Typography variant="h6">Pricing</Typography>
            <Typography variant="h6">About</Typography>
          </Stack>
          <Typography variant="h6" sx={{ flexGrow: 1, textAlign: "center" }}>
            {APP_NAME}
          </Typography>
          <Stack
            spacing={2}
            direction="row"
            sx={{ justifyContent: "end", alignItems: "center", flexGrow: 2 }}
          >
            <Button variant={"outlined"} mx="5" color="inherit">
              Demo
            </Button>
            {/* <Button
              variant={"contained"}
              color="inherit"
              sx={{ bgcolor: "black", color: "white" }}
            >
              Login
            </Button> */}
            <SignedIn>
              <UserButton afterSignOutUrl="/sign-in" />
            </SignedIn>
            <SignedOut>
              <Button
                variant="contained"
                color="inherit"
                sx={{ bgcolor: "black", color: "white" }}
                component={Link} // Pass the Link component directly
                to="/sign-in"
              >
                Sign in
              </Button>
            </SignedOut>
          </Stack>
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Navbar;
