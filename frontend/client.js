const baseEndpoint = "http://localhost:8000/api";
const loginForm = document.getElementById("login-form");
const contentContainer = document.getElementById("content-container");

// Login + store tokens
function handleLogin(event) {
    event.preventDefault();
    const loginEndpoint = `${baseEndpoint}/token/`;
    const loginFormData = new FormData(loginForm);
    const loginObjectData = Object.fromEntries(loginFormData);

    fetch(loginEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(loginObjectData)
    })
    .then(response => response.json())
    .then(token => {
        if (token.access && token.refresh) {
            localStorage.setItem("access", token.access);
            localStorage.setItem("refresh", token.refresh);
            getProductList();  // Call the protected API
        } else {
            alert("Login failed. Please check your credentials.");
        }
    })
    .catch(error => {
        console.error("Login Error:", error);
        alert("Something went wrong during login.");
    });
}

// Display products
function writeToContainer(data) {
    if (!contentContainer) return;
    if (!data || (Array.isArray(data) && data.length === 0)) {
        contentContainer.innerHTML = "<p>No products available.</p>";
    } else {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>";
    }
}

//  Refresh token if access expired
function refreshTokenAndRetry(callback) {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) {
        alert("Session expired. Please log in again.");
        logout();
        return;
    }

    const refreshEndpoint = `${baseEndpoint}/token/refresh/`;

    fetch(refreshEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem("access", data.access);
            console.log("🔄 Token refreshed");
            callback(); 
        } else {
            alert("Session expired. Please log in again.");
            logout();
        }
    })
    .catch(error => {
        console.error("Refresh Error:", error);
        logout();
    });
}


function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    contentContainer.innerHTML = "<p>You have been logged out. Please log in again.</p>";
}


function getProductList() {
    const endpoint = `${baseEndpoint}/products/`;
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
        logout();
        return;
    }

    fetch(endpoint, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`
        }
    })
    .then(response => {
        if (response.status === 401) {
            return response.json().then(data => {
                if (data.code === "token_not_valid") {
                    refreshTokenAndRetry(getProductList); 
                } else {
                    logout();
                }
            });
        }
        return response.json();
    })
    .then(data => {
        if (data && !data.code) {
            writeToContainer(data);
        }
    })
    .catch(error => {
        console.error("Product Fetch Error:", error);
        contentContainer.innerHTML = "<p>Error loading products.</p>";
    });
}

// Form listener
if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
}
