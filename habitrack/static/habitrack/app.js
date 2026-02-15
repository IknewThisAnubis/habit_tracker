// helper function to parse crff token from meta tag as cookies are not being sent with fetch requests in this setup

function getCSRFToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute('content');
}


document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".habit-btn")
  buttons.forEach((button) => {
    if (button.dataset.done === "1") {
      button.disabled = true
    }
    button.addEventListener("click", () => {
      const habitId = button.dataset.habitId
      fetch(`/habits/${habitId}/log/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "logged") {
            button.disabled = true
            const overall = document.querySelector("#overall-streak")
            if (overall && typeof data.overall_streak === "number") {
              overall.textContent = data.overall_streak
            }
          }
        })
        .catch(() => {
          window.location.reload()
        })
    })
  })
})
