from nlp.parser import judge_ambiguity


def test_judge_ambiguity():
    text1 = "Create a parallel node that contains check_assembly and interrupt_assembly as child nodes."
    text1 = "Create a sequence node with correct_positioning as its child node and interrupt_assembly as its fallback node."
    text2 = "Grab needed parts, positioning them on the assembly line, and then assemble the parts."
    text2 = "Get the necessary workpiece, position it correctly, and then assemble it."
    text3 = "Task execution: Perform the assembly process correctly and efficiently."
    text3 = "Execution task: Assemble all parts correctly and safely."
    text3 = "Perform tasks: Check that the parts are correctly positioned."
    text3 = "Perform the task of safely assembling the parts"
    print(judge_ambiguity(text3))


if __name__ == '__main__':
    test_judge_ambiguity()
