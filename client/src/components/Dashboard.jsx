import React, { useState } from "react";
import Searchbar from "./Searchbar";
import Sidebar from "./Sidebar";
import Profile from "./Profile";
import MemoriesApp from "./Memories";
import Relationships from "./Relationships";
import ChatApp from "./ChatApp";
import { Box } from "@mui/material";

const Dashboard = () => {
  // State to hold people data
  const [peopleData, setPeopleData] = useState([
    {
      name: "John Doe",
      relationship: "A close friend",
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
      relationship: "A close friend",
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
      relationship: "A close friend",
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
  ]);

  const [mainArea, setMainArea] = useState("");
  return (
    <Box sx={{ display: "flex", height: "100vh" }}>
      <Sidebar setMainArea={setMainArea} />
      <Box
        component="main"
        sx={{ flexGrow: 1, bgcolor: "background.default", p: 3 }}
      >
        {mainArea == "Profile" || mainArea == "" ? (
          <Profile />
        ) : mainArea == "Memories" ? (
          <MemoriesApp />
        ) : mainArea == "Relationships" ? (
          <Relationships
            peopleData={peopleData}
            setPeopleData={setPeopleData}
          />
        ) : mainArea == "ChatBot" ? (
          <ChatApp />
        ) : (
          <Profile />
        )}
      </Box>
    </Box>
  );
};

export default Dashboard;
