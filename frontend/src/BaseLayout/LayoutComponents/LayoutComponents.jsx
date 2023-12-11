import React, { useState, useEffect, useRef } from 'react';
import { MenuFoldOutlined, MenuUnfoldOutlined, UserOutlined, VideoCameraOutlined } from '@ant-design/icons';
import { Layout, Menu } from 'antd';
import AddModeratorRoundedIcon from '@mui/icons-material/AddModeratorRounded';
import StorageRoundedIcon from '@mui/icons-material/StorageRounded';
import {Dropdown, Badge } from 'antd';
import PaidRoundedIcon from '@mui/icons-material/PaidRounded';
import StoreRoundedIcon from '@mui/icons-material/StoreRounded';
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import { InputGroup, Button } from 'react-bootstrap';
import SearchRoundedIcon from '@mui/icons-material/SearchRounded';
import CachedRoundedIcon from '@mui/icons-material/CachedRounded';
import ShoppingCartOutlinedIcon from '@mui/icons-material/ShoppingCartOutlined';
import AccountCircleRoundedIcon from '@mui/icons-material/AccountCircleRounded';
import NotificationsRoundedIcon from '@mui/icons-material/NotificationsRounded';
import SettingsIcon from '@mui/icons-material/Settings';
import MenuIcon from '@mui/icons-material/Menu';
import MenuRoundedIcon from '@mui/icons-material/MenuRounded';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";
import DataUsageRoundedIcon from '@mui/icons-material/DataUsageRounded';
import DownloadRoundedIcon from '@mui/icons-material/DownloadRounded';
import Tooltip from '@mui/material/Tooltip';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import './LayoutComponents.css';
import itsv from '../../assets/itsv.png';
import { useNavigate } from 'react-router-dom';
import { useMediaQuery } from '@mui/material';
import useAxios from "../../utils/useAxios";
import { useAuthStore } from '../../store/auth';
import { cartEventEmitter } from '../../pages/DetalleProducto/DetalleProducto';
import NotificationsDropdown from './NotificationsDropdown';
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com"></link>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"> </link>
</head>

const { Header, Sider } = Layout;

