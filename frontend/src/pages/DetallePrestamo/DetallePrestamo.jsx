import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './DetallePrestamo.css';
import OrderCard from '../../components/ordercard/OrderCard';
import {
  MDBCol,
  MDBContainer,
  MDBRow,
} from "mdb-react-ui-kit";
import useAxios from "../../utils/useAxios";
import { useAuthStore } from '../../store/auth';
import { Navigate, useNavigate } from 'react-router-dom';

function DetallePrestamo() {
  const api = useAxios();
  const [orders, setOrders] = useState([]);
  const [isLoggedIn, user] = useAuthStore((state) => [
    state.isLoggedIn,
    state.user,
  ]);
  const userData = user();
  const navigate = useNavigate();

  useEffect(() => {
    console.log('SE EJECUTÓ EL USE');
    getOrders();
  }, []);

  const handleApproval = async () => {
    try {
      // Realiza una solicitud PUT para aprobar los registros del usuario en el servidor
      await api.put(`/aprobadoPost/${userData.user_id}/`);
      // Vuelve a cargar los préstamos actualizados después de la aprobación
      getOrders();
    } catch (error) {
      console.error(error);
    }
  };
  
  const handleRejection = async () => {
    try {
      // Realiza una solicitud PUT para rechazar los registros del usuario en el servidor
      await api.put(`/desaprobadoPost/${userData.user_id}/`);
      // Vuelve a cargar los préstamos actualizados después del rechazo
      getOrders();
    } catch (error) {
      console.error(error);
    }
  };
  

  const getOrders = async () => {
    try {
      console.log(userData.user_id);
      const response = await api.get(`/pendientes/${userData.user_id}`);
      let data = await response.data;
      setOrders(data);
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <section className="container-bg" style={{ backgroundColor: "white" }}>
      <MDBContainer className="h-100">
        <MDBRow className="justify-content-center align-items-center h-100">
          <MDBCol>
            <p>
              <span className="h2">Prestamos pendientes:</span>
            </p>

            {/* Render OrderCard components */}
            {orders.map(order => (
              <OrderCard
                key={order.id}
                id={order.id}
                boxName={order.box.name}
                elementName={order.box.element.name}
                image={order.box.element.image}
                quantity={order.quantity}
                dateOut={order.dateOut}
                // Include any other necessary props
              />
            ))}

            {/* Botones de confirmar y rechazar */}
            <div className="d-flex justify-content-end align-items-center mt-3">
              <button className="btn btn-success me-2" onClick={handleApproval}>
                <span role="img" aria-label="Checkmark">✅</span> Confirmar
              </button>
              <button className="btn btn-danger" onClick={handleRejection}>
                <span role="img" aria-label="Cross">❌</span> Rechazar
              </button>
            </div>
          </MDBCol>
        </MDBRow>
      </MDBContainer>
    </section>
  )
}

export default DetallePrestamo;
