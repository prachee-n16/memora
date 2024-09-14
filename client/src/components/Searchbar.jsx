import {
  TextField,
  InputAdornment,
  Box,
  Typography,
  Avatar,
} from "@mui/material";
import RedditIcon from "@mui/icons-material/Reddit";
import SendRoundedIcon from "@mui/icons-material/SendRounded";
import React, { useState, useEffect } from "react";
import { v1 as uuidv1 } from "uuid";

const Searchbar = () => {
  const [newMessage, setNewMessage] = useState("");
  const [channelMessages, setChannelMessages] = useState([
    {
      id: "123456789",
      user: "David",
      message: "Hey there!",
    },
  ]);

  const handleOnSubmit = async (e) => {
    e.preventDefault();
    var id = uuidv1();

    setChannelMessages((prev) => [
      ...prev,
      {
        id: id,
        message: newMessage,
        user: "Prachee Nanda",
      },
    ]);
    setNewMessage("");
  };

  return (
    <form onSubmit={handleOnSubmit}>
      <TextField
        value={newMessage}
        id="outlined-basic"
        label=""
        variant="outlined"
        fullWidth
        focused
        placeholder="Enter prompt here."
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <RedditIcon />
            </InputAdornment>
          ),
          endAdornment: (
            <InputAdornment position="end">
              <SendRoundedIcon />
            </InputAdornment>
          ),
        }}
        onChange={(e) => setNewMessage(e.target.value)}
        sx={{
          my: 2,
          mx: 5,
          borderRadius: 15,
          textAlign: "center",
          position: "fixed",
          bottom: 0,
          width: "95%",
        }}
      />
    </form>
  );
};

export default Searchbar;
