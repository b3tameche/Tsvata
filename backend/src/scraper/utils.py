import re

from constants import TAGS

def extract_skills(text: str):
    filter_stage_1: str = re.sub('(<[^<>]+>)|(<!--(.*?)-->)', ' ', text)
    filter_stage_2: str = re.sub('[\/\\(),:;?!]|((?<=\w)\.(?=\w|$))|(\s)', ' ', filter_stage_1)

    tokens = set(filter_stage_2.lower().split(' '))
    captured = tokens.intersection(TAGS.keys())
    skills = list(map(lambda x: TAGS[x][1], captured))

    return skills