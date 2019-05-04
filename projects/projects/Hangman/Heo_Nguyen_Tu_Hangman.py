from __future__ import print_function
import termios, tty, sys, random, time, operator
from color_text import Colors

################################################################################
###                                  TERMINAL                                ###
################################################################################
def stdout_reset(lines):
    '''a set of commands that deletes the current and input lines (int) amount 
    of lines above
    no input, instead writes to screen'''
    sys.stdout.write(u'\u001b[1000D')   #Moves cursor left
    sys.stdout.write(u'\u001b[' + str(lines) + 'A')       #Moves cursor up
    sys.stdout.write(u"\u001b[0J")      #Clears until the end of screen
    
    
def clear():
    '''no input -> None
    Clears system standard output (current line)'''
    sys.stdout.write(u'\u001b[1000D')   #Moves cursor left
    sys.stdout.write(u'\u001b[0K')      #Clears line
    
def decision(choices, selected = 0):
    '''Creates an interactive option-make decisions
    choices = (,)
    color = selected choice's color; defaults to Kolors.blue
    selcted = index of choices that is selected; defaults to 0
    **currently only works for 2 or 3 choices'''
    Kolors = Colors(True)
    color = Kolors.green
    
    tty.setraw(sys.stdin)   #sets up for interactive terminal activities
    
    while 1:
        size = len(choices)
        new_choices = ['  ' + i for i in choices]
        
        new_choices[selected] = color + '> ' + Kolors.underline + \
                                choices[selected] + Kolors.default + \
                                Kolors.Runderline
        
        if size == 2:
            text_to_print = '\t\t' + new_choices[0] + '\t\t\t\t' + \
            new_choices[1]
        elif size == 3:
            text_to_print = '\t\t' + new_choices[0] + '\t\t\t' + \
                            new_choices[1] + '\t\t\t' + new_choices[2]
        
        #Writes decisions in the terminal
        sys.stdout.write('\n')
        sys.stdout.write(text_to_print)
        sys.stdout.write('\n')
        sys.stdout.flush()
        
        
        #The Interactive Portion
        first_key = ord(sys.stdin.read(1))       #collects user input
        
        #CTRL-C
        if first_key == 3:
            print()
            clear()
            #Reverts terminal to original state
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
            raise Exception('''Where you just too lazy to type something in?
            Apollo and Tuetrung are annoyed that you pressed 
            CTRL-C on this amazing game.''')
        
        #ARROW KEYS
        elif first_key == 27:
            next_key = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
            if next_key[0] == 91:
                if next_key[1] == 67:    #Right Arrow
                    selection = 'right'
                elif next_key[1] == 68:  #Left Arrow
                    selection = 'left'
                else:
                    selection = None
        elif first_key in (10, 13):     #Enter/return pressed
            print('\n\n')
            clear()
            #Reverts terminal to original state
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
            return(choices[selected])           #Decision has been made!
        else:
            selection = None
            
        
        #moves selected accordingly
        if selection == 'left':
            new_selected = size - 1 if selected == 0 else selected - 1
        elif selection == 'right':
            new_selected = 0 if selected == size - 1 else selected + 1
        else:
            new_selected = selected
            
        #clears terminal
        clear()
        sys.stdout.write(u'\u001b[1F')
        clear()
        sys.stdout.write(u'\u001b[1F')
        clear()
        
        #Redo loop
        selected = new_selected
    
