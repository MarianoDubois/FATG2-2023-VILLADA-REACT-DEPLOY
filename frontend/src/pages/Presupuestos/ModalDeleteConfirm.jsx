import React, { useState, useEffect } from 'react';
import { Modal, Form, Button } from 'react-bootstrap';
import CheckRoundedIcon from '@mui/icons-material/CheckRounded';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';

const ModalDeleteConfirm = ({ onClose, onHandleDeleteConfirm }) => {
  const [title, setTitle] = useState('');
  const [selectedSpecialty, setSelectedSpecialty] = useState('');

 

  return (
    <Modal
      show={true}
      onHide={onClose}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
     <Modal.Header closeButton>
          <Modal.Title>Eliminar Presupuesto</Modal.Title>
        </Modal.Header>
        <Modal.Body>Estas seguro que deseas eliminar este presupuesto?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" style={{backgroundColor:'#FF5151', border:'none'}} onClick={onClose}>
            Cancelar
          </Button>
          <Button variant="danger" style={{backgroundColor:'#3BB273', border:'none'}} onClick={onHandleDeleteConfirm}>
            Continuar
          </Button>
        </Modal.Footer>
    </Modal>
  );
};

export default ModalDeleteConfirm;
