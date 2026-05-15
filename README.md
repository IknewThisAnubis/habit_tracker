# Habit Tracker - CS50 Web Programming Final Project

A comprehensive habit tracking web application built with Django and JavaScript that helps users build and maintain healthy habits while tracking their emotional wellbeing.

## Distinctiveness and Complexity

**Distinctiveness:**
- It is a personal wellness/productivity application, not a social platform, e-commerce site, or ordering system
- The primary focus is on individual habit formation and tracking with emotional wellbeing integration
- The calendar-based history view with mood/gratitude tracking is unique to this application

**Complexity:**
- **Multi-model backend:** Implements two interconnected models (Habit and HabitLog) with sophisticated relationships
- **Calendar functionality:** Generates interactive calendar views with date-specific data aggregation
- **Mood tracking system:** Implements a 5-level emotional scale with persistent storage
- **Gratitude journaling:** Combines habit tracking with gratitude reflection
- **Dynamic frontend:** Uses fetch API for seamless updates without full page reloads
- **Streak calculation:** Complex algorithm to calculate daily and overall habit streaks
- **Mobile-responsive design:** Fully responsive CSS grid layouts for mobile, tablet, and desktop
- **Session management:** Proper user authentication with Django's built-in auth system

## File Structure

### Backend Files

#### `habitrack/models.py`
- **Habit model:** Stores habit definitions with user association and creation timestamp
- **HabitLog model:** Stores daily habit completion records, mood, and gratitude entries
- Implements unique constraint to ensure one log per habit per day

#### `habitrack/views.py`
- **register():** User registration with automatic login after signup
- **dashboard():** Main view showing today's habits, mood tracker, and gratitude box
- **habits_page():** Manage habits - create, view, and interact with habits
- **edit_habit():** Edit existing habit names
- **delete_habit():** Remove habits
- **log_habit():** AJAX endpoint to mark habits as completed
- **history():** Calendar view showing all months with completion status
- **day_details():** AJAX endpoint returning detailed data for specific calendar days
- **save_mood_gratitude():** AJAX endpoint to save mood and gratitude entries

#### `habitrack/urls.py`
- URL routing for all views including history calendar and detail endpoints

#### `habitrack/forms.py`
- **RegisterForm:** User registration with password field
- **HabitForm:** Create/edit habits
- **MoodGratitudeForm:** Save mood and gratitude (though mainly handled via AJAX)

#### `habitrack/utils.py`
- **calculate_streak():** Calculate consecutive days a specific habit was completed
- **calculate_overall_streak():** Calculate days where ALL habits were completed

#### `habitrack/migrations/`
- Database migrations for Habit, HabitLog, and new mood/gratitude fields

### Frontend Files

#### `habitrack/templates/habitrack/layout.html`
- Base template with navigation bar
- Includes links to Dashboard, Habits, History, and Login/Logout

#### `habitrack/templates/habitrack/dashboard.html`
- Displays today's habits with toggle functionality (click to select/deselect)
- Selected habits highlighted in green
- 5-level mood tracker with emoji selectors (😢 😕 😐 🙂 😄)
- Gratitude text box for daily reflection
- Overall and individual habit streak displays
- Data attributes pass saved mood/gratitude to JavaScript for auto-loading

#### `habitrack/templates/habitrack/habits.html`
- Create new habits with form
- Display all user habits with edit/delete options
- Link to edit individual habits

#### `habitrack/templates/habitrack/edit_habit.html`
- Edit habit name
- Return to dashboard on save

#### `habitrack/templates/habitrack/history.html`
- Calendar view of the selected month with navigation
- Days with all habits completed highlighted in green
- Click any day to fetch and display:
  - Which habits were completed
  - Mood and gratitude from that day
- Month navigation (previous/next buttons)
- Mobile-responsive calendar layout

#### `habitrack/templates/registration/login.html`
- Django auth login form
- Link to registration page

#### `habitrack/static/habitrack/app.js`
- **Habit tracking:** Button click handlers for toggling selection and logging completion
- **Mood management:** Radio input change listeners and emoji selection functionality
- **Gratitude saving:** Auto-save mood and gratitude via AJAX on blur/change events
- **Calendar interaction:** `showDayDetails()` function to fetch and display day-specific data
- **Data loading:** `loadSavedMoodGratitude()` to restore saved mood/gratitude from page data attributes
- **CSRF protection:** Token retrieval and inclusion in all POST requests

#### `habitrack/static/habitrack/styles.css`
- **Layout:** Dashboard container with max-width constraints, responsive grid system
- **Habit buttons:** Toggle styling with green highlight (#90EE90) for selected habits
- **Mood tracker:** Emoji selector with hidden radio inputs, scale animation on selection
- **Gratitude box:** Full-width textarea with auto-save triggers
- **Calendar:** Full month view with day cells, green highlighting for completed days, hover effects
- **Responsive design:** Media queries for mobile (768px) and tablet (600px) breakpoints
- **Button styles:** Primary button with hover effects, navigation buttons

### Configuration Files

#### `habit_tracker/settings.py`
- Django project settings
- Database configuration (SQLite)
- Installed apps including habitrack
- Template and static file configuration

#### `habit_tracker/urls.py`
- Root URL configuration
- Includes Django auth URLs for login/logout
- Includes habitrack app URLs

#### `requirements.txt`
- Django==6.0
- Python dependencies for the project

#### `docker-compose.yml`
- PostgreSQL database service
- Django web service
- Volume management for development

#### `Dockerfile`
- Python 3.11 base image
- Install dependencies
- Expose port 8000
- Run Django development server

## How to Run Your Application

### Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for local development)

### With Docker Compose

1. **Start the application:**
   ```bash
   docker compose up -d
   ```

2. **Run migrations (first time only):**
   ```bash
   docker compose exec web python manage.py migrate
   ```

3. **Access the application:**
   - Open browser to `http://localhost:8000`


### Local Development (Without Docker)

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   - Open browser to `http://localhost:8000`

### Initial Setup

1. Register a new account
2. Create your first habit (e.g., "Morning Exercise", "Drink Water")
3. Click habits on the dashboard to mark them complete
4. Track your mood with the emoji selector
5. Record what you're grateful for
6. View your progress in the History calendar



### Future Enhancement Ideas

- Habit categories and tags
- Weekly/monthly habit goals
- Social sharing of achievements
- Habit recommendations
- Data export (CSV/PDF reports)
- Dark mode
- Habit reminders/notifications
- Habit difficulty levels
- Collaborative habit challenges
- gamifications 
