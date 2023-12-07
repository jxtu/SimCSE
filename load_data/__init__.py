from pathlib import Path

STS_PATH = Path(__file__).parent.parent.joinpath("SentEval/data/downstream/STS")
STS12_PATH = STS_PATH.joinpath("STS12-en-test")
STS13_PATH = STS_PATH.joinpath("STS13-en-test")
STS14_PATH = STS_PATH.joinpath("STS14-en-test")
STS15_PATH = STS_PATH.joinpath("STS15-en-test")
STS16_PATH = STS_PATH.joinpath("STS16-en-test")
STSBM_PATH = STS_PATH.joinpath("STSBenchmark")

SICK_PATH = Path(__file__).parent.parent.joinpath("SentEval/data/downstream/SICK")



