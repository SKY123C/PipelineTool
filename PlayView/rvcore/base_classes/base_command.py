import argparse


class RVCommand:
    long_name = None
    shot_name = None
    
    @staticmethod
    def run(parse: argparse.ArgumentParser):
        ...