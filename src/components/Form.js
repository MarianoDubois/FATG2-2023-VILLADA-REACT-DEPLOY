import React from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import '../assets/styles/Login.css'

export function Logo() {
  return (
    <div style={{ display: "block", width: 300, padding: 20 }}>
      <img src={require('../assets/img-prod/logo.png')} className='img-fluid logo' alt='...' />
    </div>
  );
}

export function Login() {
  const containerStyle = {
    marginTop: '20px', // Adjust the top margin as needed
  };
  return (
    <Form>
      <Form.Group className="mb-3" controlId="formBasicEmail">
        <Form.Label className='color'>Email address*</Form.Label>
        <Form.Control type="email" placeholder="" style={{ backgroundColor: '#EBEBEB', border: '1px solid #2E5266'}} className="rounded-3 shadow form-control-lg"/>
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
        <Form.Label className='color'>Password*</Form.Label>
        <Form.Control type="password" placeholder="" style={{ backgroundColor: '#EBEBEB', border: '1px solid #2E5266'}} className="rounded-3 shadow form-control-lg" />
      </Form.Group>
      <div>
          <div className='text-center'>
              <a href="#" className="link-dark text-decoration-none">Olvidaste tu contraseña?</a>
            </div>
          <div className='text-center' style={containerStyle}>
              <Button className='text-center rounded-5 ' size='lg' style={{ backgroundColor: '#58A4B0', border: '1px solid #58A4B0'}} variant="primary" type="submit">
                Ingresar
          </Button>
        </div>
      </div>
    </Form>
  );
}

