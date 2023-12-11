import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './AccesoDenegado.css';
import ITSVlogin from '../../assets/ITSVlogin.svg';
import Item from 'antd/es/list/Item';

function AccesoDenegado() {
  return (
    <div className="container d-flex flex-column align-items-center justify-content-center vh-100">
      <div className="text-center">
        <img
          src={ITSVlogin}
          alt="Logo"
          className="mb-4" // Adjust margin as needed
          style={{ maxWidth: '100%', height: 'auto' }}
        />
        <h1 className="display-4">Error 403</h1>
        <p className="lead">Acceso Denegado</p>
      </div>
    </div>
  );
}

export default AccesoDenegado;
