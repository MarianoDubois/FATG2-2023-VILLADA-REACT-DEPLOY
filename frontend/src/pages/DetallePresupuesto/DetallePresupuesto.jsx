import React, { useEffect, useState } from 'react';
import CardMyData from '../../components/CardMyData/CardData.jsx';
import CardUser from '../../components/CardUser/CardUser.jsx';
import './DetallePresupuesto.css';
import useAxios from '../../utils/useAxios.js';
import { useAuthStore } from '../../store/auth.js';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import DataTable from "./DataTable.jsx"
import { useParams, useNavigate } from 'react-router-dom';
import Link from 'antd/es/typography/Link.js';
import {IoCaretBackCircleSharp} from 'react-icons/io5';
import ArrowBackRoundedIcon from '@mui/icons-material/ArrowBackRounded';
import Button from 'react-bootstrap/Button';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';

function DetallePresupuesto() {
  const [isLoggedIn, user] = useAuthStore((state) => [
    state.isLoggedIn,
    state.user,
  ]);
  const [elements, setElements] = useState([]);
  const [presupuesto, setPresupuesto] = useState([]);
  const api = useAxios();
  const userData = user();
  const {id} = useParams();
  const navigate = useNavigate();
  const getElements = async () => {

    try {
      const response = await api.get('elementsEcommerce/');
      let data = await response.data;
      console.log(data);
     setElements(data);

    
    } catch (error) {
      // Manejar errores aquí
      console.error('Error al obtener datos:', error);
     
    }
  };

  const getPresupuesto = async () => {
    try {
      const response = await api.get(`budgetlog/${id}/`);
      let data = await response.data;
      console.log(response)
      setPresupuesto(data);
    } catch (error) {
      console.error(error);
    }
  };

  const updateData = async () => {
    await getPresupuesto();
  };

  useEffect(() => {
    getPresupuesto();
    getElements();
  }, []);
 
 
  return (
    <Container fluid className="text-center mt-4 mb-5" >
      <Row className="justify-content-start mb-1">
        <Col xs={1} >
          <Button variant="outline-primary" onClick={() => navigate('/presupuesto')}>
            <ChevronLeftIcon />
          </Button>
        </Col>
      </Row>
      <Row>
        <Col xs={12}>
          <DataTable presupuesto={presupuesto} onUpdate={updateData} elements={elements} />
        </Col>
      </Row>
    </Container>
  );
}


export default DetallePresupuesto;
