import React, { useEffect } from "react";
import { AppBar, Box, Toolbar } from "@mui/material";
import {
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Button,
  Typography,
  Grid,
} from "@mui/material";

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

const Memories = () => {
  return (
    <Box
      component="main"
      sx={{
        flexGrow: 1,
        bgcolor: "background.default",
        mr: "240px",
        overflowY: "auto",
      }}
    >
      <Toolbar />
      <Grid container spacing={4} md={12}>
        {memoriesData.map((memory, index) => (
          <Grid item key={index}>
            <Card sx={{ maxWidth: 345 }}>
              <CardMedia
                sx={{ height: 140 }}
                image={memory.image}
                title={memory.title}
              />
              <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                  {memory.title}
                </Typography>
                <Typography variant="body2" sx={{ color: "text.secondary" }}>
                  {memory.description}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small">Like</Button>
                <Button size="small">Share</Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Memories;
