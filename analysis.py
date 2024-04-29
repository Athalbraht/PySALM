from conf import tex_config, data_loader
from sys import argv
from manager import Analysis

if __name__ == "__main__":
    df = data_loader(argv[1])
    analysis = Analysis(tex_config, compile=True, data=df)
    analysis.register_commands()
    analysis.create_table_of_content()
    analysis.boost_commands()
    analysis.build_document()

    #df = data_loader("data/data.xlsx")
    #data = generate_metric(df)
