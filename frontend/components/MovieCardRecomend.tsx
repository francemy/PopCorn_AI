import React, { useState } from "react";
import {
    Card,
    CardContent,
    Typography,
    CardMedia,
    Box,
    IconButton,
    Tooltip,
    Chip,
} from "@mui/material";
import {
    Favorite as FavoriteIcon,
    FavoriteBorder as FavoriteBorderIcon,
    ThumbUp as ThumbUpIcon,
    ThumbUpOutlined as ThumbUpOutlinedIcon,
    ThumbDown as ThumbDownIcon,
    ThumbDownOutlined as ThumbDownOutlinedIcon,
    PlayCircle,
    NoteAltOutlined,
} from "@mui/icons-material";
import { MovieList } from "@/types/types";
import api from "@/services/api";
import RatingModal from "@/components/RatingModal"; // Modal para avaliação

interface MovieCardProps {
    movie: MovieList;
}

const MovieCard: React.FC<MovieCardProps> = ({ movie }) => {
    const [isFavorite, setIsFavorite] = useState(movie.user_interactions.favorited);
    const [likeStatus, setLikeStatus] = useState<"none" | "like" | "dislike">(movie?.user_interactions?.liked || "none");
    const [isRatingModalOpen, setIsRatingModalOpen] = useState(false);

    const safeTitle = movie.title || "Título não disponível";
    const safeImageUrl = movie.image_url || "/placeholder-movie.png";
    const safeDescription = movie.description || "Descrição não disponível";

    const handleFavorite = async () => {
        const token = localStorage.getItem("access_token");
        try {
            await api.post(
                "/favorite_movies/favorite_movie_action/",
                { movie_id: movie.id },
                { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } }
            );
            setIsFavorite(!isFavorite);
        } catch (error) {
            console.error("Erro ao atualizar favorito", error);
        }
    };

    const handleLike = async () => {
        const newLikeStatus = likeStatus === "like" ? "none" : "like";
        const token = localStorage.getItem("access_token");
        try {
            await api.post(
                "/like_dislike/like_dislike_action/",
                { movie_id: movie.id, action: newLikeStatus },
                { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } }
            );
            setLikeStatus(newLikeStatus);
        } catch (error) {
            console.error("Erro ao atualizar like", error);
        }
    };

    const handleDislike = async () => {
        const newDislikeStatus = likeStatus === "dislike" ? "none" : "dislike";
        const token = localStorage.getItem("access_token");
        try {
            await api.post(
                "/like_dislike/like_dislike_action/",
                { movie_id: movie.id, action: newDislikeStatus },
                { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } }
            );
            setLikeStatus(newDislikeStatus);
        } catch (error) {
            console.error("Erro ao atualizar dislike", error);
        }
    };

    const handleWatch = async () => {
        const token = localStorage.getItem("access_token");
        if (!token) return console.error("Token não encontrado. Usuário não autenticado.");

        try {
            await api.post(
                "/watched_movies/mark_as_watched/",
                { movie_id: movie.id },
                { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" } }
            );
            console.log("Filme marcado como assistido.");
        } catch (error) {
            console.error("Erro ao marcar como assistido", error);
        }
    };

    const openRatingModal = () => {
        setIsRatingModalOpen(true);
    };

    const closeRatingModal = () => {
        setIsRatingModalOpen(false);
    };

    return (
        <div className=" overflow-clip w-full max-h-50"> {/* Ajustado para garantir melhor responsividade */}
            <Card
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    transition: "transform 0.2s",
                    "&:hover": { transform: "scale(1.05)" },
                    height: "100%",
                    borderRadius: 2, // Adiciona borda arredondada para um visual mais suave
                }}
                elevation={4}
            >
                {/* Primeira linha: Imagem e Título */}
                <div className="h-20">
                    <CardMedia
                        component="img"
                        alt={safeTitle}
                        height={"20px"}
                        image={safeImageUrl}
                        sx={{ objectFit: "cover" }}
                        onError={(e) => { const imgElement = e.currentTarget; imgElement.src = "/placeholder-movie.png"; imgElement.onerror = null; }}
                    />
                </div>

                <CardContent sx={{ paddingBottom: "8px" }}>
                    <Typography variant="h6" component="div" sx={{ whiteSpace: 'normal', overflow: 'hidden', textOverflow: 'ellipsis', background: "white" }}>
                        {safeTitle}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'normal' }}>
                        {safeDescription}
                    </Typography>
                    <Box sx={{ display: "flex", flexWrap: "wrap", gap: 1, mt: 1, overflow: 'auto', color: 'black' }}>
                        {movie.genres.map((genre) => (
                            <Chip key={genre.id} label={genre.name} variant="outlined" color="info" sx={{ fontSize: "0.875rem" , textShadow: '9'}}  />
                        ))}
                    </Box>
                </CardContent>

                {/* Segunda linha: Interações do usuário */}
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: 2, background: "white" }}>
                    {/* Ícones de Interação */}
                    <Box sx={{ display: "flex" }}>
                        <Tooltip title="Gostei">
                            <IconButton onClick={handleLike} color={likeStatus === "like" ? "primary" : "default"}>
                                {likeStatus === "like" ? <ThumbUpIcon /> : <ThumbUpOutlinedIcon />}
                            </IconButton>
                        </Tooltip>
                        <Tooltip title="Não gostei">
                            <IconButton onClick={handleDislike} color={likeStatus === "dislike" ? "error" : "default"}>
                                {likeStatus === "dislike" ? <ThumbDownIcon /> : <ThumbDownOutlinedIcon />}
                            </IconButton>
                        </Tooltip>
                        <Tooltip title="Favoritar">
                            <IconButton onClick={handleFavorite} color={isFavorite ? "error" : "default"}>
                                {isFavorite ? <FavoriteIcon /> : <FavoriteBorderIcon />}
                            </IconButton>
                        </Tooltip>
                    </Box>

                    {/* Botão Assistir e Avaliar */}
                    <Tooltip title="Assistir">
                        <IconButton color="primary" onClick={e => { e.stopPropagation(); handleWatch(); }} sx={{ width: "auto" }}>
                            <PlayCircle />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Avaliar o filme">
                        <IconButton color="primary" onClick={openRatingModal}>
                            <NoteAltOutlined />
                        </IconButton>
                    </Tooltip>
                </Box>

                {/* Modal de Avaliação */}
                <RatingModal open={isRatingModalOpen} onClose={closeRatingModal} id_movie={movie.id} />
            </Card>
        </div>
    );
};

export default MovieCard;
