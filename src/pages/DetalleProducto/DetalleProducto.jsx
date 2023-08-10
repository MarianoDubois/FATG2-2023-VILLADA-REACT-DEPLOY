import PropTypes from 'prop-types';
import { useParams } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
import defaultpicture from '../../assets/images/defaultpicture.png';
import './DetalleProducto.css';
import Button from 'react-bootstrap/Button';


function DetalleProducto() {
  const elementId = useParams();
  const [element, setElement] = useState(null);
  const [isVerticalLayout, setIsVerticalLayout] = useState(false);
  const numeroAleatorio = Math.floor(Math.random() * 21) + 5;

  useEffect(() => {
    getElement();
    handleLayoutChange(); // Verificar el diseño inicial al cargar el componente
    window.addEventListener('resize', handleLayoutChange); // Manejar cambios de diseño en el redimensionamiento de la ventana
    return () => {
      window.removeEventListener('resize', handleLayoutChange); // Limpiar el event listener al desmontar el componente
    };
  }, [elementId]);

  const getElement = async () => {
    const proxyUrl = 'http://127.0.0.1:8000';
    let response = await fetch(`${proxyUrl}/api/elements/${elementId.id}/`);
    let data = await response.json();
    setElement(data);
  };

  const handleLayoutChange = () => {
    const isMobileLayout = window.innerWidth < 768;
    setIsVerticalLayout(!isMobileLayout);
  };
  const [quantity, setQuantity] = useState(1);

  const handleIncrement = () => {
    setQuantity(quantity + 1);
  };

  const handleDecrement = () => {
    if (quantity > 1) {
      setQuantity(quantity - 1);}
    };

  return (
    <div className='container pagecontainer'>
      {element && (
        <div className={`row product-details ${isVerticalLayout ? 'vertical-layout' : ''}`}>
          <div className='col-md-6 product-details__image-container'>
            <img
              src={element.image || defaultpicture}
              alt='Imagen'
              className='img-fluid product-details__image'
            />
          </div>
          
          <div className='col-md-6 product-details__info-container' style={{ width: '45%' }}>
            <h1 className='product-details__title'>Nombre: {element.name}</h1>
            <h1 className='product-details__description'>Descripción: {element.description}</h1>
            <h1 className='product-details__category'>Categoría: {element.category}</h1>
            <h1 className='product-details__stock'>Stock:20</h1>
          
          <div className="input-group input-group-sm"> {/* Utilizar input-group-sm para un tamaño más pequeño */}
            <span className="input-group-btn">
           <Button variant="secondary" size="sm" onClick={handleDecrement}>-</Button> {/* Utilizar size="sm" para un tamaño más pequeño */}
          </span>
          <input type="number" className="form-control form-control-sm" value={quantity} readOnly /> {/* Utilizar form-control-sm para un tamaño más pequeño */}
         <span className="input-group-btn">
           <Button variant="secondary" size="sm" onClick={handleIncrement}>+</Button> {/* Utilizar size="sm" para un tamaño más pequeño */}
          </span>
          </div>
            <Button className='botonCarrito ' size='lg' style={{ backgroundColor: '#58A4B0', border: '1px solid #58A4B0'}} variant="primary" type="submit">
                Agregar al carrito
          </Button>
        
          </div>
        </div>
      )}
      <div className={`product-details__separator ${isVerticalLayout ? 'vertical-separator' : ''}`}></div>
    </div>
  );
}

DetalleProducto.propTypes = {};

export default DetalleProducto;
