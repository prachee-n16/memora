import React, { useEffect, useState } from "react";
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
import axios from 'axios';

const fetchUserMemories = async (userId) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/get_user_memories/${userId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching user memories:", error);
    throw error;
  }
};

const Memories = () => {
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUserMemories(273) 
      .then(data => {
        console.log(data);
        setMemories(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading memories: {error.message}</div>;

  return (
    <Box component="main" sx={{ flexGrow: 1, bgcolor: "background.default", mr: "240px", overflowY: "auto" }}>
      <Toolbar />
      <Grid container spacing={4} md={12}>
        {memories.map((memory) => (
          <Grid item key={memory.memory_id}>
            <Card sx={{ maxWidth: 345 }}>
              <CardMedia 
                sx={{ height: 140 }} 
                image={memory.image ? `data:image/jpeg;base64,${memory.image}` : `${process.env.PUBLIC_URL}/background-8.jpg`}
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