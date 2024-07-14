SCRAPER_PROMPT = "Summarize the document in 3 sentences and suggest a gift based on those information {prompt}. Your answer must be in JSON formed of summary & suggest"

MINDS_AGENT_SUFFIX = "Here are some additional information that can help your results:\n{suggest_resource} \
    ###Instruction\
    \nMake it in 1 pargraph.\
    \nBe clear, concise and creative!\
    \nNo numeric points, just bullet points\
    "