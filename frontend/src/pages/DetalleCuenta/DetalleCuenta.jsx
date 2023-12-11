import React, { useEffect, useState } from 'react';
import CardMyData from '../../components/CardMyData/CardData.jsx';
import CardUser from '../../components/CardUser/CardUser.jsx';
import './DetalleCuenta.css';
import useAxios from '../../utils/useAxios';
import { useAuthStore } from '../../store/auth';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Spinner from 'react-bootstrap/Spinner';


function DetalleCuenta() {
  const [isLoggedIn, user] = useAuthStore((state) => [
    state.isLoggedIn,
    state.user,
  ]);
  const [element, setElement] = useState([]);
  const [prestamos, setPrestamos] = useState([]);
  const [specialtiesName, setSpecialtiesName] = useState('');
  const [courseName, setCourseName] = useState('');
  const api = useAxios();
  const userData = user();
  const id = userData.user_id;
  const [loading, setLoading] = useState(true); // Nuevo estado para el Spinner


  const getUser = async () => {
    try {
      setLoading(true); // Inicia el Spinner
      const response = await api.get(`http://127.0.0.1:8000/api/users/${id}/`);
      let data = await response.data;
      console.log(data);
      setElement(data);

      // Use optional chaining to safely access nested properties
      setSpecialtiesName(data.specialties?.join(', '));

      // Use optional chaining for course as well
      setCourseName(data.course?.name);
    } catch (error) {
      console.error(error);
    }finally {
      setLoading(false); // Detiene el Spinner después de la carga
    }
  };

  const getPrestamos = async () => {
    try {
      const response = await api.get(`/prestamosHistorial/${id}/`);
      let data = await response.data;
      console.log(data);
      setPrestamos(data);
    } catch (error) {
     console.log(error)
    }
  };

  useEffect(() => {
    getUser();
    getPrestamos();
  }, []);

  return (
    <div>
          {loading && (
            <div className="d-flex justify-content-center align-items-center vh-100">
              <Spinner animation="border" role="status">
               
              </Spinner>
            </div>
          )}
      
    <Container>
      
      <Row className="mt-4">
        <Col>
          <CardUser
            first_name={element.first_name}
            last_name={element.last_name}
            course={element.course?.grade} 
            specialties = {specialtiesName}
          ></CardUser>
        </Col>
      </Row>
      <Row style={{ marginTop: '2rem' }}>
        <Col>
          <CardMyData
          id={element.id}
            email={element.email}
            username={element.username}
            specialties={specialtiesName}
            updateEmail={(newEmail) => setElement((prevElement) => ({ ...prevElement, email: newEmail }))}
          ></CardMyData>
        </Col>
      </Row>
    </Container>
    </div>


  );
}

export default DetalleCuenta;
