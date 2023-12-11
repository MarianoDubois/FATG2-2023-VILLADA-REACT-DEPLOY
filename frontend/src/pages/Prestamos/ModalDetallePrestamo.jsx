import React, { useState, useEffect } from 'react';
import { Modal } from 'react-bootstrap';
import PrestamosCard from './CardPrestamos';
import CheckRoundedIcon from '@mui/icons-material/CheckRounded';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';

const ModalDetallePrestamo = ({ lista,dateOut, onClose,onHandleApproval ,onHandleRejection,onHandleDevolution,onHandleDestruction,status, isProfessor}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredLista, setFilteredLista] = useState(lista);
  const [selectedCards, setSelectedCards] = useState([]);
  const [showCheckBoxes, setShowCheckBoxes] = useState(false);
  const [quantityInputs, setQuantityInputs] = useState({}); 
  // Función para actualizar la lista filtrada cuando se cambia el término de búsqueda
  useEffect(() => {
    const filtered = lista.filter((element) =>
      element.box.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredLista(filtered);


  }, [searchTerm, lista]);

<head>
  <link rel="preconnect" href="https://fonts.googleapis.com"></link>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"> </link>
</head>

const handleAverioButtonClick = () => {
  // Mostrar cajas solo cuando se hace clic en "Se Averió"
  setShowCheckBoxes(true);

  // Inicializar los inputs de cantidad con los valores predeterminados
  const initialQuantities = {};
  filteredLista.forEach((element, index) => {
    initialQuantities[index] = element.quantity;
  });
  setQuantityInputs(initialQuantities);
};
const handleQuantityChange = (index, value, element) => {
  // Si el valor no es un número o es mayor que el límite, no actualices el estado
  if (isNaN(value) || value > element.quantity || value < 0 || value.includes('-')) {
    return;
  }

  // Actualiza el estado de las cantidades
  setQuantityInputs((prevState) => ({ ...prevState, [index]: value }));
};

const handleCardSelect = (index) => {
  console.log(selectedCards)
  // No hacer nada si las cajas no son clicables
  
  if (!showCheckBoxes) return;

  const isSelected = selectedCards.includes(index);
  if (isSelected) {
    setSelectedCards(selectedCards.filter((selectedIndex) => selectedIndex !== index));
  } else {
    
    setSelectedCards([...selectedCards, index]);
  }
};



const handleConfirmDestruction = () => {
  // Puedes realizar alguna lógica adicional aquí antes de confirmar
  console.log(selectedCards,quantityInputs)
  onHandleDestruction(selectedCards, quantityInputs);
  onClose();
};

 return (
    <Modal id="PrestamoModal" show={true} onHide={onClose} size="lg" contentClassName='custom-modal-content modal-fixed ' >
      <Modal.Header className="d-flex justify-content-between align-items-center" closeButton>
        <div className="d-flex flex-column">
          <Modal.Title>Prestamos:</Modal.Title>
          <input
            type="text"
            placeholder="Buscar Componente..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>
        {isProfessor === true ? (
        <div style={{ paddingLeft: '10%' }} className="d-flex flex-column flex-sm-row align-items-sm-center">
          {status === 'PED' ? (
            <>
              <button className="btn btn-success me-sm-2 mb-2 mb-sm-0" onClick={onHandleApproval}>
                <CheckRoundedIcon /> Confirmar
              </button>
              <button className="btn btn-danger me-sm-2 mb-2 mb-sm-0" onClick={onHandleRejection}>
                <CloseRoundedIcon /> Rechazar
              </button>
            </>
          ) : status === 'AP' ? (
            <>
              <button className="btn btn-success me-sm-2 mb-2 mb-sm-0" onClick={onHandleDevolution}>
                <CheckRoundedIcon /> Se Devolvió
              </button>
              <button className="btn btn-danger me-sm-2 mb-2 mb-sm-0" onClick={handleAverioButtonClick}>
                <CloseRoundedIcon /> Se Averió
              </button>
            </>
          ) : null}
        </div>
      ) : null}
      </Modal.Header>
      <Modal.Body id="modalBody">
        <ul style={{ listStyleType: 'none', padding: 0 }}>
        {showCheckBoxes && (
                     <div className=' d-flex justify-content-center '> 
                      <h3 >Seleccione que elementos se averiaron</h3>
                      </div>

              )}
          {filteredLista.map((element, index) => (
            <div key={index} className="d-flex align-items-center" style={{ marginBottom: '10px' }}>
              <div className='col-xs-1 col-s-4 col-md-11'>
              <PrestamosCard
                status={element.status}
                image={element.box.image}
                component={element.box.name}
                quantity={element.quantity}
              />
              </div>
              <div className='col-xs-10 col-md-2'>
              {showCheckBoxes && (
  <div style={{ marginBottom: '10px', display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
    <input
      type="checkbox"
      checked={selectedCards.includes(index)}
      onChange={() => handleCardSelect(index)}
      style={{ margin: '10px', transform: 'scale(1.5)' }}
    />
    {selectedCards.includes(index) && (
      <div style={{ marginBottom: '10px', display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
        <input
          type="number"
          value={quantityInputs[index]}
          onChange={(e) => handleQuantityChange(index, e.target.value, element)}
          min="0"
          max={element.quantity}
          style={{ marginTop: '10px', width: '50px' }}
        />
       
      </div>
    )}
  </div>

      )}
</div>
            </div>
          ))} 
        </ul>
        
      </Modal.Body>
      <Modal.Footer style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h5>Fecha De Devolucion: {dateOut}</h5>
        <button className="btn btn-secondary me-sm-2 mb-2 mb-sm-0" style={{ backgroundColor: '#58A4B0', border: 'none' }} onClick={onClose}>
          Cerrar
        </button>
        {selectedCards.length > 0 && (
          
         <button className="btn btn-primary me-sm-2 mb-2 mb-sm-0" onClick={handleConfirmDestruction}>

            Continuar
          </button>
        )}
      </Modal.Footer>
    </Modal>
  );
};

export default ModalDetallePrestamo;
