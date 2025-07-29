const loginForm = document.getElementById('login-form');
const baseEndpoint = "http://localhost:8000/api";

if (loginForm) {
  loginForm.addEventListener('submit', handleLogin);
}

function handleLogin(event) {
  event.preventDefault();

  const loginEndpoint = `${baseEndpoint}/token/`;
  const loginFormData = new FormData(loginForm);
  const loginObjectData = Object.fromEntries(loginFormData); // {username: "...", password: "..."}
  const bodyStr = JSON.stringify(loginObjectData);

  console.log("Login Data:", loginObjectData);

  fetch(loginEndpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: bodyStr
  })
  .then(res => {
    console.log("Response:", res);
    if (!res.ok) {
      throw new Error("Login failed");
    }
    return res.json();
  })
  .then(data => {
    console.log("Token Response:", data);
    // store tokens or redirect user
  })
  .catch(err => {
    console.error("Error:", err);
  });
}
