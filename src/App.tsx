import { Routes, Route } from "react-router";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import BrainOS from "./pages/BrainOS";
import CommandRoom from "./pages/CommandRoom";
import Booking from "./pages/Booking";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/brain" element={<BrainOS />} />
      <Route path="/command-room" element={<CommandRoom />} />
      <Route path="/book-call" element={<Booking />} />
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
