from socket import *
import random


def Server(command):

    inst = "This is hangman You will guess one letter at a time. If the letter is in the hidden word the '-' will be\n" \
          "replaced by the correct letter Guessing multiple letters at a time will be considered as guessing the entire\n"\
          "word (which will result in either a win or loss automatically - win if correct, loss if incorrect).You win\n"\
          "if you either guess all of the correct letters or guess the word correctly. You lose if you run out of\n" \
          "attempts. Attempts will be decremented in the case of an incorrect or repeated letter guess.\n" \
          "Enter 'Start' or 'Exit' when you're asked 'Are you Ready?' " \
          "In the game you must enter 'guess <char>' to guess or 'end' to end the game\n"

    print("Server is on")

    host = 'localhost'
    port = 5000
    print('Creating TCP socket')
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print('TCP is on')

    while True:
        c, addr = s.accept() # accept
        print("Huston, we have a connection" + str(addr))

        data = c.recv(1024).decode('utf-8')                 # received from client
        print("User's name is: ", data)
        r = "Hello "+data
        c.send(r.encode('utf-8'))
        # now udp-------------------------------------------------------

        h = '127.0.0.1'
        p = 5001
        print("Creating UDP socket")
        u = socket(AF_INET, SOCK_DGRAM)
        u.bind((h, p))
        print("Sending UDP port number to client using TCP connection...")
        c.send(str(p).encode('utf-8'))

        words = []
        with open("words.txt", 'r') as file:
            for line in file:
                line = line.strip()
                words.append(line)

        com, adds = u.recvfrom(1024)                        # 1 receive
        com = com.decode('utf-8').lower()                   # receive 'start' message or 'exit'

        while com != 'exit':
            u.sendto(inst.encode('utf-8'), adds)            # 2 send instructions
            random.shuffle(words)                           # shuffle the list and take the first
            display = []

            if command == '-r':
                word = list(words[0])                       # made it list
            else:
                word = list(command)
            print('Hidden word: ', word)
            for i in range(len(word)):
                display.append('_')
            count = 0

            display = list(display)
            print('The game is on,guess')
            u.sendto((str(display)+str((len(word)+1)-count)).encode('utf-8'), adds)            # 3 send words and count
            char, adds = u.recvfrom(1024)                   # get a guess <>, end. 4 Receive char

            while True and count < len(word)+1:
                print(char.decode('utf-8'))
                char = char.decode('utf-8').lower()
                count += 1
                if char[:3] == 'end':
                    u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
                    u.sendto(("You LOST! The word was " + str(word)).encode('utf-8'), adds)
                    break
                elif len(char) > 7:                         # it means you are trying to guess the entire word
                    o = char[6:]
                    print(o)
                    if fun(word, o):
                        u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
                        u.sendto(("You got it!!! Bulls eye! the word is " + str(o)).encode('utf-8'), adds)
                        break
                    else:
                        u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
                        u.sendto(("You LOST! The word was " + str(word)).encode('utf-8'), adds)
                        break
                elif char[:5] == 'guess':
                    display = list(display)
                    r = char[len(char) - 1]

                    for i in range(len(word)):
                        if word[i] == r:
                            display[i] = r

                    if display == word:
                        u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
                        u.sendto(("You got it!!! Bulls eye! the word is "+str(display)).encode('utf-8'), adds)
                        break
                    else:
                        u.sendto(str((len(word)+1)-count).encode('utf-8'), adds)    # 5 send count
                        print('Sending display ', display)
                        u.sendto(str(display).encode('utf-8'), adds)                # 6 send the word

                char, adds = u.recvfrom(1024)                                       # 7 Receive char again
            if display != word and count > len(word)+1:
                u.sendto(str((len(word)+1) - count).encode('utf-8'), adds)
                u.sendto(("You LOST! The word was "+str(word)).encode('utf-8'), adds)

            com, adds = u.recvfrom(1024)                                            # 8 Receive start or exit
            com = com.decode('utf-8')
            print("received com which is: ", com)
            if com == 'exit':
                break
        f, adds = u.recvfrom(1024)
        f = f.decode('utf-8')
        print(f)

        u.sendto("Closing UDP and TCP sockets...".encode('utf-8'), adds)             # 9 send end message
        u.close()
    s.close()


def fun(word, string):          # first is the current word, second received string
    string = list(string)
    for i in range(len(word)):
        if word[i] != string[i]:
            return False
    return True


a = input("Enter only '-r' (for random words) or any word:")
Server(a)
