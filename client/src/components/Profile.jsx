import React from "react";
import {
  CardHeader,
  Box,
  Toolbar,
  Typography,
  Card,
  CardContent,
  Avatar,
  Grid,
  Divider,
  CardMedia,
  Button,
  Link,
} from "@mui/material";

// Sample data
const user = {
  name: "Tejas Srikanth",
  avatar: "https://via.placeholder.com/150", // Replace with actual image URL
  description:
    "Software Developer based in San Francisco. Passionate about technology and open-source.",
  email: "tejas.srikanth@example.com",
  phone: "+1-234-567-8900",
  medicalConditions: [
    "Alzheimer's disease - affects memory and cognitive functions.",
    "High blood pressure - requires regular monitoring and medication.",
    "Heart condition - needs medication and periodic check-ups.",
    "Type II Diabetes - needs Insulin",
    "See more.",
  ],
};

const memoriesData = [
  {
    title: "Vacation in Bali",
    image: `${process.env.PUBLIC_URL}/background-0.jpg`,
    description:
      "A relaxing vacation on the beautiful beaches of Bali, enjoying the sun and surf.",
  },
  {
    title: "Graduation Day",
    image: `${process.env.PUBLIC_URL}/background-1.jpg`,
    description:
      "Celebrating graduation day with friends and family, marking the end of a significant journey.",
  },
  {
    title: "Mountain Hiking",
    image: `${process.env.PUBLIC_URL}/background-2.jpg`,
    description:
      "An adventurous hike up the mountains, experiencing breathtaking views and fresh air.",
  },
  {
    title: "Family Reunion",
    image: `${process.env.PUBLIC_URL}/background-3.jpg`,
    description:
      "A joyful family reunion with relatives coming together to share memories and catch up.",
  },
  {
    title: "City Sightseeing",
    image: `${process.env.PUBLIC_URL}/background-4.jpg`,
    description:
      "Exploring the vibrant city life, visiting famous landmarks and enjoying local cuisine.",
  },
  {
    title: "Beach Party",
    image: `${process.env.PUBLIC_URL}/background-5.jpg`,
    description:
      "A fun beach party with friends, complete with music, games, and a bonfire.",
  },
  {
    title: "Wedding Celebration",
    image: `${process.env.PUBLIC_URL}/background-6.jpg`,
    description:
      "A beautiful wedding ceremony, celebrating the union of two people in love.",
  },
  {
    title: "Camping Trip",
    image: `${process.env.PUBLIC_URL}/background-7.jpg`,
    description:
      "Spending a weekend camping in the great outdoors, enjoying nature and campfire stories.",
  },
  {
    title: "Art Exhibition",
    image: `${process.env.PUBLIC_URL}/background-8.jpg`,
    description:
      "Visiting an art exhibition, appreciating the creativity and talent of various artists.",
  },
];

const peopleSeenWith = [
  { name: "Alice Johnson", relationship: "a close friend" },
  { name: "Bob Smith", relationship: "a close friend" },
  { name: "Carol White", relationship: "a close friend" },
  { name: "David Brown", relationship: "a close friend" },
  { name: "Eva Davis", relationship: "a close friend" },
];

const Profile = () => {
  return (
    <Box
      component="main"
      sx={{ flexGrow: 1, bgcolor: "background.default", mr: "240px", p: 3 }}
    >
      <Toolbar />
      <Grid container spacing={4}>
        {/* Profile Header */}
        <Grid item xs={12} md={4}>
          <Card variant="outlined">
            <CardContent>
              <Box display="flex" alignItems="center">
                <Avatar
                  alt={user.name}
                  src={user.avatar}
                  sx={{ width: 100, height: 100, mr: 2 }}
                />
                <Box>
                  <Typography variant="h4">{user.name}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {user.description}
                  </Typography>
                </Box>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body1">
                <strong>Email:</strong> {user.email}
              </Typography>
              <Typography variant="body1">
                <strong>Phone:</strong> {user.phone}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Medical Conditions
              </Typography>
              {user.medicalConditions.map((activity, index) => (
                <Typography key={index} variant="body2" sx={{ mb: 1 }}>
                  {activity}
                </Typography>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Typography variant="h4" sx={{ my: 4, fontWeight: "bold" }} gutterBottom>
        Memories
      </Typography>
      <Grid container spacing={4}>
        {memoriesData.slice(0, 3).map((memory, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card variant="outlined">
              <CardMedia
                component="img"
                height="140"
                image={memory.image}
                alt={memory.title}
              />
              <CardContent>
                <Typography variant="h6" component="div">
                  {memory.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {memory.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      <Box sx={{ mt: 2 }}>
        <Button
          variant="outlined"
          fullWidth
          sx={{
            p: 1,
            borderColor: "#f89742",
            borderWidth: "2px",
            color: "#000000",
            fontWeight: "bold",
            textTransform: "none",
            "&:hover": {
              backgroundColor: "#f89742",
            },
          }}
          disableElevation
          component={Link}
          to="/dashboard"
          size="medium"
        >
          View more memories
        </Button>
      </Box>

      <Typography variant="h4" sx={{ my: 4, fontWeight: "bold" }} gutterBottom>
        People
      </Typography>
      <Grid container spacing={2}>
        {peopleSeenWith.map((person, index) => (
          <Grid item md={2} key={index}>
            <Card
              variant="outlined"
              sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <CardHeader
                avatar={
                  <Avatar
                    alt={person.name}
                    src={`https://via.placeholder.com/150?text=${person.name.charAt(
                      0
                    )}`} // Placeholder avatar
                  />
                }
                title={person.name}
                subheader={person.relationship}
                sx={{ textAlign: "center" }}
              />
            </Card>
          </Grid>
        ))}
      </Grid>
      <Box sx={{ mt: 2 }}>
        <Button
          variant="outlined"
          fullWidth
          sx={{
            p: 1,
            borderColor: "#f89742",
            borderWidth: "2px",
            color: "#000000",
            fontWeight: "bold",
            textTransform: "none",
            "&:hover": {
              backgroundColor: "#f89742",
            },
          }}
          disableElevation
          component={Link}
          to="/dashboard"
          size="medium"
        >
          View people
        </Button>
      </Box>
    </Box>
  );
};

export default Profile;
