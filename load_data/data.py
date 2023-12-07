import os
from typing import List, Union
from pathlib import Path
from attrs import define, frozen, field
from load_data import STS12_PATH, STS13_PATH, STS14_PATH, STS15_PATH, STS16_PATH, STSBM_PATH, SICK_PATH


@frozen
class SentPair:
    topic: str
    sent1: str
    sent2: str
    score: float = field(converter=float)


def load_year_sts(task_path: Union[str, os.PathLike], topics: List[str]):
    pairs = []
    for topic in topics:
        with open(Path(task_path).joinpath(f"STS.input.{topic}.txt"), "r", encoding="utf-8") as f:
            sent1, sent2 = zip(*[l.split("\t") for l in f.read().splitlines()])
        with open(Path(task_path).joinpath(f"STS.gs.{topic}.txt"), "r", encoding="utf-8") as f:
            raw_scores = [x for x in f.read().splitlines()]
        assert len(sent1) == len(sent2) == len(raw_scores)
        topic_lst = [topic] * len(sent1)
        for pair in zip(topic_lst, sent1, sent2, raw_scores):
            if pair[-1]:
                # remove pairs without scores
                pairs.append(SentPair(*pair))
    return pairs


def load_sts_bm(task_path: Union[str, os.PathLike], topics: List[str]):
    pairs = []
    for topic in topics:
        with open(Path(task_path).joinpath(f"sts-{topic}.csv"), 'r', encoding='utf-8') as f:
            for line in f:
                text = line.strip().split('\t')
                pair = SentPair(topic, text[5], text[6], text[4])
                pairs.append(pair)
    return pairs


def load_sick(task_path: Union[str, os.PathLike], topics: List[str]):
    pairs = []
    topic2file_mapping = {
        "train": "SICK_train.txt",
        "dev": "SICK_trial.txt",
        "test": "SICK_test_annotated.txt"
    }
    for topic in topics:
        with open(Path(task_path).joinpath(topic2file_mapping[topic]), 'r', encoding='utf-8') as f:
            skip = True
            for line in f:
                if skip:
                    skip = False
                else:
                    text = line.strip().split('\t')
                    pair = SentPair(topic, text[1], text[2], text[3])
                    pairs.append(pair)
    return pairs


@define
class STS12:
    task_name = "STS12"
    dataset_names = ['MSRpar', 'MSRvid', 'SMTeuroparl', 'surprise.OnWN', 'surprise.SMTnews']
    pairs: List[SentPair]

    @classmethod
    def from_folder(cls, task_path: Union[str, os.PathLike]):
        pairs = load_year_sts(task_path, cls.dataset_names)
        return STS12(pairs)


@define
class STS13:
    task_name = "STS13"
    dataset_names = ['FNWN', 'headlines', 'OnWN']
    pairs: List[SentPair]

    @classmethod
    def from_folder(cls, task_path: Union[str, os.PathLike]):
        pairs = load_year_sts(task_path, cls.dataset_names)
        return STS13(pairs)


@define
class STS14:
    task_name = "STS14"
    dataset_names = ['deft-forum', 'deft-news', 'headlines', 'images', 'OnWN', 'tweet-news']
    pairs: List[SentPair]

    @classmethod
    def from_folder(cls, task_path: Union[str, os.PathLike]):
        pairs = load_year_sts(task_path, cls.dataset_names)
        return STS13(pairs)


@define
class STS15:
    task_name = "STS15"
    dataset_names = ['answers-forums', 'answers-students', 'belief', 'headlines', 'images']
    pairs: List[SentPair]

    @classmethod
    def from_folder(cls, task_path: Union[str, os.PathLike]):
        pairs = load_year_sts(task_path, cls.dataset_names)
        return STS13(pairs)


class STS16:
    task_name = "STS16"
    dataset_names = ['answer-answer', 'headlines', 'plagiarism', 'postediting', 'question-question']
    pairs: List[SentPair]

    @classmethod
    def from_folder(cls, task_path: Union[str, os.PathLike]):
        pairs = load_year_sts(task_path, cls.dataset_names)
        return STS13(pairs)


@define
class STSBM:
    task_name = "STSBM"
    dataset_names = ["train", "dev", "test"]
    pairs: List[SentPair]

    @classmethod
    def from_folder(cls, task_path: Union[str, os.PathLike]):
        pairs = load_sts_bm(task_path, cls.dataset_names)
        return STSBM(pairs)


@define
class SICK:
    task_name = "SICK"
    dataset_names = ["train", "dev", "test"]
    pairs: List[SentPair]

    @classmethod
    def from_folder(cls, task_path: Union[str, os.PathLike]):
        pairs = load_sick(task_path, cls.dataset_names)
        return SICK(pairs)


if __name__ == '__main__':
    sts = SICK.from_folder(SICK_PATH)
    print(len(sts.pairs))
    print(sts.pairs[0])
