document.querySelector("#create").onclick = () => {
  fetch("/habits/create/", {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    body: new URLSearchParams({ name: "New Habit" }),
  })
}