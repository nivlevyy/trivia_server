<h1 align="center">
  <a><img src="https://github.com/nivlevyy/trivia_server/blob/main/image/trivia_server.webp" width="300"></a>
<br>
# Trivia Game: Server-Client Application**
<br>
</h1>

## **Overview**
This project is a multiplayer trivia game built using a client-server architecture. The server handles multiple clients simultaneously, manages user data and trivia questions, and ensures smooth gameplay. The clients communicate with the server to log in, answer questions, view scores, and more.

---

## **Features**
### **Server**
- Manages user authentication (login/logout) and maintains active user sessions.
- Serves trivia questions stored in a local JSON file or fetched dynamically from a web API.
- Tracks user scores and provides high scores globally.
- Supports multiple simultaneous client connections using the `select` system call.
- Includes robust error handling and logging mechanisms.

### **Client**
- User-friendly CLI for logging in, answering questions, and viewing scores.
- Allows users to:
  - Answer trivia questions.
  - View personal scores and global high scores.
  - See logged-in users.
- Handles communication with the server using a custom protocol.

---

## **Technologies Used**
- **Programming Language**: Python
- **Networking**: TCP sockets
- **Data Handling**: JSON
- **Logging**: Python’s `logging` module for debugging and tracking server and client activities.

---

## **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/trivia-game.git
   ```
2. Navigate to the project directory:
   ```bash
   cd trivia-game
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **How to Run**
### **Start the Server**
1. Run the server using:
   ```bash
   python server_tcp.py
   ```
2. The server will start listening on `0.0.0.0:5678` by default.

### **Start a Client**
1. Run the client using:
   ```bash
   python client_tcp.py
   ```
2. Follow the on-screen prompts to log in or register and start playing.

---

## **Game Workflow**
1. Users log in or register through the client interface.
2. Clients can request:
   - Trivia questions
   - Personal or global high scores
   - Logged-in user list
3. Users answer questions to earn points.
4. The server updates scores and handles all communication with active clients.

---

## **File Structure**
- **`server_tcp.py`**: Implements the server logic, handling multiple clients and game data.
- **`client_tcp.py`**: Implements the client-side logic for user interaction and communication with the server.
- **`logger_manager.py`**: Manages logging functionality for both server and clients.
- **`Users.json`**: Stores user credentials and scores.
- **`questions.json`**: Stores trivia questions and answers.

---

## **Future Enhancements**
- Add a graphical user interface (GUI) for the client.
- Implement advanced authentication mechanisms (e.g., hashed passwords).
- Add support for more question types (e.g., true/false).

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

---

