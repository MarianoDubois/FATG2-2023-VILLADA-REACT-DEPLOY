import React from 'react';
import {
  MDBCard,
  MDBCardBody,
  MDBCardImage,
  MDBCol,
  MDBRow,
} from "mdb-react-ui-kit";

export default function OrderCard(props) {
  const { id, elementName, image, quantity, dateOut } = props;

  return (
    <MDBCard className="rounded-3 mb-4">
      <MDBCardBody className="p-4">
        <MDBRow className="align-items-center">
          <MDBCol md="2" lg="2" xl="2">
            <MDBCardImage
              className="rounded-3"
              fluid
              src={image}
              alt={elementName}
            />
          </MDBCol>
          <MDBCol md="4" lg="4" xl="4">
            <p className="lead fw-normal mb-0">{elementName}</p>
          </MDBCol>
          <MDBCol md="3" lg="3" xl="3" className="d-flex align-items-center justify-content-around">
            <p className="lead fw-normal mb-0">Cantidad: {quantity}</p>
          </MDBCol>
        </MDBRow>
        <MDBRow className="mt-3">
          <MDBCol>
            <p className="lead fw-normal mb-0">Fecha de devolución: {dateOut}</p>
          </MDBCol>
        </MDBRow>
      </MDBCardBody>
    </MDBCard>
  );
}
