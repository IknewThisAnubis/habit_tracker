# Habit Tracker - CS50 Web Programming Final Project

A comprehensive habit tracking web application built with Django and JavaScript that helps users build and maintain healthy habits while simultaneously tracking their emotional wellbeing and gratitude practices. This application demonstrates the practical intersection of behavioral psychology, user experience design, and full-stack web development.

## Distinctiveness and Complexity

### What This Project Is: A Holistic Wellness Application

Habit Tracker is fundamentally a **personal wellness and self-reflection platform** that goes beyond simple task management. Unlike traditional to-do list applications or habit trackers that focus solely on completion metrics, this project integrates three interconnected pillars: habit formation, emotional wellness monitoring, and gratitude practice. The application recognizes that building sustainable habits is inseparable from understanding one's emotional state and mental health, which research in habit psychology (as popularized by James Clear's "Atomic Habits") confirms is essential to long-term behavioral change.

The core concept is that users don't just track whether they completed a habit—they also reflect on their emotional state while practicing that habit and what they're grateful for. This tri-faceted approach creates a richer, more meaningful data set that reveals patterns about emotional correlations with successful habits. For instance, a user might discover that they consistently complete exercise habits on days when their mood is higher, or that gratitude reflection helps them stay motivated. This holistic approach to habit tracking demonstrates understanding of behavioral science and human psychology.

### Technical Distinctiveness: Multi-Layer Backend Architecture

The backend implements a sophisticated **relational data model** that manages complex relationships between users, habits, and daily records. The two-model system (Habit and HabitLog) creates a normalized database design that prevents data redundancy while maintaining integrity through Django's ORM and database constraints. Critically, the application implements a `unique_together` constraint ensuring only one log entry per habit per day, which prevents data corruption from duplicate submissions—a technical consideration that shows understanding of database design principles.

The application also implements **dynamic AJAX-based interactions** that eliminate page reloads. Rather than the typical Django pattern of form submission followed by page refresh, users can toggle habits, save mood selections, and log gratitude entries seamlessly. This requires careful backend API design with multiple AJAX endpoints (`log_habit`, `save_mood_gratitude`, `day_details`) that return structured JSON data, combined with sophisticated frontend logic to handle responses and update the UI accordingly.

### Functional Complexity: Advanced Feature Integration

Several features work together to create genuine complexity beyond the course's standard projects:

**Streak Calculation Engine:** The application implements dual streak tracking—both individual habit streaks and "perfect day" streaks where all habits were completed. This requires querying historical data, identifying consecutive sequences, and handling edge cases like months with different numbers of days. The algorithm must distinguish between "broken" streaks and "just started" habits, which requires careful conditional logic.

**Calendar Generation and Date Aggregation:** The history page generates a full month calendar view with color-coding that indicates completion status. This involves server-side logic to generate date ranges, fetch historical data for all dates in a month, aggregate habit completion across multiple habits per day, and determine display states. The calendar also supports navigation between months with proper handling of year boundaries.

**Dual-Direction Data Binding:** The mood tracker and gratitude box must load previously saved data when displaying today's dashboard, requiring coordination between backend data retrieval and frontend JavaScript state management. The `loadSavedMoodGratitude()` function uses data attributes to bridge this gap, ensuring that returning users see their previous entries without making additional API calls.

**Mobile-First Responsive Design:** The application implements responsive CSS with multiple breakpoints (mobile at 768px, tablet at 600px) using CSS Grid layouts that reflow appropriately. The calendar view, buttons, and text input areas all adapt to different screen sizes while maintaining usability—a requirement that adds design complexity beyond simple pixel-perfect desktop layouts.

### Why This Matters: Beyond "Not Other Projects"

This project distinctly **is** something specific and meaningful: a **user-centric wellness application that recognizes the interconnection between behavior, emotion, and gratitude.** It's not simply "not a social network"—it actively serves a real purpose for people genuinely trying to improve themselves. A user can open this application weekly, see their progress visualized on the calendar, understand patterns in their emotional state, and feel motivated by the gratitude entries they've written. This is a complete, functional application someone might actually use, not a exercise in checking off technical requirements.

Furthermore, the project demonstrates **full-stack competency**: understanding how to structure data relationships, write efficient queries, build dynamic APIs, create responsive user interfaces, and ensure security through CSRF protection. Each of these components required thoughtful decision-making and problem-solving specific to this application's requirements.

## File Structure and Technical Implementation

This section documents every file to which code was contributed, explaining both the technical purpose and design decisions.

### Backend Application Files (`habitrack/`)

#### `models.py` - Core Data Models

