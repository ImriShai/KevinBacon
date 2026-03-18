import React from "react";
import { Link } from "react-router-dom";
import "./NavBar.css"

const Navbar: React.FC = () => {
  return (
    <ul>
        <li>
            <Link to="/">
                Home
            </Link>
        </li>
        <li>
            <Link to="/new-movie">
                New Movie
            </Link>
        </li>
    </ul>
  );
};

export default Navbar;