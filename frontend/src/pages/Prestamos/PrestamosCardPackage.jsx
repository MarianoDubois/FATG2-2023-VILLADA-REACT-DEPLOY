import React from 'react';
import './PrestamosCard.css';
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
import Card from 'react-bootstrap/Card';


const PrestamosCardPackage = ({ onClick, cliente, dateIn, dateOut, count, name, status, image, lista, user_id }) => {
  const renderComponentList = () => {
    return lista.slice(0, 1).map((item, index) => {
      const componentName = item.box.name.length > 18 ? item.box.name.slice(0, 18) + '...' : item.box.name;
      return (
        <p key={index}>{componentName}</p>
      );
    });
  };

  const moreComponentsMessage = lista.length > 1 ? `+${lista.length - 1} componentes` : null;

  return (
    <div className='prestamo-card' onClick={onClick}>
    <div className="container-fluid">
    <div className="row justify-content-center mb-3">
      <div className="col-md-12 col-xl-10">
        <Card className="shadow-0 border rounded-3 mb-3">
          <div className="card-body">
            <div className="row">
              {/* Column 1 - Photo */}
              <div className="col-md-12 col-lg-3 mb-4 mb-lg-0">
                <div className="bg-image rounded hover-zoom hover-overlay">
                 
                    <MDBCardImage
                      src={image}
                      fluid
                      className="w-60"
                    />
                    <a href="#!">
                      <div
                        className="mask"
                        style={{ backgroundColor: "rgba(251, 251, 251, 0.15)" }}
                      ></div>
                    </a>
                  
                </div>
              </div>

              {/* Column 2 - Name, Status, and Date */}
              <div className="col-md-4">
                <h5>Prestamo de {name}</h5>
                <div className="d-flex flex-row">
                  <div className="text-danger mb-1 me-2">
                    <MDBIcon fas icon="star" />
                  </div>
                </div>
                <div className="mt-1 mb-0 text-muted">
                  <span>
                    <p>Estado: {status}</p>
                  </span>
                </div>
                <span>Fecha: {dateIn}</span>
              </div>

              {/* Column 3 - Components */}
              <div className="col-md-4">
                <span>Cantidad de componentes: {count}</span>
                <div className="d-flex flex-column mt-4">
                  {renderComponentList()}
                  {moreComponentsMessage && <p>{moreComponentsMessage}</p>}
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  </div>

    </div>
  
  );
  
};

export default PrestamosCardPackage;
