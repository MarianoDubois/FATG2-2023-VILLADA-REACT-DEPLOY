import React from 'react';

import './CardUser.css'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Stack from 'react-bootstrap/Stack';
import PersonRoundedIcon from '@mui/icons-material/PersonRounded';
import {
  MDBCard,
  MDBCardBody,
  MDBCardTitle,
  MDBCardText,
  MDBCardHeader,
  MDBBtn
} from 'mdb-react-ui-kit';

<head>
  <link rel="preconnect" href="https://fonts.googleapis.com"></link>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"> </link>
</head>

export default function CardUser(props) {
  return (
    <MDBCard border='none' style={{ fontSize:'0.938rem', boxShadow:'0 2px 4px rgba(0, 0, 0, 0.05)'}}>
      <MDBCardHeader className='card-header'>Alumno</MDBCardHeader>
      <MDBCardBody>
        <Stack direction='horizontal' gap={4}>
          <div className='p-2'>
            <PersonRoundedIcon style={{fontSize:'5rem'}}></PersonRoundedIcon>
          </div>
          <Stack >
            <div>
              <p style={{fontSize:'1.6rem'}}>{props.last_name} {props.first_name}</p>
            </div>
            <div>
              <p style={{fontSize:'1.25rem'}}>{props.course} Año  </p>
              <p style={{fontSize:'1.25rem'}}>{props.specialties} </p>
            </div>
          </Stack>
        </Stack>
      </MDBCardBody>
    </MDBCard>
  );
}