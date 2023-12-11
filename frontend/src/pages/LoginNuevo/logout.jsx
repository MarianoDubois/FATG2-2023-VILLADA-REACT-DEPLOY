import { Link } from 'react-router-dom';
import { useEffect } from 'react';
import { LoggedOutView } from './home';
import { logout } from '../../utils/auth';
import { containerClasses } from '@mui/material';
import { login } from '../../utils/auth';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/auth';
import { Container, Row, Col } from 'react-bootstrap';
import './login.css';
import Button from 'react-bootstrap/Button';



<head>
  <link rel="preconnect" href="https://fonts.googleapis.com"></link>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"> </link>
</head>

const Logout = () => {
    const navigate = useNavigate();
    useEffect(() => {
        logout();
        navigate('/login');
    }, [navigate]);
    return (
        <Container className='font-family' style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', minWidth:'100' }}>
            <div className='text-center'>
                <p className='color' style={{ textAlign: 'left' }}>
                    <p style={{ fontSize: '1.4rem' }}>
                        Sesión cerrada
                    </p>
                    Cerraste sesión correctamente
                </p>
                <div >
                    <Button
                        className='button-style'
                        style={{ marginRight: '1rem' }}
                        variant='primary'
                        type='submit'
                        href='/login'
                    >
                        Iniciar sesión
                    </Button>
                    <Button
                        className='button-style'
                        variant='primary'
                        href='/signup'
                    >
                        Registrarse
                    </Button>
                </div>
            </div>
        </Container>

    )
};

export default Logout;