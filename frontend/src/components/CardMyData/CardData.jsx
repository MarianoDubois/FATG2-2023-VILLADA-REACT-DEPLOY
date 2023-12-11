import React, { useState, useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import EditRoundedIcon from '@mui/icons-material/Edit';
import CheckRoundedIcon from '@mui/icons-material/CheckRounded';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';
import LaunchRoundedIcon from '@mui/icons-material/Launch';
import Tooltip from '@mui/material/Tooltip';
import axios from 'axios';
import useAxios from "../../utils/useAxios";
import {
  MDBCard,
  MDBCardHeader,
} from 'mdb-react-ui-kit';
import { toast } from 'react-toastify';

export default function CardMyData(props) {
  const api = useAxios();
  const [isEditingEmail, setIsEditingEmail] = useState(false);
  const [isEditingUsername, setIsEditingUsername] = useState(false);
  const [email, setEmail] = useState("");

  const handleEmailChange = async () => {
    let body ={
      email:email
    }
    try {
      const response = await api.put(`/users/${props.id}/update_email/`,body);
      props.updateEmail(email);

      let data = await response.data;
      console.log(data);
      setIsEditingEmail(false)
      
    } catch (error) {
      console.error("EL EMAIL NO ES UN EMAIL");
      toast.error('El email introducido no es válido.', { style:{marginTop:'3.5rem', marginBottom:'-2rem'} }); //PONER ALERT ACA
    }
  };



 
  return (
    <MDBCard className="card-user" alignment='left' border='none'>
      <MDBCardHeader className="card-header">
        Mis Datos
      </MDBCardHeader>

      <Table hover className="card-table">
        <tbody>
          <tr>
            <th scope='col'>Email:</th>
            {!isEditingEmail ? (
              <>
                <td scope='col'>{props.email}</td>
                <td scope='col'>
                  <Tooltip title="Editar" arrow placement="right">
                    <EditRoundedIcon style={{ color: '#2E5266', cursor: 'pointer', fontSize: '0.938rem' }} onClick={() => setIsEditingEmail(true)} />
                  </Tooltip>
                </td>
              </>
            ) : (
              <>
                <td scope='col'>
                  <input
                    type="text"
                    value={email}
                    onChange={(e) => setEmail( e.target.value )}
                  />
                </td>
                <td scope='col'>
                  <Tooltip title="Guardar" arrow placement="right">
                    <CheckRoundedIcon
                      style={{ color: 'green', cursor: 'pointer', fontSize: '0.938rem' }}
                      onClick={handleEmailChange}
                      
                    />
                  </Tooltip>
                  <Tooltip title="Cancelar" arrow placement="right">
                    <CloseRoundedIcon
                      style={{ color: 'red', cursor: 'pointer', fontSize: '0.938rem' }}
                      onClick={() => {
                        setIsEditingEmail(false);
                        setEmail(props.email);
                      }}
                    />
                  </Tooltip>
                </td>
              </>
            )}
          </tr>

          <tr>
            <th scope='col'>Usuario:</th>
          
            <td scope='col'>{props.username}</td>
            <td></td>   
          
    
          </tr>

          <tr>
            <th scope='col'>Contraseña:</th>
            <td scope='col'>**********</td>
            <td scope='col'>
              <Tooltip title="Editar" arrow placement="right">
                <LaunchRoundedIcon onClick={() => { window.location.href = 'http://127.0.0.1:8000/auth/accounts/password_reset' }} style={{ color: '#2E5266', cursor: 'pointer', fontSize: '0.938rem' }} />
              </Tooltip>
            </td>
          </tr>
        </tbody>
      </Table>
    </MDBCard>
  );
}
