class ComboValidityChecker():
    def __init__(self, savedCombo, parsedMoveArray):
        self.parsedMoveArray = parsedMoveArray
        self.ryuFrameData = [
            ["5LP", 4, 12, 7, 22, "ALL", 4],
            ["5MP", 6, 15, 11, 31, "ALL", 7],
            ["5HP", 10, 18, 18, 45, "ALL", 3],
            ["5LK", 5, 12, 11, 27, "ALL", 2],
            ["5MK", 9, 14, 18, 40, "NONE", 4],
            ["5HK", 12, 17, 20, 48, "NONE", 9],
            ["2LP", 4, 11, 9, 23, "ALL", 4],
            ["2MP", 6, 14, 14, 33, "ALL", 5],
            ["2HP", 9, 19, 21, 48, "ALL", 1],
            ["2LK", 5, 11, 10, 25, "NONE", 3],
            ["2MK", 8, 12, 19, 38, "ALL", 1],
            ["2HK", 9, 16, 23, 47, "NONE", 32],
            ["6MP", 20, 22, 19, 60, "NONE", 2],
            ["6HP", 20, 27, 16, 62, "NONE", 6],
            ["4HP", 7, 17, 25, 48, "ALL", 1],
            ["4HK", 10, 26, 21, 56, "ALL", 0],
            ["6HK", 16, 17, 20, 52, "NONE", 2],
            ["236LP", 16, 0, 31, 47, "SA3", -1],
            ["236MP", 14, 0, 33, 47, "SA3", -3],
            ["236HP", 12, 0, 35, 47, "SA3", -5],
            ["236PP", 12, 0, 28, 40, "SA2 SA3", 54],
            ["623LP", 5, 25, 33, 62, "SA3", 38],
            ["623MP", 6, 25, 42, 72, "SA3", 34],
            ["623HP", 7, 25, 49, 80, "SA3", 29],
            ["623PP", 7, 24, 52, 82, "NONE", 29],
            ["214LK", 12, 18, 32, 61, "NONE", 35],
            ["214MK", 14, 31, 31, 76, "NONE", 23],
            ["214HK", 16, 46, 31, 93, "NONE", 20],
            ["214KK", 13, 51, 23, 87, "NONE", 57],
            ["236LK", 15, 24, 22, 60, "SA3", 35],
            ["236MK", 18, 24, 19, 60, "SA3", 40],
            ["236HK", 29, 29, 16, 73, "SA3", 45],
            ["236KK", 18, 25, 33, 75, "SA2 SA3", 49],
            ["214LP", 12, 21, 18, 50, "SA3", 2],
            ["214MP", 19, 21, 17, 56, "SA3", 2],
            ["214HP", 30, 36, 19, 84, "SA3", 61],
            ["214PP", 18, 21, 20, 58, "SA2 SA3", 3],
            ["214P Denjin", 21, 6, 18, 44, "SA3", 62],
            ["236236P", 8, 0, 79, 87, "NONE", 26],
            ["214214P", 12, 24, 39, 74, "NONE", 20],
            ["236236K", 5, 12, 71, 87, "NONE", 8],
            ["THROW", 5, 9, 23, 36, "NONE", 17],
            ["DI", 26, 27, 35, 87, "NONE", 65],
            ["PARRY (RAW)", 11, 56, 23, 89, "NONE", 0],
            ["PARRY", 9, 54, 24, 86, "NONE", 0],
        ]
        self.saved_combo = savedCombo
        self.results = []

    def compare_moves(self, saved_combo, player_input):
        results = []
        last_input_frame = 1

        for move_number in range(len(saved_combo)):
            if len(player_input) < len(saved_combo) and move_number == len(player_input):
                return results

            player_move = player_input[move_number][0]
            player_frame = player_input[move_number][1]
            combo_move = saved_combo[move_number][0]

            if move_number > 0:
                if player_move == combo_move:
                    if player_frame - last_input_frame == saved_combo[move_number][1] - saved_combo[move_number-1][1]:
                        result = 'Perfect'
                    else:
                        result = self.frame_data_check(player_input, move_number, last_input_frame)
                else:
                    result = f'Wrong Move: {player_move}, should be {combo_move}'
                results.append('move: ' + str(player_move) + ' result: ' + str(result))
                last_input_frame = player_frame
            else:
                if player_move == combo_move:
                    result = 'Perfect'
                else:
                    result = f'Wrong Move: {player_move}, should be {combo_move}'
                results.append('move: ' + str(player_move) + ' result: ' + str(result))
                last_input_frame = player_frame

        return results


    def frame_data_check(self, player_input, move_number, last_input_frame):
        DRC_Link = False # Initialize drive rush cancel flag to False
        player_move = player_input[move_number][0] # Move the player executed
        player_frame = player_input[move_number][1] # Frame the move was executed on
        last_player_move = player_input[move_number-1][0] # Move the player executed
        #last_player_frame = player_input[move_number-1][1] # Frame the move was executed on
        move_data = [*[row for row in self.ryuFrameData if row[0] == player_move][0]]
        last_move_data = [*[row for row in self.ryuFrameData if row[0] == last_player_move][0]]
        special_moves = [
        '236LP', '236MP', '236HP', '236PP',
        '623LP', '623MP', '623HP', '623PP',
        '214LK', '214MK', '214HK', '214KK',
        '236LK', '236MK', '236HK', '236KK',
        '214LP', '214MP', '214HP', '214PP',
        '236236P', '214214P', '236236K', 'PARRY'
        ]
        cancels = {'SA2': ['214214P', '623623P'], 'SA3': '236236K', 'ALL': special_moves, 'NONE': []}
        # Determine if current move is linked from a drive rush cancel
        if move_number > 2:
            if player_input[move_number-2][0] == 'PARRY': #If move text contains PARRY
                DRC_Link = True

        if len(move_data) != 0:
            current_startup = int(move_data[1])
            last_startup = int(last_move_data[1])
            last_total = int(last_move_data[4])
            last_advantage = int(last_move_data[6])
            last_cancel_flag = last_move_data[5]

            if DRC_Link:
                last_advantage += 4 # Add 4 frames advantage to

            if player_move in cancels[last_cancel_flag] or player_input[move_number-1][0] == 'PARRY':
                # Min and Max input frames for cancels
                min_input_frame = last_input_frame + last_startup - 4 # -4 for 4 frame input buffer
                max_input_frame = last_input_frame + last_total + last_advantage - current_startup
            else:
                # Min and Max input frames for regular links
                min_input_frame = last_input_frame + last_total - 4 # -4 for 4 frame input buffer
                max_input_frame = last_input_frame + last_total + last_advantage - current_startup

            # Evaluate timing
            if player_frame < min_input_frame:
                offset = min_input_frame - player_frame #math for number of frames early
                result = f'Early {offset} Frames'
            elif player_frame > max_input_frame:
                offset = player_frame - max_input_frame #math for number of frames late
                result = f'Late {offset} Frames'
            else:
                result = 'Good'
            return result

    def run(self):
        results = self.compare_moves(self.saved_combo, self.parsedMoveArray)
        # used for testing
        # for result in results:
        #     print(f"Move: {result['move']}, Result: {result['result']}")
        return results
# Example usage:

# def main():
#     saved_combo = [['5HP', 1], ['PARRY', 11], ['5HK', 21], ['5HP', 70], ['236LK', 81], ['236236K', 98]]
#     player_input = [['5HP', 2], ['PARRY', 13], ['5HK', 24], ['5HP', 74], ['236LK', 82], ['236236K', 99]]

#     test = ComboValidityChecker(saved_combo, player_input)
#     test.run()

# if __name__ == "__main__":
#     main()
