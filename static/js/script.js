//
// GLOBAL SCRIPT
// Basic Form Validation
// 

// --- Check if "password == confirm password" on the registration page ---
// Find the form by its id; if it is not on the page, does nothing.
const registerForm = document.getElementById("registerForm");

if (registerForm) {
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");

  registerForm.addEventListener("submit", function (event) {
    // Сhecking the standard HTML5 validation rules (required, pattern, etc.)
    if (!registerForm.checkValidity()) {
      event.preventDefault();
      registerForm.classList.add("was-validated");
      return;
    }

    // Additional check: compare the password and confirmation password
    if (password.value !== confirmPassword.value) {
      event.preventDefault(); // prevent form submission
      confirmPassword.setCustomValidity("Passwords do not match.");
      registerForm.classList.add("was-validated");
    } else {
      confirmPassword.setCustomValidity(""); // Clear the error if passwords match
    }
  });

  // Remove the error message when user starts typing again
  confirmPassword.addEventListener("input", function () {
    confirmPassword.setCustomValidity("");
  });
}

// PRODUCT FILTERING on browse-listings.html
// Works using two criteria:
// 1) Category read from the page URL
//    (e.g. browse-listings.html?category=books)
// 2) Condition (New / Second-Hand) selected from the dropdown menu

const listingsGrid = document.getElementById("listingsGrid");

if (listingsGrid) {
  const cards = Array.from(listingsGrid.querySelectorAll(".listing-card"));
  const conditionSelect = document.getElementById("filterCondition");
  const categorySelect = document.getElementById("filterCategory");
  const noResultsMessage = document.getElementById("noResultsMessage");
  const activeCategoryLabel = document.getElementById("activeCategoryLabel");

 // Read ?category=... from the URL (when navigating from the homepage)
  const urlParams = new URLSearchParams(window.location.search);
  const categoryFromUrl = urlParams.get("category");

  // If a category is provided in the URL, automatically select it
  // in the dropdown so that the filter matches the page URL
  if (categoryFromUrl && categorySelect) {
    categorySelect.value = categoryFromUrl;
    if (activeCategoryLabel) {
      activeCategoryLabel.textContent = "Showing category: " + categoryFromUrl;
    }
  }

  function applyFilters() {
    const conditionValue = conditionSelect ? conditionSelect.value : "";
    const categoryValue = categorySelect ? categorySelect.value : "";
    let visibleCount = 0;

    cards.forEach(function (card) {
      const matchesCondition = !conditionValue || card.dataset.condition === conditionValue;
      const matchesCategory = !categoryValue || card.dataset.category === categoryValue;
      const isVisible = matchesCondition && matchesCategory;

      card.style.display = isVisible ? "" : "none";
      if (isVisible) visibleCount++;
    });

    // Show the "No results found" message if no items match the filters
    if (noResultsMessage) {
      noResultsMessage.classList.toggle("d-none", visibleCount > 0);
    }
  }

  if (conditionSelect) conditionSelect.addEventListener("change", applyFilters);
  if (categorySelect) categorySelect.addEventListener("change", applyFilters);

  applyFilters(); // Apply filters immediately when the page loads
}
