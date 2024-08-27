# Chess-Like Game
This project is a chess-like game featuring custom characters with distinct movement and attack abilities. Players can select their characters and compete in a turn-based game with real-time multiplayer functionality using WebSockets.
# Project Structure

* ```index```  - Contains the client-side code (HTML, CSS, JavaScript) and static assets like images.
* ```server``` - Contains the server-side code (Node.js with Express and WebSocket).

# Run Locally

1. Clone the project

       git clone https://github.com/heyyvaibhav/Vaibhav_Agarwal_21BAI10433.git

2. Install dependencies

    Install the necessary packages for the server using npm:

        pip install websockets
3. Start the server

    Start the server with the following command:

        python server.py
    
    The server will be accessible at:

        ws://localhost:6789

4. Open the Web Client
   
    * Open the ```index.html``` file in two different browser windows (or tabs).
      
    * Both windows should connect to the server as different players.
      
5. Setup and Play the Game
   
    * Character Selection: Click on your characters (labeled with "A-" or "B-") to select them.
      
    * Highlight Valid Moves: After selecting a character, valid moves will be highlighted in green.
    
    * Performing Moves: Click on a highlighted cell to move the selected character.
    
    * Game Over: The game checks for a win condition after each move.

  # Features

  * Character Selection: Players can choose characters including Pawn, Hero1 and Hero2.

  * Real-time Gameplay: Moves and game state updates are transmitted in real-time using WebSockets.

  * Turn-based Mechanics: The game alternates turns between players.

# Characters and Movement

There are three types of characters available:

1. Pawn:

    * Moves one block in any direction (Left, Right, Forward, or Backward).

    * Move commands: L (Left), R (Right), F (Forward), B (Backward)

2. Hero1:

    * Moves two blocks straight in any direction.

    * Kills any opponent's character in its path.

    * Move commands: L (Left), R (Right), F (Forward), B (Backward)

3. Hero2:

    * Moves two blocks diagonally in any direction.

    * Kills any opponent's character in its path.

    * Move commands: FL (Forward-Left), FR (Forward-Right), BL (Backward-Left), BR (Backward-Right)
      

All moves are relative to the player's perspective.