const LayoutComponents = ({ onSearch, isProfessor }) => {
  const api = useAxios();
  
  const [isReadyForInstall, setIsReadyForInstall] = useState(false);
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(true);
  const [data, setData] = useState([]);
  const [filteredOptions, setFilteredOptions] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [myOptions, setMyOptions] = useState([]);
  const [cantCarrito, setCantCarrito] = useState(0);
  const [cantNotificaciones, setCantNotificaciones] = useState(0);
  const [notificaciones, setNotificaciones] = useState([]);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [isLoggedIn, user] = useAuthStore((state) => [
    state.isLoggedIn,
    state.user,
  ]);
  const userData = user();
  const notificationsRef = useRef();
  const handleToggleNotifications = () => {
    markNotificationsAsRead();
    setIsNotificationsOpen(!isNotificationsOpen);
  };



  useEffect(() => {
    getElement();
    getCantCarrito();
    getCantNotificaciones();
    getNotificaciones();
  }, []);


  useEffect(() => {
    // ... (otras suscripciones y efectos)
    
    // Si el dropdown de notificaciones está abierto, marca las notificaciones como leídas
    if (isNotificationsOpen) {
      markNotificationsAsRead();
    }
  }, [isNotificationsOpen]);
 



 

 const markNotificationsAsRead = async () => {
    try {
      // Realiza la solicitud al endpoint para marcar notificaciones como leídas
      const response = await api.put(`/notificacionesLeidas/${userData.user_id}/`);
      const data = await response.data;
      console.log('Notificaciones marcadas como leídas:', data);

      // Actualiza la cantidad de notificaciones leídas
      getCantNotificaciones();
    } catch (error) {
      console.error('Error al marcar notificaciones como leídas:', error);
    }
  };
  const handleNotificationsVisibleChange = (visible) => {
    // La función handleNotificationsVisibleChange se ejecutará cuando el estado del dropdown cambie (abierto/cerrado)
    if (!visible) {
      // Si el dropdown está cerrado, ejecuta la función para marcar notificaciones como leídas
      markNotificationsAsRead();
    }
  }

  useEffect(() => {
    // Suscríbete al evento del carrito para actualizar la cantidad del carrito
    const updateCart = () => {
      getCantCarrito();
    };

    cartEventEmitter.on('updateCart', updateCart);

    // Limpia la suscripción cuando se desmonta el componente
    return () => {
      cartEventEmitter.off('updateCart', updateCart);
    };
  }, []);

  useEffect(() => {
    window.addEventListener("beforeinstallprompt", (event) => {
      // Prevent the mini-infobar from appearing on mobile.
      event.preventDefault();
      console.log("👍", "beforeinstallprompt", event);
      // Stash the event so it can be triggered later.
      window.deferredPrompt = event;
      // Remove the 'hidden' class from the install button container.
      setIsReadyForInstall(true);
    });
  }, []);

async function downloadApp() {
  console.log("👍", "butInstall-clicked");
  const promptEvent = window.deferredPrompt;
  if (!promptEvent) {
    // The deferred prompt isn't available.
    console.log("oops, no prompt event guardado en window");
    return;
  }
  // Show the install prompt.
  promptEvent.prompt();
  // Log the result
  const result = await promptEvent.userChoice;
  console.log("👍", "userChoice", result);
  // Reset the deferred prompt variable, since
  // prompt() can only be called once.
  window.deferredPrompt = null;
  // Hide the install button.
  setIsReadyForInstall(false);
}
const isSmallScreen = useMediaQuery('(max-width: 950px)');
const isSmallScreen4 = useMediaQuery('(max-width: 950px)');
const isSmallScreen3 = useMediaQuery('(max-width: 950px)');
const isSmallScreen2 = useMediaQuery('(max-width: 950px)');

  const getElement = async () => {
    const proxyUrl = 'http://127.0.0.1:8000';
    let response = await fetch(`${proxyUrl}/api/elementsEcommerce/`);
    let data = await response.json();
    let uniqueOptions = new Set();

    for (var i = 0; i < data.length; i++) {
      uniqueOptions.add(data[i].name);
    }

    let optionsArray = Array.from(uniqueOptions);

    setData(data);
    setMyOptions(optionsArray);
  };

  const handleSearch = (event) => {
    event.preventDefault();
    const searchQuery = event.target.elements.searchBar.value;
    onSearch(searchQuery);
    navigate(`/tienda?searchQuery=${searchQuery}`);
   // console.log(searchQuery)  
  };

  const menu = (
    <Menu>
      {/* Aquí renderizas el contenido del modal */}
      <Menu.Item key="0">
        <NotificationsDropdown notifications={notificaciones}    onClose={() => setIsNotificationsOpen(false)} />
      </Menu.Item>
    </Menu>
  );
   
  const handleToggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  const getCantCarrito = async () => {
    try {
      const response = await api.get(`/cantCarrito/${userData.user_id}/`);
      let data = await response.data;
      console.log(data)
      setCantCarrito(data);
    } catch (error) {
      console.error(error);
    }
  };

  const getCantNotificaciones = async () => {
    try {
      const response = await api.get(`/cantNotificaciones/${userData.user_id}/`);
      const data = await response.data;
      setCantNotificaciones(data);
    } catch (error) {
      console.error(error);
    }
  };

  const getNotificaciones = async () => {
    try {
      const response = await api.get(`/notificaciones/${userData.user_id}/`);
      const data = await response.data;
      setNotificaciones(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      {/* SIDEBAR */}
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        collapsedWidth={0}
        className='sidebar'
      >

        {!collapsed && (
          <Menu theme="light" mode="inline" style={{ background: 'white' }}>
          <Menu.Item
            key="0"
            icon={collapsed ? <MenuIcon style={{ fontSize: '20px' }} /> : <ArrowBackIosIcon style={{ fontSize: '17px' }} />}
            onClick={handleToggleSidebar}
            className={collapsed ? 'menu-icon-collapsed' : 'menu-icon-expanded'}
            style={{ color: 'black',
                     backgroundColor:'transparent' }}
          />
          <Menu.Divider />
          <Menu.Item key="1" icon={<StoreRoundedIcon style={{ fontSize: '20px' }} />} onClick={() => { window.location.href = '/tienda' }}>
            Tienda
          </Menu.Item>
          {isSmallScreen3 && (
                <Menu.Item key="8" icon={<ShoppingCartOutlinedIcon  style={{ fontSize: '20px' }} />} onClick={() => { window.location.href = '/carrito' }}>
                Carrito
              </Menu.Item>
              )}
          <Menu.Item key="2" icon={<CachedRoundedIcon style={{ fontSize: '20px' }} />} onClick={() => { window.location.href = '/Prestamos' }}>
            Préstamo
          </Menu.Item>
    
          {isProfessor && (
              <Menu.Item key="3" icon={<PaidRoundedIcon style={{ fontSize: '20px' }} />} onClick={() => { window.location.href = '/presupuesto' }}>
                Presupuesto
              </Menu.Item>
            )}
            {isProfessor && (
              <Menu.Item key="4" icon={<DataUsageRoundedIcon style={{ fontSize: '20px' }} />} onClick={() => { window.location.href = '/informe' }}>
                Informe
              </Menu.Item>
            )}
            {isProfessor && (
            <Menu.Item key="5" icon={<AddModeratorRoundedIcon style={{ fontSize: '20px' }} />} onClick={() => { window.location.href = 'http://127.0.0.1:8000/admin' }}>
              Admin
            </Menu.Item>
               )}
                
              {isSmallScreen4 && (
                <Menu.Item key="6" icon={<SettingsIcon style={{ fontSize: '20px' }} />} onClick={() => { window.location.href = '/detalleCuenta' }}>
                Cuenta
              </Menu.Item>
              )}
             
           
          <div className='last-elements-sidebar'>
            <Menu.Divider className='divisorsaso'/>   
            <Menu.Item key="7" icon={<DownloadRoundedIcon style={{ fontSize: '20px' }} />} onClick={downloadApp}>
              Descargar App
            </Menu.Item>
            <Menu.Item key="6" icon={<LogoutRoundedIcon style={{ fontSize: '20px' }} />} onClick={() => { window.location.href = '/logout' }}>
              Cerrar sesión
            </Menu.Item>
          </div>
        </Menu>
        )}
      </Sider>

      {/* NAVBAR */}
      <Header >    
        <Row>
          <div className='navbar'>
            <div className='botonesnav1'>
              <Row> 
                <Col>
                  <Button
                    variant="primary"
                    type="submit"
                    className='button'
                    onClick={handleToggleSidebar}
                  >
                    <MenuRoundedIcon style={{ color: 'rgba(235, 235, 235, 0.5)' }} />
                  </Button>
                </Col>

                {!isSmallScreen2 && (
                  <Col>
                    <a href="/">
                      <img src={itsv} alt="itsv" className='logo-img' />
                    </a>   
                  </Col>
                )}  
              </Row>
            </div>
            <Col>
              <form onSubmit={handleSearch}>                
                <Autocomplete
                  className="SearchVisit"      
                  freeSolo
                  options={myOptions}
                  getOptionLabel={(option) => option}
                  value={selectedOption}
                  onChange={(event, newValue) => setSelectedOption(newValue)}
                  renderInput={(params) => (
                    <TextField
                      fullWidth
                      className="SearchVisit"
                      {...params}
                      variant="outlined"
                      name='searchBar'
                      label="Buscar productos"
                      InputLabelProps={{
                        style: { color: 'rgba(235, 235, 235, 0.5)'}  
                      }}
                      InputProps={{
                        style: { color: 'whitesmoke'}
                      }}
                    />
                  )}
                />
              </form>
            </Col>
         
          <div className='botonesnav'>
            <Row>
            <Col>
                { (
               <Tooltip title="Buscar" arrow placement="bottom">
                         <Button variant="primary" type="submit" className='button' style={{borderColor: '#2E5266', color: 'rgba(235, 235, 235, 0.5)' }}>
                           <SearchRoundedIcon />
                         </Button>
                       </Tooltip>
                
              )}
              </Col>
            
                  {!isSmallScreen3 && (
                 <Col>  
                  <Tooltip title="Carrito" arrow placement="bottom">
                    <Button
                      variant="primary"
                      type="submit"
                      className='button'
                      data-toggle="tooltip" data-placement="right" title="Carrito"
                      onClick={() => { window.location.href = '/carrito' }}
                    >
                      <Badge count={parseInt(cantCarrito)} overflowCount={9} size='small' style={{backgroundColor:'#EE8F37'}}>
                        <ShoppingCartOutlinedIcon style={{ color: 'rgba(235, 235, 235, 0.5)' }} />
                      </Badge>
                    </Button>
                  </Tooltip>            
                </Col>
                 )}
          <Col>
                { (
          
                   <Dropdown
        overlay={menu}
        trigger={['click']}
        placement="bottomLeft"
        onVisibleChange={handleNotificationsVisibleChange}
      >
        <Button ref={notificationsRef} variant="primary" className='button'>
          <Badge count={parseInt(cantNotificaciones)} overflowCount={9} size='small' style={{ backgroundColor: '#EE8F37' }}>
            <NotificationsRoundedIcon style={{ color: 'rgba(235, 235, 235, 0.5)' }} />
          </Badge>
        </Button>
      </Dropdown>
              
                
              )}
              </Col>
              {!isSmallScreen4 && (
          <Col>
              
                <Tooltip title="Configuración" arrow placement="bottom">
                  <Button variant="primary" type="submit" className='button'  data-toggle="tooltip" data-placement="right" title="Configuración" onClick={() => { window.location.href = '/detalleCuenta' }}>
                    <SettingsIcon  style={{ color: 'rgba(235, 235, 235, 0.5)' } } />
                  </Button>
                </Tooltip>
             
          </Col>
           )}
             
             </Row>

         </div>

          </div>
        </Row>
        {isNotificationsOpen && (
          <NotificationsDropdown referenceElement={notificationsRef.current} notifications={notificaciones} onClose={() => setIsNotificationsOpen(false)} />
        )}
      </Header>
    </div>       

  );
};

export default LayoutComponents;