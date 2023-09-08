"""
Module that handles parsing MD files and converting them to JSON
"""

from markdownify import markdownify as md
import markdown
import json
import re


def get_meta(question_dict: dict, key: str):
    """
    Get metadata from question_dict
    :param question_dict: dictionary that contains question metadata
    :param key: the key that will be searched in the dictionary
    :return: the value associated with key from question dict
    """
    if not key in question_dict["metadata"]:
        return ""
    if len(question_dict["metadata"][key]) == 1:
        return question_dict["metadata"][key][0]
    return question_dict["metadata"][key]

def quiz_md_to_json(file_content: str):
    """
    Converts a MD quiz to JSON quiz
    :param file_content: a quiz stored in MD format
    :return: a quiz stored in JSON format
    """
    question_arr = file_content.split("\n\n\n")
    question_arr_json = list(map(md_to_json, question_arr))
    return '[' + ','.join(question_arr_json) + ']'

def quiz_json_to_md(json_arr: list):
    """
    Converts a JSON quiz to MD quiz
    :param file_content: a quiz stored in JSON format
    :return: a quiz stored in MD format
    """
    return list(map(json_to_md, json_arr))

def json_to_md(json_obj: dict) -> str:
    """
    Generates a question in MD format from JSON string
    :param json_obj: a question stored in JSON format
    :return: a string representing a question in MD format
    """

    json_q = json_obj
    md_q = ""

    md_q += "# " + json_q["name"] + "\n\n"
    md_q += "## Question Text\n\n"
    md_q += json_q["statement"] + "\n\n"

    md_q += "## Question Answers\n\n"
    for answer in json_q["answers"]:
        ans = answer["statement"]
        grade = "+" if answer["correct"] else "-"
        md_q += grade + " " + ans + "\n\n"

    if "feedback" in json_q and json_q["feedback"] is not None:
        md_q += "## Feedback\n\n"
        md_q += json_q["feedback"] + "\n\n"

    return md_q + "\n"

def md_to_json(md_q: str) -> str:
    md_copy = str(md_q).rstrip()
    md_copy = re.sub(r'\n+', '\n', md_copy).strip('\n')

    question = {
        "name": "",
        "statement": "",
        "feedback": "",
        "metadata": {},
        "answers": [
            # {
            #     "statement": "",
            #     "correct": False,
            #     "grade": 0.0
            # }
        ],
        "correct_answers_no": 0,
    }

    q_title = md_copy.split('\n')[0][2:]
    q_body = md_copy.split('\n')[1:]
    question["name"] = q_title

    q_fiels = md_copy.split('## ')

    for field in q_fiels:
        field_name = field.split('\n')[0]

        if field_name == 'Question Text':
            question['statement'] = '\n'.join(field.split('\n')[1:])
        elif field_name == 'Question Answers':
            q_ans = field.rstrip('\n').split('\n')[1:]
            question['correct_answers_no'] = len([ans for ans in q_ans if ans[0] == '+'])
            grade = 1 / (question['correct_answers_no'] * 1.0)

            for ans in q_ans:
                if ans[0] == '+':
                    question['answers'].append(
                        {"statement": ans[2:], "correct": True, "grade": grade}
                    )
                elif ans[0] == '-':
                    question['answers'].append(
                        {"statement": ans[2:], "correct": False, "grade": 0}
                    )
        elif field_name == 'Feedback':
            question['feedback'] = '\n'.join(field.split('\n')[1:])

    return json.dumps(question, indent=4)
