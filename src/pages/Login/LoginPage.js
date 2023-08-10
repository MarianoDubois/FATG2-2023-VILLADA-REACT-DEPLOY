import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import '../../assets/styles/Login.css';
import { Logo, Login } from '../../components/Form';

const LoginPage = () => {
  return (
    <div>
      <Container>
        <Row>
          <Col xs={12} className="text-xs-center">
            <div className='top-left-image'><Logo/></div>
          </Col>
          <Col className="centered-form">
            <div className="login-container">
              <p className="login-heading"><b>Ingresá tus datos para<br/>iniciar sesión</b></p>
              <div className="login-form">
                <Login />
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default LoginPage;
