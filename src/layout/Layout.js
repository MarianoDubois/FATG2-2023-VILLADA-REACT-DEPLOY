import React from 'react';
import LayoutComponents from './LayoutComponents/LayoutComponents';


function Layout(props) {
  return (
    <div className="container">
      <LayoutComponents />
      {props.children}
    </div>
  );
}

export default Layout;
