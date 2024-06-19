from tkinter import *
from tkinter import messagebox
import random

class MineSweeperCell(Label):
    '''represents a MineSweeper cell'''

    def __init__(self,master,coord,valueDict):
        '''MineSweeperCell(master,coord) -> MineSweeperCell
        creates a new blank MineSweeperCell with (row,column) coord'''
        Label.__init__(self,master,height=1,width=2,text='',\
                               bg='white',font=('Arial',24),relief='raised')
        self.coord = coord
        self.shown = False
        self.canFlag = True
        self.value = valueDict
        #set up listeners
        self.bind('<Button-1>', self.expose)
        self.bind('<Button-3>', self.set_flag)

    def get_coord(self):
        '''MineSweeperCell.get_coord() -> tuple
        returns the (row,column) coordinate of the cell'''
        return self.coord

    def get_value(self):
        '''MineSweeperCell.get_value() -> string
        returns the string of the cell (Bomb, blank, or number)'''
        return self.value[self.coord]

    def is_expose(self):
        '''MineSweeperCell.is_shown() -> boolean
        returns True if the cell value is shown, False if not'''
        return self.shown

    def expose(self, event):
        '''MineSweeperCell.show()
        shows what value the cell contains'''
        colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
        self['text']=self.value.get(self.coord) #change the text of the cell
        if type(self.value.get(self.coord))==int:
            self['fg']=colormap[self.value.get(self.coord)]
            self['bg'] = 'lightgrey'
        elif self.value.get(self.coord)=='':
            self['bg'] = 'lightgrey'
            self.master.auto_expose(self.coord)
        elif self.value.get(self.coord)=='*':
            self.master.end_game() #game ends when a bomb is pressed
        self.shown = True 
        self.canFlag = False
        self.master.check_win()
            
    def set_flag(self, event):
        '''MineSweeperCell.set_flag()
        sets a flag onto the cell'''
        if self.canFlag == True:
            self['text'] = '*'
            self.bind('<Button-1>', self.nothing) #disable the button
            self.bind('<Button-3>', self.unset_flag)
            self.master.change_numbomb('1')
            self.shown = True
            self.canFlag = False

    def nothing(self, event):
        '''MineSweeperCell.nothing()'''
        pass

    def unset_flag(self, event):
        '''MineSweeperCell.unset_flag()
        unset the flag that is set onto the cell'''
        self['text'] = ''
        self.bind('<Button-1>', self.expose) #activate the button
        self.bind('<Button-3>', self.set_flag)
        self.master.change_numbomb('2')
        self.shown = False
        self.canFlag = True