################################################################################
###                                   INPUT                                  ###
################################################################################
def input(text, extra=0, min_chr=None, min_txt=None, \
          not_in=None, nin_txt='It is already taken.'):
    '''Uses Python3 input module using Python2's raw_input()
    A better version of the raw_input()
    try:
        name = raw_input(text)
    except NameError:
        pass
    finally:
        return name'''
        
    '''
    text = text to come before input
    
    extra (int=0) = extra line above that gets erased
    
    min_chr (None) = minimum character length
    min_txt (str='The character minimum length is {min_chr + 1}. Try again.') 
        = text if data is not greater than min
        
    not_in (tuple=(,)) = checks if data is in or not in not_in
    nin_txt (str='It is already taken.') = if data is in not_in
    '''
    
    tty.setraw(sys.stdin)   #sets up for interactive terminal activities
    
    print('\n')
    sys.stdout.write(u'\u001b[2A')       #Moves cursor up
    sys.stdout.write(text)
    
    data = ''
    index = 0
    
    if min_chr is None:
        min_chr = 0
        
    if min_txt is None:
        min_txt = 'The character minimum length is %s. Try again.' % \
                  str(min_chr + 1)
                  
    # min, nin, special
    offenses = [0, 0, 0]
        
    
    # Personal Terminal
    while True:
        charc = ord(sys.stdin.read(1))  #char code
        
        # Commands
        
        #CTRL-C
        if charc == 3:
            print()
            clear()
            #Reverts terminal to original state
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
            raise Exception('''Where you just too lazy to type something in?
            Apollo and Tuetrung are annoyed at why you pressed 
            CTRL-C on this amazing game.''')

        #INPUT (lower, upper, space)
        elif 65 <= charc <= 90  \
          or 97 <= charc <= 122 \
          or charc == 32:
            
            data = data[:index] + chr(charc) + data[index:] #adds data
            index += 1
            
        #ARROW KEYS
        elif charc == 27:
            chr1 = ord(sys.stdin.read(1))
            chr2 = ord(sys.stdin.read(1))
            
            if chr1 == 91:
                #RIGHT
                if chr2 == 67:
                    index = min(len(data), index + 1)
                
                #LEFT
                elif chr2 == 68:
                    index = max(0, index - 1)
                    
        #ENTER
        elif charc in (10, 13):
            # DEV
            if data == 'DEV':
                print('\n')
                clear()
                #Reverts terminal to original state
                termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, \
                 original_terminal)
                print('DEV mode has been activated')
                return data
                
            
            # too short
            if len(data) <= min_chr:
                stdout_reset(1)
                
                offenses = [0, offenses[1] + 1, 0]
                if offenses[1] == 1:
                    print(min_txt)
                else:
                    print(min_txt + ' x' + str(offenses[1]))
                
            # data is taken
            elif not_in is not None and data in not_in:
                stdout_reset(1)
                
                offenses = [offenses[0] + 1, 0, 0]
                if offenses[0] == 1:
                    print(nin_txt)
                else:
                    print(nin_txt + ' x' + str(offenses[0]))
                
            # send data
            else:
                print('\n')
                clear()
                #Reverts terminal to original state
                termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, \
                 original_terminal)
                return data
                
            
        #BACKSPACE
        elif charc == 127:
            data = data[:-1]
            if index > 0:
                index -= 1
                
        #SPECIAL CHARACTERS
        else:
            stdout_reset(1)
            offenses = [0, 0, offenses[2] + 1]
            print('Special characters ore not allowed.', end='')
            if offenses[2] > 1:
                print(' x' + str(offenses[2]))
            else:
                print()
        
        # Make extra line below
        clear()
        print('\n')
        sys.stdout.write(u'\u001b[2A')       #Moves cursor up
        
        # Show current data
        sys.stdout.write(text)
        sys.stdout.write(data)
        
        # Cursor
        sys.stdout.write(u"\u001b[1000D")   #Move cursor to end
        #Move to index
        sys.stdout.write(u'\u001b[' + str(index + len(text)) + 'C')
        sys.stdout.flush()
  
