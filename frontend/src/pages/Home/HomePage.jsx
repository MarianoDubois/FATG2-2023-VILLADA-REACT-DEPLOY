import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './HomePage.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Carousel from 'react-bootstrap/Carousel';
import ClockPage from './ClockPage';
import foto1 from '../../assets/fotarda1.jpg';
import foto2 from '../../assets/fotarda2.jpg';
import img3 from './the-team.jpg';
import { useAuthStore } from '../../store/auth';
import { getCurrentToken } from '../../utils/auth';

function HomePage() {
  const [isLoggedIn, user] = useAuthStore((state) => [
    state.isLoggedIn,
    state.user,
  ]);

  const token = getCurrentToken();
  const userData = user();
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  const [userDetails, setUserDetails] = useState({});

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    window.addEventListener('resize', handleResize);

    // Cleanup event listener on component unmount
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/users/${userData.user_id}/`);
        const userDataApi = await response.json();
        setUserDetails(userDataApi);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    };

    fetchUserData();
  }, [userData.user_id]);

  // Rest of the code remains the same for larger screens
  return (
    <Container className='margen d-flex align-items-center justify-content-center'>
      <Row className='align-items-center justify-content-center'>
        <Col md={12}>
          <div className='margenasos'>
            <h1>Bienvenido {userDetails.first_name} {userDetails.last_name}!</h1>
            <div className="square border border-1 border-dark rounded-pill text-center" style={{ width: "150px" }}>
              <ClockPage />
            </div>
          </div>
        </Col>
        <Row>
          <Col md={12}>
            <div className="carousel-container">
              <Carousel fade indicators={false}>
                <Carousel.Item>
                  <img
                    className="d-block w-100"
                    src="https://www.itsv.edu.ar/itsv/images/panoramicas/c_electricidad.jpg?1699747203772"
                    alt="First slide"
                  />
                </Carousel.Item>
                <Carousel.Item>
                  <img
                    className="d-block w-100"
                    src="https://www.itsv.edu.ar/itsv/images/panoramicas/a_frente.jpg?1699747200027"
                    alt="Second slide"
                  />
                </Carousel.Item>
                <Carousel.Item>
                  <img
                    className="d-block w-100"
                    src={img3}
                    style={{ maxHeight: "100%" }}
                    alt="Third slide"
                  />
                </Carousel.Item>
                {/* Add more Carousel.Item for additional images */}
              </Carousel>
            </div>
          </Col>
        </Row>
      </Row>
    </Container>
  );
}

export default HomePage;
