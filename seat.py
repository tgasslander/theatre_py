class Seat:
    ''' Theatre seat '''
    free = True
    claimed = False

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def toggle_claim(self):
        un = ''
        if (self.claimed):
            un = 'un'
        print(f'{un}claimed {self.get_label()}')
        self.claimed = not self.claimed

    def reserve(self):
        print(f'reserved {self.get_label()}')
        self.claimed = False
        self.free = False

    def unreserve(self):
        print(f'unreserved {self.get_label()}')
        self.free = True

    def is_claimed(self):
        return self.claimed

    def is_free(self):
        return self.free

    def get_col(self):
        return self.col

    def get_row(self):
        return self.row

    def get_label(self):
        row_label = self.row + 1
        col_label = chr(65 + self.col)
        return f'{row_label}{col_label}'

    def display(self):
        print(f'row: {self.row}, col: {self.col} free:{self.free} claimed:{self.claimed}')
