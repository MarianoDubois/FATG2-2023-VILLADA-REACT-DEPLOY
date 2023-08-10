import {
  BrowserRouter as Router,
  Routes,
  Route
} from "react-router-dom";
import LoginPage from "./pages/Login/LoginPage";
import HomePage from "./pages/Home/HomePage";
import DetalleProducto from "./pages/DetalleProducto/DetalleProducto";
import Layout from "./layout/Layout";
import * as React from 'react';
import Ecommerce from "./pages/Ecommerce/Ecommerce.jsx";
import  './assets/styles/App.css';

function App() {
  return (
    <Router>
      <div className="container">
        <div className="app">
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/*" element={<LayoutWrapper />} />
          </Routes>
        </div>
      </div>
    </Router>
    
  );
}

function LayoutWrapper() {
  return (
    <Layout>
      <Routes>
      
      <Route path="/" element={<HomePage />} />
        <Route path= "/tienda" element={<Ecommerce/>}/>
        <Route path="/detalleProducto/:id" element={<DetalleProducto />} />
      </Routes>
    </Layout>
  );
}

export default App;
