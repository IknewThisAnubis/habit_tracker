// Helper function to parse CSRF token from meta tag
function getCSRFToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute('content');
}
// Show details for a specific calendar day
function showDayDetails(year, month, day) {
  fetch(`/history/${year}/${month}/${day}/`)
    .then(response => response.json())
    .then(data => {
      const detailsDiv = document.getElementById('day-details');
      let habitsHtml = '<h3>Habits for ' + data.date + '</h3>';
      habitsHtml += '<ul>';
      data.habits.forEach(habit => {
        const status = habit.completed ? '✓ Completed' : '○ Not completed';
        habitsHtml += `<li>${habit.name}: ${status}</li>`;
      });
      habitsHtml += '</ul>';

      if (data.mood) {
        const moods = { 1: '😢', 2: '😕', 3: '😐', 4: '🙂', 5: '😄' };
        habitsHtml += `<p><strong>Mood:</strong> ${moods[data.mood]}</p>`;
      }

      if (data.gratitude) {
        habitsHtml += `<p><strong>Gratitude:</strong> ${data.gratitude}</p>`;
      }

      detailsDiv.innerHTML = habitsHtml;
    })
    .catch(error => console.error('Error:', error));
}
// Load saved mood and gratitude from data attributes
function loadSavedMoodGratitude() {
  const container = document.querySelector('.dashboard-container');
  if (!container) return;

  const savedMood = container.dataset.mood;
  const savedGratitude = container.dataset.gratitude;

  if (savedMood) {
    const moodInput = document.querySelector(`input[name="mood"][value="${savedMood}"]`);
    if (moodInput) {
      moodInput.checked = true;
    }
  }

  if (savedGratitude) {
    const gratitudeInput = document.querySelector('textarea[name="gratitude"]');
    if (gratitudeInput) {
      gratitudeInput.value = savedGratitude;
    }
  }
}

// Save mood and gratitude
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

// Initialize event listeners on page load
document.addEventListener('DOMContentLoaded', () => {
  // Load saved mood and gratitude
  loadSavedMoodGratitude();

  // Habit button handlers
  const buttons = document.querySelectorAll('.habit-btn');
  buttons.forEach((button) => {
    // Add selected class if already done today
    if (button.dataset.done === '1') {
      button.classList.add('selected');
    }

    button.addEventListener('click', () => {
      const habitId = button.dataset.habitId;

      // Toggle selected state
      button.classList.toggle('selected');

      fetch(`/habits/${habitId}/log/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCSRFToken()
        }
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === 'logged') {
            const overall = document.querySelector('#overall-streak');
            if (overall && typeof data.overall_streak === 'number') {
              overall.textContent = data.overall_streak;
            }
          }
        })
        .catch(() => {
          window.location.reload();
        });
    });
  });

  // Mood change listener
  const moodInputs = document.querySelectorAll('input[name="mood"]');
  moodInputs.forEach(input => {
    input.addEventListener('change', () => {
      saveMoodGratitude();
    });
  });
});

