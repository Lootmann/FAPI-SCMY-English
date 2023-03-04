import React from "react";
import { Link } from "react-router-dom";

function Header() {
  return (
    <div className="p-4 text-xl text-slate-200 bg-slate-800 flex gap-4 items-baseline">
      <p className="text-2xl">English Master</p>
      <Link to={`sentences`}>Sentence</Link>
    </div>
  );
}

export default Header;