################################################################################
###                                 SCOREBOARD                               ###
################################################################################
class Scoreboard():
    def __init__(self):
        '''initializes people dictionary'''
        self.people = {}
        self.OFFSET = 7 #random.randint(1, 50)
        
        #funny joke
        if len(self.decrypt()) == 5:
            self.people.update({
                '[ADMIN] Apollo Heo': 1000000000000000,
                '[ADMIN] Tuetrung Nguyen': 1000000000000000,
                '[HACKER] @#$^#@@%%@#$%$#': 9999999999999999,
                'totally-not-Mr. Brown': 999999999999999
            })
            self.update()
    
    def update(self, filename='scoreboard.txt'):
        '''updates scoreboard file, encrypts to binary
        filename defaults to scoreboard.txt -> None'''
        with open(filename, 'r+') as f:
            f.truncate()
            for key, value in self.people.items():
                string_data = key + '&' + str(value)
                write_data = ' '.join(format(ord(char) + self.OFFSET, 'b') \
                    for char in string_data)
                
                real_data = ''
                for bit in write_data.split(' '):
                    real_data += '0' * (8 - len(bit)) + bit + ' '
                f.write(real_data + '\n')
                
    def decrypt(self, filename='scoreboard.txt'):
        '''uses filename (defaults to scoreboard.txt) to update
        Scoreboard().people json object
        filename -> None'''
        self.people = {}
        scores = {}
        with open(filename, 'r') as f:
            people_data = f.read().split('\n')
            
        for person in people_data:
            if person not in ('', '\n'):
                binary_code = person.split(' ')
                current_data = ''
                #Converts binary to text
                for char in binary_code:
                    if char not in ('', '\n'):
                        current_data += chr(int(char, 2) - self.OFFSET)
                    
                #interprets text
                name, score = current_data.split('&')
                scores[name] = int(score)
         
        self.people = scores   
        return scores
        
            
    def add_people(self, person, score):
        '''person, score -> adds player to the scoreboard
        if person already exists, it is overriden'''
        self.people[person] = score
        
    def show_scoreboard(self):
        '''shows scoreboard'''
        INDENT = 15, 40, 67     # for the 3 columns
        with open('ASCII Art/scoreboard_text.txt', 'r') as f:
            scoreboard_text = f.read()
            
        sorted_people = sorted(self.people.items(), key=operator.itemgetter(1) \
        , reverse=True)
        
        counter = 0
        for person in sorted_people:
            counter += 1
            key, value = person[0], str(person[1])
            scoreboard_text += '\n' + ' ' * (INDENT[0] - len(str(counter)))
            scoreboard_text += str(counter) + ' ' * INDENT[1] + key
            extra_space = ' ' * int(INDENT[2] - len(key) - len(value))
            scoreboard_text += extra_space + value
            
        return scoreboard_text + '\n'
        



################################################################################
###                                 FUNCTIONS                                ###
################################################################################
def word_bank():
    '''reads word_bank.txt and stores them as a list that returns'''
    with open('word_bank.txt', 'r') as f:
        words = f.read().split('\n')
        
    return_words = []
    for word in words:
        if word[0] != '#':
            return_words.append(word)
            
    return return_words

def hangman_display(guessed, secret):
    '''Hangman Function, where the player guesses letters. If the player guesses
    all of the words within a certain amount of guesses, then the player wins. 
    If the player passes the amount of guesses given, then the player will lose.
    (tuple, str) -> str
    '''
    for guess in guessed:
        if guess == secret:
            return secret
    
    display_text = ''
    for char in secret:
        if char.lower() in guessed  + (' ',):
            display_text += char
        else:
            display_text += '-'
    return display_text
    
################################################################################
###                                  ASCII ART                               ###
################################################################################
def print_ascii_art(filename):
    '''prints ASCII Art located in the child directory ASCII Art
    filename(str) -> None'''
    with open('ASCII Art/' + filename, 'r') as f:
        return f.read()
        
def eagle_animation_2():
    '''EAGLE INTRO COOL ANIMATION
    APOLLO and TUETRUNG presents
    PRESIDENTS HANGMAN
    does an eagle animation, no input nor output'''
    def print_eagle(eagle, INDENT):
        '''prints eagle with indent'''
        for line in eagle:
            sys.stdout.write('\n')
            clear()
            sys.stdout.write(' ' * INDENT + line)
        sys.stdout.write('\n')
        clear()
        sys.stdout.flush()
        
    with open('ASCII Art/Eagle', 'r') as f:
        eagle = f.read().split('\n')
        
    INDENT = 0
    
    tty.setraw(sys.stdin)   #sets up for interactive terminal activities
    while INDENT < 125:
        print_eagle(eagle, INDENT)
        
        #resets
        sys.stdout.write(u'\u001b[1000D')   #Moves cursor left
        sys.stdout.write(u'\u001b[33A')     #Moves cursor up 33
        sys.stdout.write(u"\u001b[0J")      #Clears until the end of screen
            
        time.sleep(0.08)
        INDENT += 3
        
    #ending centered eagle
    time.sleep(1.15)
    print_eagle(eagle, 55)
    sys.stdout.write('\n')
    clear()
    
    #Reverts terminal to original state
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
    
