__version__ = "v0.1.0"
from conf import tex_config, data_loader
from sys import argv
from manager import Analysis


print("""
########################################
## Starting analysis...
## StatPAI {}
## Author Albert Szadziński
## License: MIT
########################################

      """.format(__version__))

if __name__ == "__main__":
    df = data_loader(argv[1])
    analysis = Analysis(tex_config, data=df)
    analysis.register_commands()
    analysis.create_table_of_content()
    analysis.boost_commands()
    analysis.build_document()
    analysis.compile()

    # df = data_loader("data/data.xlsx")
    # data = generate_metric(df)
