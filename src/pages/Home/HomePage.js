import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import officeImage from './office.jpg';
import './HomePage.css'
function HomePage() {
  return (
    <div className='container pagecontainer'>
      <div>
        <h1>Bienvenido a Scrumtonstock</h1>
      </div>
      <div>
      <img src={officeImage} className="img-fluid" alt="" />
    </div>
    </div>
  );
}

export default HomePage;
