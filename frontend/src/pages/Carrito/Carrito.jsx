import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Carrito.css';
import CartCard from '../../components/cartcard/CartCard';
import Button from 'react-bootstrap/Button';
import ShoppingCartOutlinedIcon from '@mui/icons-material/ShoppingCartOutlined';
import Spinner from 'react-bootstrap/Spinner';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import { toast } from 'react-toastify';
import { MDBCol, MDBContainer, MDBRow } from "mdb-react-ui-kit";
import useAxios from "../../utils/useAxios";
import { useAuthStore } from '../../store/auth';
import { Navigate, useNavigate } from 'react-router-dom';

function Carrito() {
  const api = useAxios();
  const [carrito, setCarrito] = useState([]);
  const [dateInputData, setDateInputData] = useState('');
  const [loading, setLoading] = useState(true);
  const [isLoggedIn, user] = useAuthStore((state) => [
    state.isLoggedIn,
    state.user,
  ]);
  const userData = user()
  const navigate = useNavigate();

  useEffect(() => {
    console.log('SE EJECUTO EL USE')
    getCarrito();
  }, []);

  const getCarrito = async () => {
    try {
      setLoading(true);
      console.log(userData.user_id);
      const response = await api.get(`/carrito/${userData.user_id}`);
      let data = await response.data;
      setCarrito(data);
      console.log(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (log_id) => {
    try {
      await api.delete(`/log/${log_id}`);
      getCarrito();
    } catch (error) {
      console.error(error);
    }
  };

  const handleCommentChange = (id, newComment) => {
    const updatedCart = carrito.map(item => {
      if (item.id === id) {
        return {
          ...item,
          observation: newComment,
        };
      }
      return item;
    });

    setCarrito(updatedCart);
  };

  const handleQuantityChange = (id, newQuantity) => {
    const updatedCart = carrito.map(item => {
      if (item.id === id) {
        return {
          ...item,
          quantity: newQuantity,
        };
      }
      return item;
    });

    setCarrito(updatedCart);
  };

  const handleContinue = async () => {
    if (!dateInputData) {
      toast.warning('Selecciona una fecha de devolución', { style: { marginTop: '3rem', marginBottom: '-2rem' } });
      return;
    }

    try {
      for (const item of carrito) {
        console.log(item);
        const updateData = {
          quantity: item.quantity,
          observation: item.observation,
        };
        console.log(updateData);

        try {
          await api.put(`/logCantidad/${item.id}/`, updateData);

          try {
            const response = await api.put(`/logPost/${userData.user_id}/`, { dateout: dateInputData });
            console.log(response.data.response);
            navigate('/');

          } catch (error) {
            console.log(error);
            toast.warning('Ha ocurrido un error...', { style: { marginTop: '3.5rem', marginBottom: '-2.5rem' } });
          }

          console.log('Actualizaciones exitosas');
          navigate('/');

        } catch (error) {
          console.error('Error al actualizar registros:', error);

        }
      }
      toast.success('Préstamo solicitado!', { style: { marginTop: '3.5rem', marginBottom: '-2.5rem' } });
    } catch (error) {
      console.error('Error en la solicitud PUT:', error);
      toast.warning('No hay stock disponible', { style: { marginTop: '3.5rem', marginBottom: '-2.5rem' } });
    }
  };

  const handleObservationChangeInCartCard = (id, newObservation) => {
    handleCommentChange(id, newObservation);
  };

  return (
    <div>
      {loading && (
        <div className="d-flex justify-content-center align-items-center vh-100">
          <Spinner animation="border" role="status">
          </Spinner>
        </div>
      )}
      {!loading && (
        <section className="container-bg" style={{ fontFamily: 'Roboto, sans-serif' }}>
          <MDBContainer className="h-100">
            <MDBRow className="justify-content-center align-items-center h-100">
              <MDBCol>
                <p style={{ fontSize: '1.563rem' }}>
                  <ShoppingCartOutlinedIcon style={{ marginRight: '0.5rem' }} />
                  Carrito
                </p>

                {carrito.length > 0 ? (
                  carrito.map((item) => (
                    <CartCard
                      key={item.id}
                      id={item.id}
                      name={item.box.name}
                      title={item.box.element.name}
                      image={item.box.image}
                      quantity={item.quantity}
                      comments={item.observation}
                      handleDelete={handleDelete}
                      handleQuantityChange={handleQuantityChange}
                      handleCommentChange={handleObservationChangeInCartCard}
                      current_stock={item.box.current_stock}
                    />
                  ))
                ) : (
                  <p className="text-center">¡Agregá tu próximo pedido! </p>
                )}

                <div className="mb-2 d-flex justify-content-between">
                  <div>
                    <label style={{ marginRight: '0.3rem' }} htmlFor="datetimeInput" className="form-label">
                      Fecha de devolución:
                    </label>

                    <input
                      className='date-style'
                      type="date"
                      name="dateInput"
                      min={new Date().toISOString().split('T')[0]}
                      value={dateInputData}
                      onChange={(e) => setDateInputData(e.target.value)}
                    />
                  </div>
                  <div className="mb-2 d-flex flex-column justify-content-between align-items-center">
                    {dateInputData === '' && (
                      <OverlayTrigger
                        placement="top"
                        overlay={
                          <Tooltip id="tooltip-disabled">
                            Debes establecer una fecha de devolución
                          </Tooltip>
                        }
                      >
                        <span className='siguiente-container'>
                          <Button
                            className='btn-style'
                            onClick={handleContinue}
                            disabled={!dateInputData}
                          >
                            Siguiente
                          </Button>
                        </span>
                      </OverlayTrigger>
                    )}
                    {dateInputData !== '' && (
                      <Button
                        className='btn-style'
                        onClick={handleContinue}
                        disabled={!dateInputData}
                      >
                        Siguiente
                      </Button>
                    )}
                  </div>
                </div>
              </MDBCol>
            </MDBRow>
          </MDBContainer>
        </section>
      )}
    </div>
  );
}

export default Carrito;
