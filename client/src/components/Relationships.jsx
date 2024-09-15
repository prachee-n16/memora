import {
  Box,
  Toolbar,
  Typography,
  Grid,
  Avatar,
  CardHeader,
  Divider,
} from "@mui/material";
import React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";

const people = [
  {
    name: "John Doe",
    conversations: [
      {
        date: "2024-09-12",
        topic: "Vacation Plans",
        content:
          "We discussed plans for the upcoming vacation to Bali. John is excited about visiting the beaches and exploring the local culture.",
      },
      {
        date: "2024-09-10",
        topic: "Work Project",
        content:
          "John shared updates on his current project, mentioning how he's integrating a new API into their software. He's facing some challenges with the authentication process.",
      },
    ],
  },
  {
    name: "Jane Smith",
    conversations: [
      {
        date: "2024-09-11",
        topic: "Hiking Gear",
        content:
          "Jane mentioned she's looking for new hiking boots for an upcoming trip to the mountains.",
      },
      {
        date: "2024-09-09",
        topic: "Career Development",
        content:
          "We talked about Jane's plans to take a certification course to further her skills in data science.",
      },
    ],
  },
  {
    name: "Emily Johnson",
    conversations: [
      {
        date: "2024-09-14",
        topic: "Art Exhibition",
        content:
          "Emily shared her excitement about attending a modern art exhibition downtown this weekend.",
      },
      {
        date: "2024-09-07",
        topic: "Cooking Classes",
        content:
          "Emily is thinking about enrolling in a series of cooking classes to learn how to make Italian dishes.",
      },
    ],
  },
];

const Relationships = () => {
  const defaultAvatar =
    "https://t3.ftcdn.net/jpg/02/43/12/34/360_F_243123463_zTooub557xEWABDLk0jJklDyLSGl2jrr.jpg";
  return (
    <Box component="main" sx={{ flexGrow: 1, mr: "240px" }}>
      <Toolbar />
      <Grid container spacing={4}>
        {people.map((person, index) => (
          <Grid item xs={12} key={index}>
            <Card variant="outlined">
              <CardHeader
                avatar={
                  <Avatar
                    alt={person.name}
                    src={person.avatar || defaultAvatar} // Fallback to default if no avatar
                  />
                }
                title={person.name}
                titleTypographyProps={{ variant: "h4", component: "div" }} // Customizing the title style
                subheader="A close friend!"
                subheaderTypographyProps={{
                  variant: "subtitle1",
                  color: "text.secondary",
                }}
                sx={{ paddingBottom: 0 }}
              />
              <CardContent>
                <Divider />
                {person.conversations.map((conversation, convIndex) => (
                  <Box key={convIndex} sx={{ paddingTop: 2 }}>
                    <Typography variant="subtitle1" color="text.secondary">
                      {conversation.date} - {conversation.topic}
                    </Typography>
                    <Typography variant="body2">
                      {conversation.content}
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Relationships;
