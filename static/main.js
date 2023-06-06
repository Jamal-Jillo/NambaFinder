//function showToast(text){
//  var x=document.getElementById("toast");
//  x.classList.add("show");
//  x.innerHTML=text;
//  setTimeout(function(){
//    x.classList.remove("show");
//  },3000);
//}


function showToast(operator) {
    var x = document.getElementById("toast");
    x.classList.add("show");
    x.innerHTML = "Phone number belongs to: " + operator;
    setTimeout(function () {
        x.classList.remove("show");
    }, 3000);
}


//function searchNumber() {
//    var phoneNumber = document.getElementById("searchInput").value;
//    var xhr = new XMLHttpRequest();
//    xhr.open("POST", "/", true);
//    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
//    xhr.onreadystatechange = function () {
//      if (xhr.readyState === XMLHttpRequest.DONE) {
//        if (xhr.status === 200) {
//          var response = JSON.parse(xhr.responseText);
//          showToast(response.operator);
//        } else {
//          showToast("Error occurred. Please try again.");
//        }
//      }
//    };
//    xhr.send("phone_number=" + encodeURIComponent(phoneNumber));
//  }


function searchNumber() {
  var phoneNumber = document.getElementById("searchInput").value;
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

