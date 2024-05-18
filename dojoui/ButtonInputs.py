from inputs import devices
from inputs import get_gamepad
from datetime import datetime, timedelta
import math
import threading
import time
from ComboValidityCheck import ComboValidityChecker

class ButtonInputs:
    def __init__(self, savedCombo):     #the best way to use this would be to call one instance of this class and then call the run function with the selected combo each time a player selects a combo.
        self.event_codes = [
            'ABS_Z',
            'ABS_RZ',
            'BTN_TL',
            'BTN_SOUTH',
            'BTN_WEST',
            'BTN_NORTH',
            'BTN_EAST',
            'BTN_SELECT',
            "ABS_HAT0X",
            "ABS_HAT0Y",
            "BTN_TR",
            "BTN_TL2"
        ]

        self.input_states = {code: 0 for code in self.event_codes}

        self.array = []
        self.events = []
        self.parsedInputArray = []
        self.parsedMoveArray = []
        self.timer = datetime.now()
        self.start_loop_time = datetime.now()
        self.maxTime = 30
        self.threadstop = True
        self.savedCombo = savedCombo

    def get_updates(self, array):
        update = []

        for index, row in enumerate(array):
            if (1 in row) or (-1 in row) or (255 in row):
                temp = self.moveMap(row)
                update.extend(temp)
                index += 2

        if update:
            self.parsedInputArray.append(update)


    def moveMap(self, array):
        moves = []
        frameNumber = self.timer / timedelta(seconds = 1) * 60
        if frameNumber < self.maxTime * 60:
            if array[9] == 1:
                moves.append('2')
            if array[9] == -1:
                moves.append('8')
            if array[8] == -1:
                moves.append('4')
            if array[8] == 1:
                moves.append('6')
            if array[5] == 1:
                moves.append("LP")
            if array[4] == 1:
                moves.append("MP")
            if array[10] == 1:
                moves.append('HP')
            if array[3] == 1:
                moves.append("LK")
            if array[6] == 1:
                moves.append("MK")
            if array[1] == 255:
                moves.append('HK')
            if array[2] == 1:
                moves.append('DI')
            if array[0] == 255:
                moves.append('PARRY')
            if array[7] == 1:
                moves.append("Select")
            moves.append(math.floor(frameNumber))
        return moves

    def moveParser(self):
        i = 0
        temp = 0
        while (i < len(self.parsedInputArray)):
            if (self.parsedInputArray[i] == ["test", "Test"]):
                break
            temp = i
            i += self.SA1(i) + self.SA2(i) + self.SA3(i)
            if i == temp:
                i += self.SM1(i) + self.SM2(i) + self.SM3(i) + self.SM4(i) + self.SM5(i)
                if i == temp:
                    i += self.twoLP(i) + self.twoLK(i) + self.twoMP(i) + self.twoMK(i) + self.twoHP(i) + self.twoHK(i) + self.sixMP(i) + self.sixHP(i) + self.fourHP(i) + self.sixHK(i) + self.fourHK(i) + self.parry(i) + self.DI(i)
                    if i == temp:
                        i += self.fiveLP(i) + self.fiveLK(i) + self.fiveMP(i) + self.fiveMK(i) + self.fiveHP(i) + self.fiveHK(i)
                        if i == temp:
                            i = i+1

    #super arts
    def SA1(self, index):
        moveposs = ["LP", "MP", "HP"]
        #cancelposs = ["LP", "MP", "HP", "LK", "MK", "HK"]

        try:
            if (self.parsedInputArray[index][0] == '2'):    #[2]
                match(len(self.parsedInputArray[index+1])):
                    case 2:
                        if (self.parsedInputArray[index+1][0] == '6' and self.parsedInputArray[index+2][0] == "2" and self.parsedInputArray[index+3][0] == "2" and self.parsedInputArray[index+3][1] == "6"): #[2, 6, 2, 3]
                            match(len(self.parsedInputArray[index+4])):
                                case 2:
                                    if (self.parsedInputArray[index+4][0] == "6"): #[2, 6, 2, 3, 6]
                                        match(len(self.parsedInputArray[index+5])):
                                            case 2:
                                                if (self.parsedInputArray[index + 5][0] in moveposs): #[2, 6, 2, 3, 6, P]
                                                    self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+5][-1]])
                                                    return 6
                                            case 3:
                                                if (self.parsedInputArray[index + 5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 6, 2, 3, 6, 6+P]
                                                    self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+5][-1]])
                                                    if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 6, 2, 3, 6, 6+P, 6/P]
                                                        return 7
                                                    else:
                                                        return 6
                                case 3:
                                    if (self.parsedInputArray[index + 4][0] == "6" and self.parsedInputArray[index+4][1] in moveposs): #[2, 6, 2, 3, 6+P]
                                        self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+4][-1]])
                                        if (self.parsedInputArray[index+5][0] == "6" or self.parsedInputArray[index+5][0] == self.parsedInputArray[index+4][1]): #[2, 6, 2, 3, 6+P, 6/P]
                                            return 6
                                        else:
                                            return 5
                    case 3:
                        if (self.parsedInputArray[index+1][0] == "2" and self.parsedInputArray[index+1][1] == "6"): #[2, 3]
                            match(len(self.parsedInputArray[index+2])):
                                case 2:
                                    if(self.parsedInputArray[index+2][0] == "6"): #[2, 3, 6]
                                        match(len(self.parsedInputArray[index+3])):
                                            case 2:
                                                if (self.parsedInputArray[index+3][0] == "2"): #[2, 3, 6, 2]
                                                    match len(self.parsedInputArray[index+4]):
                                                        case 2:
                                                            if (self.parsedInputArray[index+4][0] == "6"): #[2, 3, 6, 2, 6]
                                                                match len(self.parsedInputArray[index+5]):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+5][0] in moveposs): #[2, 3, 6, 2, 6, P]
                                                                            self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+5][-1]])
                                                                            return 6
                                                                    case 3:
                                                                        if (self.parsedInputArray[index+5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, 2, 6, 6+P]
                                                                            self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+5][-1]])
                                                                            if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #2, 3, 6, 2, 6, 6+P, 6/P]
                                                                                return 7
                                                                            else:
                                                                                return 6
                                                        case 3:
                                                            if (self.parsedInputArray[index+4][0] == "2" and self.parsedInputArray[index+4][1] == "6"): #[2, 3, 6, 2, 3]
                                                                match len(self.parsedInputArray[index+5]):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+5][0] == "6"): #[2, 3, 6, 2, 3, 6]
                                                                            match len(self.parsedInputArray[index+6]):
                                                                                case 2:
                                                                                    if self.parsedInputArray[index+6][0] in moveposs:#[2, 3, 6, 2, 3, 6, P]
                                                                                        self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                                                                        return 7
                                                                                case 3:
                                                                                    if self.parsedInputArray[index+6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs:#[2, 3, 6, 2, 3, 6, 6+P]
                                                                                        self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                                                                        if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, 2, 3, 6, 6+P, 6/P]
                                                                                            return 8
                                                                                        else:
                                                                                            return 7
                                                                    case 3:
                                                                        if (self.parsedInputArray[index+5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, 2, 3, 6+P]
                                                                            self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+5][-1]])
                                                                            if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #2, 3, 6, 2, 3, 6+P, 6/P]
                                                                                return 7
                                                                            else:
                                                                                return 6
                                #                 elif (self.parsedInputArray[index+3][0] in cancelposs and self.parsedInputArray[index+4][0] == "2"): #[2, 3, 6, LK, 2]
                                #                     match(len(self.parsedInputArray[index+5])):
                                #                         case 2:
                                #                             if (self.parsedInputArray[index+5][0] == "6"): #[2, 3, 6, LK, 2, 6]
                                #                                 match(len(self.parsedInputArray[index+6])):
                                #                                     case 2:
                                #                                         if (self.parsedInputArray[index+6][0] in moveposs): #[2, 3, 6, LK, 2, 6, P]
                                #                                             self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                #                                             self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                #                                             return 7
                                #                                     case 3:
                                #                                         if (self.parsedInputArray[index + 6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, LK, 2, 6, 6+P]
                                #                                             self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                #                                             self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                #                                             if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, LK, 2, 6, 6+P, 6/P]
                                #                                                 return 8
                                #                                             else:
                                #                                                 return 7
                                #                         case 3:
                                #                             if (self.parsedInputArray[index+5][0] == "2" and self.parsedInputArray[index+5][1] == "6"): #[2, 3, 6, LK, 2, 3]
                                #                                 match (len(self.parsedInputArray[index+6])):
                                #                                     case 2:
                                #                                         if (self.parsedInputArray[index+6][0] == "6"): #[2, 3, 6, LK, 2, 3, 6]
                                #                                             match (len(self.parsedInputArray[index+7])):
                                #                                                 case 2:
                                #                                                     if (self.parsedInputArray[index + 7][0] in moveposs): #[2, 3, 6, LK, 2, 3, 6, P]
                                #                                                         self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                #                                                         self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+7][-1]])
                                #                                                         return 8
                                #                                                 case 3:
                                #                                                     if (self.parsedInputArray[index+7][0] == "6" and self.parsedInputArray[index + 7][1] in moveposs): #[2, 3, 6, LK, 2, 3, 6, 6+P]
                                #                                                         self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                #                                                         self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+7][-1]])
                                #                                                         if (self.parsedInputArray[index+8][0] == "6" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]):  #[2, 3, 6, LK, 2, 3, 6, 6+P, 6/P]
                                #                                                             return 9
                                #                                                         else:
                                #                                                             return 8
                                #                                     case 3:
                                #                                         if (self.parsedInputArray[index+6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, LK, 2, 3, 6+P]
                                #                                             self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                #                                             self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                #                                             if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, LK, 2, 3, 6+P, 6/P]
                                #                                                 return 8
                                #                                             else:
                                #                                                 return 7
                                #             case 3:
                                #                 if (self.parsedInputArray[index+3][0] == "6" and self.parsedInputArray[index+3][0] in cancelposs): #[2, 3, 6, 6+LK]
                                #                     if (self.parsedInputArray[index+4][0] == "6" or self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][1]): #[2, 3, 6, 6+LK, 6/LK]
                                #                         if (self.parsedInputArray[index+5][0] == "2"): #[2, 3, 6, 6+LK, 6/LK, 2]
                                #                             match(len(self.parsedInputArray[index+6])):
                                #                                 case 2:
                                #                                     if (self.parsedInputArray[index+6][0] == "6"): #[2, 3, 6, 6+LK, 6/LK, 2, 6]
                                #                                         match (len(self.parsedInputArray[index+7])):
                                #                                             case 2:
                                #                                                 if (self.parsedInputArray[index + 7][0] in moveposs): #[2, 3, 6, 6+LK, 6/LK, 2, 6, P]
                                #                                                     self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                #                                                     self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+7][-1]])
                                #                                                     return 8
                                #                                             case 3:
                                #                                                 if (self.parsedInputArray[index+7][0] == "6" and self.parsedInputArray[index + 7][1] in moveposs): #[2, 3, 6, 6+LK, 6/LK, 2, 6, 6+P]
                                #                                                     self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                #                                                     self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+7][-1]])
                                #                                                     if (self.parsedInputArray[index+8][0] == "6" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]): #[2, 3, 6, 6+LK, 6/LK, 2, 6, 6+P, 6/P]
                                #                                                         return 9
                                #                                                     else:
                                #                                                         return 8
                                #                                 case 3:
                                #                                     if (self.parsedInputArray[index+6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, 6+LK, 6/LK, 2, 6+P]
                                #                                         self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                #                                         self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                #                                         if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 6+P, 6/P]
                                #                                             return 8
                                #                                         else:
                                #                                             return 7
                                #                     elif (self.parsedInputArray[index+4][0] == "2"): #[2, 3, 6, 6+LK, 2]
                                #                         match(len(self.parsedInputArray[index+5])):
                                #                             case 2:
                                #                                 if (self.parsedInputArray[index+5][0] == "6"): #[2, 3, 6, 6+LK, 2, 6]
                                #                                     match (len(self.parsedInputArray[index+6])):
                                #                                         case 2:
                                #                                             if (self.parsedInputArray[index + 6][0] in moveposs): #[2, 3, 6, 6+LK, 2, 6, P]
                                #                                                 self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                #                                                 self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                #                                                 return 7
                                #                                         case 3:
                                #                                             if (self.parsedInputArray[index + 6][1] in moveposs): #[2, 3, 6, 6+LK, 2, 6, 6+P]
                                #                                                 self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                #                                                 self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                #                                                 if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, 6+LK, 2, 6, 6+P, 6/P]
                                #                                                     return 8
                                #                                                 else:
                                #                                                     return 7
                                #                             case 3:
                                #                                 if (self.parsedInputArray[index+5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, 6+LK, 2, 6+P]
                                #                                     self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                #                                     self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+5][-1]])
                                #                                     if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6, 6+LK, 2, 6+P, 6/P]
                                #                                         return 7
                                #                                     else:
                                #                                         return 6
                                # case 3:
                                #     if(self.parsedInputArray[index+2][0] == "6" and self.parsedInputArray[index+2][1] in moveposs): #[2, 3, 6+k]
                                #         if (self.parsedInputArray[index+3][0] == "6" or self.parsedInputArray[index+3][0] == self.parsedInputArray[index+2][1]): #[2, 3, 6+K, 6/K]
                                #             if (self.parsedInputArray[index+4][0] == "2"): #[2, 3, 6+K, 6/K, 2]
                                #                 match(len(self.parsedInputArray[index+5])):
                                #                     case 2:
                                #                         if (self.parsedInputArray[index+5][0] == "6"): #[2, 3, 6+K, 6/K, 2, 6]
                                #                             match (len(self.parsedInputArray[index+6])):
                                #                                 case 2:
                                #                                     if (self.parsedInputArray[index + 6][0] in moveposs): #[2, 3, 6+K, 6/K, 2, 6, P]
                                #                                         self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1]], self.parsedInputArray[index+2][-1])
                                #                                         self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                #                                         return 7
                                #                                 case 3:
                                #                                     if (self.parsedInputArray[index+6][0] == "6" and self.parsedInputArray[index + 6][1] in moveposs):  #[2, 3, 6+K, 6/K, 2, 6, 6+P]
                                #                                         self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                #                                         self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                #                                         if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6+K, 6/K, 2, 6, 6+P, 6/P]
                                #                                             return 8
                                #                                         else:
                                #                                             return 7
                                #                     case 3:
                                #                         if (self.parsedInputArray[index+5][0] == "2" and self.parsedInputArray[index+5][1] == "6"): #[2, 3, 6+K, 6/K, 2, 3]
                                #                             match(len(self.parsedInputArray[index+6])):
                                #                                 case 2:
                                #                                     if (self.parsedInputArray[index+6][0] == "6"): #[2, 3, 6+K, 6/K, 2, 3, 6]
                                #                                         match(len(self.parsedInputArray[index+7])):
                                #                                             case 2:
                                #                                                 if (self.parsedInputArray[index + 7][0] in moveposs): #[2, 3, 6+K, 6/K, 2, 3, 6, P]
                                #                                                     self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                #                                                     self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+7][-1]])
                                #                                                     return 8
                                #                                             case 3:
                                #                                                 if (self.parsedInputArray[index + 7][0]== "6" and self.parsedInputArray[index + 7][1] in moveposs): #[2, 3, 6+K, 6/K, 2, 3, 6, 6+P]
                                #                                                     self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                #                                                     self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+7][-1]])
                                #                                                     if (self.parsedInputArray[index+8][0] == "6" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]): #[2, 3, 6+K, 6/K, 2, 3, 6, 6+P, 6/P]
                                #                                                         return 9
                                #                                                     else:
                                #                                                         return 8
                                #                                 case 3:
                                #                                     if (self.parsedInputArray[index + 6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6+K, 6/K, 2, 3, 6+P]
                                #                                         self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                #                                         self.parsedMoveArray.append(["236236P", self.parsedInputArray[index+6][-1]])
                                #                                         if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6+K, 6/K, 2, 3, 6+P, 6/P]
                                #                                             return 8
                                #                                         else:
                                #                                             return 7
        except IndexError:
            return 0

        return 0

    def SA2(self, index):
        moveposs = ["LP", "MP", "HP"]
        cancelposs = ["LP", "MP", "HP", "LK", "MK", "HK"]

        try:
            if (self.parsedInputArray[index][0] == '2'):    #[2]
                match(len(self.parsedInputArray[index+1])):
                    case 2:
                        if (self.parsedInputArray[index+1][0] == '4' and self.parsedInputArray[index+2][0] == "2" and self.parsedInputArray[index+3][0] == "2" and self.parsedInputArray[index+3][1] == "4"): #[2, 1, 4, 2]
                            match(len(self.parsedInputArray[index+4])):
                                case 2:
                                    if (self.parsedInputArray[index+4][0] == "4"): #[2, 4, 2, 1, 4]
                                        match(len(self.parsedInputArray[index+5])):
                                            case 2:
                                                if (self.parsedInputArray[index + 5][0] in moveposs): #[2, 4, 2, 1, 4, P]
                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                    return 6
                                            case 3:
                                                if (self.parsedInputArray[index + 5][0] == "4" and self.parsedInputArray[index+5][1] in moveposs): #[2, 4, 2, 1, 4, 4+P]
                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                    if (self.parsedInputArray[index+6][0] == "4" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 4, 2, 1, 4, 4+P, 4/P]
                                                        return 7
                                                    else:
                                                        return 6
                                case 3:
                                    if (self.parsedInputArray[index + 4][0] == "4" and self.parsedInputArray[index+4][1] in moveposs): #[2, 4, 2, 1, 4+P]
                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+4][-1]])
                                        if (self.parsedInputArray[index+5][0] == "4" or self.parsedInputArray[index+5][0] == self.parsedInputArray[index+4][1]): #[2, 4, 2, 1, 4+P, 4/P]
                                            return 6
                                        else:
                                            return 5
                    case 3:
                        if (self.parsedInputArray[index+1][0] == "2" and self.parsedInputArray[index+1][1] == "4"): #[2, 1]
                            match(len(self.parsedInputArray[index+2])):
                                case 2:
                                    if(self.parsedInputArray[index+2][0] == "4"): #[2, 1, 4]
                                        match(len(self.parsedInputArray[index+3])):
                                            case 2:
                                                if (self.parsedInputArray[index+3][0] == "2"): #[2, 1, 4, 2]
                                                    match len(self.parsedInputArray[index+4]):
                                                        case 2:
                                                            if (self.parsedInputArray[index+4][0] == "4"): #[2, 1, 4, 2, 4]
                                                                match len(self.parsedInputArray[index+5]):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+5][0] in moveposs): #[2, 1, 4, 2, 4, P]
                                                                            self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                                            return 6
                                                                    case 3:
                                                                        if (self.parsedInputArray[index+5][0] == "4" and self.parsedInputArray[index+5][1] in moveposs): #[2, 1, 4, 2, 4, 4+K]
                                                                            self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                                            if (self.parsedInputArray[index+6][0] == "4" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #2, 1, 4, 2, 4, 4+K, 4/K]
                                                                                return 7
                                                                            else:
                                                                                return 6
                                                        case 3:
                                                            if (self.parsedInputArray[index+4][0] == "2" and self.parsedInputArray[index+4][1] == "4"): #[2, 1, 4, 2, 1]
                                                                match len(self.parsedInputArray[index+5]):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+5][0] == "4"): #[2, 1, 6, 2, 3, 6]
                                                                            match len(self.parsedInputArray[index+6]):
                                                                                case 2:
                                                                                    if self.parsedInputArray[index+6][0] in moveposs:#[2, 3, 6, 2, 3, 6, K]
                                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                                        return 7
                                                                                case 3:
                                                                                    if self.parsedInputArray[index+6][0] == "4" and self.parsedInputArray[index+6][1] in moveposs:#[2, 3, 6, 2, 3, 6, 6+K]
                                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                                        if (self.parsedInputArray[index+7][0] == "4" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, 2, 3, 6, 6+K, 6/K]
                                                                                            return 8
                                                                                        else:
                                                                                            return 7
                                                                    case 3:
                                                                        if (self.parsedInputArray[index+5][0] == "4" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, 2, 3, 6+K]
                                                                            self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                                            if (self.parsedInputArray[index+6][0] == "4" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #2, 3, 6, 2, 3, 6+K, 6/K]
                                                                                return 7
                                                                            else:
                                                                                return 6
                                                            elif (self.parsedInputArray[index+4][0] == "4" and self.parsedInputArray[index+4][1] in moveposs): #[2, 3, 6, 2, 6+K]
                                                                self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                if (self.parsedInputArray[index+5][0] == "4" or self.parsedInputArray[index+5][0] == self.parsedInputArray[index+4][1]): #[2, 3, 6, 2, 6+K, 6/K]
                                                                    return 6
                                                                else:
                                                                    return 5
                                                elif (self.parsedInputArray[index+3][0] in cancelposs and self.parsedInputArray[index+4][0] == "2"): #[2, 3, 6, LK, 2]
                                                    match(len(self.parsedInputArray[index+5])):
                                                        case 2:
                                                            if (self.parsedInputArray[index+5][0] == "4"): #[2, 3, 6, LK, 2, 6]
                                                                match(len(self.parsedInputArray[index+6])):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+6][0] in moveposs): #[2, 3, 6, LK, 2, 6, K]
                                                                            self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                            self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                            return 7
                                                                    case 3:
                                                                        if (self.parsedInputArray[index + 6][0] == "4" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, LK, 2, 6, 6+K]
                                                                            self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                            self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                            if (self.parsedInputArray[index+7][0] == "4" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, LK, 2, 6, 6+K, 6/K]
                                                                                return 8
                                                                            else:
                                                                                return 7
                                                        case 3:
                                                            if (self.parsedInputArray[index+5][0] == "2" and self.parsedInputArray[index+5][1] == "4"): #[2, 3, 6, LK, 2, 3]
                                                                match (len(self.parsedInputArray[index+6])):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+6][0] == "4"): #[2, 3, 6, LK, 2, 3, 6]
                                                                            match (len(self.parsedInputArray[index+7])):
                                                                                case 2:
                                                                                    if (self.parsedInputArray[index + 7][0] in moveposs): #[2, 3, 6, LK, 2, 3, 6, K]
                                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                        return 8
                                                                                case 3:
                                                                                    if (self.parsedInputArray[index+7][0] == "4" and self.parsedInputArray[index + 7][1] in moveposs): #[2, 3, 6, LK, 2, 3, 6, 6+K]
                                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                        if (self.parsedInputArray[index+8][0] == "4" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]):  #[2, 3, 6, LK, 2, 3, 6, 6+K, 6/K]
                                                                                            return 9
                                                                                        else:
                                                                                            return 8
                                                                    case 3:
                                                                        if (self.parsedInputArray[index+6][0] == "4" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, LK, 2, 3, 6+K]
                                                                            self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                            self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                            if (self.parsedInputArray[index+7][0] == "4" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, LK, 2, 3, 6+K, 6/K]
                                                                                return 8
                                                                            else:
                                                                                return 7
                                                            elif (self.parsedInputArray[index+5][0] == "4" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, LK, 2, 6+K]
                                                                self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                                if (self.parsedInputArray[index+6][0] == "4" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6, LK, 2, 6+K, 6/K]
                                                                    return 7
                                                                else:
                                                                    return 6
                                            case 3:
                                                if (self.parsedInputArray[index+3][0] == "4" and self.parsedInputArray[index+3][0] in cancelposs): #[2, 3, 6, 6+LK]
                                                    if (self.parsedInputArray[index+4][0] == "4" or self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][1]): #[2, 3, 6, 6+LK, 6/LK]
                                                        if (self.parsedInputArray[index+5][0] == "2"): #[2, 3, 6, 6+LK, 6/LK, 2]
                                                            match(len(self.parsedInputArray[index+6])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index+6][0] == "4"): #[2, 3, 6, 6+LK, 6/LK, 2, 6]
                                                                        match (len(self.parsedInputArray[index+7])):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index + 7][0] in moveposs): #[2, 3, 6, 6+LK, 6/LK, 2, 6, K]
                                                                                    self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                    return 8
                                                                            case 3:
                                                                                if (self.parsedInputArray[index+7][0] == "4" and self.parsedInputArray[index + 7][1] in moveposs): #[2, 3, 6, 6+LK, 6/LK, 2, 6, 6+K]
                                                                                    self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                    if (self.parsedInputArray[index+8][0] == "4" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]): #[2, 3, 6, 6+LK, 6/LK, 2, 6, 6+K, 6/K]
                                                                                        return 9
                                                                                    else:
                                                                                        return 8
                                                                case 3:
                                                                    if (self.parsedInputArray[index+6][0] == "2" and self.parsedInputArray[index+6][1] == "4"): #[2, 3, 6, 6+LK, 6/LK, 2, 3]
                                                                        match len(self.parsedInputArray[index+7]):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index+7][0] == "4"): #[2, 3, 6, 6+K, 6/K, 2, 3, 6]
                                                                                    match len(self.parsedInputArray[index+8]):
                                                                                        case 2:
                                                                                            if (self.parsedInputArray[index+8][0] in moveposs): #[2, 3, 6, 6+K, 6/K, 2, 3, 6, K]
                                                                                                self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                                self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+8][-1]])
                                                                                                return 9
                                                                                        case 3:
                                                                                            if (self.parsedInputArray[index+8][0] == "4" and self.parsedInputArray[index+8][1] in moveposs): #[2, 3, 6, 6+K, 6/K, 2, 3, 6, 6+K]
                                                                                                self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                                self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+8][-1]])
                                                                                                if (self.parsedInputArray[index+9][0] == "4" or self.parsedInputArray[index+9][0] == self.parsedInputArray[index+8][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 3, 6, 6+K, 6/K]
                                                                                                    return 10
                                                                                                else:
                                                                                                    return 9
                                                                            case 3:
                                                                                if (self.parsedInputArray[index+7][0] == "4" and self.parsedInputArray[index+7][1] in moveposs): #[2, 3, 6, 6+K, 6/K, 2, 3, 6+K]
                                                                                    self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                    if (self.parsedInputArray[index+8][0] == "4" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 3, 6+K, 6/K]
                                                                                        return 9
                                                                                    else:
                                                                                        return 8
                                                                    elif (self.parsedInputArray[index+6][0] == "4" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, 6+LK, 6/LK, 2, 6+K]
                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                        if (self.parsedInputArray[index+7][0] == "4" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 6+K, 6/K]
                                                                            return 8
                                                                        else:
                                                                            return 7
                                                    elif (self.parsedInputArray[index+4][0] == "2"): #[2, 3, 6, 6+LK, 2]
                                                        match(len(self.parsedInputArray[index+5])):
                                                            case 2:
                                                                if (self.parsedInputArray[index+5][0] == "4"): #[2, 3, 6, 6+LK, 2, 6]
                                                                    match (len(self.parsedInputArray[index+6])):
                                                                        case 2:
                                                                            if (self.parsedInputArray[index + 6][0] in moveposs): #[2, 3, 6, 6+LK, 2, 6, K]
                                                                                self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                                return 7
                                                                        case 3:
                                                                            if (self.parsedInputArray[index + 6][1] in moveposs): #[2, 3, 6, 6+LK, 2, 6, 6+K]
                                                                                self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                if (self.parsedInputArray[index+7][0] == "4" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, 6+LK, 2, 6, 6+K, 6/K]
                                                                                    return 8
                                                                                else:
                                                                                    return 7
                                                            case 3:
                                                                if (self.parsedInputArray[index+5][0] == "2" and self.parsedInputArray[index+5][1] == "4"): #[2, 3, 6, 6+LK, 2, 3]
                                                                        match len(self.parsedInputArray[index+6]):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index+6][0] == "4"): #[2, 3, 6, 6+K, 2, 3, 6]
                                                                                    match len(self.parsedInputArray[index+7]):
                                                                                        case 2:
                                                                                            if (self.parsedInputArray[index+7][0] in moveposs): #[2, 3, 6, 6+K, 2, 3, 6, K]
                                                                                                self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                                self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                                return 8
                                                                                        case 3:
                                                                                            if (self.parsedInputArray[index+7][0] == "4" and self.parsedInputArray[index+7][1] in moveposs): #[2, 3, 6, 6+K, 2, 3, 6, 6+K]
                                                                                                self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                                self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                                if (self.parsedInputArray[index+8][0] == "4" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 3, 6, 6+K, 6/K]
                                                                                                    return 9
                                                                                                else:
                                                                                                    return 8
                                                                            case 3:
                                                                                if (self.parsedInputArray[index+6][0] == "4" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, 6+K, 2, 3, 6+K]
                                                                                    self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                                    if (self.parsedInputArray[index+7][0] == "4" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 3, 6+K, 6/K]
                                                                                        return 8
                                                                                    else:
                                                                                        return 7
                                                                elif (self.parsedInputArray[index+5][0] == "4" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, 6+LK, 2, 6+K]
                                                                    self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                                    if (self.parsedInputArray[index+6][0] == "4" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6, 6+LK, 2, 6+K, 6/K]
                                                                        return 7
                                                                    else:
                                                                        return 6
                                case 3:
                                    if(self.parsedInputArray[index+2][0] == "4" and self.parsedInputArray[index+2][1] in moveposs): #[2, 3, 6+k]
                                        if (self.parsedInputArray[index+3][0] == "4" or self.parsedInputArray[index+3][0] == self.parsedInputArray[index+2][1]): #[2, 3, 6+K, 6/K]
                                            if (self.parsedInputArray[index+4][0] == "2"): #[2, 3, 6+K, 6/K, 2]
                                                match(len(self.parsedInputArray[index+5])):
                                                    case 2:
                                                        if (self.parsedInputArray[index+5][0] == "4"): #[2, 3, 6+K, 6/K, 2, 6]
                                                            match (len(self.parsedInputArray[index+6])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index + 6][0] in moveposs): #[2, 3, 6+K, 6/K, 2, 6, K]
                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                        return 7
                                                                case 3:
                                                                    if (self.parsedInputArray[index+6][0] == "4" and self.parsedInputArray[index + 6][1] in moveposs):  #[2, 3, 6+K, 6/K, 2, 6, 6+K]
                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                        if (self.parsedInputArray[index+7][0] == "4" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6+K, 6/K, 2, 6, 6+P, 6/K]
                                                                            return 8
                                                                        else:
                                                                            return 7
                                                    case 3:
                                                        if (self.parsedInputArray[index+5][0] == "2" and self.parsedInputArray[index+5][1] == "4"): #[2, 3, 6+K, 6/K, 2, 3]
                                                            match(len(self.parsedInputArray[index+6])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index+6][0] == "4"): #[2, 3, 6+K, 6/K, 2, 3, 6]
                                                                        match(len(self.parsedInputArray[index+7])):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index + 7][0] in moveposs): #[2, 3, 6+K, 6/K, 2, 3, 6, K]
                                                                                    self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                    return 8
                                                                            case 3:
                                                                                if (self.parsedInputArray[index + 7][0]== "4" and self.parsedInputArray[index + 7][1] in moveposs): #[2, 3, 6+K, 6/K, 2, 3, 6, 6+K]
                                                                                    self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+7][-1]])
                                                                                    if (self.parsedInputArray[index+8][0] == "4" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]): #[2, 3, 6+K, 6/K, 2, 3, 6, 6+K, 6/K]
                                                                                        return 9
                                                                                    else:
                                                                                        return 8
                                                                case 3:
                                                                    if (self.parsedInputArray[index + 6][0] == "4" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6+K, 6/K, 2, 3, 6+K]
                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                        if (self.parsedInputArray[index+7][0] == "4" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6+K, 6/K, 2, 3, 6+K, 6/K]
                                                                            return 8
                                                                        else:
                                                                            return 7
                                                        elif (self.parsedInputArray[index+5][0] == "4" and self.parsedInputArray[index + 5][1] in moveposs):  #[2, 3, 6+K, 6/K, 2, 6+K]
                                                            self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                            self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                            if (self.parsedInputArray[index+6][0] == "4" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6+K, 6/K, 2, 6+k, 6/K]
                                                                return 7
                                                            else:
                                                                return 6
                                        elif (self.parsedInputArray[index+3][0] == "2"): #[2, 3, 6+K, 2]
                                                match(len(self.parsedInputArray[index+4])):
                                                    case 2:
                                                        if (self.parsedInputArray[index+4][0] == "4"): #[2, 3, 6+K, 2, 6]
                                                            match (len(self.parsedInputArray[index+5])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index + 5][0] in moveposs): #[2, 3, 6+K, 2, 6, K]
                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                                        return 6
                                                                case 3:
                                                                    if (self.parsedInputArray[index+5][0] == "4" and self.parsedInputArray[index + 5][1] in moveposs):  #[2, 3, 6+K, 2, 6, 6+K]
                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                                        if (self.parsedInputArray[index+6][0] == "4" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6+K, 6/K, 2, 6, 6+P, 6/K]
                                                                            return 7
                                                                        else:
                                                                            return 6
                                                    case 3:
                                                        if (self.parsedInputArray[index+4][0] == "2" and self.parsedInputArray[index+4][1] == "4"): #[2, 3, 6+K, 2, 3]
                                                            match(len(self.parsedInputArray[index+5])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index+5][0] == "4"): #[2, 3, 6+K, 2, 3, 6]
                                                                        match(len(self.parsedInputArray[index+6])):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index + 6][0] in moveposs): #[2, 3, 6+K, 2, 3, 6, K]
                                                                                    self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                                    return 7
                                                                            case 3:
                                                                                if (self.parsedInputArray[index + 6][0]== "4" and self.parsedInputArray[index + 6][1] in moveposs): #[2, 3, 6+K, 2, 3, 6, 6+K]
                                                                                    self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                                    self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+6][-1]])
                                                                                    if (self.parsedInputArray[index+7][0] == "4" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6+K, 2, 3, 6, 6+K, 6/K]
                                                                                        return 8
                                                                                    else:
                                                                                        return 7
                                                                case 3:
                                                                    if (self.parsedInputArray[index + 5][0] == "4" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6+K, 2, 3, 6+K]
                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+5][-1]])
                                                                        if (self.parsedInputArray[index+6][0] == "4" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6+K, 2, 3, 6+K, 6/K]
                                                                            return 7
                                                                        else:
                                                                            return 6
                                                        elif (self.parsedInputArray[index+4][0] == "4" and self.parsedInputArray[index + 4][1] in moveposs):  #[2, 3, 6+K, 2, 6+K]
                                                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["214214P", self.parsedInputArray[index+4][-1]])
                                                                        if (self.parsedInputArray[index+5][0] == "4" or self.parsedInputArray[index+5][0] == self.parsedInputArray[index+4][1]): #[2, 3, 6+K, 2, 6+k, 6/K]
                                                                            return 6
                                                                        else:
                                                                            return 5

        except IndexError:
            return 0

        return 0

    def SA3(self, index):
        moveposs = ["LK", "MK", "HK"]
        cancelposs = ["LP", "MP", "HP", "LK", "MK", "HK"]

        try:
            if (self.parsedInputArray[index][0] == '2'):    #[2]
                match(len(self.parsedInputArray[index+1])):
                    case 2:
                        if (self.parsedInputArray[index+1][0] == '6' and self.parsedInputArray[index+2][0] == "2" and self.parsedInputArray[index+3][0] == "2" and self.parsedInputArray[index+3][1] == "6"): #[2, 6, 2, 3]
                            match(len(self.parsedInputArray[index+4])):
                                case 2:
                                    if (self.parsedInputArray[index+4][0] == "6"): #[2, 6, 2, 3, 6]
                                        match(len(self.parsedInputArray[index+5])):
                                            case 2:
                                                if (self.parsedInputArray[index + 5][0] in moveposs): #[2, 6, 2, 3, 6, K]
                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                    return 6
                                            case 3:
                                                if (self.parsedInputArray[index + 5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 6, 2, 3, 6, 6+K]
                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                    if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 6, 2, 3, 6, 6+K, 6/K]
                                                        return 7
                                                    else:
                                                        return 6
                                case 3:
                                    if (self.parsedInputArray[index + 4][0] == "6" and self.parsedInputArray[index+4][1] in moveposs): #[2, 6, 2, 3, 6+K]
                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+4][-1]])
                                        if (self.parsedInputArray[index+5][0] == "6" or self.parsedInputArray[index+5][0] == self.parsedInputArray[index+4][1]): #[2, 6, 2, 3, 6+K, 6/K]
                                            return 6
                                        else:
                                            return 5
                    case 3:
                        if (self.parsedInputArray[index+1][0] == "2" and self.parsedInputArray[index+1][1] == "6"): #[2, 3]
                            match(len(self.parsedInputArray[index+2])):
                                case 2:
                                    if(self.parsedInputArray[index+2][0] == "6"): #[2, 3, 6]
                                        match(len(self.parsedInputArray[index+3])):
                                            case 2:
                                                if (self.parsedInputArray[index+3][0] == "2"): #[2, 3, 6, 2]
                                                    match len(self.parsedInputArray[index+4]):
                                                        case 2:
                                                            if (self.parsedInputArray[index+4][0] == "6"): #[2, 3, 6, 2, 6]
                                                                match len(self.parsedInputArray[index+5]):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+5][0] in moveposs): #[2, 3, 6, 2, 6, K]
                                                                            self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                                            return 6
                                                                    case 3:
                                                                        if (self.parsedInputArray[index+5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, 2, 6, 6+K]
                                                                            self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                                            if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #2, 3, 6, 2, 6, 6+K, 6/K]
                                                                                return 7
                                                                            else:
                                                                                return 6
                                                        case 3:
                                                            if (self.parsedInputArray[index+4][0] == "2" and self.parsedInputArray[index+4][1] == "6"): #[2, 3, 6, 2, 3]
                                                                match len(self.parsedInputArray[index+5]):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+5][0] == "6"): #[2, 3, 6, 2, 3, 6]
                                                                            match len(self.parsedInputArray[index+6]):
                                                                                case 2:
                                                                                    if self.parsedInputArray[index+6][0] in moveposs:#[2, 3, 6, 2, 3, 6, K]
                                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                                        return 7
                                                                                case 3:
                                                                                    if self.parsedInputArray[index+6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs:#[2, 3, 6, 2, 3, 6, 6+K]
                                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                                        if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, 2, 3, 6, 6+K, 6/K]
                                                                                            return 8
                                                                                        else:
                                                                                            return 7
                                                                    case 3:
                                                                        if (self.parsedInputArray[index+5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, 2, 3, 6+K]
                                                                            self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                                            if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #2, 3, 6, 2, 3, 6+K, 6/K]
                                                                                return 7
                                                                            else:
                                                                                return 6
                                                            elif (self.parsedInputArray[index+4][0] == "6" and self.parsedInputArray[index+4][1] in moveposs): #[2, 3, 6, 2, 6+K]
                                                                self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                if (self.parsedInputArray[index+5][0] == "6" or self.parsedInputArray[index+5][0] == self.parsedInputArray[index+4][1]): #[2, 3, 6, 2, 6+K, 6/K]
                                                                    return 6
                                                                else:
                                                                    return 5
                                                elif (self.parsedInputArray[index+3][0] in cancelposs and self.parsedInputArray[index+4][0] == "2"): #[2, 3, 6, LK, 2]
                                                    match(len(self.parsedInputArray[index+5])):
                                                        case 2:
                                                            if (self.parsedInputArray[index+5][0] == "6"): #[2, 3, 6, LK, 2, 6]
                                                                match(len(self.parsedInputArray[index+6])):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+6][0] in moveposs): #[2, 3, 6, LK, 2, 6, K]
                                                                            self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                            self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                            return 7
                                                                    case 3:
                                                                        if (self.parsedInputArray[index + 6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, LK, 2, 6, 6+K]
                                                                            self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                            self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                            if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, LK, 2, 6, 6+K, 6/K]
                                                                                return 8
                                                                            else:
                                                                                return 7
                                                        case 3:
                                                            if (self.parsedInputArray[index+5][0] == "2" and self.parsedInputArray[index+5][1] == "6"): #[2, 3, 6, LK, 2, 3]
                                                                match (len(self.parsedInputArray[index+6])):
                                                                    case 2:
                                                                        if (self.parsedInputArray[index+6][0] == "6"): #[2, 3, 6, LK, 2, 3, 6]
                                                                            match (len(self.parsedInputArray[index+7])):
                                                                                case 2:
                                                                                    if (self.parsedInputArray[index + 7][0] in moveposs): #[2, 3, 6, LK, 2, 3, 6, K]
                                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                        return 8
                                                                                case 3:
                                                                                    if (self.parsedInputArray[index+7][0] == "6" and self.parsedInputArray[index + 7][1] in moveposs): #[2, 3, 6, LK, 2, 3, 6, 6+K]
                                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                        if (self.parsedInputArray[index+8][0] == "6" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]):  #[2, 3, 6, LK, 2, 3, 6, 6+K, 6/K]
                                                                                            return 9
                                                                                        else:
                                                                                            return 8
                                                                    case 3:
                                                                        if (self.parsedInputArray[index+6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, LK, 2, 3, 6+K]
                                                                            self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                            self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                            if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, LK, 2, 3, 6+K, 6/K]
                                                                                return 8
                                                                            else:
                                                                                return 7
                                                            elif (self.parsedInputArray[index+5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, LK, 2, 6+K]
                                                                self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                                self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                                if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6, LK, 2, 6+K, 6/K]
                                                                    return 7
                                                                else:
                                                                    return 6
                                            case 3:
                                                if (self.parsedInputArray[index+3][0] == "6" and self.parsedInputArray[index+3][0] in cancelposs): #[2, 3, 6, 6+LK]
                                                    if (self.parsedInputArray[index+4][0] == "6" or self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][1]): #[2, 3, 6, 6+LK, 6/LK]
                                                        if (self.parsedInputArray[index+5][0] == "2"): #[2, 3, 6, 6+LK, 6/LK, 2]
                                                            match(len(self.parsedInputArray[index+6])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index+6][0] == "6"): #[2, 3, 6, 6+LK, 6/LK, 2, 6]
                                                                        match (len(self.parsedInputArray[index+7])):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index + 7][0] in moveposs): #[2, 3, 6, 6+LK, 6/LK, 2, 6, K]
                                                                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                    return 8
                                                                            case 3:
                                                                                if (self.parsedInputArray[index+7][0] == "6" and self.parsedInputArray[index + 7][1] in moveposs): #[2, 3, 6, 6+LK, 6/LK, 2, 6, 6+K]
                                                                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                    if (self.parsedInputArray[index+8][0] == "6" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]): #[2, 3, 6, 6+LK, 6/LK, 2, 6, 6+K, 6/K]
                                                                                        return 9
                                                                                    else:
                                                                                        return 8
                                                                case 3:
                                                                    if (self.parsedInputArray[index+6][0] == "2" and self.parsedInputArray[index+6][1] == "6"): #[2, 3, 6, 6+LK, 6/LK, 2, 3]
                                                                        match len(self.parsedInputArray[index+7]):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index+7][0] == "6"): #[2, 3, 6, 6+K, 6/K, 2, 3, 6]
                                                                                    match len(self.parsedInputArray[index+8]):
                                                                                        case 2:
                                                                                            if (self.parsedInputArray[index+8][0] in moveposs): #[2, 3, 6, 6+K, 6/K, 2, 3, 6, K]
                                                                                                self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                                self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+8][-1]])
                                                                                                return 9
                                                                                        case 3:
                                                                                            if (self.parsedInputArray[index+8][0] == "6" and self.parsedInputArray[index+8][1] in moveposs): #[2, 3, 6, 6+K, 6/K, 2, 3, 6, 6+K]
                                                                                                self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                                self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+8][-1]])
                                                                                                if (self.parsedInputArray[index+9][0] == "6" or self.parsedInputArray[index+9][0] == self.parsedInputArray[index+8][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 3, 6, 6+K, 6/K]
                                                                                                    return 10
                                                                                                else:
                                                                                                    return 9
                                                                            case 3:
                                                                                if (self.parsedInputArray[index+7][0] == "6" and self.parsedInputArray[index+7][1] in moveposs): #[2, 3, 6, 6+K, 6/K, 2, 3, 6+K]
                                                                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                    if (self.parsedInputArray[index+8][0] == "6" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 3, 6+K, 6/K]
                                                                                        return 9
                                                                                    else:
                                                                                        return 8
                                                                    elif (self.parsedInputArray[index+6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, 6+LK, 6/LK, 2, 6+K]
                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                        if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 6+K, 6/K]
                                                                            return 8
                                                                        else:
                                                                            return 7
                                                    elif (self.parsedInputArray[index+4][0] == "2"): #[2, 3, 6, 6+LK, 2]
                                                        match(len(self.parsedInputArray[index+5])):
                                                            case 2:
                                                                if (self.parsedInputArray[index+5][0] == "6"): #[2, 3, 6, 6+LK, 2, 6]
                                                                    match (len(self.parsedInputArray[index+6])):
                                                                        case 2:
                                                                            if (self.parsedInputArray[index + 6][0] in moveposs): #[2, 3, 6, 6+LK, 2, 6, K]
                                                                                self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                                return 7
                                                                        case 3:
                                                                            if (self.parsedInputArray[index + 6][1] in moveposs): #[2, 3, 6, 6+LK, 2, 6, 6+K]
                                                                                self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6, 6+LK, 2, 6, 6+K, 6/K]
                                                                                    return 8
                                                                                else:
                                                                                    return 7
                                                            case 3:
                                                                if (self.parsedInputArray[index+5][0] == "2" and self.parsedInputArray[index+5][1] == "6"): #[2, 3, 6, 6+LK, 2, 3]
                                                                        match len(self.parsedInputArray[index+6]):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index+6][0] == "6"): #[2, 3, 6, 6+K, 2, 3, 6]
                                                                                    match len(self.parsedInputArray[index+7]):
                                                                                        case 2:
                                                                                            if (self.parsedInputArray[index+7][0] in moveposs): #[2, 3, 6, 6+K, 2, 3, 6, K]
                                                                                                self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                                self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                                return 8
                                                                                        case 3:
                                                                                            if (self.parsedInputArray[index+7][0] == "6" and self.parsedInputArray[index+7][1] in moveposs): #[2, 3, 6, 6+K, 2, 3, 6, 6+K]
                                                                                                self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                                self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                                if (self.parsedInputArray[index+8][0] == "6" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 3, 6, 6+K, 6/K]
                                                                                                    return 9
                                                                                                else:
                                                                                                    return 8
                                                                            case 3:
                                                                                if (self.parsedInputArray[index+6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6, 6+K, 2, 3, 6+K]
                                                                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                                    if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]):  #[2, 3, 6, 6+LK, 6/LK, 2, 3, 6+K, 6/K]
                                                                                        return 8
                                                                                    else:
                                                                                        return 7
                                                                elif (self.parsedInputArray[index+5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6, 6+LK, 2, 6+K]
                                                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                                    if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6, 6+LK, 2, 6+K, 6/K]
                                                                        return 7
                                                                    else:
                                                                        return 6
                                case 3:
                                    if(self.parsedInputArray[index+2][0] == "6" and self.parsedInputArray[index+2][1] in moveposs): #[2, 3, 6+k]
                                        if (self.parsedInputArray[index+3][0] == "6" or self.parsedInputArray[index+3][0] == self.parsedInputArray[index+2][1]): #[2, 3, 6+K, 6/K]
                                            if (self.parsedInputArray[index+4][0] == "2"): #[2, 3, 6+K, 6/K, 2]
                                                match(len(self.parsedInputArray[index+5])):
                                                    case 2:
                                                        if (self.parsedInputArray[index+5][0] == "6"): #[2, 3, 6+K, 6/K, 2, 6]
                                                            match (len(self.parsedInputArray[index+6])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index + 6][0] in moveposs): #[2, 3, 6+K, 6/K, 2, 6, K]
                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                        return 7
                                                                case 3:
                                                                    if (self.parsedInputArray[index+6][0] == "6" and self.parsedInputArray[index + 6][1] in moveposs):  #[2, 3, 6+K, 6/K, 2, 6, 6+K]
                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                        if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6+K, 6/K, 2, 6, 6+P, 6/K]
                                                                            return 8
                                                                        else:
                                                                            return 7
                                                    case 3:
                                                        if (self.parsedInputArray[index+5][0] == "2" and self.parsedInputArray[index+5][1] == "6"): #[2, 3, 6+K, 6/K, 2, 3]
                                                            match(len(self.parsedInputArray[index+6])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index+6][0] == "6"): #[2, 3, 6+K, 6/K, 2, 3, 6]
                                                                        match(len(self.parsedInputArray[index+7])):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index + 7][0] in moveposs): #[2, 3, 6+K, 6/K, 2, 3, 6, K]
                                                                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                    return 8
                                                                            case 3:
                                                                                if (self.parsedInputArray[index + 7][0]== "6" and self.parsedInputArray[index + 7][1] in moveposs): #[2, 3, 6+K, 6/K, 2, 3, 6, 6+K]
                                                                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+7][-1]])
                                                                                    if (self.parsedInputArray[index+8][0] == "6" or self.parsedInputArray[index+8][0] == self.parsedInputArray[index+7][1]): #[2, 3, 6+K, 6/K, 2, 3, 6, 6+K, 6/K]
                                                                                        return 9
                                                                                    else:
                                                                                        return 8
                                                                case 3:
                                                                    if (self.parsedInputArray[index + 6][0] == "6" and self.parsedInputArray[index+6][1] in moveposs): #[2, 3, 6+K, 6/K, 2, 3, 6+K]
                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                        if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6+K, 6/K, 2, 3, 6+K, 6/K]
                                                                            return 8
                                                                        else:
                                                                            return 7
                                                        elif (self.parsedInputArray[index+5][0] == "6" and self.parsedInputArray[index + 5][1] in moveposs):  #[2, 3, 6+K, 6/K, 2, 6+K]
                                                            self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                            self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                            if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6+K, 6/K, 2, 6+k, 6/K]
                                                                return 7
                                                            else:
                                                                return 6
                                        elif (self.parsedInputArray[index+3][0] == "2"): #[2, 3, 6+K, 2]
                                                match(len(self.parsedInputArray[index+4])):
                                                    case 2:
                                                        if (self.parsedInputArray[index+4][0] == "6"): #[2, 3, 6+K, 2, 6]
                                                            match (len(self.parsedInputArray[index+5])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index + 5][0] in moveposs): #[2, 3, 6+K, 2, 6, K]
                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                                        return 6
                                                                case 3:
                                                                    if (self.parsedInputArray[index+5][0] == "6" and self.parsedInputArray[index + 5][1] in moveposs):  #[2, 3, 6+K, 2, 6, 6+K]
                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                                        if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6+K, 6/K, 2, 6, 6+P, 6/K]
                                                                            return 7
                                                                        else:
                                                                            return 6
                                                    case 3:
                                                        if (self.parsedInputArray[index+4][0] == "2" and self.parsedInputArray[index+4][1] == "6"): #[2, 3, 6+K, 2, 3]
                                                            match(len(self.parsedInputArray[index+5])):
                                                                case 2:
                                                                    if (self.parsedInputArray[index+5][0] == "6"): #[2, 3, 6+K, 2, 3, 6]
                                                                        match(len(self.parsedInputArray[index+6])):
                                                                            case 2:
                                                                                if (self.parsedInputArray[index + 6][0] in moveposs): #[2, 3, 6+K, 2, 3, 6, K]
                                                                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                                    return 7
                                                                            case 3:
                                                                                if (self.parsedInputArray[index + 6][0]== "6" and self.parsedInputArray[index + 6][1] in moveposs): #[2, 3, 6+K, 2, 3, 6, 6+K]
                                                                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                                    self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+6][-1]])
                                                                                    if (self.parsedInputArray[index+7][0] == "6" or self.parsedInputArray[index+7][0] == self.parsedInputArray[index+6][1]): #[2, 3, 6+K, 2, 3, 6, 6+K, 6/K]
                                                                                        return 8
                                                                                    else:
                                                                                        return 7
                                                                case 3:
                                                                    if (self.parsedInputArray[index + 5][0] == "6" and self.parsedInputArray[index+5][1] in moveposs): #[2, 3, 6+K, 2, 3, 6+K]
                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+5][-1]])
                                                                        if (self.parsedInputArray[index+6][0] == "6" or self.parsedInputArray[index+6][0] == self.parsedInputArray[index+5][1]): #[2, 3, 6+K, 2, 3, 6+K, 6/K]
                                                                            return 7
                                                                        else:
                                                                            return 6
                                                        elif (self.parsedInputArray[index+4][0] == "6" and self.parsedInputArray[index + 4][1] in moveposs):  #[2, 3, 6+K, 2, 6+K]
                                                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                                                        self.parsedMoveArray.append(["236236K", self.parsedInputArray[index+4][-1]])
                                                                        if (self.parsedInputArray[index+5][0] == "6" or self.parsedInputArray[index+5][0] == self.parsedInputArray[index+4][1]): #[2, 3, 6+K, 2, 6+k, 6/K]
                                                                            return 6
                                                                        else:
                                                                            return 5

        except IndexError:
            return 0

        return 0

    #special moves
    def SM1(self, index):
        moveposs = ["LP", "MP", "HP"]

        try:
            if (self.parsedInputArray[index][0] == '2'):
                if len(self.parsedInputArray[index+1]) == 3:
                    if (self.parsedInputArray[index+1][0] == "2" and self.parsedInputArray[index+1][1] == "6"): # [2, 3]
                        match len(self.parsedInputArray[index+2]):
                            case 2:
                                if (self.parsedInputArray[index+2][0] == "6"): #[2, 3, 6]
                                    match(len(self.parsedInputArray[index+3])):
                                        case 2:
                                            if (self.parsedInputArray[index+3][0] in moveposs): #[2, 3, 6, P]
                                                self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                                return 4
                                        case 3:
                                            if (self.parsedInputArray[index + 3][0] == "6" and self.parsedInputArray[index+3][1] in moveposs): #[2, 3, 6, 6+P]
                                                self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                                if (self.parsedInputArray[index+4][0] == "6" or self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][1]): #[2, 3, 6, 6+P, 6/P]
                                                    return 5
                                                else:
                                                    return 4
                            case 3:
                                if (self.parsedInputArray[index+2][0] == "6" and self.parsedInputArray[index+2][1] in moveposs): #[2, 3, 6+P]
                                    self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                                    if (self.parsedInputArray[index+3][0] == "6" or self.parsedInputArray[index+3][0] == self.parsedInputArray[index+2][1]): #[2, 3, 6+P, 6/P]
                                        return 4
                                    else:
                                        return 3
        except IndexError:
            return 0

        return 0

    def SM2(self, index):
        moveposs = ["LP", "MP", "HP"]
        try:
            if (self.parsedInputArray[index][0] == '6' and self.parsedInputArray[index+1][0] == "2"): # [6, 2]
                match len(self.parsedInputArray[index+2]):
                    case 3:
                        if (self.parsedInputArray[index+2][0] == "2" and self.parsedInputArray[index+2][1] == "6"): #[6, 2, 3]
                            match(len(self.parsedInputArray[index+3])):
                                case 2:
                                    if (self.parsedInputArray[index+3][0] in moveposs): #[6, 2, 3, P]
                                        self.parsedMoveArray.append(["623"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                        return 4
                                case 3:
                                    if (self.parsedInputArray[index + 3][0] == "2" and self.parsedInputArray[index+3][1] in moveposs) or (self.parsedInputArray[index + 3][0] == "6" and self.parsedInputArray[index+3][1] in moveposs): #[6, 2, 3, 2/6+P]
                                        self.parsedMoveArray.append(["623"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                        if (self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][0] or self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][1]): #[6, 2, 3, 2/6+P, 2/6/P]
                                            return 5
                                        else:
                                            return 4
                                case 4:
                                    if (self.parsedInputArray[index + 3][0] == "2" and self.parsedInputArray[index+3][1] == "6" and self.parsedInputArray[index+3][2] in moveposs): #[6, 2, 3, 3+P]
                                        self.parsedMoveArray.append(["623"+self.parsedInputArray[index+3][2], self.parsedInputArray[index+3][-1]])
                                        if (len(self.parsedInputArray[index+4]) == 2):
                                            if (self.parsedInputArray[index+4][0] == "2" or self.parsedInputArray[index+4][0] == "6" or self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][2]):
                                                return 5
                                            else:
                                                return 4
                                        else:
                                            return 5
                    case 4:
                        if (self.parsedInputArray[index+2][0] == "2" and self.parsedInputArray[index+2][1] == "6" and self.parsedInputArray[index+2][2] in moveposs): #[6, 2, 3+P]
                            if (len(self.parsedInputArray[index+3]) == 2):
                                if (self.parsedInputArray[index+3][0] == "2" or self.parsedInputArray[index+3][0] == "6" or self.parsedInputArray[index+3][0] in moveposs):
                                    return 4
                                else:
                                    return 3
                            else:
                                return 4
        except IndexError:
            return 0
        return 0

    def SM3(self, index):
        moveposs = ["LK", "MK", "HK"]

        try:
            if (self.parsedInputArray[index][0] == '2' and self.parsedInputArray[index+1][0] == "2" and self.parsedInputArray[index+1][1] == "4"): # [2, 1]
                match len(self.parsedInputArray[index+2]):
                    case 2:
                        if (self.parsedInputArray[index+2][0] == "4"): #[2, 1, 4]
                            match(len(self.parsedInputArray[index+3])):
                                case 2:
                                    if (self.parsedInputArray[index+3][0] in moveposs): #[2, 1, 4, K]
                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                        return 4
                                case 3:
                                    if (self.parsedInputArray[index + 3][0] == "4" and self.parsedInputArray[index+3][1] in moveposs): #[2, 1, 4, 4+K]
                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                        if (self.parsedInputArray[index+4][0] == "4" or self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][1]): #[2, 1, 4, 4+K, 4/K]
                                            return 5
                                        else:
                                            return 4
                    case 3:
                        if (self.parsedInputArray[index+2][0] == "4" and self.parsedInputArray[index+2][1] in moveposs): #[2, 1, 4+K]
                            self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                            if (self.parsedInputArray[index+3][0] == "4" or self.parsedInputArray[index+3][0] == self.parsedInputArray[index+2][1]): #[2, 1, 4+K, 4/K]
                                return 4
                            else:
                                return 3
        except IndexError:
            return 0
        return 0

    def SM4(self, index):
        moveposs = ["LK", "MK", "HK"]
        try:
            if (self.parsedInputArray[index][0] == '2' and self.parsedInputArray[index+1][0] == "2" and self.parsedInputArray[index+1][1] == "6"): # [2, 3]
                match len(self.parsedInputArray[index+2]):
                    case 2:
                        if (self.parsedInputArray[index+2][0] == "6"): #[2, 3, 6]
                            match(len(self.parsedInputArray[index+3])):
                                case 2:
                                    if (self.parsedInputArray[index+3][0] in moveposs): #[2, 3, 6, K]
                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                        return 4
                                case 3:
                                    if (self.parsedInputArray[index + 3][0] == "6" and self.parsedInputArray[index+3][1] in moveposs): #[2, 3, 6, 6+K]
                                        self.parsedMoveArray.append(["236"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                        if (self.parsedInputArray[index+4][0] == "6" or self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][1]): #[2, 3, 6, 6+K, 6/K]
                                            return 5
                                        else:
                                            return 4
                    case 3:
                        if (self.parsedInputArray[index+2][0] == "6" and self.parsedInputArray[index+2][1] in moveposs): #[2, 3, 6+K]
                            self.parsedMoveArray.append(["236"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                            if (self.parsedInputArray[index+3][0] == "6" or self.parsedInputArray[index+3][0] == self.parsedInputArray[index+2][1]): #[2, 3, 6+K, 6/K]
                                return 4
                            else:
                                return 3
        except IndexError:
            return 0
        return 0

    def SM5(self, index):
        moveposs = ["LP", "MP", "HP"]

        try:
            if (self.parsedInputArray[index][0] == '2' and self.parsedInputArray[index+1][0] == "2" and self.parsedInputArray[index+1][1] == "4"): # [2, 1]
                match len(self.parsedInputArray[index+2]):
                    case 2:
                        if (self.parsedInputArray[index+2][0] == "4"): #[2, 1, 4]
                            match(len(self.parsedInputArray[index+3])):
                                case 2:
                                    if (self.parsedInputArray[index+3][0] in moveposs): #[2, 1, 4, P]
                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][0], self.parsedInputArray[index+3][-1]])
                                        return 4
                                case 3:
                                    if (self.parsedInputArray[index + 3][0] == "4" and self.parsedInputArray[index+3][1] in moveposs): #[2, 1, 4, 4+P]
                                        self.parsedMoveArray.append(["214"+self.parsedInputArray[index+3][1], self.parsedInputArray[index+3][-1]])
                                        if (self.parsedInputArray[index+4][0] == "4" or self.parsedInputArray[index+4][0] == self.parsedInputArray[index+3][1]): #[2, 1, 4, 4+P, 4/P]
                                            return 5
                                        else:
                                            return 4
                    case 3:
                        if (self.parsedInputArray[index+2][0] == "4" and self.parsedInputArray[index+2][1] in moveposs): #[2, 1, 4+P]
                            self.parsedMoveArray.append(["214"+self.parsedInputArray[index+2][1], self.parsedInputArray[index+2][-1]])
                            if (self.parsedInputArray[index+3][0] == "4" or self.parsedInputArray[index+3][0] == self.parsedInputArray[index+2][1]): #[2, 1, 4+P, 4/P]
                                return 4
                            else:
                                return 3
        except IndexError:
            return 0

        return 0

    #crouching normals
    def twoLP(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "2" and self.parsedInputArray[index][1] == "LP"): #[2+LP]
            self.parsedMoveArray.append(["2LP", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "2" or self.parsedInputArray[index+1][0] == "LP"): #[2+LP, 2/LP]
                return 2
            else:
                return 1
        return 0

    def twoLK(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "2" and self.parsedInputArray[index][1] == "LK"): #[2+LK]
            self.parsedMoveArray.append(["2LK", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "2" or self.parsedInputArray[index+1][0] == "LK"): #[2+LK, 2/LK]
                return 2
            else:
                return 1
        return 0

    def twoMP(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "2" and self.parsedInputArray[index][1] == "MP"): #[2+MP]
            self.parsedMoveArray.append(["2MP", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "2" or self.parsedInputArray[index+1][0] == "MP"): #[2+MP, 2/MK]
                return 2
            else:
                return 1
        return 0

    def twoMK(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "2" and self.parsedInputArray[index][1] == "MK"): #[2, 2+MK]
            self.parsedMoveArray.append(["2MK", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "2" or self.parsedInputArray[index+1][0] == "MK"): #[2+MK, 2/MK]
                return 2
            else:
                return 1
        return 0

    def twoHP(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "2" and self.parsedInputArray[index][1] == "HP"): #[2+HP]
            self.parsedMoveArray.append(["2HP", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "2" or self.parsedInputArray[index+1][0] == "HP"): #[2+HP, 2/HP]
                return 2
            else:
                return 1
        return 0

    def twoHK(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "2" and self.parsedInputArray[index][1] == "HK"): #[2+HK]
            self.parsedMoveArray.append(["2HK", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "2" or self.parsedInputArray[index+1][0] == "HK"): #[2+HK, 2/HK]
                return 2
            else:
                return 1
        return 0

    #command normals
    def sixMP(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "6" and self.parsedInputArray[index][1] == "MP"): #[2, 2+MK]
            self.parsedMoveArray.append(["6MP", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "6" or self.parsedInputArray[index+1][0] == "MP"): #[2+MK, 2/MK]
                return 2
            else:
                return 1
        return 0

    def sixHP(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "6" and self.parsedInputArray[index][1] == "HP"): #[2, 2+MK]
            self.parsedMoveArray.append(["6HP", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "6" or self.parsedInputArray[index+1][0] == "HP"): #[2+MK, 2/MK]
                return 2
            else:
                return 1
        return 0

    def fourHP(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "4" and self.parsedInputArray[index][1] == "HP"): #[2, 2+MK]
            self.parsedMoveArray.append(["4HP", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "4" or self.parsedInputArray[index+1][0] == "HP"): #[2+MK, 2/MK]
                return 2
            else:
                return 1
        return 0

    def sixHK(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "6" and self.parsedInputArray[index][1] == "HK"): #[2, 2+MK]
            self.parsedMoveArray.append(["6HK", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "6" or self.parsedInputArray[index+1][0] == "HK"): #[2+MK, 2/MK]
                return 3
            else:
                return 2
        return 0

    def fourHK(self, index):
        if (len(self.parsedInputArray[index]) != 3):
            return 0

        if (self.parsedInputArray[index][0] == "4" and self.parsedInputArray[index][1] == "HK"): #[2, 2+MK]
            self.parsedMoveArray.append(["4HK", self.parsedInputArray[index][-1]])
            if (self.parsedInputArray[index+1][0] == "4" or self.parsedInputArray[index+1][0] == "HK"): #[2+MK, 2/MK]
                return 2
            else:
                return 1
        return 0

    #standing normals
    def fiveLP(self, index):
        if (self.parsedInputArray[index][0] == "LP"):
            self.parsedMoveArray.append(["5LP", self.parsedInputArray[index][-1]])
            return 1
        return 0

    def fiveLK(self, index):
        if (self.parsedInputArray[index][0] == "LK"):
            self.parsedMoveArray.append(["5LK", self.parsedInputArray[index][-1]])
            return 1
        return 0

    def fiveMP(self, index):
        if (self.parsedInputArray[index][0] == "MP"):
            self.parsedMoveArray.append(["5MP", self.parsedInputArray[index][-1]])
            return 1
        return 0

    def fiveMK(self, index):
        if (self.parsedInputArray[index][0] == "MK"):
            self.parsedMoveArray.append(["5MK", self.parsedInputArray[index][-1]])
            return 1
        return 0

    def fiveHP(self, index):
        if (self.parsedInputArray[index][0] == "HP"):
            self.parsedMoveArray.append(["5HP", self.parsedInputArray[index][-1]])
            return 1
        return 0

    def fiveHK(self, index):
        if (self.parsedInputArray[index][0] == "HK"):
            self.parsedMoveArray.append(["5HK", self.parsedInputArray[index][-1]])
            return 1
        return 0

    #parry/DI
    def parry(self, index):
        match (len(self.parsedInputArray[index])):
            case 2:
                if ("PARRY" in self.parsedInputArray[index]):
                    self.parsedMoveArray.append(["PARRY", self.parsedInputArray[index][-1]])
                    return 1
            case 3:
                if ("PARRY" in self.parsedInputArray[index]):
                    self.parsedMoveArray.append(["PARRY", self.parsedInputArray[index][-1]])
                    if (self.parsedInputArray[index+1][0] == "PARRY" or self.parsedInputArray[index+1][0] == self.parsedInputArray[index][0]):
                        return 2
                    else:
                        return 1
        return 0

    def DI(self, index):
        match (len(self.parsedInputArray[index])):
            case 2:
                if ("DI" in self.parsedInputArray[index]):
                    self.parsedMoveArray.append(["DI", self.parsedInputArray[index][-1]])
                    return 1
            case 3:
                if ("DI" in self.parsedInputArray[index]):
                    self.parsedMoveArray.append(["DI", self.parsedInputArray[index][-1]])
                    if (self.parsedInputArray[index+1][0] == "DI" or self.parsedInputArray[index+1][0] == self.parsedInputArray[index][0]):
                        return 2
                    else:
                        return 1
        return 0

    def framefixer(self):
        if self.parsedMoveArray:
            temp = self.parsedMoveArray[0][1]
            for row in self.parsedMoveArray:
                row[1] = row[1] - temp + 1
            for i in range(1, len(self.parsedMoveArray)):
                self.parsedMoveArray[i][1] = self.parsedMoveArray[i][1] - self.parsedMoveArray[i-1][1]

    def timer_controller(self):
        self.start_loop_time = datetime.now()
        while True:
            self.timer = datetime.now() - self.start_loop_time
            if self.threadstop == False:
                break


    def run(self):
        self.events.clear()
        self.array.clear()
        self.parsedInputArray.clear()
        self.parsedMoveArray.clear()
        self._monitor_thread = threading.Thread(target=self.timer_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()
        count = 0

        while self.timer < timedelta(seconds = self.maxTime):
            self.events = get_gamepad()

            for event in self.events:
                if (event.ev_type != "Sync"):
                    self.input_states[event.code] = event.state

            #print(self.input_states)

            if (self.input_states["BTN_SELECT"] == 1) and self.timer > timedelta(seconds = 0.5):
                print("reset button hit")
                self.parsedMoveArray.append("reset")
                break

            if count % 2 == 0:
                self.array.append([self.input_states[code] for code in self.event_codes])
                count += 1
            else:
                count = 0

            self.get_updates(self.array)
            self.array.clear()

        self.threadstop = False
        for i in range(9):
            self.parsedInputArray.append(["test", "Test"])

        print(self.parsedInputArray)
        resetVar = False
        try:
            if self.parsedMoveArray[0] == "reset":
                resetVar = True
                self.parsedMoveArray.pop()
        except IndexError:
            pass

        print("parsed moves")
        self.parsedInputArray = [row for row in self.parsedInputArray if row[-1] != 0]
        print(self.parsedInputArray)
        self.moveParser()
        self.framefixer()

        if len(self.savedCombo) != 0:
            combovalid = ComboValidityChecker(self.savedCombo, self.parsedMoveArray)
            output = combovalid.run()

            if resetVar == True:
                output = ["Reset Button Hit"] + output
        else:
            output = "no feedback given"
        return output


# used for example testing
#if __name__ == "__main__":
#     saved_combo = [['5HP', 1], ['PARRY', 11], ['5HK', 21], ['5HP', 70], ['236LK', 81], ['236236K', 98]]
#     button_input = ButtonInputs(saved_combo)
#     button_input.run()
