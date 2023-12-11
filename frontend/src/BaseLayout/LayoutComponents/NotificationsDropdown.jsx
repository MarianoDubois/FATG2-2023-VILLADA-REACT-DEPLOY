// NotificationsDropdown.jsx
import {React, useEffect,useState} from 'react';
import { List, Avatar } from 'antd';
import NotificationsRoundedIcon from '@mui/icons-material/NotificationsRounded';
import KeyboardReturnRoundedIcon from '@mui/icons-material/KeyboardReturnRounded';
import CheckBoxRoundedIcon from '@mui/icons-material/CheckBoxRounded';
import CancelRoundedIcon from '@mui/icons-material/CancelRounded';
import './NotificationsDropdown.css'; // Agrega un archivo de estilos para este componente
import styled from '@emotion/styled';

const NotificationsDropdown = ({ notifications,referenceElement, onClose }) => {
    const [position, setPosition] = useState({ top: 0, left: 0 });
    useEffect(() => {
      // Log sorted notifications
      const sortedNotifications = notifications.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      console.log(sortedNotifications);
  
      if (referenceElement) {
          const rect = referenceElement.getBoundingClientRect();
          const dropdownWidth = 350;
          setPosition({
              top: rect.bottom + window.scrollY,
              left: rect.left - dropdownWidth + window.scrollX,
          });
      }
  }, [referenceElement, notifications]);
  

      // Example timestamp formatting function
      const formatTimestamp = (timestamp) => {
        const date = new Date(timestamp);
      
        // Get date components
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = String(date.getFullYear()).slice(-2);
      
        // Get time components
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
      
        // Format: DD/MM/YY\nHH:mm (with a line break between date and time)
        return `${day}/${month}/${year}\n${hours}:${minutes}`;
      };
      

const getNotificationIcon = (type) => {
  const iconWrapperStyle = {
    alignItems: 'center',
    justifyContent: 'center',
    height: '100%', // Ensure the wrapper takes the full height
  };

  switch (type) {
    case 'DV':
      return(<div style={iconWrapperStyle}> <KeyboardReturnRoundedIcon /></div>); // Replace with the actual arrow icon component
    case 'PD':
      return(<div style={iconWrapperStyle}> <NotificationsRoundedIcon /></div>);
    case 'DP':
      return(<div style={iconWrapperStyle}> <CancelRoundedIcon /></div>); // Replace with the actual X icon component
    case 'AP':
      return(<div style={iconWrapperStyle}> <CheckBoxRoundedIcon /></div>); // Replace with the actual checkmark icon component
    default:
      return(<div style={iconWrapperStyle}> <NotificationsRoundedIcon /></div>); // Default case, you can handle this as per your requirement
  }
};
    
  return (
    <div className="notifications-dropdown"  style={{ top: position.top}}>
      <List
      dataSource={notifications.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))}
      renderItem={(item) => (
        <List.Item className={item.status === 'unread' ? 'unread-notification' : 'read-notification'}>
          <div className='notificacionardas'>
            <List.Item.Meta
              avatar={<Avatar icon={getNotificationIcon(item.type_of_notification)} />}
              title={<a href="/Prestamos">{item.message}</a>}
              description={<div>{formatTimestamp(item.timestamp)}</div>}
            />
  </div>
</List.Item>

  )}
/>

    </div>
  );
};

export default NotificationsDropdown;