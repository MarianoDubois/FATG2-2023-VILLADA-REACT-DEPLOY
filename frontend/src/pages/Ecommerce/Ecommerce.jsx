import React, { useState, useEffect } from 'react';
import './Ecommerce.css';
import CardExample from '../../components/card/CardExample';
import WordList from '../../components/card/filtros';
import Dropdown from '../../components/FiltrosCelus/Dropdown'
import defaultpicture from '../../assets/images/defaultpicture.png';
import { useSearchParams } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Spinner from 'react-bootstrap/Spinner';
import useAxios from '../../utils/useAxios';
import { useParams } from 'react-router-dom';
import Pagination from '../../components/pagination/Paginacion'; // Import the Pagination component
import PropTypes from 'prop-types';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import IconButton from '@mui/material/IconButton';

<head>
  <link rel="preconnect" href="https://fonts.googleapis.com"></link>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin></link>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap" rel="stylesheet"></link>
</head>


function Ecommerce({ allItems }) {
  const api = useAxios();
  const [count, setCount] = useState(1);
  const [cards, setCards] = useState([]);
  const [filteredCards, setFilteredCards] = useState([]);
  const [searchParams] = useSearchParams();
  const searchQuery = searchParams.get('searchQuery');
  const { name } = useParams();
  const [showWordList, setShowWordList] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  const pageSize = 10; // Number of cards per page
  const [page, setPage] = useState(1);

  useEffect(() => {
    getElement();
  }, [page]);

  useEffect(() => {
    filterCards();
  }, [searchQuery]);

  const getElement = async () => {
    const endpoint = allItems
      ? `ecommercePaginacion/?page=${page}`
      : `filtroCategoria/${encodeURIComponent(name)}/?page=${page}`;

    try {
      const response = await api.get(`${endpoint}`);
      let data = await response.data;
      setCount(data.count);
      let results = data.results;
      // Replace null or empty images with the default image
      const updatedData = results.map((card) => ({
        ...card,
        image: card.image || defaultpicture,
      }));

      setCards(updatedData);
      setFilteredCards(updatedData);
      setIsLoading(false);
    } catch (error) {
      console.error('Error al obtener datos:', error);
      setIsLoading(false);
    }
  };

  const filterCards = () => {
    let filteredCardsData = cards;

    if (searchQuery && searchQuery.trim() !== '') {
      filteredCardsData = cards.filter((card) =>
        card.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredCards(filteredCardsData);
  };

  return (
    <div className="tratandodecentrar" >
      {isLoading && (
        <div className="d-flex justify-content-center align-items-center vh-100">
          <Spinner animation="border" role="status">
          </Spinner>
        </div>
      )}


      <Container className = "mt-4" >
          <Col md = "12"> 
            {!isLoading ? (
 
              <>   
          <Row>
              <div className="mr-12"> 
                <WordList />
              </div>
          </Row>

              <Row className="mt-4">             
                {filteredCards.length === 0 ? (
                  <div className="text-center">
                    <h2>No hay productos disponibles para esta categoría.</h2>
                    <a href="/tienda" className="btn btn-primary">
                      Volver a la tienda
                    </a>
                  </div>
                ) : (
                  <>
                  
                  
                    {filteredCards.map((card, index) => (
                      <div key={index} >
                        <CardExample
                          title={card.name}
                          text={card.description}
                          image={card.image}
                          id={card.id}
                          current_stock={card.current_stock}
                        />
                      </div>
                    ))}
                    <Row>
                    <div className="d-flex justify-content-center mt-4">
                      <Pagination
                        totalRecords={count}
                        pageLimit={pageSize}
                        pageNeighbours={1}
                        currentPage={page}
                        onPageChanged={setPage}
                      />
                    </div>
                  
                    </Row>
                  </>
                )}
                  </Row>

              </>
            ) : null}

          </Col>

      </Container>
    </div>
  );
}


Ecommerce.propTypes = {
  allItems: PropTypes.bool,
};

export default Ecommerce;
