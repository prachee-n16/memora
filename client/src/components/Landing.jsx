import React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";

const Landing = () => {
  return (
    <Box
      sx={{
        m: "10vh",
        height: "70vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Typography variant="h1" sx={{ textAlign: "center", fontWeight: "bold" }}>
        where every <br /> memory matters!
      </Typography>
      <Typography variant="h5" sx={{ mt: 2 }}>
        Designed with compassion and care to empower Alzheimer's Patients and
        their Caregivers
      </Typography>
      <Stack direction="row" spacing={4} sx={{ mt: 4 }}>
        <Button
          variant="contained"
          sx={{ mt: 4, bgcolor: "#9569ec", textTransform: "none" }}
        >
          Get Started
        </Button>
        <Button
          variant="contained"
          sx={{
            mt: 4,
            bgcolor: "#FFFFFF",
            color: "black",
            textTransform: "none",
          }}
        >
          Demo?
        </Button>
      </Stack>
    </Box>
  );
};

export default Landing;
