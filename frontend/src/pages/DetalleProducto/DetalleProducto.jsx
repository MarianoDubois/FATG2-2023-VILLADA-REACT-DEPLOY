import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import { useAuthStore } from '../../store/auth';
import { getRefreshToken } from '../../utils/auth';
import useAxios from '../../utils/useAxios';
import defaultpicture from '../../assets/images/defaultpicture.png';
import './DetalleProducto.css';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import TextField from '@mui/material/TextField';
import { EventEmitter } from 'events';
import { toast } from 'react-toastify';

<head>
  <link rel="preconnect" href="https://fonts.googleapis.com"></link>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"> </link>
</head>

// Lista de categorías con nombres correspondientes a los IDs
const categorias = [
  { id: 1, nombre: "Electrónica" },
  { id: 2, nombre: "Ropa" },
  // Agrega más categorías según sea necesario
];
export const cartEventEmitter = new EventEmitter();
function DetalleProducto() {
  
  const [observation, setObservation] = useState(''); // Estado para la observación

  const handleObservationChange = (value) => {
    setObservation(value);
  };
  
  const [user] = useAuthStore((state) => [state.user]);
  const userData = user();
  const [posRes, setPostRes] = useState('');
  const [element, setElement] = useState(null);
  const [isVerticalLayout, setIsVerticalLayout] = useState(false);
  const numeroAleatorio = Math.floor(Math.random() * 21) + 5;
  const [quantity, setQuantity] = useState(1);
  const navigate = useNavigate();
  const api = useAxios();
  const { id } = useParams();
  const [disableButton, setDisableButton] = useState('');

  useEffect(() => {
    console.log(userData);
    getElement();
    getStockInfo();
    getStock(); // Agrega esta llamada para obtener el stock
    handleLayoutChange();
    window.addEventListener('resize', handleLayoutChange);
    return () => {
      window.removeEventListener('resize', handleLayoutChange);
    };
  }, [id]);

  const getElement = async () => {
    try {
      const response = await api.get(`/elements/${id}/`);
      console.log(response);
      let data = await response.data;
      setElement(data);
      console.log(userData.user_id);
    } catch (error) {
      console.error(error);
    }
  };

  const getStockInfo = async () => {
    try {
      const stockResponse = await api.get(`/stock/${id}/`); 
      console.log(stockResponse);
    }
    catch (error) {
      console.error(error);
    }
  }

  const getStock = async () => {
    try {
      const stockResponse = await api.get(`/stock/${id}`);
      const stockData = stockResponse.data;
      if (stockData.length > 0) {
        // Tomar el primer valor de current_stock en la respuesta
        const firstStock = stockData[0].current_stock;
        setElement(prevElement => ({ ...prevElement, stock: firstStock }));
      } else {
        // En caso de que no haya datos de stock en la respuesta
        console.warn('No se encontraron datos de stock en la respuesta.');
        setDisableButton('disabled');
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleLayoutChange = () => {
    const isMobileLayout = window.innerWidth < 768;
    setIsVerticalLayout(!isMobileLayout);
  };

  const handleIncrement = () => {
    setQuantity(quantity + 1);
  };

  const handleDecrement = () => {
    if (quantity > 1) {
      setQuantity(quantity - 1);
    }
  };

  const handleSubmit = async (e) => {
    if (e) {
      e.preventDefault();
    }
  
    let body = {
      box: element.id,
      borrower: userData.user_id,
      lender: userData.user_id,
      status: 'CAR',
      quantity: 1,
      observation: observation, 
      dateIn: null,
      dateOut: null,
    };
  
    try {
      const response = await api.post(`/logPost/${userData.user_id}/`, body);
      console.log(response.data);
      setPostRes(response.data.response);
      cartEventEmitter.emit('updateCart');
      navigate('/tienda');
      toast.success('Producto añadido!', { style:{marginTop:'3.5rem', marginBottom:'-2.5rem'} });
    } catch (error) {
      setPostRes(error.response.data);
      toast.error('Este producto ya fue añadido.', { style:{marginTop:'3.5rem', marginBottom:'-2.5rem'} });
    }
  };
  
  
  

  const backButtonStyle = {
    position: 'absolute',
    top: 20,
    left: 5,
  };

  return (
    <div className="container detalleproducto-container" style={{ position: 'relative' }}>
      <div style={backButtonStyle}>
        <Button variant="outline-primary" onClick={() => navigate('/tienda')}>
          <ChevronLeftIcon />
        </Button>
      </div>
      {element && (
      <div className={`row product-details ${isVerticalLayout ? 'vertical-layout' : ''}`}>
        <div className="col-md-6 product-details__image-container">
          <img
            src={element.image || defaultpicture}
            alt="Imagen"
            className="img-fluid product-details__image"
          />
        </div>

    <div className="col-md-6 product-details__info-container">
      <h1 className="product-details__title"> {element.name}</h1>
      <h1 className="product-details__description">Descripción: {element.description}</h1>
      <h1 className="product-details__category">
        Categoría: {element.category.name}
      </h1>
      <h1 className="product-details__stock">
        <span style={{ color: element.stock !== undefined ? '#212529' : 'black' }}>Stock:</span>{' '}
        <span style={{ color: element.stock === undefined ? 'red' : 'black' }}>
          {element.stock !== undefined ? element.stock : 'No disponible'}
        </span>
      </h1>



          {/* Campo de observación */}
          <TextField
            label="Observación"
            variant="outlined"
            fullWidth
            margin="normal"
            color="primary"
            placeholder="Escribe tu observación"
            value={observation}
            onChange={(e) => handleObservationChange(e.target.value)}
            sx={{ width: '80%' }}
          />
          <Button
            className={`botonCarrito ${disableButton}`}
            size="lg"
            style={{ backgroundColor: '#58A4B0', border: '1px solid #58A4B0', left: '5px' }}
            variant="primary"
            type="submit"
            onClick={handleSubmit}>
            Agregar al carrito
          </Button>
          
        </div>
      </div>
    )}

      <div className={`product-details__separator ${isVerticalLayout ? 'vertical-separator' : ''}`}></div>
    </div>
  );
}

export default DetalleProducto;
