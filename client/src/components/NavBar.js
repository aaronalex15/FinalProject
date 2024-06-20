import { Toaster } from "react-hot-toast";
import { NavLink } from "react-router-dom";
import { useContext } from "react";
import { UserContext } from "../components/UserContext";
import "../index.css";

const NavBar = () => {
  const { currentUser, handleLogout } = useContext(UserContext);

  return (
    <div>
      <Toaster />
      <div className="nav">
        <nav className="navbar">
          {!currentUser && (
            <>
              <NavLink to="/registration">Login</NavLink>
              <br />
            </>
          )}
          {currentUser && (
            <>
              <NavLink to="/">Home</NavLink>
              <br />
              <NavLink to={`/users/${currentUser.id}`}>My Profile</NavLink>
              <br />
              <NavLink to="/cart">My Cart</NavLink>
              <br />
              <NavLink onClick={handleLogout}>Logout</NavLink>
            </>
          )}
        </nav>
      </div>
    </div>
  );
};

export default NavBar;
