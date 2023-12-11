

import React, { useState, useEffect } from 'react';
import PrestamosCardPackage from './PrestamosCardPackage';
import useAxios from '../../utils/useAxios';
import './Prestamos.css';
import OrdenarPorPrestamos from './OrdenarPor';
import { useAuthStore } from '../../store/auth';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Spinner from 'react-bootstrap/Spinner';
import SearchRoundedIcon from '@mui/icons-material/SearchRounded';
import { TextField } from "@mui/material";
import Button from 'react-bootstrap/Button';
import InputAdornment from '@mui/material/InputAdornment';
import Pagination from '../../components/pagination/Paginacion';
import ModalDetallePrestamo from './ModalDetallePrestamo';


<head>
  <link rel="preconnect" href="https://fonts.googleapis.com"></link>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"> </link>
</head>
const Prestamos = ({ isProfessor }) => {
  const [user] = useAuthStore((state) => [state.user]);
  const userData = user();
  const api = useAxios();
  const [data, setData] = useState([]);
  const [selectedPackage, setSelectedPackage] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [finalSearchTerm, setFinalSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(1);
  const pageSize = 10;
  const [selectedStatus, setSelectedStatus] = useState("");

  useEffect(() => {
    if (isProfessor !== null) {
      getPrestamos();
    }
  }, [page, finalSearchTerm, selectedStatus]);

  useEffect(() => {
    if (isProfessor !== null) {
      getPrestamos();
    }
  }, [isProfessor]);

  const handleStatusFilter = async () => {
    try {
      if (selectedStatus) {
        const endpoint = `/filtroStatusPrestamos/${selectedStatus}/?page=${page}`;
        const response = await api.get(endpoint);
        console.log(response.data);
        setData(response.data.results);
        setCount(response.data.count);
      }
    } catch (error) {
      console.error(error);
    }
  };
  const handleStatusChange = (status) => {
    setSearchTerm("")
    setSelectedStatus(status);
    // Puedes realizar alguna acción adicional aquí si es necesario
  };

  const handleOrderChange = (orderType) => {
    // Lógica para manejar el cambio de orden
    // Aquí puedes actualizar el estado según el tipo de orden
    // Puedes cambiar la lógica según tus necesidades
    console.log("Orden cambiado:", orderType);
  };

  const handleApproval = async (dateIn, packageUserId) => {
    try {
      await api.put(`/aprobadoPost/${packageUserId}/${dateIn}/`);
      getPrestamos();
      closeModal();
      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  const handleSearch = () => {
    setSelectedStatus("")
    setFinalSearchTerm(searchTerm);
    setPage(1);
    getPrestamos();
  };

  const HandleDevolution = async (dateIn, packageUserId) => {
    try {
      await api.put(`/devueltoPost/${packageUserId}/${dateIn}/`);
      getPrestamos();
      closeModal();
      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  const HandleDestruction = async (selectedPackage, selectedCards, quantityInputs) => {
    try {
      for (const selectedIndex of selectedCards) {
        const element = selectedPackage.lista[selectedIndex];
        const quantityDestroyed = quantityInputs[selectedIndex] || 0;
        const fechaDevuelto = new Date().toISOString().split('T')[0];
        const fechaDevueltoHora = new Date().toISOString().slice(0, 16).replace('T', ' ');

        const logData = {
          box_id: element.box.id,
          borrower_id: element.borrower.id,
          lender_id: element.lender.id,
          status: 'ROT',
          quantity: quantityDestroyed,
          observation: `Item Averiado en la fecha ${fechaDevueltoHora}`,
          dateIn: selectedPackage.dateIn,
          dateOut: fechaDevuelto,
        };

        await api.post('/log/', logData);
      }

      try {
        console.log("Ahora devolviendo todo")
        HandleDevolution(selectedPackage.dateIn, selectedPackage.id_user);
      } catch (error) {
        console.error(error);
        setIsLoading(false);
      }

      closeModal();
      setIsLoading(false);

    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  const handleRejection = async (dateIn, packageUserId) => {
    try {
      await api.put(`/desaprobadoPost/${packageUserId}/${dateIn}/`);
      getPrestamos();
      closeModal();
      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  const getPrestamos = async () => {
    try {
      let endpoint;
      if ((finalSearchTerm === "" || searchTerm === "" || !finalSearchTerm )&&(selectedStatus === "")) {
        if (isProfessor) {
          endpoint = `/allPrestamos/?page=${page}`;
        } else {
          endpoint = `/prestamosHistorial/${userData.user_id}/?page=${page}`;
        }
      } else {
        if (isProfessor) {
          endpoint = `/buscadorPrestamo/${searchTerm}/?page=${page}`;
        }
      }

      // Aquí puedes agregar la lógica para ordenar según el estado seleccionado
      if (selectedStatus) {
        if (isProfessor) {
          endpoint = `/filtroStatusPrestamos/${selectedStatus}/?page=${page}`;

        }
        else{
        endpoint = `/filtroStatusPrestamos/${selectedStatus}/${userData.user_id}/?page=${page}`;}
      }

      const response = await api.get(endpoint);
      if (response.data === "No se encontraron logs para este usuario.") {
        setData([]);
      } else {
        const data = response.data.results;
        setCount(response.data.count);
       
        setData(data);
      }

      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
    }
  };

  const openModal = (packageData) => {
    setSelectedPackage(packageData);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setSelectedPackage(null);
    setIsModalOpen(false);
  };

  return (
    <div className="tratandodecentrar">
      {!isLoading ? (
        <Container>
          <Col>
            {/* Search Bar */}
            <Row className="col-md-12">
              <Col md="auto">
                <div className="mr-12 mt-4">
                  <OrdenarPorPrestamos onOrderChange={handleOrderChange} onSelectedStatus={handleStatusChange} />
                </div>
              </Col>
              {isProfessor === true && (
                <Col>
                  <div className="d-flex align-items-center mt-4">
                    <TextField
                      fullWidth
                      id="SearchVisit"
                      variant="outlined"
                      label="Buscar Por Nombre De Alumno o Username"
                      className="SearchVisit"
                      inputProps={{ value: searchTerm }}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <Button variant="outline-secondary" onClick={() => handleSearch()}>
                              <SearchRoundedIcon />
                            </Button>
                          </InputAdornment>
                        ),
                      }}
                    />
                  </div>
                </Col>
              )}
            </Row>
            
            {/* Prestamos Cards */}
            <Row className="mt-4">
              <div>
                {data.length > 0 ? (
                  data.map((prestamo, index) => (
                    <PrestamosCardPackage
                      onClick={() => openModal(prestamo)}
                      key={index}
                      image={prestamo.imagen}
                      status={prestamo.estado}
                      name={prestamo.nombre}
                      dateIn={prestamo.dateIn}
                      dateOut={prestamo.dateOut}
                      count={prestamo.count}
                      lista={prestamo.lista}
                      user_id={prestamo.id_user}
                    />
                  ))
                ) : (
                  <p className='d-flex justify-content-center'>No hay préstamos disponibles.</p>
                )}
              </div>
            </Row>
  
            <div className="d-flex justify-content-center mt-4">
              <Pagination
                totalRecords={count}
                pageLimit={pageSize}
                pageNeighbours={1}
                currentPage={page}
                onPageChanged={setPage}
              />
            </div>
  
            <Row>
              {isModalOpen && (
                <ModalDetallePrestamo
                  onHandleApproval={() => handleApproval(selectedPackage.dateIn, selectedPackage.id_user)}
                  onHandleRejection={() => handleRejection(selectedPackage.dateIn, selectedPackage.id_user)}
                  onHandleDevolution={() => HandleDevolution(selectedPackage.dateIn, selectedPackage.id_user)}
                  onHandleDestruction={(selectedCards, quantityInputs) =>
                    HandleDestruction(selectedPackage, selectedCards, quantityInputs)
                  }
                  dateOut={selectedPackage.dateOut}
                  lista={selectedPackage.lista}
                  onClose={closeModal}
                  isProfessor={isProfessor}
                  status={selectedPackage.estado}
                />
              )}
            </Row>
          </Col>
        </Container>
      ):( <div className="d-flex justify-content-center align-items-center vh-100">
      <Spinner animation="border" role="status"></Spinner>
    </div>)}
    </div>
  );
  
};

export default Prestamos;
