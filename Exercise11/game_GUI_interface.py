import tkinter as tk
import ex11_utils
from typing import List, Tuple, Iterable, Optional, Dict, Set,TypeVar
import time

################################################ CONSTANTS ############################################################
BUTTON_HOVER_COLOR = "red"
REGULAR_COLOR = "lightgray"
BUTTON_ACTIVE_COLOR = "slateblue"
BUTTON_STYLE = {"font": ("Courier", 30), "borderwidth": 1, "relief": tk.RAISED, "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}

################################################ VARIABLES ############################################################
Board = List[List[str]]
data : Dict[str, Dict[str, List]]
########################################################################################################################

class Boogle_Gui:
    # Init dict containing all data needed for the controller to operate
    __buttons_dict = {}
    __buttons_dict["board"] = {}
    __buttons_dict["board"]["buttons"] = []
    __buttons_dict["board"]["characters"] = []
    __buttons_dict["board"]["coordinates"] = []
    __buttons_dict["display"] = {}
    __buttons_dict["display"]["buttons"] = []
    __buttons_dict["display"]["characters"] = ["Submit","EndGame","Start"]

    def __init__(self, board: Board, words: Set):
        self.board = board
        self.board_width = len(board[0])
        self.board_height = len(board)
        self.correct_words: List = []

        # init main window
        root = tk.Tk()
        root.title("Boggle Game")
        root.geometry("450x900")
        # root.resizable(False,False)
        self.__main_window = root


        # init upper, middle, lower frames
        self.__init_frames()
        # init buttons for upper and lower frames
        self.__init_buttons_in_given_frame()
        # init labels
        self.__init_labels()
    def __init_frames(self):
        # create upper frame
        self.__upper_frame = tk.Frame(self.__main_window, bg="brown", highlightbackground=REGULAR_COLOR,
                                      highlightthickness=7, padx=6, pady=6, bd=2, relief="solid")
        self.__upper_frame.pack(side="top", fill="both", expand=True)
        self.__upper_frame.pack_forget()

        # create middle frame
        self.__middle_frame = tk.Frame(self.__main_window, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                       highlightthickness=5, padx=6, pady=6, bd=2, relief="solid")
        self.__middle_frame.pack(side="top", fill="both", expand=True)
        self.__middle_frame.pack_forget()

        # create lower frame
        self.__lower_frame = tk.Frame(self.__main_window, bg="brown", highlightbackground=REGULAR_COLOR,
                                      highlightthickness=5, padx=6, pady=6, bd=2, relief="solid")
        self.__lower_frame.pack(side="bottom", fill="both", expand=True)

    def __init_labels(self):
        # Label of current selected word
        self.__curr_word_display = tk.Label(self.__middle_frame, font=("Courier", 25), bg="black", width=23,
                                            relief="ridge")
        self.__curr_word_display.pack(side="top", fill="x")
        # Label of all prev selected legal words
        self.__selected_words_display = tk.Label(self.__middle_frame, font=("Courier", 25), bg="black", width=23,
                                                 relief="ridge")
        self.__selected_words_display.pack(side="top", fill="x",expand=True)
        # Label of the score from beginning of game
        self.__score_display = tk.Label(self.__middle_frame, font=("Courier", 30), bg="black", width=23, relief="ridge")
        self.__score_display.pack(side="top", fill="x")
        # Label of the message for the player
        self.__message_display = tk.Label(self.__middle_frame, font=("Courier", 25,"bold"), bg="black", width=23,
                                          relief="ridge")
        self.__message_display.pack(side="top", fill="both")

        # Label of the time left
        self.__time_display = tk.Label(self.__middle_frame, font=("Courier", 25, "bold"), bg="black", width=23,
                                       relief="ridge")
        self.__time_display.pack(side="top", fill="x")

    def __init_buttons_in_given_frame(self):
        """
        Method used to create game buttons.
        used in Initiation
        """
        # create grid (allow it to be resized with main window)
        for col in range(self.board_height):
            self.__upper_frame.columnconfigure(col, weight=1)

        for row in range(self.board_width):
            self.__upper_frame.rowconfigure(row, weight=1)

        # create buttons for Board
        for row in range(self.board_height):
            for col in range(self.board_width):
                button_char = self.board[row][col]
                self.__buttons_dict["board"]["characters"].append(button_char)
                self.__buttons_dict["board"]["coordinates"].append((row,col))
                self.__make_button(self.__upper_frame, button_char, BUTTON_STYLE, row, col)

        # create display buttons
        self.__make_button(self.__lower_frame, "Submit", BUTTON_STYLE, row=0, col=0,pack = False)
        self.__make_button(self.__lower_frame, "EndGame", BUTTON_STYLE, row=1, col=0,pack=False)
        self.__make_button(self.__lower_frame, "Start", BUTTON_STYLE, row=3, col=5)

    def __make_button(self, daddy_frame, button_char: str, button_style: dict, row: int, col: int,pack = True) -> None:
        """
        general method used to initiate a button in the GUI interface
        """
        button = tk.Button(daddy_frame, text=button_char, **button_style)
        if pack:
            button.grid(row=row, column=col, sticky=tk.NSEW)

        if button_char in self.__buttons_dict["board"]["characters"]:
            self.__buttons_dict["board"]["buttons"].append(button)
        else:
            self.__buttons_dict["display"]["buttons"].append(button)

        def __on_enter(event) -> None:
            button['background'] = BUTTON_HOVER_COLOR

        def __on_leave(event) -> None:
            button['background'] = REGULAR_COLOR

        button.bind("<Enter>", __on_enter)
        button.bind("<Leave>", __on_leave)



    ################################################ GETTERS ############################################################

    def get_button_dict(self):
        return self.__buttons_dict

    def get_label_display(self, text: str) -> tk.Label:
        """
        method that return the corresponding label
        :param text:
        """
        if text == "score":
            return self.__score_display
        if text == "message":
            return self.__message_display
        if text == "curr_word":
            return self.__curr_word_display
        if text == "chosen_words":
            return self.__selected_words_display
        if text == "time":
            return self.__time_display

    def get_frame(self, text: str):
        """
        function that returns the frames in main_window
        """
        if text == "upper":
            return self.__upper_frame
        if text == "middle":
            return self.__middle_frame
        if text == "lower":
            return self.__lower_frame

    ################################################ SETTERS ############################################################

    def set_time_display(self, end_time) -> None:
        """
        method to set the intial time for the game
        will update time label every second
        """
        curr_time = time.time()
        time_left = int(end_time - curr_time)
        if time_left > 0:
            self.__time_display["text"] = str(time_left) + " sec left to play"
            self.__main_window.after(1000, self.set_time_display, end_time)
        else:
            self.set_message_display("time is up the game is over")
            self.__time_display.after(3000, lambda: self.end_game())

    def set_message_display(self, display_text: str) -> None:
        self.__message_display["text"] = "INFO: " + display_text

    def set_curr_word_display(self, display_text: str) -> None:
        self.__curr_word_display["text"] = "current word: " + display_text

    def set_selected_words_display(self, display_text: str) -> None:
        self.__selected_words_display["text"] = "good words: " +display_text

    def set_score_display(self, new_score: int) -> None:
        self.__score_display["text"] = "score: " + str(new_score)

    def set_board_button_command(self, button_coords, cmd) -> None:
        """
        method that uses button_coordinate to setup relevant button. (by char doesnt work)
        """
        button_idx = self.__buttons_dict["board"]["coordinates"].index(button_coords)
        self.__buttons_dict["board"]["buttons"][button_idx].configure(command=cmd)

    def set_display_button_command(self, button_char, cmd) -> None:
        """
        method that uses button_char to setup relevant diaplay button.
        """
        button_idx = self.__buttons_dict["display"]["characters"].index(button_char)
        self.__buttons_dict["display"]["buttons"][button_idx].configure(command=cmd)


    def update_label(self,label, text, after_text, time):
        if label == "message":
            label = self.__message_display
        label.config(text=text)
        label.after(time, lambda: label.config(text=after_text))

    ################################################ INTERFACE ############################################################

    def run_interface(self) -> None:
        """
        method used to run the interface
        """
        self.__main_window.mainloop()

    def end_game(self) -> None:
        self.__main_window.after(11000,lambda :self.__main_window.destroy())

