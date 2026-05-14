// helper function to parse crff token from meta tag as cookies are not being sent with fetch requests in this setup

function getCSRFToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute('content');
}


document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".habit-btn")
  buttons.forEach((button) => {
    // Add selected class if already done today
    if (button.dataset.done === "1") {
      button.classList.add("selected");
    }
    
    button.addEventListener("click", () => {
      const habitId = button.dataset.habitId
      
      // Toggle selected state
      button.classList.toggle("selected");
      
      fetch(`/habits/${habitId}/log/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "logged") {
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

  // Add mood change listener
  const moodInputs = document.querySelectorAll('input[name="mood"]');
  moodInputs.forEach(input => {
    input.addEventListener('change', () => {
      saveMoodGratitude();
    });
  });
})

function saveMoodGratitude() {
  const mood = document.querySelector('input[name="mood"]:checked')?.value;
  const gratitude = document.querySelector('textarea[name="gratitude"]')?.value || '';
  
  const formData = new FormData();
  formData.append('mood', mood || '');
  formData.append('gratitude', gratitude);
  
  fetch('/save-mood-gratitude/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': getCSRFToken()
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log('Mood and gratitude saved!');
  })
  .catch(error => console.error('Error:', error));
}

