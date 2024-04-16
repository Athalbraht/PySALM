from openai import OpenAI


class AI():
    """AI assistant class for astat analysys."""

    def __init__(self, model="gpt-3.5-turbo"):
        """Client init."""
        self.client = OpenAI()
        self.model = model,
        self.research_context = self.load_context()

    def make_it_free(self):
        """Disable online requests, keep prompt locally and ask manually :D."""
        pass

    def request(self):
        """Make API request."""
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role" : "system",
                    "content" : ""
                },
                {
                    "role" : "user",
                    "content" : ""
                }
            ]
        )
        return completion.choices[0].message

    def generate_abstract(self):
        """Generate abstract based on summary."""
        pass

    def generate_research_questions(self):
        """Generate research question section."""
        pass

    def generate_methods(self):
        """Generate methods section based on used tools."""
        pass

    def generate_captions(self):
        """Generate plot and tabs descriptions."""
        pass

    def generate_description(self):
        """Generate statistic data description."""
        pass

    def generate_correlation(self):
        """Try to describe global results."""
        pass

    def generate_summary(self):
        """Generate statistic data description."""
        pass
