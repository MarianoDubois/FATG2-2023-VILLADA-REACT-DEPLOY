import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import useAxios from '../../utils/useAxios';
import Table from 'react-bootstrap/Table';
import {
  MDBBadge,
  MDBCard,
  MDBCardBody,
  MDBCardTitle,
  MDBCardText,
  MDBCardHeader,
  MDBCardFooter,
  MDBBtn,
  MDBListGroup,
  MDBListGroupItem,
  MDBTable,
  MDBTableHead,
  MDBTableBody,
} from 'mdb-react-ui-kit';
import { useAuthStore } from '../../store/auth';

const CardPendientes = () => {
  const api = useAxios();
  const [element, setElement] = useState([]);
  const [isLoggedIn, user] = useAuthStore((state) => [
    state.isLoggedIn,
    state.user,
  ]);

  useEffect(() => {
    getElement();
  }, []);

  const getElement = async () => {
    try {
      const response = await api.get(`/pendientes/${userData.user_id}`);
      let data = await response.data;
      setElement(data);
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };
  function formatBoxName(name) {
    if (name.length > 14) {
      return name.substring(4, 14) + '...';
    } else {
      return name.substring(4);
    }
  }

  const userData = user();

  // Función para formatear una cadena de fecha y hora en solo fecha
  const formatDate = (datetimeString) => {
    const dateObject = new Date(datetimeString);
    const year = dateObject.getFullYear();
    const month = (dateObject.getMonth() + 1).toString().padStart(2, '0');
    const day = dateObject.getDate().toString().padStart(2, '0');

    return `${year}-${month}-${day}`;
  };

  return (
    <MDBCard alignment='left' style={{ backgroundColor: 'white', border: 'none', width: '33%', minHeight: '35vh', maxHeight: '50vh', minWidth: '50vh' }}>       
     <MDBCardHeader style={{ color: 'white' }}>Pendientes</MDBCardHeader>
      <Table hover style={{ marginBottom: '0', height: '100%' }}>
        <thead>
          <tr>
            <th scope='col'>Fecha</th>
            <th scope='col'>Producto</th>
            <th scope='col'>Cantidad</th>
          </tr>
        </thead>
        <tbody>
        </tbody>
      </Table>
    </MDBCard>
  );
};

export default CardPendientes;
