from conf import tex_config
from manager import Analysis

if __name__ == "__main__":
    analysis = Analysis(tex_config)
    analysis.register_commands()
    analysis.create_table_of_content()
    analysis.boost_commands()

    #df = data_loader("data/data.xlsx")
    #data = generate_metric(df)
