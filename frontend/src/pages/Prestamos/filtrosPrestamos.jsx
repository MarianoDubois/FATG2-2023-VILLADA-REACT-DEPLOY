import React, { useEffect, useState } from 'react';
import useAxios from '../../utils/useAxios';
import { useParams, Link } from 'react-router-dom';
import { DropdownButton, Dropdown } from 'react-bootstrap';
import IconButton from '@mui/material/IconButton';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';

const FiltrosPrestamos = () => {
  const api = useAxios();
  const { id } = useParams();
  const [parentCategories, setParentCategories] = useState([]);
  const [childrenCategories, setChildrenCategories] = useState([]);
  const [categoryVisibility, setCategoryVisibility] = useState({});

  useEffect(() => {
    getElement();
  }, []);

  const handleFilter = (categoryId) => {
    console.log('funcionan los links!!', categoryId);
    // Implement your logic to handle filtering based on the selected category
  };

  const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  const toggleCategoryVisibility = (categoryId) => {
    setCategoryVisibility({
      ...categoryVisibility,
      [categoryId]: !categoryVisibility[categoryId],
    });
  };

  const getElement = async () => {
    try {
      const response = await api.get(`/category/`);
      const data = response.data;

      const filteredParentCategories = data.filter(
        (category) =>
          category.category === null &&
          (category.name === 'equipos' ||
            category.name === 'componentes' ||
            category.name === 'insumos' ||
            category.name === 'kits arduino')
      );

      const formattedChildrenCategories = data.filter(
        (category) => category.category !== null
      );

      setParentCategories(filteredParentCategories);
      setChildrenCategories(formattedChildrenCategories);

      const initialCategoryVisibility = {};
      filteredParentCategories.forEach((category) => {
        initialCategoryVisibility[category.id] = false;
      });
      setCategoryVisibility(initialCategoryVisibility);
    } catch (error) {
      console.error(error);
    }
  };

  const getCategoryNameById = (categoryId) => {
    const category = parentCategories.find((item) => item.id === categoryId);
    return category ? category.name : '';
  };

  return (
    <div className="word-list">
      <Dropdown>
        <Dropdown.Toggle
          variant="black"
          id="dropdown-filtros"
          style={{ backgroundColor: 'white', color: 'black' }}
        >
          Filtros
        </Dropdown.Toggle>
        <Dropdown.Menu>
          {parentCategories.map((parentCategory) => (
            <Dropdown key={parentCategory.id} style={{ backgroundColor: 'white' }}>
              <Dropdown.Toggle
                variant="black"
                id={`dropdown-${parentCategory.id}`}
                style={{ backgroundColor: 'white', color: 'black' }}
              >
                {capitalizeFirstLetter(parentCategory.name)}
              </Dropdown.Toggle>
  
              <Dropdown.Menu style={{ backgroundColor: 'white' }}>
                {childrenCategories
                  .filter(
                    (child) => child.category.id === parentCategory.id
                  )
                  .map((child) => (
                    <Dropdown.Item
                      key={child.id}
                      href={`/tienda/${child.name}`}
                      style={{
                        textDecoration: 'none',
                        color: 'black',
                        backgroundColor: 'white',
                      }}
                    >
                      {capitalizeFirstLetter(child.name)}
                    </Dropdown.Item>
                  ))}
              </Dropdown.Menu>
            </Dropdown>
          ))}
        </Dropdown.Menu>
      </Dropdown>
    </div>
  );
};

export default FiltrosPrestamos;