class MineSweeperGrid(Frame):
    '''object for MineSweeper grid'''

    def __init__(self,master,numrow,numcolumn,numbomb):
        '''MineSweeperGrid(master)
        creates a new blank MineSweeper grid'''
        Frame.__init__(self,master,bg='black')
        self.grid()
        self.numbomb = numbomb
        self.numrow = numrow
        self.numcolumn = numcolumn
        self.numBombFrame = Frame(self,bg='white')
        self.numBombFrame.grid(row=numrow*2+1)
        self.numBombLabel = Label(self.numBombFrame,text=self.numbomb,font=('Arial',24))
        self.numBombLabel.grid(row=numrow*2+1,column=numcolumn)
        self.cells = {}
        self.valueList = []
        for x in range(numbomb):
            self.valueList.append('*')
        for x in range((self.numrow*numcolumn)-numbomb):
            self.valueList.append('empty')
        random.shuffle(self.valueList)
        #set up the numbers according to nearby bombs
        for x in range(len(self.valueList)):
            a = 0
            if self.valueList[x]=='empty':
                if x > numcolumn-1: #if not in first row 
                    if self.valueList[x-numcolumn]=='*': #check cell above
                        a+=1
                if x < len(self.valueList)-numcolumn: #if not in last row
                    if self.valueList[x+numcolumn]=='*': #check cell below
                        a+=1
                if (x+1)%numcolumn != 0: #if not in last column
                    if self.valueList[x+1]=='*': #check cell on the right
                        a+=1
                if x%numcolumn != 0: #of not in first column
                    if self.valueList[x-1]=='*': #check cell on the left
                        a+=1
                if x < len(self.valueList)-numcolumn and (x+1)%numcolumn != 0: #if not last row nor last column
                    if self.valueList[x+numcolumn+1]=='*': #check cell on the bottom right
                        a+=1
                if x < len(self.valueList)-numcolumn and x%numcolumn != 0: #if not last row nor first column
                    if self.valueList[x+numcolumn-1]=='*': #check cell on the bottom left
                        a+=1
                if x > numcolumn-1 and x%numcolumn != 0: #if not first row nor first column
                    if self.valueList[x-numcolumn-1]=='*': #check cell on top left
                        a+=1
                if x > numcolumn-1 and (x+1)%numcolumn != 0: #if not first row nor last column
                    if self.valueList[x-numcolumn+1]=='*': #check cell on top right
                        a+=1
                if a == 0: #if no bombs nearby
                    self.valueList[x] = '' #empty cell
                else:
                    self.valueList[x] = a #integer cell
        self.value={}
        b = 0
        #set up a dict that puts the values in terms of coordinate
        while b != numrow*numcolumn:
            for row in range(numrow):
                for column in range(numcolumn):
                    coord = (row,column)
                    self.value[coord] = self.valueList[b]
                    b += 1
        #set up the cells
        for row in range(numrow):
            for column in range(numcolumn):
                coord = (row,column)
                self.cells[coord] = MineSweeperCell(self,coord,self.value)
                self.cells[coord].grid(row=2*row,column=2*column)

    def end_game(self):
        '''MineSweeperGrid.end_game()
        activated whenever the user press on a bomb'''
        for row in range(self.numrow):
            for column in range(self.numcolumn):
                coord = (row,column)
                #show all bombs
                if self.value.get(coord) == '*':
                    self.cells.get(coord)['text'] = '*'
                    self.cells.get(coord)['bg'] = 'red'
        #show message
        messagebox.showerror('Minesweeper','KABOOM! You lose.',parent=self)

    def auto_expose(self, coord):
        '''MineSweeperGrid.auto_expose()
        auto exposes nearby cells when a blank cell is pressed'''
        row = coord[0]
        column = coord[1]
        while column != self.numcolumn: #if not last column, expose cells to the right
            row = coord[0]
            while row != self.numrow: #if not last row, expose cells under it
                if type(self.value.get((row,column)))==int: #expose cell
                    self.expose_2((row, column))
                elif self.value.get((row,column)) == '':
                    self.expose_2((row, column))
                if column+1 != self.numcolumn:
                    self.expose_2((row, column+1)) #expose nearby cells
                if column-1 != -1:
                    self.expose_2((row, column-1))
                if type(self.value.get((row,column)))==int: #end auto expose in this column
                    row = self.numrow-1
                row += 1
            row = coord[0]
            while row != -1:#if not first row, expose cells above it 
                if type(self.value.get((row,column)))==int: #expose cell
                    self.expose_2((row, column))
                elif self.value.get((row,column)) == '':
                    self.expose_2((row, column))
                if column+1 != self.numcolumn:
                    self.expose_2((row, column+1)) #expose nearby cells
                if column-1 != -1:
                    self.expose_2((row, column-1))
                if type(self.value.get((row,column)))==int: #end auto expose in this row
                    row = 0
                row -= 1
            column += 1
            if type(self.value.get((coord[0],column)))==int:
                column = self.numcolumn
        column = coord[1]      
        while column != -1: #if not first column, expose cells to the left
            row = coord[0]
            while row != self.numrow: #if not last row, expose cells under it
                if type(self.value.get((row,column)))==int: #expose cell
                    self.expose_2((row, column))
                elif self.value.get((row,column)) == '':
                    self.expose_2((row, column))
                if column+1 != self.numcolumn:
                    self.expose_2((row, column+1)) #expose nearby cells
                if column-1 != -1:
                    self.expose_2((row, column-1))
                if type(self.value.get((row,column)))==int: #end in this row
                    row = self.numrow-1
                row += 1
            row = coord[0]
            while row != -1: #if not first row, expose cells above it
                if type(self.value.get((row,column)))==int: #expose cell
                    self.expose_2((row, column))
                elif self.value.get((row,column)) == '':
                    self.expose_2((row, column))
                if column+1 != self.numcolumn:
                    self.expose_2((row, column+1)) #expose nearby cells
                if column-1 != -1:
                    self.expose_2((row, column-1))
                if type(self.value.get((row,column)))==int: #end in this row
                    row = 0
                row -= 1
            column -= 1
            if type(self.value.get((coord[0],column)))==int: #end expose in this column
                column = -1
            
    def expose_2(self, coord):
        '''MineSweeperGrid.show()
        shows what value the cell contains'''
        if self.cells.get(coord).shown == False:
            if self.value.get(coord) != '*':
                colormap = ['','blue','darkgreen','red','purple','maroon','cyan','black','dim gray']
                #show value of cell
                self.cells.get(coord)['text']=self.value.get(coord)
                self.cells.get(coord)['bg'] = 'lightgrey'
                if type(self.value.get(coord))==int:
                    self.cells.get(coord)['fg']=colormap[self.value.get(coord)]
                self.cells.get(coord).shown = True
        self.check_win()
        self.cells.get(coord).canFlag = False

    def change_numbomb(self,number):
        '''MineSweeperGrid.change_numbomb()
        changes the number at the bottom of the frame'''
        if number == '1': #if activated by MineSweeperCell.set_flag()
            self.numbomb -= 1
            self.numBombLabel['text'] = self.numbomb
        elif number == '2': #if activated by MineSweeperCell.unset_flag()
            self.numbomb += 1
            self.numBombLabel['text'] = self.numbomb

    def check_win(self):
        '''MineSweeperGrid.check_win()
        checks if the player wins whenever a cell is pressed'''
        a = 0
        for row in range(self.numrow):
            for column in range(self.numcolumn):
                if self.cells.get((row,column)).shown == True: #if all cells are shown
                    a += 1
        if a == self.numrow*self.numcolumn:
            messagebox.showerror('Congratulations -- You Win!',parent=self) #show msg

def play_mineSweeper():
    '''play_mineSweeoer()
    plays the MineSweeper game'''
    root = Tk()
    root.title('MineSweeper')
    game = MineSweeperGrid(root, 10, 12, 15)
    game.mainloop()

play_mineSweeper()
