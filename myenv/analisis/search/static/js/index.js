document.addEventListener("DOMContentLoaded", () => {
  var captureButton = document.getElementById("captureData")
  captureButton.addEventListener("click", async () => {
    var data = document.getElementById("search").value;
    console.log(data);
  });
});
