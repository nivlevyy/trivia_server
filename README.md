<h1 align="center">
  <a><img src="https://github.com/nivlevyy/trivia_server/blob/main/image/trivia_server.webp" width="300"></a>
<br>
Trivia Game: Server-Client Application
<br>
</h1>

## Overview

This project is a multiplayer trivia game built using a client-server architecture. The server handles multiple clients simultaneously, manages user data and trivia questions, and ensures smooth gameplay. Clients communicate with the server to log in, answer questions, view scores, and more.

---

## Features

### Server
- Manages user authentication (login/logout) and maintains active user sessions.
- Serves trivia questions stored in a local JSON file or fetched dynamically from a web API.
- Tracks user scores and provides global high scores.
- Supports multiple simultaneous client connections using the `select` system call.
- Includes robust error handling and logging mechanisms.

### Client
- User-friendly CLI for logging in, answering questions, and viewing scores.
- Allows users to:
  - Answer trivia questions.
  - View personal scores and global high scores.
  - See logged-in users.
- Handles communication with the server using a custom protocol.

---

## Technologies Used

- **Programming Language**: Python
- **Networking**: TCP sockets
- **Data Handling**: JSON
- **Logging**: Python’s `logging` module

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nivlevyy/trivia_server.git
   ```
2. Navigate to the project directory:
   ```bash
   cd trivia_server
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

### Start the Server
Run the server:
```bash
python main.py --role server --port 5678 --host 0.0.0.0
```

### Start a Client
Run the client:
```bash
python main.py --role client --port 5678 --host 127.0.0.1
```

---

## Game Workflow

1. **Log In or Register:**
   - Clients can log in with a username and password or register a new account.
   - Default users are stored in `Users.json`. You can add more manually.
2. **Gameplay Options:**
   - `1`: Answer trivia questions.
   - `2`: View personal scores.
   - `3`: View global high scores.
   - `4`: See logged-in users.
   - `5`: Quit the game.
3. **Questions Handling:**
   - Questions are retrieved from `questions.json` or dynamically fetched from a web API (configurable in the server).
4. **Scoring:**
   - Correct answers increase the user’s score.
   - High scores are displayed in descending order.

---

## Configuration

- **Switch Questions Source:**
  Modify `load_questions` or `load_questions_from_web` in `server_tcp.py`:
  ```python
  questions = self.load_questions()  # Local JSON
  # OR
  questions = self.load_questions_from_web()  # Web API
  ```

- **Change Port or Host:**
  Specify these options when running `main.py`:
  ```bash
  python main.py --role server --port 5678 --host 0.0.0.0
  python main.py --role client --port 5678 --host 127.0.0.1
  ```

---

## File Structure

```plaintext
trivia_server/
├── main.py                # Entry point for server or client
├── server_tcp.py          # Server logic
├── client_tcp.py          # Client logic
├── logger_manager.py      # Logging functionality
├── Users.json             # User data
├── questions.json         # Trivia questions
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
```

---

## Future Enhancements

- Add a graphical user interface (GUI) for the client.
- Implement advanced authentication (e.g., hashed passwords).
- Add support for more question types (e.g., true/false).

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---




