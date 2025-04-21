document.addEventListener("DOMContentLoaded", () => {
  fetchCategories(); // load categories first
  fetchProducts(); // initially load all products
});

function fetchCategories() {
  fetch("/categories/")
    .then((response) => response.json())
    .then((categories) => {
      const categoryList = document.getElementById("category-list");
      categoryList.innerHTML = "";
      const Allli = document.createElement("li");
      Allli.textContent = "All Products";
      Allli.onclick = () => fetchProducts("All Products");
      categoryList.appendChild(Allli);
      categories.forEach((category) => {
        const li = document.createElement("li");
        li.textContent = category.title;
        li.onclick = () => fetchProducts(category.title);
        categoryList.appendChild(li);
      });
    })
    .catch((error) => console.error("Error loading categories:", error));
}
function fetchProducts(categoryId = null) {
  let url = categoryId ? `/categories/${categoryId}/products/` : "products/";
  if (categoryId === "All Products") {
    url = "products/";
  }
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      const container = document.getElementById("product-list");
      container.innerHTML = "";

      data.forEach((product) => {
        const tile = document.createElement("div");
        tile.className = "product-tile";

        const imageUrl = product.image
          ? product.image
          : "/static/images/fillImage.jpg";

        tile.innerHTML = `
            <h3>${product.name}</h3>
            <img src="${imageUrl}" alt="${product.name}" />
            <p class="price">₹${product.price}</p>
            <p>Brand: ${product.brand}</p>
            <p>${product.description || "No description"}</p>
          `;

        container.appendChild(tile);
      });
    })
    .catch((error) => console.error("Error loading products:", error));
}
