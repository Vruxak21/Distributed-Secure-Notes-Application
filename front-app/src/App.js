import { Routes, Route } from "react-router-dom";
import { Home } from "./pages/Home/Home";
import { Register } from "./pages/Register/Register";
import { Login } from "./pages/Login/Login";
import { NewNote } from "./components/notes/create/NewNote";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route path="/notes/new" element={<NewNote />} />
      <Route path="*" element={<Home />} />
    </Routes>
  );
}

export default App;
