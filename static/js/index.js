document.addEventListener("DOMContentLoaded", function () {
  const reasonSelect = document.getElementById("reason");
  const otherReasonContainer = document.getElementById("otherReasonContainer");
  const otherReasonInput = document.getElementById("otherReason");

  reasonSelect.addEventListener("change", function () {
    if (this.value === "Other") {
      otherReasonContainer.style.display = "block";
      otherReasonInput.required = true;
    } else {
      otherReasonContainer.style.display = "none";
      otherReasonInput.required = false;
      otherReasonInput.value = ""; // Clear input when hidden
    }
  });
});

//Prevents a future data from being entered.
let today = new Date().toISOString().split("T")[0];
document.getElementById("date").setAttribute("max", today);

flatpickr("#time", {
  enableTime: true,
  noCalendar: true,
  dateFormat: "h:i K", // 12-hour format with AM/PM
  time_24hr: false,
});
