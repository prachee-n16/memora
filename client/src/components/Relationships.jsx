import React, { useEffect, useState } from "react";
import {
  Box,
  Toolbar,
  Button,
  Typography,
  Grid,
  Avatar,
  CardHeader,
  Divider,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from "@mui/material";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import EditRoundedIcon from "@mui/icons-material/EditRounded";
import RefreshRoundedIcon from "@mui/icons-material/RefreshRounded";
import axios from "axios";

const fetchUserPeople = async (userId) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/get_user_people/${userId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching user people:", error);
    throw error;
  }
};

const Relationships = () => {
  const [peopleData, setPeopleData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);
  const [currentPerson, setCurrentPerson] = useState(null);

  const updatePeopleData = () => {
    setLoading(true);
    fetchUserPeople(273) // Replace with actual user ID
      .then(data => {
        console.log(data);
        setPeopleData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  };

  useEffect(() => {
    updatePeopleData();
  }, []);

  const handleOpen = (person) => {
    setCurrentPerson(person);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setCurrentPerson(null);
  };

  const handleChange = (field, value) => {
    setCurrentPerson({ ...currentPerson, [field]: value });
  };

  const handleSave = () => {
    // Here you would typically send an API request to update the person
    // For now, we'll just update the local state
    const updatedData = peopleData.map(person => 
      person.person_id === currentPerson.person_id ? currentPerson : person
    );
    setPeopleData(updatedData);
    handleClose();
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading relationships: {error.message}</div>;

  return (
    <Box component="main" sx={{ flexGrow: 1, mr: "240px" }}>
      <Toolbar />
      <Button
        variant="outlined"
        sx={{
          position: "absolute",
          top: "70px",
          right: "0px",
          mt: 4,
          p: 4,
          mx: 4,
          borderColor: "#9c9998",
          borderWidth: "2px",
          color: "#9c9998",
          fontWeight: "bold",
          textTransform: "none",
          width: "10px",
          height: "10px",
        }}
        disableElevation
        onClick={updatePeopleData}
        size="medium"
      >
        <RefreshRoundedIcon />
      </Button>
      <Grid container spacing={4}>
        {peopleData.map((person) => (
          <Grid item xs={12} key={person.person_id}>
            <Card variant="outlined">
              <CardHeader
                avatar={
                  <Avatar
                    alt={person.name}
                    src={person.picture ? `data:image/jpeg;base64,${person.picture}` : undefined}
                  />
                }
                action={
                  <IconButton
                    aria-label="edit"
                    onClick={() => handleOpen(person)}
                  >
                    <EditRoundedIcon />
                  </IconButton>
                }
                title={person.name}
                titleTypographyProps={{ variant: "h4", component: "div" }}
                subheader={person.relationship}
                subheaderTypographyProps={{
                  variant: "subtitle1",
                  color: "text.secondary",
                }}
                sx={{ paddingBottom: 0 }}
              />
              <CardContent>
                <Divider />
                <Typography variant="body2" sx={{ mt: 2 }}>
                  {person.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Edit Person</DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Name"
            fullWidth
            value={currentPerson?.name || ""}
            onChange={(e) => handleChange("name", e.target.value)}
          />
          <TextField
            margin="dense"
            label="Relationship"
            fullWidth
            value={currentPerson?.relationship || ""}
            onChange={(e) => handleChange("relationship", e.target.value)}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={4}
            value={currentPerson?.description || ""}
            onChange={(e) => handleChange("description", e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSave} color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Relationships;