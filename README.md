The server can only play the game with one client

ServerTCP-UDP.py
      1. Server receives a command ‘-r’ to pick a word randomly or a custom string to be used
      throughout the program
      2. It creates a TCP socket and accepts a connection from a client
      3. Receives a ‘name’ from a user and sends back ‘Hello .{}’.format(name)
      4. Creates a UDP Socket and sends its port number to the client to start a game
      5. Reads from a words.txt and creates a list of words called ‘words’
      6. Receives a start or exit message in a loop from a client, from which a client can enter
      ‘exit’ to exit
      7. Sends instructions and starts the game
      8.
      If a custom string is not provided. It shuffles the ‘words’ list and chooses one word
      9. Creates a dashed version of that word and sends it and len(word)+1 as a count to the
      client
      10. In another loop it plays the game receiving back ‘guess <char>’ and checking against
      characters in the word. If the character in the list, it replaces all instances of that char in
      the dasher version and sends it back including (len(word)+1) - count[count is
      incremented previously]
      11. Client can exit guessing loop by entering ‘end’. If a client runs out of guesses he/she
      loses.
      12. Client can also guess an entire word by entering guess <string> and the game for
      guessing this word will finish if the guessed word is right or wrong
      13. If client sends an exit message, server closes the ports and waits for the new
      connections
      
ClientTCP-UDP.py
      1. Receives name of the server host and its port number
      2. Creates a TCP socket and connects
      3. Sends a name to Server and receives back hello+name
      4. Receives UDP port number from server
      5. Creates its own UDP port number and interacts with the server
      6. It has two loops to interact with the server first loop to start or exit(in which it receives
      instructions) and the second loop for playing the game by guessing letters of a word that
      is provided.
      7. In the game you can enter guess<sp><char> -> to guess a letter, guess<sp><string> ->
      to guess an entire word, end -> to end this game
