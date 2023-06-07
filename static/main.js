document.addEventListener("DOMContentLoaded", function () {
  function showToast(operator) {
    var x = document.getElementById("toast");
    x.classList.add("show");
    x.innerHTML = "Phone number belongs to: " + operator;
    setTimeout(function () {
      x.classList.remove("show");
    }, 3000);
  }

  function validatePhoneNumber(phoneNumber) {
    // Check phone number validity using your validation logic
    var firstThreeDigits = phoneNumber.slice(0, 3);
    var numberDigits = phoneNumber.slice(3);

    if (firstThreeDigits === "254" && numberDigits.length !== 9) {
      // Invalid number: must be 12 digits for international numbers starting with 254
      return false;
    } else if (firstThreeDigits !== "254" && numberDigits.length !== 7) {
      // Invalid number: must be 10 digits for local numbers
      return false;
    }

    return true;
  }

  function searchNumber(event) {
    if (event) {
      event.preventDefault();
    }

    var phoneNumber = document.getElementById("searchInput").value;

    if (!validatePhoneNumber(phoneNumber)) {
      // Phone number format is invalid
      // Show error message or apply red glow to the input field
      var errorMessage = "Invalid Number";
      var errorElement = document.getElementById("error");
      errorElement.textContent = errorMessage;
      document.getElementById("searchInput").classList.add("is-invalid");
      return;
    }

    // Phone number format is valid, proceed with the search
    // Remove any error styling from the input field
    document.getElementById("searchInput").classList.remove("is-invalid");

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    // Find the CSRF token input element
    var csrfTokenElement = document.querySelector('input[name="csrf_token"]');
    if (csrfTokenElement) {
      // Get the CSRF token value
      var csrfToken = csrfTokenElement.value;
      // Set the CSRF token in the request headers
      xhr.setRequestHeader("X-CSRFToken", csrfToken);
    }

    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          var response = JSON.parse(xhr.responseText);
          showToast(response.operator);
        } else {
          showToast("Error occurred. Please try again.");
        }
      }
    };
    xhr.send("phone_number=" + encodeURIComponent(phoneNumber));
  }

  // Attach event listener to the form submit event
  var searchForm = document.getElementById("searchForm");
  searchForm.addEventListener("submit", searchNumber);

  // Attach event listener to the search button click event
  var searchButton = document.getElementById("searchButton");
  searchButton.addEventListener("click", searchNumber);

  // Attach event listener to the Enter key press event
  var searchInput = document.getElementById("searchInput");
  searchInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      searchNumber(event);
    }
  });
});
