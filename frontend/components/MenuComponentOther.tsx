"use client"
import {  AppBar, Typography, Toolbar, Container } from "@mui/material";
import Link from "next/link";
import { useMemo } from "react";


const MenuComponent2: React.FC = () => {
    const baseURL = useMemo(()=>process.env.NEXT_PUBLIC_APP_URL|| "http://localhost:3000/",[])
    return (
        <Container>
        <AppBar position="sticky" sx={{ padding: 1 ,direction:"inherit"}}>
            <Toolbar>
               
                
                
                <Typography variant="h6" sx={{ flexGrow: 1, textAlign: 'center', color: 'white' }} >

                    <Link href={baseURL}>PopCorn AI</Link>
                </Typography>

            </Toolbar>
        </AppBar>
        </Container>
    );
};

export default MenuComponent2;
