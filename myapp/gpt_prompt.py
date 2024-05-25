Multipe_choice_blank_System_message = '''
When we ask you to create a problem, write the keyword 'problem' as it is and do not write the number of the problem 'problem1' like 1. And next to it,
be sure to leave two spaces and write the problem content. This part should be processed in one line. And be sure to leave two spaces between the problem and the problem content so that it can be divided by split("  ").

When we ask you to create a problem, we do not want additional answers except for the part related to the problem. (ex Yes, I understand)
And never give a problem with multiple answers and make sure there is only one problem answer.
When you ask me to create multiple problems, be sure to output '----------------' between the problem and the problem. Nothing should be there except for this. Whether it's a space or an enter.

Make all the problems solvable at the level of a university undergraduate 1st to 2nd year student and make them at a level that helps understand the major.
And in the case of multiple choice questions, make the answer very clear. If you do well, I'll give you $30.
'''

def prompt_1(count, subject, rags, tempt_problem):
    return f'''
Create {count} {subject} blank multiple choice questions using the {subject} template material.
There must be a blank like '____' in the problem. It is a format in which you have to match the blank with the correct answer.
Example 1) In Java, _____ is a keyword used when inheriting a parent class.
Example 2) In C++, the destructor uses the ___ keyword.

Example 3) In Python, _____ is a data structure that stores values using hash values.
And give me only 4 choices and give me a keyword like 1.) to distinguish the order for each choice. There must be 1.) for each number.

And make sure that the problem and the choice and the correct answer are all separated by an enter. The choice should also take up one line per choice.
Put the correct answer right below the multiple choice choice. When putting the correct answer, put it like this: Correct answer: 1.) java And there must be only one correct answer.
Don't give me a problem like {tempt_problem} because I already have it.
Don't give me a problem related to the example because I can't use the example as a material.
ex(specific class or method name)
When printing the problem, it is most important to keep the constraints I put.  remove all markdown i want text only. no number state in individual problem, only 'problem' we want
'''


Multipe_choice_short_answer_System_message = '''
When we ask you to make a problem, write the keyword 'problem' as it is and don't write how many problems it is. There should be no keyword like 1 in 'problem1'. And next to it,
make sure to leave two spaces and write the problem content. This part should be processed in one line. And make sure to leave two spaces between the problem and the problem content so that it can be divided by split("  ").

When we ask you to make a problem, we don't want any additional answers except for the part related to the problem. (ex I understand)
And don't give me a problem with multiple correct answers and make sure there is only one correct answer to the problem.
When you ask me to make multiple problems, make sure to print '----------------' between the problem and the problem. There should be nothing else except for this. Whether it's a space or an enter.

Make all the problems so that they can be solved at the level of a university undergraduate 1st to 2nd year student and make them at a level that helps them understand the major.
And in the case of multiple choice questions, make sure the answer is very clear. If you do well, I'll give you $30.
'''

def prompt_2(count, subject, rags, tempt_problem):
    return f''' 
Make {count} {subject} short answer questions in multiple choice format by referring to the {subject} template material. 
The problem must be in an intact form without missing words, and the answer must be simple. For example, a problem where one or two words or a line of code is the answer is fine. 

And give me only 4 multiple choice questions and give me a keyword for each multiple choice question to distinguish the order. Make sure there is 1.) after each number.

And make sure the problem and the multiple choice questions and the answer are all separated by an enter. The multiple choice questions should also take up one line per question.
Put the answer right below the multiple choice questions. When putting the answer, put it like this: Answer: 1.) java And make sure there is only one answer.
Don't make a similar question to the {tempt_problem} question because there is already a question.
Don't make a question related to the example because you can't refer to the example as a material.
ex(specific class or method name)
When outputting the problem, it is most important to keep the constraints I put. remove all markdown i want text only. no number state in individual problem, only 'problem' we want
'''

Multipe_choice_one_sentence_System_message = '''
When we ask you to make a problem, write the 'problem' keyword as it is and don't write how many problems it is. There should be no keyword like 1 in 'problem1'. And then,
make sure to put two spaces next to it and write the problem content. This part should be processed in one line. And make sure to put two spaces between the problem and the problem content so that it can be divided by split("  ").

When we ask you to make a problem, we don't want any additional answers except for the part related to the problem. (ex I understand)
And don't make a problem with multiple answers and make sure there is only one answer to the problem.
When you ask me to make multiple problems, make sure to output '----------------' between the problem and the problem. There should be nothing else except for this. Whether it's a space or an enter.

Make all the problems at the level of university undergraduate 1st to 2nd year students and make them at the level that helps them understand the major.
And for multiple choice questions, make sure the answer is very clear. If you do well, I'll give you $30.
'''

def prompt_3(count, subject, rags, tempt_problem):
    return f''' 
Make {count} {subject} multiple choice questions by referring to the {subject} template material. 
The problem must be in the form of a complete word without missing words, and the choice must be in the form of a single sentence.
Output the choice in the form of a sentence with at least 6 phrases each.
And give the choice only in the form of 4 multiple choices, and give the order by the same keyword for each choice. There must be 1.) for each number.

And make sure that the problem and the choice and the answer are all separated by an enter. The choice must also occupy one line per choice.
Put the answer right below the multiple choice choice. When putting the answer, put it like "Answer: 1.) "Overloading is a technique that makes the method name the same and the parameter different." And there must be only one answer.
Don't give similar content to the {tempt_problem} problem because there is already a problem.
Don't give problems related to examples because you can't refer to the example as a material. ex(specific class or method name)
When outputting the problem, it is most important to keep the constraints I put.remove all markdown i want text only. no number state in individual problem, only 'problem' we want
'''

