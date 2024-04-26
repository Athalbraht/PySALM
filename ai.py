import os
from openai import OpenAI
from pandas import DataFrame, read_csv


class Responses(DataFrame):
    """Responses handles for AI class."""

    templates_path = ""

    @staticmethod
    def init(templates_path):
        """Create or load templates DataFrame."""
        try:
            print("- Loading response templates from file {}".format(templates_path))
            df = read_csv(templates_path)
            obj = Responses(df)
        except Exception as e:
            print(e)
            print("\t- cannot load file, creating new one")
            df = DataFrame(
                {
                    "alias" : [],
                    "prompt" : [],
                    "output" : [],
                    # "type" : [],
                    # "content" : [],
                    # "mode"  : [],
                    # "system-prompt"  : [],
                    # "user-prompt"  : [],
                },
                dtype=str,
            )
            obj = Responses(df)
            obj.to_csv(templates_path)

        templates_path = os.path.abspath(templates_path)
        obj.templates_path = templates_path
        return obj

    def find_index(self, alias):
        try:
            idx = self[self['alias'] == alias].index[-1]
        except:
            self.loc[len(self) + 1] = [alias, '', '']
            idx = self[self['alias'] == alias].index[-1]
        finally:
            return idx

    def update_prompt(self, alias, prompt):
        self.loc[self.find_index(alias), 'prompt'] += prompt
        self.save()

    def update_response(self, alias, msg):
        self.loc[self.find_index(alias), 'output'] = msg
        self.save()

    def get_response(self,alias):
        return self.loc[self.find_index(alias), 'output'] 


    def save(self):
        """Save temlates to file."""
        print("\t- saving templates to {}".format(self.templates_path))
        self.to_csv(self.templates_path)


class AI():
    """AI assistant class for astat analysys."""

    def __init__(self, config=None):
        """Client init."""
        self.client = OpenAI()
        self.config = config
        self.model = config['AImodel'],
        self.research_context = self.load_context()
        self.responses = Responses(config['templates.csv'])

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
