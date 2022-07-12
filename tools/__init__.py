import pandas as pd


class Lexique():

    def __init__(self):
        #On importe le lexique
        lex = pd.read_csv('http://www.lexique.org/databases/Lexique383/Lexique383.tsv', sep='\t')
        lex.dropna(subset = ["ortho"], inplace=True)
        lex = lex[lex["ortho"].str.contains("-")==False]
        lex = lex[lex["ortho"].str.contains(" ")==False]
        self.lex = lex
        self.letters_remaining = {chr(97 + i) : 1 for i in range(26)}
        #On va retirer quelques lettres car quelques lettres ne sont pas présentes dans le bomb party
        self.letters_remaining.pop('k', None)
        self.letters_remaining.pop('w', None)
        self.letters_remaining.pop('x', None)
        self.letters_remaining.pop('y', None)
        self.letters_remaining.pop('z', None)


    def reset_remaining(self):
        for key, value in self.letters_remaining.items():
            if value != 0 :
                return False

        self.letters_remaining = {chr(97 + i) : 1 for i in range(26)}
        #On va retirer quelques lettres car quelques lettres ne sont pas présentes dans le bomb party
        self.letters_remaining.pop('k', None)
        self.letters_remaining.pop('w', None)
        self.letters_remaining.pop('x', None)
        self.letters_remaining.pop('y', None)
        self.letters_remaining.pop('z', None)

        return True



    def remove_word(self, word):
        self.lex[self.lex["ortho"] != word]


    def look_for(self, substr) :

        proposition = self.lex.loc[self.lex['ortho'].str.contains(substr, case=False)]

        secu = proposition.sample().iloc[0]['ortho']

        i_max = 0
        score_max = 0

        i = 0
        score = 0
        for index, row in proposition.iterrows():
            word_test = row['ortho']
            for key,value in self.letters_remaining.items():
                if value != 0 and key in word_test :
                    score += 1

            if score > score_max :
                i_max = i

            score = 0
            i += 1

        word = proposition.iloc[i_max]['ortho']

        self.remove_word(word)

        return word,secu




def select_coord(img_name):
    import numpy as np
    import pyautogui
    from PIL import Image
    import matplotlib.widgets as widgets
    import matplotlib.pyplot as plt

    pyautogui.screenshot(img_name)

    def onselect(eclick, erelease):
        global x1, y1, x2, y2
        if eclick.ydata>erelease.ydata:
            eclick.ydata,erelease.ydata=erelease.ydata,eclick.ydata
        if eclick.xdata>erelease.xdata:
            eclick.xdata,erelease.xdata=erelease.xdata,eclick.xdata
        ax.set_ylim(erelease.ydata,eclick.ydata)
        ax.set_xlim(eclick.xdata,erelease.xdata)
        fig.canvas.draw()

        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata


    fig = plt.figure()
    ax = fig.add_subplot(111)

    im = Image.open(img_name)
    arr = np.asarray(im)
    plt_image=plt.imshow(arr)
    rs=widgets.RectangleSelector(
        ax, onselect, drawtype='box',
        rectprops = dict(facecolor='blue', edgecolor = 'black', alpha=0.5, fill=True))
    plt.show()

    x_min, x_max = min(x1,x2), max(x1,x2)
    y_min, y_max = min(y1,y2), max(y1,y2)
    return x_min, y_min, x_max - x_min, y_max - y_min
