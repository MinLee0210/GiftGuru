INSTRUCTION_FINETUNE_PREFIX = '''
For the following tasks, make plans that can solve the problem step-by-step. For each plan, indicate which external tool together with tool input to retrieve evidence. You can store the evidence into a variable #E that can be called by later tools. (Plan, #E1, Plan, #E2, Plan, ...) 

Tools can be one of the following:
Wikipedia[input]: Worker that search for similar page contents from Wikipedia. Useful when you need to get holistic knowledge about people, places, companies, historical events, or other subjects. The response are long and might contain some irrelevant information. Input should be a search query.
LLM[input]: A pretrained LLM like yourself. Useful when you need to act with general world knowledge and common sense. Prioritize it when you are confident in solving the problem yourself. Input can be any instruction.

Question: What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?
Plan: Search for more information about Colorado orogeny.
#E1 = Wikipedia[Colorado orogeny]
Plan: Find out the area that eastern sector of the Colorado orogeny extends into.
#E2 = LLM[What is the name of the area that eastern sector of Colorado extends into? Given context: #E1]
Plan: Search for more information about the area.
#E3 = Wikipedia[#E2]
Plan: Find out the elevation range for the area.
#E4 = LLM[What is elevation range for the area #E2? Given context: #E3]

Question: Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?
Plan: Search for more information about Milhouse.
#E1 = Wikipedia[Milhouse]
Plan: Find out who Matt Groening named Milhouse after.
#E2 = LLM[Who did Matt Groening name Milhouse after? Given context: #E1]

'''

INSTRUCTION_FINETUNE_SUFFIX = '''
Now make plans for each of the following questions. Your answer should follow the same format as the exemplars above. Like this:
Question: xxxx
Plan: xxxx
#E1 = xxxx
Plan: xxxx
...

'''