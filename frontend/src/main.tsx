import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "./styles/index.css";

import App from "./components/App";
import SentenceTop from "./components/sentences/index";
import Sentence from "./components/sentences/sentence";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/sentence",
        element: <SentenceTop />,
      },
      {
        path: "/sentences/:sentenceId",
        element: <Sentence />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);