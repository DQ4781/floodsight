function getPrediction() {
  fetch("/predict", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById(
        "predictionOutput"
      ).innerHTML = `Day 1: ${data.prediction[0][0]}, Day 2: ${data.prediction[0][1]}, Day 3: ${data.prediction[0][2]}`;
    })
    .catch((error) => {
      console.error("Error fetching data: ", error);
      document.getElementById("predictionOutput").innerHTML =
        "Failed to retrieve prediction.";
    });
}