def eagle_animation():
    '''does an eagle animation, no input nor output'''
    def print_eagle(eagle, INDENT, min_, max_):
        '''prints eagle with indent'''
        print()
        for line in eagle:
            clear()
            line_to_print = ' ' * INDENT + line
            print(line_to_print[min_:min(max_, len(line_to_print))])
        sys.stdout.write('\n')
        clear()
        sys.stdout.flush()
        
    with open('ASCII Art/Eagle', 'r') as f:
        eagle = f.read().split('\n')
        
    INDENT = 0
    MAX_INDENT = 200
    MIN_INDENT = 83
    
    START_1 = MIN_INDENT
    
    tty.setraw(sys.stdin)   #sets up for interactive terminal activities
    
    # MOVES RIGHT
    while INDENT < MIN_INDENT + 15:
        print_eagle(eagle, INDENT, START_1, MAX_INDENT + INDENT)
            
        time.sleep(0.08)
        #resets and moves down
        stdout_reset(33)
        
        INDENT += 3
        
    time.sleep(3.5)
    
    # MOVES LEFT
    while INDENT > -5:
        print_eagle(eagle, INDENT, START_1, MAX_INDENT + INDENT + 100 - INDENT)
        
        time.sleep(0.08)
        #resets if not last
        if INDENT > -2:
            stdout_reset(34)
            
        INDENT -= 3
        
    time.sleep(2)
    
    #Reverts terminal to original state
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
        
    
################################################################################
###                                   SCENES                                 ###
################################################################################
def introduction(scoreboard):
    '''input the scoreboard
    
    Initializes the game, sets it up with:
    -. eagle animation
    -. game name
    -. ask for name
    '''
    Kolors = Colors(True)
    
    LIVES = 5
    
    # eagle animation
    eagle_animation()
    
    # game name
    print('\n' * 2)
    
    # ask for name
    while 1:
        name = input('----- What is your name? (type DEV as the name to view \
the word before you guess. However, your individual score will not be \
displayed in the scoreboard) ', \
        not_in=scoreboard.people, nin_txt='Name is already taken.')
        
        if len(name) >= 30:
            stdout_reset(2)
            print('Name cannot exceed 30 characters.')
        else:
            break

        
    print('That\'s a good name I guess, but Tuetrung is better.')
    
    print('\nUse arrow keys to decide and then press enter.')
    
    return name, LIVES
    
def game_rules(LIVES):
    '''LIVES (int) how many guesses per word -> None
    prints game rules'''
    print('You have %s lives. This means that you have %s tries to guess the \
word until you lose the game. You can guess a letter at a time and clues will \
be given on the length of each word, if there are multiple words. Also the \
position of the letter will be displayed as you guess, and only incorrect \
guesses will count twoards your \"tries\" left.' % (LIVES, LIVES))
    
def play_again(name):
    '''Asks the player if they want to play the game again. If the answer is 
    yes, then gives the player another word/s to guess. If the answer is no, 
    then it exits the game.'''
    print('Would you like to play again?')
    play_again_ = decision(('Yes', 'No'))
    return True if play_again_ == 'Yes' else False
    
################################################################################
###                                    GAME                                  ###
################################################################################
class Player:
    '''Player object to keep track of scoreboard, name and score
    (scoreboard, name) -> (Player)'''
    def __init__(self, scoreboard, name):
        self.scoreboard = scoreboard
        self.name = name
        self.score = 0
        
    def update(self, score, override=False):
        '''score = add score to current
        ovverride (defaults to False) instead overrides instead of adding to 
        current score
        returns None'''
        if override:
            self.score = score
        else:
            self.score += score
            
        self.scoreboard.add_people(self.name, self.score)
        
def check_screen_width():
    '''prints a bunch of -'s to make sure our eagle intro animation will not 
    break
    no input -> None'''
    print('First we need to check the screen width is set up.')
    print('|' + '-' * 235 + '|')
    print('Either zoom out the screen or close down the Cloud9 sidebars to \
expand your screen\'s width. Make sure you can see both | on the same line.')
    print('When you are ready to continue, press enter.')
    
    tty.setraw(sys.stdin)   #sets up for interactive terminal activities
    
    text = 'Press enter to continue '
    
    # Personal Terminal
    while True:
        charc = ord(sys.stdin.read(1))  #char code
        
        #CTRL-C
        if charc == 3:
            print()
            clear()
            #Reverts terminal to original state
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
            raise Exception('''Where you just too lazy to type something in?
            Apollo and Tuetrung are annoyed at why you pressed 
            CTRL-C on this amazing game.''')
            
        #ENTER
        elif charc in (10, 13):
            print('\n')
            clear()
            #Reverts terminal to original state
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, \
             original_terminal)
            break
        
        # Make extra line below
        clear()
        print('\n')
        sys.stdout.write(u'\u001b[2A')       #Moves cursor up
        
        # Shows text
        sys.stdout.write(text)
        sys.stdout.flush()
        
        
    # delete Press enter line
    clear()
    stdout_reset(6)
    sys.stdout.flush()
    
