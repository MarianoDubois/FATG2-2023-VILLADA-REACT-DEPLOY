import React, { useState } from 'react';
import LayoutComponents from './LayoutComponents/LayoutComponents';

function Layout(props) {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (query) => {
    setSearchQuery(query);
    //console.log(query)
  };

  return (
    <div className="container">
      <LayoutComponents isProfessor={props.isProfessor} onSearch={handleSearch} />
      {props.children }
    </div>
  );
}

export default Layout;
