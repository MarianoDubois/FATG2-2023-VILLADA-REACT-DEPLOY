import React, { useState,useEffect } from 'react';
import Table from 'react-bootstrap/Table';
import {
  MDBCard,
  MDBCardHeader,
} from 'mdb-react-ui-kit';
import { useNavigate } from 'react-router-dom';
import ReactPaginate from 'react-paginate';
import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded';
import { AiFillQuestionCircle } from "react-icons/ai";
import useAxios from '../../utils/useAxios';
import { HiPlusCircle, HiPencil,HiOutlineXMark,HiMiniCheck } from "react-icons/hi2";
import Tooltip from 'react-png-tooltip';
import ModalNewPresupuesto from './ModalNewPresupuesto';
import ModalDeleteConfirm from './ModalDeleteConfirm';
import './DataTable.css';
import KeyboardArrowLeftRoundedIcon from '@mui/icons-material/KeyboardArrowLeftRounded';
import KeyboardArrowRightRoundedIcon from '@mui/icons-material/KeyboardArrowRightRounded';
import { toast } from 'react-toastify';


const DataTable = ({ presupuestos , specialties,setShouldRefresh}) => {
  let api = useAxios();
  const navigate = useNavigate();
  const handleRowClick = (presupuestoId, event) => {
    // Check if the click occurred on the button
    const isButtonClick =
    event.target.tagName === 'BUTTON' || event.target.closest('button');
    console.log(event.target.tagName)
    // If it's a button click, don't navigate
    if (isButtonClick) {
      console.log("Es un boton")
      return;
    }
  
    // Navigate to the details page
    navigate(`${presupuestoId}`);
  }
  
  const itemsPerPage = 10;
  const [currentPage, setCurrentPage] = useState(0);
  const [sortColumn, setSortColumn] = useState(null);
  const [postRes, setPostRes] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isModalDeleteConfirmOpen, setIsModalDeleteConfirmOpen] = useState(false);
  const [sortDirection, setSortDirection] = useState('asc');
  
  const [selectedBudget, setSelectedBudget] = useState(null);

  const getRowTextColor = (estado) => {
    if (estado === "PROGRESO") {
      return "text-warning"; // Amarillo
    } else if (estado === "COMPLETADO") {
      return "text-success"; // Verde
    }
    return ""; // El color de texto predeterminado
  };


  const closeModal = () => {
    setIsModalOpen(false)
  }

  const closeModalDeleteConfirm = () => {
    setIsModalDeleteConfirmOpen(false)
  }

  
    const handleDeleteConfirm = async () => {
    try {
     // Inicia el Spinner

      const response = await api.delete(`/budget/${selectedBudget}`);
      let data = await response.data;
      console.log(data)
      setShouldRefresh(true);
      toast.success('Presupuesto eliminado.', { style:{marginTop:'3.5rem', marginBottom:'-2.5rem'} });
    } catch (error) {
      console.error(error);
      toast.error('Ha ocurrido un error...', { style:{marginTop:'3.5rem', marginBottom:'-2.5rem'} });
  };



    setIsModalDeleteConfirmOpen(false)
  }

  const handleDeleteConfirmProgress = (budgetId) => {
    setSelectedBudget(budgetId)
    setIsModalDeleteConfirmOpen(true)
  }



  

  

  const handleNewBudget = async (title, selectedSpecialty) => {
    console.log(title,selectedSpecialty)
    // Define los datos del nuevo presupuesto
    const newBudgetData = {
      name: title, // Utiliza el título proporcionado
      status: "PROGRESO", // O "COMPLETADO" según sea necesario
      speciality: selectedSpecialty, // Utiliza la especialidad seleccionada
    };

    try {
      // Realiza la solicitud POST para crear un nuevo presupuesto
      const response = await api.post('/budget/', newBudgetData);
      const newBudgetId = response.data.id;

      // Muestra la respuesta del servidor en la consola
      console.log(response.data);

      // Realiza una acción de redirección a '/tienda' o ajusta según sea necesario
      navigate(`${newBudgetId}`);
      toast.success('Presupuesto creado!', { style:{marginTop:'3.5rem', marginBottom:'-2.5rem'} });
    } catch (error) {
      // En caso de error, muestra el mensaje de error en la consola
      console.error(error);
      toast.error('Ha ocurrido un error...', { style:{marginTop:'3.5rem', marginBottom:'-2.5rem'} });
      // Puedes manejar el error y mostrar un mensaje de error al usuario si es necesario
    }
  };
  const handlePageClick = ({ selected }) => {
    setCurrentPage(selected);
  };

  const offset = currentPage * itemsPerPage;

  // Función para ordenar los datos en función del estado de clasificación y la columna seleccionada
  const sortedData = () => {
    if (!sortColumn) {
      return presupuestos.slice(offset, offset + itemsPerPage);
    }
    
    return [...presupuestos].sort((a, b) => {
      const valueA = a[sortColumn];
      const valueB = b[sortColumn];

      if (valueA < valueB) {
        return sortDirection === 'asc' ? -1 : 1;
      }
      if (valueA > valueB) {
        return sortDirection === 'asc' ? 1 : -1;
      }
      return 0;
    }).slice(offset, offset + itemsPerPage);
  };

  // Función para cambiar el filtro de clasificación
  const handleSortChange = (column) => {
    if (column === sortColumn) {
      // Si hacemos clic en la misma columna, cambia la dirección de ordenamiento
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // Si hacemos clic en una nueva columna, establece la columna y la dirección de ordenamiento predeterminada (ascendente)
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  return (
    <MDBCard className="my-4 p-3" >
     <MDBCardHeader style={{fontSize:"2rem"}} className="sub-blue-its text-white d-flex justify-content-between align-items-center">
        <div>
          <span>Presupuestos</span>
          <Tooltip tooltip={<AiFillQuestionCircle style={{marginLeft:'10px'}}></AiFillQuestionCircle>}>
            Para editar hacer click en la fila del presupuesto.
        </Tooltip>
        </div>
          
        <div className="hover-scale" onClick={()=> setIsModalOpen(true)}>
          <HiPlusCircle data-toggle="tooltip" data-placement="right" title="Agregar presupuesto"/>
        </div>
      </MDBCardHeader>

      <Table responsive striped bordered hover className="mt-3 table-responsive">
        <thead>
          <tr>
            <th scope='col' onClick={() => handleSortChange('id')} className='col-1'>
              ID {sortColumn === 'id' && (sortDirection === 'asc' ? '▲' : '▼')} 
            </th>
            <th scope='col' onClick={() => handleSortChange('name')} className='col-7'>
              Nombre {sortColumn === 'name' && (sortDirection === 'asc' ? '▲' : '▼')}
            </th>
            <th scope='col' onClick={() => handleSortChange('status')}c lassName='col-1'>
              Estado {sortColumn === 'status' && (sortDirection === 'asc' ? '▲' : '▼')}
            </th>
            <th scope='col' onClick={() => handleSortChange('speciality.name')} className='col-2'>
              Especialidad {sortColumn === 'speciality.name' && (sortDirection === 'asc' ? '▲' : '▼')}
            </th>
            <th scope='col' onClick={() => handleSortChange('speciality.name')} className='col-1'>
              
            </th>
          </tr>
        </thead>
        <tbody>
          {sortedData().map((presupuesto) => (
            <tr
              key={presupuesto.id}
              onClick={(event) => handleRowClick(presupuesto.id, event)}
              className={`cursor-pointer`}
            >
              <td className='text-center'>{presupuesto.id}</td>
              <td>{presupuesto.name}</td>
              <td className={`progress-abbreviate ${getRowTextColor(presupuesto.status)}`}>{presupuesto.status}</td>
              <td className='text-center'>{presupuesto.speciality.name !== null ? presupuesto.speciality.name : ' '}</td>
              <td className="text-center">
                <button className="btn btn-sm btn-block ml-2" style={{backgroundColor:'#FF5151', color:'white'}} onClick={() => handleDeleteConfirmProgress(presupuesto.id)}>
                  <HiOutlineXMark />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
      <div className="pagination justify-content-center">
        <ReactPaginate
          activeClassName={'active'}
          breakClassName={'item break-me'}
          previousLabel={<KeyboardArrowLeftRoundedIcon style={{color:'#2E5266'}}/>}
          nextLabel={<KeyboardArrowRightRoundedIcon style={{color:'#2E5266'}}/>}
          breakLabel={'...'}
          pageCount={Math.ceil(presupuestos.length / itemsPerPage)}
          marginPagesDisplayed={2}
          pageRangeDisplayed={5}
          onPageChange={handlePageClick}
          containerClassName={'pagination'}
          pageClassName={'item pagination-page'}
          previousClassName={"item previous"}
          nextClassName={"item"}
        />
      </div>
      {isModalOpen && (
        <ModalNewPresupuesto
        onHandleNewBudget={handleNewBudget} // Sin función anónima
        specialties={specialties}
        onClose={closeModal}
        />
      )}
      {isModalDeleteConfirmOpen && (
        <ModalDeleteConfirm
        onHandleDeleteConfirm={handleDeleteConfirm} // Sin función anónima
        onClose={closeModalDeleteConfirm}
        />
      )}
    </MDBCard>
  );
};

export default DataTable;
