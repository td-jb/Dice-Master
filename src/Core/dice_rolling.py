import random

def roll_dice(num_dice: int, sides: int, modifier: int = 0) -> int:
    """
    Rolls a specified number of dice with a given number of sides and applies a modifier.

    Args:
        num_dice (int): The number of dice to roll.
        sides (int): The number of sides on each die.
        modifier (int): A value to add to the total roll. Default is 0.

    Returns:
        int: The total result of the dice rolls plus the modifier.
    """
    total = sum(random.randint(1, sides) for _ in range(num_dice))
    return total + modifier

def roll_dice_details(num_dice: int, sides: int, modifier: int = 0) -> dict:
    """
    Rolls dice and provides detailed results including individual rolls and the total.

    Args:
        num_dice (int): The number of dice to roll.
        sides (int): The number of sides on each die.
        modifier (int): A value to add to the total roll. Default is 0.

    Returns:
        dict: A dictionary containing individual rolls, the modifier, and the total.
    """
    rolls = [random.randint(1, sides) for _ in range(num_dice)]
    total = sum(rolls) + modifier
    return {
        "rolls": rolls,
        "modifier": modifier,
        "total": total
    }
