import React, { useState, useEffect } from 'react';
import ListGroup from 'react-bootstrap/ListGroup';

import useAxios from '../../utils/useAxios';
const MostRequestedElements = ({ endpoint }) => {
  const api = useAxios()
  const [elements, setElements] = useState([]);

  useEffect(() => {
    api.get(endpoint).then((response) => {
      setElements(response.data);
    });
  }, []);

  return (  
    <div className="container mt-4">
      <ListGroup as="ul">
        <ListGroup.Item as="li" active className="white-text" style={{ color: 'white !important' }}>
          Elementos más pedidos
        </ListGroup.Item>
        <ListGroup.Item as="li">
          <div className="d-flex justify-content-between align-items-center subheader font-bold">
            <span>Elementos</span>
            <span className="badge badge-primary badge-pill text-dark-black">
              Cantidad
            </span>
          </div>
        </ListGroup.Item>
        {elements.map((element) => (
          <ListGroup.Item key={element.id} as="li">
            <div className="d-flex justify-content-between align-items-center subheader">
              <span>{element.name}</span>
              <span className="badge badge-primary badge-pill text-dark-black margin-span">
                {element.num_borrowed_logs}
              </span>
            </div>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </div>
  );
};

export default MostRequestedElements