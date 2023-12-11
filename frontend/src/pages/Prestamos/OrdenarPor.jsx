import React, { useEffect, useState } from 'react';
import useAxios from '../../utils/useAxios';
import { Dropdown } from 'react-bootstrap';

const OrdenarPorPrestamos = ({ onOrderChange, onSelectedStatus }) => {
  const api = useAxios();
  const [options, setOptions] = useState([]);

  useEffect(() => {
    // Lógica para obtener opciones (si es necesario)
  }, []);

  const handleOrderChange = (orderType) => {
    // Lógica para manejar el cambio de orden
    onOrderChange(orderType);
  };

  const handleStatusChange = (status) => {
    // Lógica para manejar el cambio de orden
    onSelectedStatus(status);
  };
  return (
    <div className="word-list">
      <Dropdown>
        <Dropdown.Toggle
          variant="black"
          id="dropdown-filtros"
          style={{ backgroundColor: 'white', color: 'black' }}
        >
          Ordenar por
        </Dropdown.Toggle>
        <Dropdown.Menu>
          <Dropdown.Item onClick={() => handleOrderChange('fecha')}>Fecha</Dropdown.Item>
          <Dropdown.Item onClick={() => handleOrderChange('componentes')}>Componentes</Dropdown.Item>
          <Dropdown>
            <Dropdown.Toggle
              variant="black"
              id="dropdown-estado"
              style={{ backgroundColor: 'white', color: 'black' }}
            >
              Estado
            </Dropdown.Toggle>
            <Dropdown.Menu>
              <Dropdown.Item onClick={() => onSelectedStatus('AP')}>Aprobado</Dropdown.Item>
              <Dropdown.Item onClick={() => onSelectedStatus('PED')}>Pendiente</Dropdown.Item>
              <Dropdown.Item onClick={() => onSelectedStatus('VEN')}>Vencido</Dropdown.Item>
              <Dropdown.Item onClick={() => onSelectedStatus('DEV')}>Devuelto</Dropdown.Item>
              <Dropdown.Item onClick={() => onSelectedStatus('TAR')}>Devuelto Tardio</Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Dropdown.Menu>
      </Dropdown>
    </div>
  );
};

export default OrdenarPorPrestamos;
