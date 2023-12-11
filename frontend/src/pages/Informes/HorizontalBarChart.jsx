import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';

const HorizontalBarChart = ({ data }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    const defaultData = {
      labels: ['Label 1', 'Label 2', 'Label 3'], // Coloca etiquetas predeterminadas
      values: [0, 0, 0], // Coloca valores predeterminados
    };

    const actualData = data || defaultData;

    const lenderUsernames = actualData.map(item => item.lender__username);
    const vencidosCounts = actualData.map(item => item.vencidos_count);

    const ctx = chartRef.current.getContext('2d');

    // Destruye el gráfico anterior si existe
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    chartInstance.current = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: lenderUsernames,
        datasets: [
          {
            label: 'Vencidos Count',
            data: vencidosCounts,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          x: {
            beginAtZero: true,
          },
        },
      },
    });
  }, [data]);

  return <canvas id="horizontalBar" ref={chartRef}></canvas>;
};

export default HorizontalBarChart;
