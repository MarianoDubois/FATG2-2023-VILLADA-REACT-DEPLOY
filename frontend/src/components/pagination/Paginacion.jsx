import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

function Pagination(props) {
  const {
    totalRecords, // Establecer un valor predeterminado en caso de que totalRecords sea null
    pageLimit,
    pageNeighbours,
    onPageChanged,
  } = props;

  const totalPages = Math.ceil(totalRecords / pageLimit) || 1; // Usar 1 si totalRecords es falsy



  const [currentPage, setCurrentPage] = useState(1);

  const gotoPage = (page) => {
    const newPage = Math.max(1, Math.min(page, totalPages));
    setCurrentPage(newPage);

    if (onPageChanged) {
      onPageChanged(newPage);
    }
  };

  const handlePrevClick = () => {
    gotoPage(currentPage - 1);
  };

  const handleNextClick = () => {
    gotoPage(currentPage + 1);
  };

  const range = (start, end) => {
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  };

  const getPageNumbers = () => {
    const totalNumbers = pageNeighbours * 2 + 3;
    const totalBlocks = totalNumbers + 2;

    if (totalPages > totalBlocks) {
      const startPage = Math.max(2, currentPage - pageNeighbours);
      const endPage = Math.min(totalPages - 1, currentPage + pageNeighbours);
      let pages = range(startPage, endPage);

      const hasLeftSpill = startPage > 2;
      const hasRightSpill = totalPages - endPage > 1;
      const spillOffset = totalNumbers - (pages.length + 1);

      if (hasLeftSpill && !hasRightSpill) {
        const extraPages = range(startPage - spillOffset, startPage - 1);
        pages = ["LEFT-ELLIPSIS", ...extraPages, ...pages];
      } else if (!hasLeftSpill && hasRightSpill) {
        const extraPages = range(endPage + 1, endPage + spillOffset);
        pages = [...pages, ...extraPages, "RIGHT-ELLIPSIS"];
      } else if (hasLeftSpill && hasRightSpill) {
        pages = ["LEFT-ELLIPSIS", ...pages, "RIGHT-ELLIPSIS"];
      }

      return [1, ...pages, totalPages];
    }

    return range(1, totalPages);
  };


  const renderPagination = () => {
    console.log("totalRecords:", totalRecords);
    console.log("totalPages:", totalPages);
    if (!totalRecords || totalPages === 1) return console.log("PUTOo");

    const pages = getPageNumbers();

    return (
      <ul className="pagination">
        {pages.map((page, index) => {
          if (page === "LEFT-ELLIPSIS") {
            return (
              <li key={index} className="page-item disabled">
                <span className="page-link">...</span>
              </li>
            );
          }
          if (page === "RIGHT-ELLIPSIS") {
            return (
              <li key={index} className="page-item disabled">
                <span className="page-link">...</span>
              </li>
            );
          }
          return (
            <li
              key={index}
              className={`page-item ${currentPage === page ? "active" : ""}`}
            >
              <span
                className="page-link"
                onClick={() => gotoPage(page)}
              >
                {page}
              </span>
            </li>
          );
        })}
      </ul>
    );
  };

  return (
    <nav>
      
      {renderPagination()}
    </nav>
  );
}

Pagination.propTypes = {
  totalRecords: PropTypes.number.isRequired,
  pageLimit: PropTypes.number,
  pageNeighbours: PropTypes.number,
  onPageChanged: PropTypes.func
};

export default Pagination;
