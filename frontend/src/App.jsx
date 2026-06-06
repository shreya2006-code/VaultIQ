import { useState, useEffect } from "react";
import axios from "axios";
import Register from "./Register";
import Login from "./Login";


function App() {
  const username = localStorage.getItem("username");

  const logout = () => {
    localStorage.removeItem("username");
    window.location.reload();
  };
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [links, setLinks] = useState([]);

  const analyzeURL = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/ai/summarize",
        {
          url: url,
        }
      );

      setResult(response.data.result);
    } catch (error) {
      console.error(error);
      setResult(null);
    }
  };

  const fetchLinks = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/links"
      );

      setLinks(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const deleteLink = async (id) => {
    try {
      await axios.delete(
        `http://127.0.0.1:8000/links/${id}`
      );

      fetchLinks();
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchLinks();
  }, []);

  return (
    <div>
      {username && (
        <>
          <h2>
            Welcome, {username} 👋
          </h2>

          <button onClick={logout}>
            Logout
          </button>
        </>
      )}

      <Register />

      <hr />

      <Login />
    </div>
  );
}

export default App;