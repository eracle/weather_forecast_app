import React, { useState } from 'react';
import { MapContainer, TileLayer, useMapEvents } from 'react-leaflet';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'leaflet/dist/leaflet.css';

import { Container, Row, Col, Form, Button, Modal } from 'react-bootstrap';
function LocationMarker({ setLat, setLon }) {
  useMapEvents({
    click(e) {
      const newPos = e.latlng;
      setLat(newPos.lat.toFixed(4));
      setLon(newPos.lng.toFixed(4));
    },
  });

  return null; // Omitting the marker for simplicity as requested
}

function App() {
  const [lat, setLat] = useState('');
  const [lon, setLon] = useState('');
  const [detailing, setDetailing] = useState('current');
  const [showModal, setShowModal] = useState(false);
  const [weatherData, setWeatherData] = useState({});

const fetchWeather = async () => {
  // Construct the URL with query parameters
  const queryParams = new URLSearchParams({ lat, lon, detailing }).toString();
  const url = `/weather/forecast/?${queryParams}`;

  try {
    // Send the request to the backend
    const response = await fetch(url);

    // Check if the request was successful
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`); // Or handle error responses as needed
    }

    // Parse the JSON response
    const data = await response.json();

    // Update state with the fetched data and show the modal
    setWeatherData(data);
    setShowModal(true);
  } catch (error) {
    console.error("Failed to fetch weather data:", error);
    // Optionally, update UI to show an error message
  }
};


  return (
  <>
    <Container fluid className="p-0 d-flex" style={{ height: '100vh' }}>
      <Col xs={12} md={8} className="p-0 d-flex">
        <MapContainer center={[37.7749, -122.4194]} zoom={13} style={{ width: '100%', flexGrow: 1 }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <LocationMarker setLat={setLat} setLon={setLon} />
        </MapContainer>
      </Col>
      <Col xs={12} md={4} className="d-flex flex-column p-4" style={{ overflowY: 'auto' }}>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="3">Latitude:</Form.Label>
          <Col sm="9">
            <Form.Control type="text" value={lat} readOnly />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="3">Longitude:</Form.Label>
          <Col sm="9">
            <Form.Control type="text" value={lon} readOnly />
          </Col>
        </Form.Group>
        <Form.Group as={Row} className="mb-3">
          <Form.Label column sm="3">Detailing:</Form.Label>
          <Col sm="9">
            <Form.Select value={detailing} onChange={(e) => setDetailing(e.target.value)}>
              <option value="current">Current weather</option>
              <option value="minute">Minute forecast for 1 hour</option>
              <option value="hourly">Hourly forecast for 48 hours</option>
              <option value="daily">Daily forecast for 7 days</option>
            </Form.Select>
          </Col>
        </Form.Group>
        <Button onClick={fetchWeather} className="align-self-center">Fetch Weather</Button>
      </Col>
    </Container>
      <Modal show={showModal} onHide={() => setShowModal(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Weather Data</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {/* Display weather data here. For example: */}
          <Container fluid>
            <Row>
              <Col>Temperature:</Col>
              <Col>{weatherData.current?.temp} °C</Col>
            </Row>
            <Row>
              <Col>Humidity:</Col>
              <Col>{weatherData.current?.humidity} %</Col>
            </Row>
            <Row>
              <Col>Description:</Col>
              <Col>{weatherData.current?.weather?.[0]?.description}</Col>
            </Row>
            {/* Add more data as needed */}
          </Container>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>

  );
}

export default App;
