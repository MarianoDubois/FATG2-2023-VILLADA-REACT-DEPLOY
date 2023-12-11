import React, { useState, useEffect } from 'react';
import ListGroup from 'react-bootstrap/ListGroup';
import useAxios from '../../utils/useAxios';
import EventBusyIcon from '@mui/icons-material/EventBusy';

const TasaVencidos = ({ endpoint }) => {
    const api = useAxios();
    const [vencidoPercentage, setVencidoPercentage] = useState(null);

    useEffect(() => {
        api.get(endpoint).then((response) => {
            const roundedRate = Math.round(response.data[0].vencido_percentage * 10) / 10;
            setVencidoPercentage(roundedRate);
        });
    }, []);

    return (
        <div className="container mt-4">
            <ListGroup as="ul" className='wide'>
                <ListGroup.Item as="li" className='num font-bold'>
                    <span className='icono-tasa'><EventBusyIcon></EventBusyIcon></span>
                    {vencidoPercentage !== null ? `${vencidoPercentage}%` : 'Cargando...'}
                </ListGroup.Item>
                <ListGroup.Item as="li" className="white-text" style={{ color: 'white !important' }}>
    Tasa vencidos
</ListGroup.Item>

            </ListGroup>
        </div>
    );
}

export default TasaVencidos;

