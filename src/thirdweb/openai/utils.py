class PromptUtils:
    @staticmethod
    def create_prompt_for_summarization(text: str) -> str:
        prompt = (f"Please summarize the following note's content and return "
                  f"the summary without any additional comments or explanations."
                  f" Ensure the summary is at least half the length of the original content. TEXT: {text}")
        return prompt