Blank_System_message = '''
When we ask you to make a problem, write the 'problem' keyword as it is and don't write how many problems it is. There should be no keywords like 1 in 'problem1'. And next to it,
Make sure to leave two spaces and write the problem content. This part must be processed in one line. And make sure to leave two spaces between the problem and the problem content so that it can be divided by split("  ").

When we ask you to make a problem, we don't want any additional answers except for the part related to the problem.
(ex I understand)
When you ask me to make a short answer blank type problem, it must be a problem where there is a blank in the problem and the answer is to match what is in the blank.
When you ask me to make multiple problems, make sure to output '----------------' between the problem and the problem. Nothing else should be there except for this. Whether it's a space or an enter.

Make all the problems at the level of a university undergraduate 1st to 2nd year student and make them at the level that helps them understand the major.
'''

def prompt_4(count, subject, rags, tempt_problem): 
    return f''' 
Make {count} {subject} short answer blank type problems by referring to the {subject} template material
There must be a blank in the problem, such as '____'. Put the blank in the middle of the problem, not at the end. The format is to match the blank as the answer.

Put the answer right below the problem. When putting the answer, put it like "Answer: Extends".
Don't give similar content to the {tempt_problem} problem because it already exists.
Don't give problems related to the example because you can't refer to the example as a material. ex(specific class or method name)
When outputting the problem, it is most important to keep the constraints I put. remove all markdown i want text only. no number state in individual problem, only 'problem' we want
'''

Short_answer_message = '''
When we ask you to make a problem, write the 'problem' keyword as it is and don't write how many problems it is. There should be no keywords like 1 in 'problem1'. And next to it,
make sure to leave two spaces and write the problem content. This part should be processed in one line. And make sure to leave two spaces between the problem and the problem content so that it can be divided by split("  ").

When we ask you to make a problem, we don't want any additional answers except for the part related to the problem. (ex I understand)
When you ask me to make a short answer problem, you have to make a problem that can be summarized in one sentence as an answer.
When you ask me to make multiple problems, make sure to output '----------------' between the problem and the problem. Nothing else should be there except for this. Whether it's a space or an enter.

Make all the problems so that they can be solved at the level of a university undergraduate 1st to 2nd year student and make them at a level that helps understand the major.
'''

def prompt_5(count, subject, rags, tempt_problem):
    return f'''
Make {count} {subject} short answer problems by referring to the {subject} template material
Put the answer right below the problem. When putting the answer, put it like this "Answer: Overloading is a method of making the method name the same and the parameter different."
When outputting the problem, it is most important to keep the constraints I put.
And the problem must be in Korean.
Don't give the same content as the {tempt_problem} problem because there is already a problem.
You can't refer to the example as a material, so don't give a problem related to the example. ex(specific class or method name) remove all markdown i want text only. no number state in individual problem, only 'problem' we want
'''
OX_message = '''
When we ask you to make a problem, write the 'problem' keyword as it is and don't write how many problems it is 'problem1' like 1. And next to it,
make sure to leave two spaces and write the problem content. This part must be processed in one line. And make sure to leave two spaces between the problem and the problem content so that it can be divided by split("  ").

When we ask you to make a problem, we don't want any additional answers except for the part related to the problem. (ex I understand)
When you ask me to make an OX problem, don't put a phrase like O?X? next to the problem, just write the problem. Don't ask if it's O or X.

When you ask me to make multiple problems, make sure to print '----------------' between the problem and the problem. Nothing else should be there except for this. No spaces or enter.
Make all the problems at the level of a university undergraduate 1st or 2nd year student and make them at the level of helping them understand the major.
'''

def prompt_6(count, subject, rags, tempt_problem):
    return f'''
Make {count} {subject} OX problems by referring to the {subject} template material
Put the answer right below the problem. When putting the answer, put it like "Answer: O"
Don't make a similar problem to {tempt_problem} problem. Don't make it at all. And make it exactly in the form I ask for. remove all markdown i want text only. no number state in individual problem, only 'problem' we want

Make it an OX problem.
When printing the problem, it is most important to keep the constraints I put. And make the problem in Korean.
'''

Code_message = '''
When we ask you to make a code related problem, write the keyword 'problem' as it is and don't write how many problems it is. There should be no keywords like 1 in 'problem1'. And write the problem content right below the problem.
When we ask you to make a problem, we don't want any additional answers except for the part related to the problem.
(ex I understand)
When you ask me to make multiple problems, print '----------------' between the problems. There should be nothing else except for this. No spaces or enter.
'''

def prompt_7(count):
    return f'''
Make {count} code related problems in Python at an advanced level. It is a problem that I have to write code, and make it in a format that leaves the middle part of the code blank.
However, if there is nothing at all, it will be strange, so write the basic variable definition or function definition related code.
And I want the part that is left blank to be more than 3 lines. I think I need to write about 3 lines of code. And make a problem by marking what code is needed using the TODO comment.
'''

sys_feedback = ''

prompt_lst = [0, prompt_1,prompt_2,prompt_3,prompt_4,prompt_5,prompt_6, prompt_7]
System_lst = [0, Multipe_choice_blank_System_message, Multipe_choice_short_answer_System_message, Multipe_choice_one_sentence_System_message, Blank_System_message, Short_answer_message, OX_message, Code_message]