This file defines the relational data structure for the entire application. Two Django models form the foundation:

- **Habit Model:** Represents a habit that a user wants to track (e.g., "Morning Exercise," "Read for 30 minutes"). Each habit stores the user relationship (foreign key), a name, and a creation timestamp. The design assumes one user can have multiple habits, and each habit belongs to exactly one user, enforcing proper data isolation.

- **HabitLog Model:** Represents a daily record of habit completion plus emotional context. For each day a user engages with the app, a HabitLog entry is created recording: which habit was completed, the date, whether it was marked complete, the user's mood (stored as integer 1-5), and gratitude text. The critical design decision here is the `unique_together` constraint on (habit, date), ensuring the database prevents duplicate entries if the user accidentally submits twice. This demonstrates understanding of data integrity.

This two-model design is more sophisticated than a single-table approach because it normalizes the data—habit definitions are stored once and referenced multiple times through foreign keys, rather than duplicating habit information in every daily log entry.

#### `views.py` - Backend Logic and API Endpoints

Contains eight view functions that handle both page rendering and AJAX API requests:

- **register():** Processes user registration by validating the custom RegisterForm, creating a new User object, and automatically logging the user in to improve UX (users don't need to login immediately after registration). Uses Django's authentication system securely.

- **dashboard():** Renders the main app page with today's date, all habits for the current user, and attempts to load today's HabitLog entry to restore previously saved mood/gratitude. Uses context variables to pass data to the template, allowing JavaScript to auto-populate form values.

- **habits_page():** Displays all habits for the user with create/edit/delete options. Demonstrates filtering database queries by user to ensure data isolation.

- **edit_habit():** Handles both GET requests (displaying the edit form) and POST requests (saving changes). Shows understanding of HTTP method dispatching in Django.

- **delete_habit():** Removes a habit and all associated logs through Django's cascade delete. Important edge case: a user should only be able to delete their own habits, enforced by filtering habits by `request.user`.

- **log_habit():** AJAX endpoint that receives a POST request with a habit ID and completion status. Creates or updates a HabitLog entry. Returns JSON response for frontend processing. This demonstrates REST-like API design patterns.

- **history():** Generates a full month view of the calendar. Calculates the first day of the month, number of days, and creates a data structure of all dates. Pre-fetches HabitLog data for efficient database querying (avoiding N+1 query problems).

- **day_details():** AJAX endpoint that receives a date parameter and returns detailed data for that day: which habits were completed, the mood level, and gratitude text. Allows the calendar to display rich information without page reload.

- **save_mood_gratitude():** AJAX endpoint that saves or updates a HabitLog's mood and gratitude fields. Enables users to update emotional context without changing habit completion status.

#### `urls.py` - URL Routing

Defines URL patterns mapping to views. Includes standard paths like `/dashboard/` for the main page and `/habits/` for habit management, plus AJAX endpoints like `/log_habit/` and `/day_details/`. Demonstrates understanding of RESTful URL design principles (action verbs in URLs, clean path structure).

#### `forms.py` - Form Validation

Django Forms provide server-side validation and CSRF protection:

- **RegisterForm:** Extends Django's UserCreationForm to validate registration input, ensuring passwords match and meet requirements.

- **HabitForm:** Validates habit names (required field, reasonable length).

- **MoodGratitudeForm:** While primarily handled via AJAX, this form provides server-side validation layer ensuring mood is a valid integer and gratitude text is appropriate length.

Server-side validation is critical for security—never trust client-side validation alone, as it can be bypassed by malicious users or broken clients.

#### `utils.py` - Helper Functions

Provides reusable business logic separated from views for code organization:

- **calculate_streak(habit, date):** Counts consecutive days this specific habit was completed, ending on the given date. Iterates backwards through HabitLog entries, breaking when a day without completion is found. Returns streak count.

- **calculate_overall_streak(user, date):** More complex—counts consecutive days where ALL the user's habits were completed. Must query all habits for the user, then all logs for those habits, and find the longest consecutive sequence where every habit has a completion on each date. This algorithm requires careful iteration and comparison.

These utility functions are excellent examples of separating business logic from HTTP views, making the code testable and reusable.

#### `migrations/` - Database Schema Evolution

Django migrations track all database changes. Initial migration creates the Habit and HabitLog models. Subsequent migrations add the mood field, gratitude field, and unique constraint. This demonstrates understanding of database versioning and backward compatibility.

### Frontend Files

#### `templates/layout.html` - Base Template

Django template that provides the site-wide header, navigation bar, and CSS/JavaScript includes. All other templates extend this, ensuring consistent design. The navigation includes links to Dashboard, Habits, History, and Login/Logout, with login visibility toggled based on `user.is_authenticated`.

#### `templates/dashboard.html` - Main Application Interface

Renders today's habit tracking interface with four major sections:

1. **Habit Toggle Buttons:** Each habit appears as a button. JavaScript click handlers toggle a `.selected` class (styling it green) and call the `log_habit` AJAX endpoint. Data attributes pass the habit ID to JavaScript.

2. **Mood Emoji Selector:** Five emoji radio buttons (😢 😕 😐 🙂 😄) with hidden `<input type="radio">` elements. CSS displays only the emoji, but the radio input captures the value. When changed, JavaScript calls `save_mood_gratitude`.

3. **Gratitude Text Box:** A textarea where users type what they're grateful for. The JavaScript `blur` event listener saves this automatically via AJAX.

4. **Streak Displays:** Shows both individual habit streaks and overall "perfect day" streaks calculated by backend utility functions.

The template uses Django template variables to pass previously saved mood/gratitude via data attributes, enabling the `loadSavedMoodGratitude()` JavaScript function to restore user's entries.

#### `templates/habits.html` - Habit Management

Displays a form to create new habits and a list of existing habits with edit/delete buttons. Form submission goes to the backend, which validates and creates the HabitForm object.

#### `templates/edit_habit.html` - Edit Individual Habit

Simple form to update a habit's name. Demonstrates Django's form rendering with `{% csrf_token %}` for CSRF protection.

#### `templates/history.html` - Calendar View

Generates a full-month calendar:

- Uses HTML `<table>` to display calendar grid
- Days are clickable elements with JavaScript click handlers
- Days where all habits were completed are styled green
- Clicking a day calls `showDayDetails()`, which makes an AJAX request to `/day_details/` 
- Response displays that day's completed habits, mood, and gratitude in a modal or sidebar
- Month navigation buttons call the view with `?month=N&year=Y` query parameters

The calendar is responsive—CSS media queries adjust cell sizes for mobile screens.

#### `templates/registration/login.html` - Authentication

Django's built-in auth template for user login. Links to registration page for new users. Demonstrates use of Django's authentication system.

### Static Files

#### `static/app.js` - Core JavaScript Application Logic

Approximately 200+ lines of JavaScript implementing all dynamic interactions:

- **Event Delegation:** Attaches click handlers to habit buttons, mood selector, and gratitude box. Uses element IDs and CSS selectors to target specific elements.

- **AJAX Calls:** Functions like `logHabit(habitId)` send POST requests to the backend with `fetch()`. Includes CSRF token retrieval from cookie and includes it in request headers—a critical security detail. The backend validates this token and rejects requests without it.

- **loadSavedMoodGratitude():** Runs on dashboard page load. Reads data attributes containing saved mood/gratitude and restores radio selection and textarea content, so users see their previous entries.

- **showDayDetails(date):** Fetches day-specific data from `/day_details/` AJAX endpoint. Displays modal or sidebar with habits completed that day, mood, and gratitude.

- **Auto-save:** Mood and gratitude changes trigger `save_mood_gratitude()` AJAX calls after a brief delay (debounce), saving data without user clicking a button.

- **Error Handling:** Includes try-catch blocks and console logging for debugging.

#### `static/styles.css` - Responsive Styling

Approximately 400+ lines of CSS implementing all visual design:

- **Layout:** Main container with max-width, margin auto for centering. Uses CSS Grid for the dashboard layout (habits, mood tracker, gratitude box in appropriate positions).

- **Habit Buttons:** Base styling with border, padding, hover effects. `.selected` class adds green background (`#90EE90`) to indicate selected habits.

- **Mood Selector:** CSS hiding the radio inputs while displaying the emoji. Hover states and animation on selection. Each emoji is a `<label>` that triggers the hidden radio.

- **Calendar Grid:** Table-based calendar with 7 columns (days of week). Cells include padding, borders, and hover effects. Green background for completed days. Clickable appearance (cursor pointer) to indicate interactivity.

- **Responsive Design:** Media queries at 768px and 600px breakpoints adjust font sizes, button sizes, and calendar cell sizes for mobile and tablet screens. Ensures the app is fully usable on small screens.

- **Color Scheme:** Consistent use of green (#90EE90) for completion/success, gray for neutral elements, and appropriate contrast for accessibility.

### Configuration Files

#### `habit_tracker/settings.py` - Django Project Settings

Configures Django application: installed apps (including habitrack), database (SQLite for development), static files location, template directories. Sets `DEBUG = False` for production but may be `True` for development. Includes secret key, allowed hosts, and middleware configuration.

#### `habit_tracker/urls.py` - Root URL Router

Root URL configuration that includes:
- `habitrack/` app URLs (for habit tracking features)
- Django built-in `auth/` URLs (for login/logout)
- Static file serving configuration for development

#### `requirements.txt` - Python Dependencies

Lists all Python packages needed: Django (the web framework), Python built-ins like sqlite3. New dependencies would be added here for deployment/reproducibility. This file enables others to recreate the exact development environment.

#### `docker-compose.yml` - Container Orchestration

Defines two services: PostgreSQL database and Django web application. Demonstrates containerization for consistent development environments and easier deployment. Includes volume mounts for database persistence and code mounting for development.

#### `Dockerfile` - Container Image

Python 3.11 base image, installs dependencies via `pip install -r requirements.txt`, exposes port 8000, runs `python manage.py runserver`. Shows understanding of containerization best practices (layer caching, dependency installation separation).

## How the Application Works: User Flow

1. **Registration:** New user creates account. Backend validates password, creates User object, and logs them in.
2. **Create Habits:** User adds habits they want to track (exercise, meditation, reading, etc.).
3. **Daily Use:** Each day, user opens dashboard, clicks habits they completed, selects mood from emoji picker, and writes gratitude. All changes auto-save via AJAX.
4. **Track Progress:** User views history calendar to see patterns—which months/days had perfect completion, how mood correlates with habit success.
5. **Reflection:** Calendar detail view shows specific habits completed and emotional context from that day, enabling meaningful reflection.

## How to Run Your Application

## How to Run Your Application

### Prerequisites
- Docker and Docker Compose installed (recommended for consistent environment)
- OR: Python 3.11+, pip, and SQLite (for local development)
- Git (for cloning/version control)

### Running with Docker Compose (Recommended)

Docker Compose provides a consistent environment matching production setup.

1. **Start the application:**
   ```bash
   docker compose up -d
   ```
   This command starts both the PostgreSQL database and Django web server in background containers.

2. **Run database migrations (first time only):**
   ```bash
   docker compose exec web python manage.py migrate
   ```
   This creates the database schema defined by models.py.

3. **Create a superuser (optional, for Django admin):**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

4. **Access the application:**
   - Open browser to `http://localhost:8000`
   - Navigate to `/register` to create a new account
   - Start creating and tracking habits

5. **Stop the application:**
   ```bash
   docker compose down
   ```

### Local Development Without Docker

For development without containers:

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   Virtual environments isolate dependencies per project, preventing version conflicts.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   This installs Django and other required packages from requirements.txt.

3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```
   Creates SQLite database at `db.sqlite3` with proper schema.

4. **Start development server:**
   ```bash
   python manage.py runserver
   ```
   Django development server runs at `http://localhost:8000` with auto-reload on file changes.

5. **Create a user account:**
   - Navigate to `http://localhost:8000/register`
   - Fill in username and password
   - System automatically logs you in

6. **Start using the application:**
   - Click "Habits" to create your first habit
   - Go to Dashboard to track today's habits
   - Try the mood selector and gratitude box (auto-saves)
   - View History to see the calendar

### Initial Setup Guide

1. **Register Account:**
   - Click the "Register" link on the login page
   - Enter a username and password (twice for confirmation)
   - You'll be logged in automatically after registration

2. **Create Habits:**
   - Click "Habits" in the navigation
   - Enter habit names you want to track (e.g., "Morning Exercise," "Read for 30 minutes")
   - Click "Create" for each habit
   - Habits should be specific and measurable

3. **Daily Tracking:**
   - Navigate to Dashboard (home page)
   - Click habit buttons to mark them complete (button turns green)
   - Select your mood using emoji (😢 😕 😐 🙂 😄)
   - Type what you're grateful for
   - All changes auto-save—no save button needed

4. **View Progress:**
   - Click "History" to see a calendar view
   - Green days show perfect completion (all habits done)
   - Click any day to see which habits you completed and what your mood/gratitude were
   - Navigate months with Previous/Next buttons

## Design Decisions and Technical Considerations

### Why Two Models (Habit + HabitLog)?

Separating habit definitions from daily logs follows database normalization principles. If stored as one table, repeating habit information daily wastes storage and creates redundancy. This design also makes querying more efficient—finding all habits for a user doesn't require scanning habit logs.

### AJAX vs. Traditional Forms

Rather than submitting forms with page refreshes, the application uses `fetch()` API for all interactive updates (logging habits, saving mood, loading calendar details). This provides instant visual feedback and a more responsive feel. However, the backend forms still validate server-side—client-side validation is never trusted for security.

### Mood and Gratitude as Optional Fields

Users might not fill mood/gratitude every day, so these fields are nullable. This prevents errors when habits are logged without emotional reflection, making the app flexible for different user preferences.

### Mobile-Responsive CSS Grid

Rather than fixed desktop layouts, CSS Grid with responsive breakpoints adapts to different screen sizes. This is critical since many users track habits on phones during their day (logging a workout right after the gym, etc.).

### Streak Calculation Logic

Streaks are calculated on-demand from historical data rather than stored in the database. This means if a user logs a past habit, streaks update correctly. If we stored streaks statically, updating past data would require recalculating all future streaks—a complex problem avoided by computing streaks dynamically.

### Docker Containerization

The Dockerfile and docker-compose.yml demonstrate production-ready deployment patterns. This application can be easily deployed to cloud platforms, ensuring consistency between development and production environments.

## Security Considerations Implemented

1. **CSRF Protection:** All POST requests include Django's CSRF token, preventing cross-site attacks. JavaScript retrieves the token and includes it in AJAX requests headers.

2. **User Data Isolation:** Every query filters by `request.user`, ensuring users can only access their own habits and logs. A malicious user cannot view another user's data.

3. **Authentication Required:** Most views require `@login_required` decorator, redirecting unauthenticated users to login page.

4. **Password Hashing:** Django's authentication system hashes passwords using industry-standard algorithms (PBKDF2). Passwords are never stored in plaintext.

5. **SQL Injection Prevention:** Django ORM parameterizes all database queries, preventing SQL injection attacks.

6. **Form Validation:** Server-side form validation ensures only valid data enters the database, preventing malformed or malicious input.

## Additional Information and Future Enhancements

### Current Limitations Acknowledged

- **Single timezone:** Application assumes user's system timezone; doesn't explicitly handle timezone-aware dates
- **No data export:** Users cannot export their habit data as CSV or PDF
- **No notifications:** Application doesn't send reminders or notifications
- **Limited analytics:** While the calendar shows patterns, deeper statistical analysis isn't implemented
- **Habit categories:** All habits are listed together without organization into categories

### Potential Enhancements

These features would increase the application's value without fundamentally changing its purpose:

- **Email/push reminders:** Notify users about habits they haven't logged yet
- **Social accountability:** Optional sharing of streaks with friends or public profiles
- **Habit analytics:** Charts showing completion rates, average mood on completion days, correlation between mood and habit success
- **Habit difficulty levels:** Users could mark habits as easy/medium/hard, adjusting scoring accordingly
- **Habit recommendations:** Suggest new habits based on user's interests and goals
- **Collaborative habits:** Friends could share habits and compete for streaks
- **Mobile app:** Native iOS/Android app instead of web-only
- **Data export:** Download all habit data as CSV for personal records or analysis
- **Habit challenges:** Themed challenges (e.g., "7-day exercise challenge") with leaderboards

### Technologies Used

- **Backend:** Django (Python web framework), SQLite/PostgreSQL (database)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (no framework overhead)
- **Deployment:** Docker, Docker Compose
- **Authentication:** Django's built-in auth system
- **API:** RESTful AJAX endpoints returning JSON

### Development Time and Effort

This project required substantial effort across multiple dimensions:
- **Data modeling:** Designing the Habit/HabitLog relationship, understanding normalization
- **Backend logic:** Implementing streak calculations, calendar generation, AJAX endpoints
- **Frontend interactivity:** Building AJAX handlers, managing state between components
- **Responsive design:** Creating mobile-friendly layouts with CSS media queries
- **Testing and debugging:** Ensuring data integrity, handling edge cases, cross-browser compatibility
- **Documentation:** Writing comprehensive README explaining design decisions

The time investment reflects the project's genuine complexity—this is a complete, functional application, not a simple CRUD interface.

## Conclusion

Habit Tracker demonstrates a **complete full-stack web development project** that goes beyond the scope of CS50's earlier projects. It's not simply "different"—it serves a real, meaningful purpose for people trying to improve their lives through better habits. The technical implementation shows understanding of database design, backend architecture, frontend interactivity, and user experience design. The application integrates behavioral psychology principles (the importance of emotional awareness in habit formation) with sound software engineering practices (separation of concerns, data normalization, security).

This project represents genuine learning and problem-solving, with each component thoughtfully designed to serve the larger application goal: helping users build sustainable habits while understanding the emotional context of their behavior. 
