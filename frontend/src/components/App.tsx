import { useState } from "react";
import Header from "./header";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <div className="text-xl">
      <Header />

      <div className="p-4">
        <Outlet />
      </div>
    </div>
  );
}

export default App;
