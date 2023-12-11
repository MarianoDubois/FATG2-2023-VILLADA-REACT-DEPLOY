import React, { useState, useEffect } from 'react';
import Card from 'react-bootstrap/Card';
import PollOutlinedIcon from '@mui/icons-material/PollOutlined';
import useAxios from '../../utils/useAxios';

const DiaDemandado = ({ subtitle }) => {
  const [dateInData, setDateInData] = useState([]);
  const axiosInstance = useAxios();

  useEffect(() => {
    axiosInstance
      .get('/estadisticas/date/')
      .then(response => {
        if (response.data.length > 0) {
          const { dateIn } = response.data[0];

          // Formatear la fecha en el formato "DD/MM"
          const formattedDate = new Date(dateIn).toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
          });

          setDateInData(formattedDate);
        }
      })
      .catch(error => {
        console.error('Error al obtener datos:', error);
      });
  }, [axiosInstance]);

  return (
    <Card className='customCard' style={{marginTop:'12px'}}>
      <Card.Body style={{paddingTop:'9px'}}>
        <div className="d-flex align-items-center">
        <div className="mr-3" style={{ marginRight:'5px'}}>
            <PollOutlinedIcon sx={{ fontSize: 40 }} style={{ alignSelf: 'center' }} />
          </div>
          <div>
            <h6 style={{ margin: '0' }}>{dateInData}</h6>
            <p style={{ margin: '0', fontSize: '0.7rem' }}>{subtitle}</p>
          </div>
        </div>
      </Card.Body>
    </Card>
  );
};

export default DiaDemandado;
