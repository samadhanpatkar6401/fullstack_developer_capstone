import React, { useState } from "react";
import "./Register.css";  // make sure this CSS exists
import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";
import close_icon from "../assets/close.png";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const goHome = () => window.location.href = window.location.origin;

  const register = async (e) => {
    e.preventDefault();
    const register_url = window.location.origin + "/djangoapp/register/";
    const res = await fetch(register_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userName,
        password,
        firstName,
        lastName,
        email
      }),
    });
    const json = await res.json();
    if (json.status === "Authenticated") {
      sessionStorage.setItem("username", json.userName);
      window.location.href = window.location.origin;
    } else if (json.error === "Already Registered") {
      alert("This username is already registered.");
      window.location.href = window.location.origin;
    }
  };

  return (
    <div className="register_container" style={{ width: "50%" }}>
      <div className="header" style={{ display: "flex", justifyContent: "space-between" }}>
        <span className="text">Sign Up</span>
        <a href="/" onClick={goHome}>
          <img style={{ width: "1cm" }} src={close_icon} alt="Close"/>
        </a>
      </div>
      <form onSubmit={register}>
        <div className="inputs">
          <div className="input">
            <img src={user_icon} className="img_icon" alt="Username"/>
            <input type="text" placeholder="Username" onChange={e => setUserName(e.target.value)} />
          </div>
          <div className="input">
            <img src={user_icon} className="img_icon" alt="First Name"/>
            <input type="text" placeholder="First Name" onChange={e => setFirstName(e.target.value)} />
          </div>
          <div className="input">
            <img src={user_icon} className="img_icon" alt="Last Name"/>
            <input type="text" placeholder="Last Name" onChange={e => setLastName(e.target.value)} />
          </div>
          <div className="input">
            <img src={email_icon} className="img_icon" alt="Email"/>
            <input type="email" placeholder="Email" onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="input">
            <img src={password_icon} className="img_icon" alt="Password"/>
            <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
          </div>
        </div>
        <div className="submit_panel">
          <input className="submit" type="submit" value="Register" />
        </div>
      </form>
    </div>
  );
};

export default Register;