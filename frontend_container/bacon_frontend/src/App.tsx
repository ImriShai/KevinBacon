import { Routes, Route } from "react-router-dom";
import  DistanceForm from "./Form";
import NewMovie from "./NewMovie";
import Navbar from "./NavBar";
import "./App.css"
import "./form.css"

const App: React.FC = () => {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/" element={<DistanceForm />} />
        <Route path="/new-movie" element={<NewMovie />} />
      </Routes>
    </>
  );
};

export default App;