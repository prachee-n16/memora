import React, { useState } from "react";
import Searchbar from "./Searchbar";
import Sidebar from "./Sidebar";
import Profile from "./Profile";
import MemoriesApp from "./Memories";
import Relationships from "./Relationships";
import ChatApp from "./ChatApp";
import { Box } from "@mui/material";

const Dashboard = () => {
  const [mainArea, setMainArea] = useState("");
  console.log(mainArea);
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
          <Relationships />
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
