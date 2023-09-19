################################################ IMPORTS #############################################################

import ex11_utils as utils
import game_logic
import game_GUI_interface
import tkinter as tk
from typing import List, Tuple, Iterable, Optional, Dict, Callable, Any
import time
from pygame import mixer


################################################ CONSTANTS #############################################################
WORDS_FILE_NAME = "boggle_dict.txt"
ALL_WORDS = set(open(WORDS_FILE_NAME, "r").read().split("\n"))
EMPTY_WORD = ""
ORIGINAL_MESSAGE = "you can continue the game"
################################################ NOTES #################################################################
# YOU SHOULD RUN THIS FILE
########################################################################################################################


class BoggleController:
    def __init__(self):
        self.__board = utils.randomize_board()
        self.__board_width = len(self.__board[0])
        self.__board_height = len(self.__board)

        self.__gui = game_GUI_interface.Boogle_Gui(
            board=self.__board, words=ALL_WORDS)
        self.__game = game_logic.BoggleGame(
            board=self.__board, words=ALL_WORDS)
        self.__buttons_dict = self.__gui.get_button_dict()

        self.__init_buttons_commands()

        self.__init_labels()

    def __init_labels(self):
        # init score Label
        current_score = self.__game.get_score()
        self.__gui.set_score_display(current_score)
        # init message Label
        current_message = self.__gui.set_message_display(
            "You have 3 minutes! To start the game press START")
        self.__gui.set_score_display(current_score)
        # init current_word Label
        self.__gui.set_curr_word_display(EMPTY_WORD)
        # init previously selected legal words
        self.__gui.set_selected_words_display(EMPTY_WORD)
        # init time label
        self.time = 180

    def __init_buttons_commands(self):
        # create board buttons commands - reference buttons by coordinates
        for button_coord in self.__buttons_dict["board"]["coordinates"]:
            action = self.__init_command(button_coord)
            self.__gui.set_board_button_command(button_coord, action)

        # create display buttons commands - reference button by character
        for button_text in self.__buttons_dict["display"]["characters"]:
            action = self.__init_command(button_text)
            self.__gui.set_display_button_command(button_text, action)

    def __init_command(self, button_val: Any) -> Callable:
        """
        method used to create command for bottons in the gui_interface
        used in __init_buttons_commands
        """
        # board_commands
        if button_val in self.__buttons_dict["board"]["coordinates"]:
            def command():

                # check if can add to path
                # update gui interface and append coord to curr_path
                if self.__game.can_add_to_path(button_val):
                    current_word = self.__game.get_curr_word()
                    self.__gui.set_curr_word_display(current_word)
                else:
                    # make sound
                    mixer.init()
                    mixer.music.load("GUI_music/wrong_string.mp3")
                    mixer.music.play()
                    # display message
                    text, subsequent_text = "wrong coordinate chosen! choose again !", "continue playing the game! time is ticking.."
                    self.__gui.update_label(
                        "message", text, subsequent_text, 5000)
            return command

        # display commands
        elif button_val == "Submit":
            def command():
                if self.__game.is_curr_path_legal():
                    # set current word to be empty
                    self.__gui.set_curr_word_display(EMPTY_WORD)

                    # update score
                    self.__gui.set_score_display(self.__game.get_score())

                    # updates pre_selected_words
                    current_words_display = ",".join(
                        self.__game.get_legal_chosen_words())
                    self.__gui.set_selected_words_display(
                        current_words_display)

                    # display message
                    text, subsequent_text = "GREAT JOB", "continue playing the game! time is ticking.."
                    self.__gui.update_label(
                        "message", text, subsequent_text, 3000)

                    # make sound
                    mixer.init()
                    mixer.music.load("GUI_music/good_word.mp3")
                    mixer.music.play()
                else:
                    # display message
                    text, subsequent_text = "the word chosen was chosen illegally or it is not a word", "continue playing the game! time is ticking.."
                    self.__gui.update_label(
                        "message", text, subsequent_text, 3000)

                    # make sound
                    mixer.init()
                    mixer.music.load("GUI_music/wrong_word.mp3")
                    mixer.music.play()

            return command

        elif button_val == "EndGame":
            def command():
                # make sound
                mixer.init()
                mixer.music.load("GUI_music/end_game.mp3")
                mixer.music.play()

                # set message
                self.__gui.set_message_display("The game has ended, goodby")
                self.__gui.end_game()
                # remove submit and endgame buttons
                self.__buttons_dict["display"]["buttons"][1].destroy()
                self.__buttons_dict["display"]["buttons"][0].destroy()
            return command

        elif button_val == "Start":
            def command():
                # make sound
                mixer.init()
                mixer.music.load("GUI_music/start.mp3")
                mixer.music.play()
                # reveal relevant frames at start of game
                self.__buttons_dict["display"]["buttons"][2].grid(
                    row=3, column=0, sticky=tk.NSEW)
                self.__buttons_dict["display"]["buttons"][1].grid(
                    row=2, column=0, sticky=tk.NSEW)
                self.__buttons_dict["display"]["buttons"][0].grid(
                    row=1, column=0, sticky=tk.NSEW)

                upper_frame = self.__gui.get_frame("upper")
                upper_frame.pack(side="top", fill="both", expand=True)

                middle_frame = self.__gui.get_frame("middle")
                middle_frame.pack(side="top", fill="both", expand=True)

                # display start message
                text, subsequent_text = "The game has started", "you can chose words"
                self.__gui.update_label("message", text, subsequent_text, 3000)

                # initialize start timer
                current_time = time.time()
                self.__gui.set_time_display(end_time=current_time+180)

                # destroy button start after pressed
                self.__buttons_dict["display"]["buttons"][-1].destroy()
            return command

    def run(self) -> None:
        self.__gui.run_interface()


if __name__ == "__main__":
    BoggleController().run()
