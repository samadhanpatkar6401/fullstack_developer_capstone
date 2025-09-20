import React, { useState } from "react";
import "./Login.css";
import Header from "../Header/Header";

const Login = ({ onClose }) => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [open, setOpen] = useState(true);

  // ✅ Always include the trailing slash to match Django’s URL
  const login_url = `${window.location.origin}/djangoapp/login/`;

  const login = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch(login_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userName: userName,
          password: password,
        }),
      });

      const json = await res.json();

      if (res.ok && json.status === "Authenticated") {
        // ✅ Save username in session storage
        sessionStorage.setItem("username", json.userName);
        setOpen(false);
      } else {
        alert(
          json.error ||
            json.status ||
            "❌ Login failed. Please check your credentials."
        );
      }
    } catch (err) {
      console.error("Login error:", err);
      alert("⚠️ Network or server error. Try again later.");
    }
  };

  // ✅ If login successful → redirect to homepage
  if (!open) {
    window.location.href = "/";
    return null;
  }

  return (
    <div>
      <Header />
      <div onClick={onClose}>
        <div
          onClick={(e) => e.stopPropagation()}
          className="modalContainer"
        >
          <form className="login_panel" onSubmit={login}>
            <div>
              <span className="input_field">Username </span>
              <input
                type="text"
                placeholder="Username"
                className="input_field"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                required
              />
            </div>
            <div>
              <span className="input_field">Password </span>
              <input
                type="password"
                placeholder="Password"
                className="input_field"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div>
              <input className="action_button" type="submit" value="Login" />
              <input
                className="action_button"
                type="button"
                value="Cancel"
                onClick={() => setOpen(false)}
              />
            </div>
            <a className="loginlink" href="/register">
              Register Now
            </a>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
