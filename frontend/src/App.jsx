import { useState, useEffect } from "react";
import axios from "axios";

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
    <div className="container">
      <h1>VaultIQ</h1>
      <p>AI-Powered Bookmark Manager</p>

      <div className="input-section">
        <input
          type="text"
          placeholder="Paste a URL here..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button onClick={analyzeURL}>
          Analyze
        </button>
      </div>

      <div className="results">
        <h2>Results</h2>

        {result && (
          <>
            <h3>Title</h3>
            <p>{result.title}</p>

            <h3>AI Analysis</h3>
            <p>{result.ai_result}</p>
          </>
        )}
      </div>

      <div className="saved-links">
        <h2>Saved Bookmarks</h2>

        {links.map((link) => (
          <div key={link.id}>
            <h3>{link.title}</h3>

            <p>{link.category}</p>

            <a
              href={link.url}
              target="_blank"
              rel="noreferrer"
            >
              Visit Link
            </a>

            <button
              onClick={() => deleteLink(link.id)}
            >
            Delete
            </button>

            <hr />
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;