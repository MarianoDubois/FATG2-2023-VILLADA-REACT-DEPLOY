// CardPrestamos.jsx
import React from 'react';
import './PrestamosCard.css'; // Importa tu archivo CSS
import {
  MDBCard,
  MDBCardBody,
  MDBCardImage,
  MDBRow,
  MDBCol,
  MDBIcon,
  MDBRipple,
  MDBBtn, 
} from 'mdb-react-ui-kit';
const PrestamosCard = ({ status,image, cliente,component,quantity}) => {
  return (
    <div className='prestamo-card'>
        <div className='img-container'>
      <MDBRow className="justify-content-center mb-0">
        <MDBCol md="12" xl="10">
          <MDBCard className="shadow-0 border rounded-3 mt-5 mb-3">
            <MDBCardBody>
              <MDBRow>
                <MDBCol md="12" lg="3" className="mb-4 mb-lg-0">
                  <MDBRipple
                    rippleColor="light"
                    rippleTag="div"
                    className="bg-image rounded hover-zoom hover-overlay">
                    <MDBCardImage
                      src={image}
                      fluid
                      className="w-100"
                    />
                    <a href="#!">
                      <div
                        className="mask"
                        style={{ backgroundColor: "rgba(251, 251, 251, 0.15)" }}
                      ></div>
                    </a>
                  </MDBRipple>
                </MDBCol>
                <MDBCol md="6">
                 
                  <div className="d-flex flex-row">
                    <div className="text-danger mb-1 me-2">
                     
                      
                    </div>
                  </div>
                  <div className="mt-1 mb-0 text-muted">
                    <span><p>Estado: {status}</p></span>
                    
                  </div>
                    

                    

                    <span>
                      Componente:{component}
                      <br />
                    </span>
                    <span>
                      Cantidad:{quantity}
                      <br />
                    </span>
                    <div>
                 
                  </div>
                </MDBCol>
               
              </MDBRow>
            </MDBCardBody>
          </MDBCard>
        </MDBCol>
      </MDBRow>
      
      </div>
    </div>
  );
};

export default PrestamosCard;



