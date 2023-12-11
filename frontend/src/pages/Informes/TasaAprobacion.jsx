import React, { useState, useEffect } from 'react';
import ListGroup from 'react-bootstrap/ListGroup';
import useAxios from '../../utils/useAxios';
import AddTaskIcon from '@mui/icons-material/AddTask';

const TasaAprobacion = ({ endpoint }) => {
    const api = useAxios();
    const [approvalRate, setApprovalRate] = useState(null);

    useEffect(() => {
        api.get(endpoint).then((response) => {
            const roundedRate = Math.round(response.data[0].approval_rate * 10) / 10;
            setApprovalRate(roundedRate);
        });
    }, []);

    return (
        <div className="container mt-4">
            <ListGroup as="ul" className='wide'>
                <ListGroup.Item as="li" className='num font-bold'>
                    <span className='icono-tasa'><AddTaskIcon></AddTaskIcon></span>
                    {approvalRate !== null ? `${approvalRate}%` : 'Cargando...'}
                </ListGroup.Item>
                <ListGroup.Item as="li" className="white-text" style={{ color: 'white !important' }}>
    Tasa aprobación
</ListGroup.Item>
            </ListGroup>
        </div>
    );
}

export default TasaAprobacion;

