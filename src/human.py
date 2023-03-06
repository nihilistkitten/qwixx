"""A human agent."""
from .qwixx import Agent


class HumanAgent(Agent):
    """A human agent."""

    def move(self, dice, boards, active_player):
        print(f"Player {self.number} to move.")
        print()

        print("YOUR BOARD:")
        print(boards[self.number])
        print()

        print("DICE:")
        print(dice)
        print()

        if active_player == self.number:
            print("It is your turn.")
        else:
            print("It is not your turn.")

        numbers_taken = 0

        public_number = input("Would you like to take the public number? [y/n] ")
        if public_number == "y":
            while True:
                try:
                    color = input(
                        "What color would you like to add it to? [r/y/g/b/cancel]"
                    )
                    if color == "cancel":
                        break
                    boards[self.number].cross(dice.public_sum, color)
                    numbers_taken += 1
                    break
                except ValueError as e:
                    print(e)

        if active_player == self.number:
            private_number = input("Would you like to use a private number? [y/n] ")
            if private_number == "y":
                while True:
                    try:
                        color = input(
                            "What color would you like to add it to? [r/y/g/b/cancel]"
                        )
                        if color == "cancel":
                            break
                        options = dice.options_for(color)
                        number = int(
                            input(
                                f"What number would you like to use? [{options[0]}/{options[1]}]"
                            )
                        )
                        if number not in options:
                            print("Invalid choice. Please try again.")
                            continue
                        boards[self.number].cross(number, color)
                        numbers_taken += 1
                        break
                    except ValueError as e:
                        print(e)

            if numbers_taken == 0:
                print("You took a neg.")
                boards[self.number].negs += 1
