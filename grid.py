import game


def create_searchflow(x_fields, y_fields):
    separator = x_fields, 0

    f_hor = []
    for y in range(y_fields):
        for x in range(x_fields):
            f_hor.append((x, y))
        f_hor.append(separator)

    f_vert = []
    for x in range(x_fields):
        for y in range(y_fields):
            f_vert.append((x, y))
        f_vert.append(separator)

    f_slash = []
    for x in range(2, x_fields):
        y = 0
        while x > -1 and y < y_fields:
            f_slash.append((x, y))
            x -= 1
            y += 1
        f_slash.append(separator)
    for y in range(1, y_fields - 2):
        x = x_fields - 1
        while x > -1 and y < y_fields:
            f_slash.append((x, y))
            x -= 1
            y += 1
        f_slash.append(separator)

    f_bslash = []
    for x in range(x_fields - 3, 0, -1):
        y = 0
        while x < x_fields and y < y_fields:
            f_bslash.append((x, y))
            x += 1
            y += 1
        f_bslash.append(separator)
    for y in range(y_fields - 2):
        x = 0
        while x < x_fields and y < y_fields:
            f_bslash.append((x, y))
            x += 1
            y += 1
        f_bslash.append(separator)

    return f_hor, f_vert, f_slash, f_bslash


def translate(pos, borderpos):
    return (pos - borderpos) / game.blocksize

def translate_back(index, borderpos):
    return borderpos + index * game.blocksize


class Grid:
    searchflow = create_searchflow(game.nr_columns, game.nr_rows)

    def __init__(self):
        self.left = game.arena.left
        self.top = game.arena.top
        self.x_fields = game.nr_columns
        self.y_fields = game.nr_rows

        self.tops = {}
        self.grid = self.new_grid()

        self.to_kill = []
        self.to_drop = []

    def new_grid(self):
        grid = []
        for x in range(self.x_fields):
            self.tops[x] = self.y_fields #setting initial columns heights
            grid.append([None for y in range(self.y_fields)])
        grid.append(['b']) #breaking point, self.grid[self.x_fields][0] to access
        return grid

    def take(self, transporter):
        x = translate(transporter.rect.left, self.left)
        for b in transporter.sprites():
            y = translate(b.rect.top, self.top)
            self.grid[x][y] = b.colorkey
        y = translate(transporter.rect.top, self.top)
        if y < 0:
            return False
        self.tops[x] = y
        return True

    def columntop(self, left):
        x = translate(left, self.left)
        return translate_back(self.tops[x], self.top)

    def search(self):
        matches = []
        match = []
        found = []
        temp = []
        for flow in Grid.searchflow:
            prev = None
            nr_blocks = 1
            for x, y in flow:
                xy = x, y
                ckey = self.grid[x][y]
                if ckey:
                    if ckey == prev:
                        nr_blocks += 1
                    else:
                        if nr_blocks > 2:
                            for xy in temp:
                                if xy not in match:
                                    match.append(xy)
                                    if xy not in found:
                                        found.append(xy)
                            if ckey == 'b':
                                del temp[:]
                                nr_blocks = 1
                                prev = None
                                if match:
                                    matches.append(len(match))
                                    match = []
                                continue
                        del temp[:]
                        nr_blocks = 1
                    temp.append(xy)
                if match:
                    matches.append(len(match))
                    match = []
                prev = ckey
        bottoms = {}
        for x, y in found:
            self.grid[x][y] = None
            pos = (translate_back(x, self.left), translate_back(y, self.top))
            if pos not in self.to_kill:
                self.to_kill.append(pos)
            if y == self.tops[x]:
                self.tops[x] += 1
                continue
            if x not in bottoms:
                bottoms[x] = y
                continue
            if y > bottoms[x]:
                bottoms[x] = y
        for x in bottoms:
            y = bottoms[x] - 1
            dist = 1
            left = translate_back(x, self.left)
            while not y < self.tops[x]:
                if self.grid[x][y]:
                    ckey = self.grid[x][y]
                    self.grid[x][y] = None
                    self.to_drop.append(((left, translate_back(y, self.top)), dist * game.blocksize))
                    self.grid[x][y + dist] = ckey
                else:
                    dist += 1
                y -= 1
            self.tops[x] += dist
        return matches

    def __str__(self):
        s = ''
        for y in range(self.y_fields):
            for x in range(self.x_fields):
                if self.grid[x][y]:
                    s = s + ' ' + self.grid[x][y]
                else:
                    s = s + ' .'
            s = s + '\n'
        return s
