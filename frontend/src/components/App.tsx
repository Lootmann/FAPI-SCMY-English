import Header from "./header";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <div className="text-xl h-screen flex flex-col">
      <Header />

      <div className="flex justify-center h-[calc(100vh-4rem)]">
        <div className="h-full w-3/4">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default App;
