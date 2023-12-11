import React from 'react';
import Clock from 'react-live-clock';
import moment from 'moment-timezone';
import 'moment/locale/es'; // Import the locale data if needed
import 'moment-timezone/data/packed/latest.json'; // Replace 'latest' with the appropriate version

export default class ClockPage extends React.Component {
  render() {
    return (
      <Clock format={'HH:mm:ss'} ticking={true} timezone={'America/Argentina/Cordoba'} />
    );
  }
}
