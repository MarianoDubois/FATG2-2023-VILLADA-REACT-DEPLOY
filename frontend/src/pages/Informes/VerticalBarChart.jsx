import React, { useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';

const VerticalBarChart = ({ data }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (data.length === 0) return;

    let labels = [];
let values = [];

if (Array.isArray(data)) {
  labels = data.map(item => item.box_nombre);
  values = data.map(item => item.cantidad_logs_rotos);
}

    const ctx = chartRef.current.getContext('2d');

    // Destruye el gráfico anterior si existe
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    chartInstance.current = new Chart(ctx, {
      type: 'bar', // Use 'bar' for a vertical bar chart
      data: {
        labels: labels,
        datasets: [
          {
            label: 'My First Dataset',
            data: values,
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 205, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(201, 203, 207, 0.2)',
            ],
            borderColor: [
              'rgb(255, 99, 132)',
              'rgb(255, 159, 64)',
              'rgb(255, 205, 86)',
              'rgb(75, 192, 192)',
              'rgb(54, 162, 235)',
              'rgb(153, 102, 255)',
              'rgb(201, 203, 207)',
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          x: { // Use 'y' instead of 'x' for vertical bars
            beginAtZero: true,
          },
        },
      },
    });
  }, [data]);

  return <canvas id="verticalBar" ref={chartRef}></canvas>;
};

export default VerticalBarChart;
