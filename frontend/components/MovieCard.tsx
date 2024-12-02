"use client";
import React, { useState, useEffect } from "react";
import { 
  Card, 
  CardContent, 
  Typography, 
  CardMedia, 
  Button, 
  Box, 
  IconButton, 
  Tooltip,
  useMediaQuery, 
  Theme,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { 
  Favorite as FavoriteIcon, 
  FavoriteBorder as FavoriteBorderIcon,
  ThumbUp as ThumbUpIcon,
  ThumbUpOutlined as ThumbUpOutlinedIcon,
  ThumbDown as ThumbDownIcon,
  ThumbDownOutlined as ThumbDownOutlinedIcon
} from "@mui/icons-material";
import { truncateText } from "@/utils";
import { MovieList } from "@/types/types";
import axios from "axios";
import api from "@/services/api";

interface MovieCardProps {
  movie: MovieList;
  onWatch?: (movieId: number) => void;
}

const MovieCard: React.FC<MovieCardProps> = ({ movie, onWatch }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  // State for interaction buttons
  const [isFavorite, setIsFavorite] = useState(movie.user_interactions.favorited);
  const [likeStatus, setLikeStatus] = useState<'none' | 'liked' | 'disliked'>(
    movie.user_interactions.liked ? 'liked' : (movie.user_interactions.liked === false ? 'disliked' : 'none')
  );

  const token = localStorage.getItem("access_token");

  // Validate and sanitize movie data
  const safeTitle = movie.title || "Título não disponível";
  const safeImageUrl = movie.image_url || "/placeholder-movie.png";
  const safeDescription = movie.description || "Descrição não disponível";

  // Adjust truncation based on screen size
  const titleMaxLength = isMobile ? 20 : 30;
  const descriptionMaxLength = isMobile ? 50 : 100;

  // Interaction Handlers
  const handleFavorite = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsFavorite(!isFavorite);

    try {
      await api.post(
        "/api/favorite_movie/",
        { movie_id: movie.id },
        {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        }
      );
    } catch (error) {
      console.error("Error updating favorite status", error);
    }
  };

  const handleLike = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const newLikeStatus = likeStatus === "liked" ? "none" : "liked";
    setLikeStatus(newLikeStatus);

    try {
      await api.post(
        "/api/like_dislike/",
        { movie_id: movie.id, action: newLikeStatus },
        {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        }
      );
    } catch (error) {
      console.error("Error updating like status", error);
    }
  };

  const handleDislike = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const newDislikeStatus = likeStatus === "disliked" ? "none" : "disliked";
    setLikeStatus(newDislikeStatus);

    try {
      await api.post(
        "/api/like_dislike/",
        { movie_id: movie.id, action: newDislikeStatus },
        {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        }
      );
    } catch (error) {
      console.error("Error updating dislike status", error);
    }
  };

  const handleWatch = () => {
    if (onWatch && movie.id) {
      onWatch(movie.id);
    }
  };

  return (
    <Card 
      sx={{ 
        width: "100%", 
        maxWidth: 345, 
        height: "100%", 
        display: "flex", 
        flexDirection: "column",
        transition: "transform 0.2s",
        "&:hover": {
          transform: "scale(1.03)",
          boxShadow: theme.shadows[4],
        },
      }}
      elevation={2}
    >
      <Box position="relative">
        <CardMedia
          component="img"
          alt={safeTitle}
          height={isMobile ? 180 : 220}
          image={safeImageUrl}
          sx={{ 
            objectFit: "cover",
            backgroundColor: theme.palette.grey[200],
          }}
          onError={(e) => {
            const imgElement = e.currentTarget;
            imgElement.src = "/placeholder-movie.png";
            imgElement.onerror = null;
          }}
        />
        <Box 
          position="absolute" 
          top={8} 
          right={8} 
          display="flex" 
          alignItems="center"
        >
          <Tooltip title={isFavorite ? "Remover dos favoritos" : "Adicionar aos favoritos"}>
            <div>
              <IconButton 
                onClick={handleFavorite}
                sx={{ 
                  bgcolor: "rgba(255,255,255,0.7)", 
                  "&:hover": { 
                    bgcolor: "rgba(255,255,255,0.9)", 
                  } 
                }}
              >
                {isFavorite ? (
                  <FavoriteIcon color="error" />
                ) : (
                  <FavoriteBorderIcon color="primary" />
                )}
              </IconButton>
            </div>
          </Tooltip>
        </Box>
      </Box>
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography 
          variant="h6" 
          component="div" 
          gutterBottom
          sx={{ 
            fontSize: isMobile ? "1rem" : "1.25rem",
            fontWeight: 600,
          }}
        >
          {truncateText(safeTitle, titleMaxLength)}
        </Typography>
        <Typography 
          variant="body2" 
          color="textSecondary" 
          sx={{ 
            flexGrow: 1,
            mb: 2,
            height: isMobile ? "auto" : 50,
            overflow: "hidden",
            textOverflow: "ellipsis",
          }}
        >
          {truncateText(safeDescription, descriptionMaxLength)}
        </Typography>
      </CardContent>
      <Box 
        sx={{ 
          p: 2, 
          pt: 0,
          display: "flex", 
          justifyContent: "space-between", 
          alignItems: "center",
        }}
      >
        <Box display="flex" alignItems="center">
          <Tooltip title="Gostei">
            <div>
              <IconButton 
                onClick={handleLike} 
                color={likeStatus === "liked" ? "primary" : "default"}
              >
                {likeStatus === "liked" ? <ThumbUpIcon /> : <ThumbUpOutlinedIcon />}
              </IconButton>
            </div>
          </Tooltip>
          <Tooltip title="Não gostei">
            <div>
              <IconButton 
                onClick={handleDislike}
                color={likeStatus === "disliked" ? "error" : "default"}
              >
                {likeStatus === "disliked" ? <ThumbDownIcon /> : <ThumbDownOutlinedIcon />}
              </IconButton>
            </div>
          </Tooltip>
        </Box>
        <Button 
          variant="contained" 
          color="primary" 
          size={isMobile ? "small" : "medium"}
          onClick={handleWatch}
          sx={{ 
            width: isMobile ? "auto" : "100%",
            maxWidth: 200,
          }}
        >
          Assistir
        </Button>
      </Box>
    </Card>
  );
};

export default MovieCard;