def points_calc(LIVES, random_word, guess_bank):
    '''LIVES (int), random_word (str), guess_bank (tuple) 
    -> calculated score (int)
    uses each option, along with 50 bonus points for winning to be updated to 
    the scoreboard'''
    WIN_SCORE = 50
    
    lives_score = (LIVES) ** 5
    word_score = 35 - len(random_word)
    guess_score = 26 - len(guess_bank)
    
    return WIN_SCORE + lives_score * 8 + word_score * 7 + guess_score * 13
    
def print_game_screen(player, ascii_art, LIVES, word_print, guessed_char, \
                      random_word):
    '''prints game screen with the following inputs:
    player = Player object
    ascii_art = art to display
    LIVES = number of guesses left
    word_print = word the hangman game should show
    guessed_char = all characters user has already guessed
    random_word = hidden word player is trying to guess
    
    and ouput to the screen the following:
    name, score
    ascii art
    word to show
    guessed so far
    guesses left
    guess input'''
    LINE = 150
    print_text = ''
    
    #playser
    name_text = 'Name: %s' % player.name
    score_text = 'Score: %s' % player.score
    empty_space = ' ' * (LINE - len(name_text) - len(score_text))
    name_score_text = name_text + empty_space + score_text
    print_text += name_score_text
    
    print_text += '\n' * 3
    # ascii art
    ascii_text = ''
    ASCII_INDENT = 30
    ascii_image = ascii_art
    
    for line in ascii_image:
        print_text += ' ' * ASCII_INDENT + line + '\n'
        
    print_text += '\n' * 3
    
    
    #word to show
    word_to_show = 'Currently known: %s' % word_print
    
    #guessed so far
    guessed_so_far = 'Guessed so far: %s' % ', '.join(sorted(guessed_char))
    
    #guesses left
    guesses_left = 'Guessed left: %s' % LIVES
    
    print_text += word_to_show + '\n' + guessed_so_far + '\n' + guesses_left
    
    #print
    for line in print_text.split('\n'):
        sys.stdout.write(line + '\n')
        clear()
    sys.stdout.write('\n' * 2)
    
    #DEV
    if player.name == 'DEV':
        print('The word is: %s' % random_word)
        clear()
    
    #guess input
    while 1:
        guess = input('Guess a letter. ')
        if guess.lower() == random_word.lower():
            break
        
        tty.setraw(sys.stdin)   #sets up for interactive terminal activities
        stdout_reset(3)
        
        #fix terminal
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
        
        print()
        
        if True:
        #if len(guess) != 1:
        #    print('You may only guess one letter at a time.')
        #else:
            print()
            break
     
    #return lowercase if only one character   
    if len(guess) == 1:
        return guess.lower()
    else:
        return guess
    
        
def game(lives, player, LIVES, random_word):
    '''game loop: one-word guessing hangman game
    lives(int), player (Player), LIVES (int), random_word(str)
    -> returns LIVES, random_word or None
    depends or if you won or lost, respectively'''
    tty.setraw(sys.stdin)   #sets up for interactive terminal activities
    
    name = player.name
    
    guess_bank = ()
    prev = '', ''
    ascii_art = print_ascii_art('USA Flag').split('\n')
    display_txt = hangman_display(guess_bank, random_word)
        
    while 1:
        guess = print_game_screen(player, ascii_art, lives, display_txt, \
        guess_bank, random_word)
        
        if guess not in guess_bank:
            guess_bank += (guess,)
            
        display_txt = hangman_display(guess_bank, random_word)
        
        prev = prev[1], display_txt
            
        #WINS GAME
        if '-' not in display_txt:
            #fix terminal
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
            clear()
            print('The word was %s!' % random_word)
            time.sleep(1)
            
            print('You won the game %s!' % name)
            time.sleep(1)
            
            earned_pts = points_calc(lives, random_word, guess_bank)
            print('You earned %s points!' % earned_pts)
            time.sleep(2)
            
            player.score += earned_pts
            return LIVES, random_word
            
        #If display_txt hasn't changed yet
        elif prev[0] == prev[1] or \
             prev[1].replace('-', '').replace(' ', '') == '':
            lives -= 1
         
        #GAME OVER   
        if lives == 0:
            #fix terminal
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
            print('The word was %s!' % random_word)
            time.sleep(1)
            print('You lose!')
            return
        
        #resets
        stdout_reset(25)
        
        #DEV
        if player.name == 'DEV':
            stdout_reset(1)
        
