import { useEffect, useState } from 'react';
import { login } from '../../utils/auth';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/auth';
import { Container, Row, Col } from 'react-bootstrap';
import './login.css';
import VisibilityRoundedIcon from '@mui/icons-material/VisibilityRounded';
import VisibilityOffRoundedIcon from '@mui/icons-material/VisibilityOffRounded';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import ITSVlogin from '../../assets/ITSVlogin.svg';
import Link from 'antd/es/typography/Link';


<head>
  <link rel="preconnect" href="https://fonts.googleapis.com"></link>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"> </link>
</head>

const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const isLoggedIn = useAuthStore((state) => state.isLoggedIn);

    useEffect(() => {
        if (isLoggedIn()) {
            navigate('/');
        }
    }, []);

    const resetForm = () => {
        setUsername('');
        setPassword('');
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        const { error } = await login(username, password);
        if (error) {
            alert(error);
        } else {
            navigate('/');
            resetForm();
        }
    };
    return (
        
      <Container className='font-family'>
        
        <Row>          
          <Col  style={{display:'flex', justifyContent:'center'}}>
            <div style={{marginTop:'4rem'}}>
              <img src={ITSVlogin} alt="Logo" style={{width:'10rem'}}/>
            </div>
          </Col>
        </Row>

        <Row>
          <Col className="centered-form">
            <div className="login-container">
              <p className="login-heading">
                Ingresá tus datos para<br/>iniciar sesión
              </p>
              <div className="login-form">
                <Form onSubmit={handleLogin}>

                  <Form.Group  className="mb-3" controlId="formBasicEmail">
                    <Form.Label className='color'>Nombre *</Form.Label>
                    <Form.Control
                    id="username"
                    name="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    type="text" placeholder="Nombre de usuario" className="input-styleado"/>
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="formBasicPassword">
                    <Form.Label className='color'>Contraseña *</Form.Label>
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                        <Form.Control 
                            type={showPassword ? 'text' : 'password'}
                            id="password"
                            name="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Contraseña"
                            className="input-styleado"
                        />
                    </div>
                  </Form.Group>
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                        <Button
                            onClick={() => setShowPassword(!showPassword)}
                            variant="light"
                            style={{ display: 'flex', alignItems: 'center' }}
                        >
                            {showPassword ? <VisibilityRoundedIcon style={{ fontSize: '1rem' }} /> : <VisibilityOffRoundedIcon style={{ fontSize: '1rem' }} />}
                        </Button>
                        <p style={{ margin: '0 0 0 0.3rem', fontSize: '0.875rem', opacity:'70%' }}>Mostrar Contraseña</p>
                    </div>

                  <div className='text-center' style={{marginTop:'0.5rem', marginBottom:'1rem'}}>
                    <Link href='http://127.0.0.1:8000/auth/accounts/password_reset' style={{color:' #2E5266'}} > ¿Olvidaste tu contraseña? </Link>
                  </div>
                  
                  <div className='text-center'>
                    <Button
                      className='button-style'
                      variant='primary'
                      type='submit'
                      style={{marginRight:'1rem'}}
                    >
                      Ingresar
                    </Button>
                  
                    <Button
                      className='button-style'
                      variant='primary'
                      href='/signup'
                    >
                      Registrarse
                    </Button>
                  </div>

                </Form>
              </div>
            </div>
          </Col>
        </Row>

      </Container>

    );
};

export default Login;