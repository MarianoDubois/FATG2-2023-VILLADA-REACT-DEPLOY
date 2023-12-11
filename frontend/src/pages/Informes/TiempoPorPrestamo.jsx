import React, { useState, useEffect } from 'react';
import Card from 'react-bootstrap/Card';
import AccessTimeOutlinedIcon from '@mui/icons-material/AccessTimeOutlined';
import useAxios from '../../utils/useAxios';

const TiempoPorPrestamo = () => {
  const [averageDuration, setAverageDuration] = useState('');
  const axiosInstance = useAxios();

  useEffect(() => {
    axiosInstance
      .get('/estadisticas/avgDate/')
      .then(response => {
        const { average_duration } = response.data;
        setAverageDuration(average_duration);
      })
      .catch(error => {
        console.error('Error al obtener datos:', error);
      });
  }, [axiosInstance]);

  return (
    <Card className='customCard'>
      <Card.Body style={{paddingTop:'9px'}}>
        <div className="d-flex align-items-center" style={{marginBottom:'2px !important'}}>
          <div className="mr-3" style={{ marginRight:'5px'}}>
            <AccessTimeOutlinedIcon sx={{ fontSize: 40 }} style={{ alignSelf: 'center'}} />
          </div>
          <div>
            <h6 style={{ margin: '0', fontSize: '1rem' }}>{averageDuration}</h6>
            <p style={{ margin: '0', fontSize: '0.7rem' }}>Tiempo por préstamo</p>
          </div>
        </div>
      </Card.Body>
    </Card>
  );
};

export default TiempoPorPrestamo;
