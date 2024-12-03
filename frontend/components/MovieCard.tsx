import React, { useState } from "react";
import { 
  Card, 
  CardContent, 
  Typography, 
  CardMedia, 
  Button, 
  Box, 
  IconButton, 
  Tooltip,
  Modal,
  useMediaQuery
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
import api from "@/services/api";
import RatingModal from "@/components/RatingModal"; // Importando o componente RatingModal

interface MovieCardProps {
  movie: MovieList;
  onWatch?: (movieId: number) => void;
}

const MovieCard: React.FC<MovieCardProps> = ({ movie, onWatch }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  const [isFavorite, setIsFavorite] = useState(movie.user_interactions.favorited);
  const [likeStatus, setLikeStatus] = useState<'none' | 'like' | 'dislike'>(movie?.user_interactions?.liked || 'none');
  const [isModalOpen, setIsModalOpen] = useState(false); // Estado para a RatingModal
  const [isRatingModalOpen, setIsRatingModalOpen] = useState(false); // Estado para controlar a modal de avaliação

  const safeTitle = movie.title || "Título não disponível";
  const safeImageUrl = movie.image_url || "/placeholder-movie.png";
  const safeDescription = movie.description || "Descrição não disponível";

  const titleMaxLength = isMobile ? 20 : 30;
  const descriptionMaxLength = isMobile ? 50 : 100;

  const handleFavorite = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const token = localStorage.getItem("access_token");
    try {
      await api.post(
        "/favorite_movies/favorite_movie_action/",
        { movie_id: movie.id },
        {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      setIsFavorite(!isFavorite);
    } catch (error) {
      console.error("Error updating favorite status", error);
    }
  };

  const handleLike = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const newLikeStatus = likeStatus === "like" ? "none" : "like";
    const token = localStorage.getItem("access_token");
    try {
      await api.post(
        "/like_dislike/like_dislike_action/",
        { movie_id: movie.id, action: newLikeStatus },
        {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      setLikeStatus(newLikeStatus);
    } catch (error) {
      console.error("Error updating like status", error);
    }
  };

  const handleDislike = async (e: React.MouseEvent) => {
    e.stopPropagation();
    const newDislikeStatus = likeStatus === "dislike" ? "none" : "dislike";
    const token = localStorage.getItem("access_token");
    try {
      await api.post(
        "/like_dislike/like_dislike_action/",
        { movie_id: movie.id, action: newDislikeStatus },
        {
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );
      setLikeStatus(newDislikeStatus);
    } catch (error) {
      console.error("Error updating dislike status", error);
    }
  };

  const handleWatch = async (movieId: any) => {
    try {
      const token = localStorage.getItem('access_token');
      if (!token) {
        console.error('Token não encontrado. Usuário não autenticado.');
        return;
      }

      const response = await api.post(
        '/watched_movies/mark_as_watched/',
        { movie_id: movieId },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 201) {
        console.log('Filme marcado como assistido com sucesso.');
      } else if (response.status === 200) {
        console.log('O filme já foi assistido. Contador incrementado.');
      }
    } catch (error) {
      console.error('Erro ao marcar o filme como assistido:', error);
    }
  };

  const openRatingModal = () => {
    setIsRatingModalOpen(true); // Abre a modal de avaliação
  };

  const closeRatingModal = () => {
    setIsRatingModalOpen(false); // Fecha a modal de avaliação
  };

  return (
    <Card sx={{ width: "100%",padding: 2,justifyContent:"center", maxWidth: 345, height: "100%", display: "flex", flexDirection: "column", transition: "transform 0.2s", "&:hover": { transform: "scale(1.03)", boxShadow: theme.shadows[4] }, }} elevation={2}>
      <Box position="relative">
        <CardMedia
          component="img"
          alt={safeTitle}
          height={isMobile ? 180 : 220}
          image={safeImageUrl}
          sx={{ objectFit: "cover", backgroundColor: theme.palette.grey[200] }}
          onError={(e) => { const imgElement = e.currentTarget; imgElement.src = "/placeholder-movie.png"; imgElement.onerror = null; }}
        />
        <Box position="absolute" top={8} right={8} display="flex" alignItems="center">
          <Tooltip title={isFavorite ? "Remover dos favoritos" : "Adicionar aos favoritos"}>
            <div>
              <IconButton onClick={handleFavorite} sx={{ bgcolor: "rgba(255,255,255,0.7)", "&:hover": { bgcolor: "rgba(255,255,255,0.9)" } }}>
                {isFavorite ? <FavoriteIcon color="error" /> : <FavoriteBorderIcon color="primary" />}
              </IconButton>
            </div>
          </Tooltip>
        </Box>
      </Box>
      <CardContent sx={{ flexGrow: 1 }} onClick={() => setIsModalOpen(true)}>
        <Typography variant="h6" component="div" gutterBottom sx={{ fontSize: isMobile ? "1rem" : "1.25rem", fontWeight: 600 }}>
          {truncateText(safeTitle, titleMaxLength)}
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ flexGrow: 1, mb: 2, height: isMobile ? "auto" : 50, overflow: "hidden", textOverflow: "ellipsis" }}>
          {truncateText(safeDescription, descriptionMaxLength)}
        </Typography>
      </CardContent>
      <Box sx={{ p: 2, pt: 0, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <Box display="flex" alignItems="center">
          <Tooltip title="Gostei">
            <div>
              <IconButton onClick={handleLike} color={likeStatus === "like" ? "primary" : "default"}>
                {likeStatus === "like" ? <ThumbUpIcon /> : <ThumbUpOutlinedIcon />}
              </IconButton>
            </div>
          </Tooltip>
          <Tooltip title="Não gostei">
            <div>
              <IconButton onClick={handleDislike} color={likeStatus === "dislike" ? "error" : "default"}>
                {likeStatus === "dislike" ? <ThumbDownIcon /> : <ThumbDownOutlinedIcon />}
              </IconButton>
            </div>
          </Tooltip>
        </Box>
        <Tooltip title="Assistir">
          <Button variant="contained" color="primary" size={isMobile ? "small" : "medium"} onClick={e => { e.stopPropagation(); handleWatch(movie.id); }} sx={{ width: isMobile ? "auto" : "100%", maxWidth: 200 }}>
            Assistir
          </Button>
        </Tooltip>
        <Button variant="outlined" color="primary" onClick={openRatingModal}>
          Avaliar
        </Button>
      </Box>

      {/* Modal de Detalhes do Filme */}
      <RatingModal open={isRatingModalOpen} onClose={closeRatingModal} id_movie={movie.id} />
    </Card>
  );
};

export default MovieCard;
