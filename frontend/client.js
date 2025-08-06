const baseEndpoint = "http://localhost:8000/api";
const loginForm = document.getElementById("login-form");
const searchForm = document.getElementById("search-form");
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


function handleSearch(event) {
    event.preventDefault();

    const formData = new FormData(searchForm);         
    const data = Object.fromEntries(formData);         
    let searchParams = new URLSearchParams(data);
    const endpoint = `${baseEndpoint}/search/?${searchParams}`;
    const accessToken = localStorage.getItem("access");

    fetch(endpoint, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            ...(accessToken && { Authorization: `Bearer ${accessToken}` })
        }
    })
    .then(response => {
        if (response.status === 401) {
            return response.json().then(data => {
                if (data.code === "token_not_valid") {
                    refreshTokenAndRetry(() => handleSearch(event)); // 🔁 retry after refresh
                } else {
                    logout();
                }
            });
        }
        return response.json();
    })
    .then(data => {
        if (data && contentContainer) {
            contentContainer.innerHTML = "";  

            if (data.hits && Array.isArray(data.hits)) {
                if (data.hits.length > 0) {
                    let htmlStr = "<ul>";  

                for (let result of data.hits) {
            console.log("Result:", result);  
            htmlStr += `
                <li style="margin-bottom: 1rem; border: 1px solid #ccc; padding: 1rem; border-radius: 8px;">
                    <strong>${result.title ?? "No Title"}</strong><br>
                    <small>Seller: ${result.user_username ?? "Unknown"}</small><br>
                    Price: ₹${result.price ?? "N/A"}<br>
                    Sale Price: ₹${result.sale_price ?? "N/A"}<br>
                    Tags: ${Array.isArray(result._tags) ? result._tags.join(", ") : "None"}
                </li>
            `;
        }

        htmlStr += "</ul>";  // Close the list after the loop
        contentContainer.innerHTML = htmlStr;

                } else {
                    contentContainer.innerHTML = "<p>No results found</p>";
                }
            } else {
                contentContainer.innerHTML = "<p>No results found</p>";
            }
        }
    })
    .catch(error => {
        console.error("Search Error:", error);
        alert("Something went wrong during Search.");
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

if (searchForm) {
    searchForm.addEventListener("submit", handleSearch);
}



async function searchProducts() {
  const query = document.getElementById("searchInput").value;
  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = "Searching...";

  try {
    const response = await fetch(`http://localhost:8000/api/search/?q=${encodeURIComponent(query)}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        // Add this only if your search endpoint is protected
        // "Authorization": `Bearer ${localStorage.getItem("access")}`
      }
    });

    const data = await response.json();
    console.log("API response data:", data);

    const products = data.results || data;  // handle paginated or direct list
    if (!Array.isArray(products)) {
      throw new Error("Invalid data format: Expected an array of products");
    }

    resultsContainer.innerHTML = "";

    if (products.length === 0) {
      resultsContainer.innerHTML = "<p>No results found.</p>";
      return;
    }

    products.forEach(product => {
      const card = document.createElement("div");
      card.className = "product-card";
      card.innerHTML = `
        <h3>${product.title}</h3>
        <p>${product.content || "No description available"}</p>
        <p><strong>Price:</strong> $${product.price}</p>
      `;
      resultsContainer.appendChild(card);
    });

  } catch (error) {
    console.error("Search Error:", error);
    resultsContainer.innerHTML = `<p>Error: ${error.message}</p>`;
  }
}

window.searchProducts = searchProducts;