from conf import tex_config
from manager import Session

if __name__ == "__main__":
    analysis = Session(tex_config)
    analysis.create_table_of_content()
    analysis.boost_instructions()

    #df = data_loader("data/data.xlsx")
    #data = generate_metric(df)
