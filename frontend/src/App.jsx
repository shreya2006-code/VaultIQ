import { useState, useEffect } from "react";
import axios from "axios";
import Register from "./Register";

function App() {
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
      <h1>VaultIQ</h1>

      <Register />
    </div>
  );
}

export default App;