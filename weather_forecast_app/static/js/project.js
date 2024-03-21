import React from 'react';
import ReactDOM from "react-dom/client";
import App from 'Components/App/App';

document.addEventListener("DOMContentLoaded", function() {
  const root = ReactDOM.createRoot(document.getElementById("reactWrapper"));
  root.render(<App />);
});

