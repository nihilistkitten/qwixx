from src.human import HumanAgent
from src.qwixx import Qwixx

if __name__ == "__main__":
    Qwixx([HumanAgent, HumanAgent]).play()
