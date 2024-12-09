"use client"
import { Menu, MenuItem, IconButton, Button, AppBar, Typography, Toolbar, Container } from "@mui/material";
import { useMemo, useState } from "react";
import LogoutButton from "@/components/LogoutButton";
import AddPreferenceModal from "@/components/AddPreferenceModal";
import Link from "next/link";

// Ícones SVG
export const setaBaixo: React.JSX.Element = <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 17.25 12 21m0 0-3.75-3.75M12 21V3" />
</svg>;

export const setaCima: React.JSX.Element = <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
    <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 6.75 12 3m0 0 3.75 3.75M12 3v18" />
</svg>;

export const menu: React.JSX.Element = <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
    <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
</svg>;
const MenuComponent: React.FC = () => {
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const [modalOpen, setModalOpen] = useState(false);
    const baseURL = useMemo(()=>process.env.NEXT_PUBLIC_APP_URL|| "http://localhost:3000/",[])

    const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    return (
        <Container>
            <AppBar position="sticky" sx={{ padding: 1, direction: "inherit" }}>
                <Toolbar>


                    {/* Botão de menu */}
                    <IconButton
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        onClick={handleMenuOpen}
                        sx={{ marginLeft: 0 }} // Garantir espaço à esquerda
                    >
                        {menu} {anchorEl ? setaCima : setaBaixo}
                    </IconButton>
                    <Typography variant="h6" sx={{ flexGrow: 1, textAlign: 'center', color: 'white' }}>
                        <Link href={baseURL}>PopCorn AI</Link>
                    </Typography>

                    {/* Menu */}
                    <Menu
                        anchorEl={anchorEl}
                        open={Boolean(anchorEl)}
                        onClose={handleMenuClose}
                        sx={{ mt: 2 }} // Aumenta a distância do menu
                    >
                        <MenuItem>
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={() => setModalOpen(true)}
                                sx={{ width: '100%' }}
                            >
                                Adicionar Nova Preferência
                            </Button>
                        </MenuItem>
                        <MenuItem onClick={handleMenuClose}>Perfil</MenuItem>
                        <MenuItem onClick={handleMenuClose}>Configurações</MenuItem>
                        <MenuItem onClick={handleMenuClose}>
                            <LogoutButton />
                        </MenuItem>
                    </Menu>

                    {/* Modal */}
                    <AddPreferenceModal open={modalOpen} onClose={() => setModalOpen(false)} />
                </Toolbar>
            </AppBar>
        </Container>
    );
};

export default MenuComponent;