def credits():
    '''no input -> None
    Shows credits, printing line by line, giving appreciation to those who 
    deserve it (us)
    At the end, player has a chance to go back to the main menu'''
    tty.setraw(sys.stdin)   #prevents users from messing up format
    
    INDENT = ' '  * 35
    with open('credits.txt', 'r') as f:
        credits_text = f.read().split('\n')
        
    counter = 0
    for line in credits_text:
        if counter <= 5:
            time_sleep = 0.2
        elif counter <= 12:
            time_sleep = 0.4
        else:
            time_sleep = 1
            
        time.sleep(time_sleep)
        print(INDENT + line)
        clear()
        
        counter += 1
        
    #fix terminal
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
        
def main_menu_decision():
    '''Gives the player option to go back to Main Menu or exit the progarm.
    no input -> None'''
    score_menu = decision(('Back to Main', 'Exit Program'))
                
    if score_menu[:4] == 'Back':
        game_menu = 'Play Game'
        no_decision = False
        
    else:
        sys.exit()
        
def cool_text(text):
    '''text (str) -> prints cool text (None)
    This adds spaces, <'s, spaces, the test, spaces, >'s and more spaces
    Then waits 1.5 second'''
    print(' ' * 8 + '<' * 35 + ' ' * 10 + text + ' ' * 10 + '>' * 35)
    time.sleep(1)

def hangman():
    '''runs hangman game
    terminal is set up,
    scoreboard is initialized, 
    animation plays,
    main menu choices are given
    no input -> None'''
    #if True:
    try:
        global original_terminal
        original_terminal = termios.tcgetattr(sys.stdin)    #saves copy
        #WE WILL BREAK THE TERMINAL
        
        #Make sure the screen width is not too small
        check_screen_width()
        time.sleep(1)
        
        #Initialize scoreboard and player
        scoreboard = Scoreboard()
        scoreboard.decrypt()
        _, lives = name, LIVES = introduction(scoreboard)
        player = Player(scoreboard, name)
        scoreboard.add_people(player.name, player.score)
        scoreboard.update()
        
        global no_decision
        no_decision = True
        global game_menu
        
        print()
        
        while 1:
            cool_text('MAIN MENU')
            
            # Canadian Flag
            print(print_ascii_art('Canadian Flag'))
            
            # Decision for User
            if no_decision:
                game_menu = decision(('Play Game', 'Scoreboard', 'Credits'))
            
            # Play Game
            if game_menu[:4] == 'Play':
                game_rules(LIVES)
                
                words = word_bank()
            
                while 1:
                    random_word = random.choice(words)
                    if random_word[0] != '#':
                        break
                    
                guess_bank = ()
            
                while 1:
                    print(hangman_display(('',), random_word))
                    game_return = game(lives, player, LIVES, random_word)
                    #fix terminal
                    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, \
                      original_terminal)
                    
                    #update scoreboard
                    scoreboard.add_people(player.name, player.score)
                    scoreboard.update()
                    
                    if game_return is None:
                        break
                    
                    if play_again(name) is False:
                        break
                    
                    print('Let\'s play again!')
                    words.remove(random_word)
                    guess_bank += (random_word,)
                    random_word = random.choice(words)
                    
                main_menu_decision()
                
            
            # Scoreboard
            elif game_menu == 'Scoreboard':
                print(scoreboard.show_scoreboard())
                main_menu_decision()
                
            # Credits
            elif game_menu == 'Credits':
                credits()
                main_menu_decision()
                
                
    except:
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
        print()
        clear()
        print('Please leave for the next person to try.')
        sys.exit()
        
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, original_terminal)
    
if __name__ == '__main__':
    hangman()