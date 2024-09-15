import React, { useState, useEffect, useRef } from "react";
import {
  AppBar,
  Box,
  Toolbar,
  TextField,
  InputAdornment,
  Typography,
  Avatar,
  Button,
  Modal,
} from "@mui/material";
import RedditIcon from "@mui/icons-material/Reddit";
import SendRoundedIcon from "@mui/icons-material/SendRounded";
import MicIcon from "@mui/icons-material/Mic";
import { v1 as uuidv1 } from "uuid";
import axios from "axios";

function stringToColor(string) {
  if (string === "Prachee Nanda") {
    return "purple";
  } else if (string === "memora") {
    return "#FF4500";
  } else {
    let hash = 0;
    let i;

    /* eslint-disable no-bitwise */
    for (i = 0; i < string.length; i += 1) {
      hash = string.charCodeAt(i) + ((hash << 5) - hash);
    }

    let color = "#";

    for (i = 0; i < 3; i += 1) {
      const value = (hash >> (i * 8)) & 0xff;
      color += `00${value.toString(16)}`.slice(-2);
    }
    /* eslint-enable no-bitwise */

    return color;
  }
}

export function stringAvatar(name) {
  return {
    sx: {
      bgcolor: stringToColor(name),
      color: "#FFF",
    },
    children: `${name.split(" ")[0][0]}${name.split(" ")[1][0]}`,
  };
}

const ChatApp = () => {
  const [newMessage, setNewMessage] = useState("");
  const [channelMessages, setChannelMessages] = useState([
    {
      id: "1234",
      user: "Memora AI",
      message: "Ask me anything :)",
    },
  ]);
  const [isRecording, setIsRecording] = useState(false);
  const [audioModalOpen, setAudioModalOpen] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const formRef = useRef(null); // Form reference

  const handleOnSubmit = async (e) => {
    e.preventDefault();
    const id = uuidv1();
  
    setChannelMessages((prev) => [
      ...prev,
      {
        id: id,
        message: newMessage,
        user: "Prachee Nanda",
      },
    ]);
  
    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: newMessage }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let aiMessage = '';
  
      setChannelMessages((prev) => [
        ...prev,
        {
          id: uuidv1(),
          message: '',
          user: "Memora AI",
        },
      ]);
  
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        aiMessage += chunk;
  
        setChannelMessages((prev) => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1].message = aiMessage;
          return newMessages;
        });
      }
    } catch (error) {
      console.error("Error calling chat endpoint:", error);
    }
  
    setNewMessage("");
  };

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    audioChunksRef.current = [];
  
    mediaRecorderRef.current.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };
  
    mediaRecorderRef.current.onstop = async () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("audio", audioBlob, "audio.wav");
  
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/transcribe",
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        setNewMessage(response.data.transcription); // Set the transcribed message
        setAudioModalOpen(false);
      } catch (error) {
        console.error("Error transcribing audio:", error);
      }
    };
  
    mediaRecorderRef.current.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  useEffect(() => {
    if (newMessage) {
      formRef.current.requestSubmit(); // Automatically submit the form
    }
  }, [newMessage]); // Trigger form submission when a new message is set

  return (
    <Box
      component="main"
      sx={{ flexGrow: 1, bgcolor: "background.default", mr: "240px" }}
    >
      <Toolbar />
      <Box>
        <Typography sx={{ mt: 2 }} fontWeight="700" variant="h3" align="center">
          <Box
            component="span"
            sx={{
              color: "#f89742",
            }}
          >
            mem
          </Box>
          ora
        </Typography>
        <Typography variant="subtitle1" fontWeight="400" align="center">
          This is the beginning of this chat.
        </Typography>
      </Box>
      <Box>
        {channelMessages.map((message, index) => (
          <Box display="flex" key={message.id} sx={{ direction: "row", p: 2 }}>
            {message.user && (
              <Avatar
                variant="rounded"
                key={message.id + "Avatar"}
                sx={{ width: 24, height: 24, mx: 5 }}
                {...stringAvatar(message.user)}
              />
            )}
            <Box key={message.id + "Message"}>
              <Typography
                sx={{
                  border: "1px solid black",
                  p: 2,
                  mx: 2,
                  borderRadius: "10px",
                }}
              >
                {message.message}
              </Typography>
            </Box>
            <Box sx={{ flexGrow: 1 }} />
          </Box>
        ))}
      </Box>
      <form ref={formRef} onSubmit={handleOnSubmit}>
        <TextField
          value={newMessage}
          id="outlined-basic"
          label=""
          variant="outlined"
          focused
          placeholder="Enter prompt here."
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Button
                  onClick={() => setAudioModalOpen(true)}
                  sx={{ minWidth: 0, p: 0 }}
                  color="black"
                >
                  <MicIcon />
                </Button>
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
            width: "80%",
          }}
        />
      </form>
      <Modal
        open={audioModalOpen}
        onClose={() => setAudioModalOpen(false)}
        aria-labelledby="audio-input-modal"
        aria-describedby="modal-for-audio-input"
      >
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 400,
            bgcolor: "#FFF8E1",
            borderRadius: "16px",
            boxShadow: "0 4px 30px rgba(0, 0, 0, 0.1)",
            p: 4,
            textAlign: "center",
          }}
        >
          <Typography
            id="audio-input-modal"
            variant="h5"
            component="h2"
            sx={{
              fontWeight: "bold",
              color: "#B85C38",
              mb: 3,
            }}
          >
            Ask Memora a Question
          </Typography>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: 2,
            }}
          >
            <Box
              sx={{
                width: 100,
                height: 100,
                borderRadius: "50%",
                bgcolor: isRecording ? "#B85C38" : "#E0E0E0",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                transition: "all 0.3s ease",
              }}
            >
              <MicIcon sx={{ fontSize: 48, color: "#FFF" }} />
            </Box>
            <Button
              onClick={isRecording ? stopRecording : startRecording}
              variant="contained"
              sx={{
                bgcolor: isRecording ? "#D32F2F" : "#B85C38",
                color: "#FFF",
                "&:hover": {
                  bgcolor: isRecording ? "#B71C1C" : "#8B4513",
                },
                borderRadius: "24px",
                px: 4,
                py: 1,
                fontWeight: "bold",
              }}
            >
              {isRecording ? "Stop Recording" : "Start Recording"}
            </Button>
          </Box>
          <Typography
            variant="body2"
            sx={{ mt: 3, color: "#666", fontStyle: "italic" }}
          >
            {isRecording ? "Recording in progress..." : "Click to start"}
          </Typography>
        </Box>
      </Modal>
    </Box>
  );
};


export default ChatApp;