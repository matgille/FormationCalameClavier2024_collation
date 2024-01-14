def test():
    print("OK")


# Deux fonctions permettant de produire les données au format qui est nécessité par collatex
def import_annotated_data(text_path:str):
    with open(text_path, "r") as input_text:
        text_as_list = [line.replace("\n", "") for line in input_text.readlines()][1:]
    output_list = []
    for line in text_as_list:
        splits = line.split("\t")
        print(splits)
        output_list.append(splits)
    return output_list

def create_json_input_for_collatex(dict_of_text, collate_on="lemmas"):
    output_dict = {"witnesses": []}
    for sigla, text in dict_of_text.items():
        witness_dict = {"id": sigla}
        tokens = []
        for token in text:
            form, case, mood, numb, person, tense, lemma, pos = token
            morph = case+mood+numb+person+tense
            if collate_on == "lemmas":
                tokens.append({"t": form, "n":lemma, "lemma": lemma, "pos": pos, "morph":morph})
            elif collate_on == "lemmas+pos":
                tokens.append({"t": form, "n":f"{lemma}|{pos}", "lemma": lemma, "pos": pos, "morph":morph})
            elif collate_on == "pos":
                tokens.append({"t": form, "n":f"{pos}", "lemma": lemma, "pos": pos, "morph":morph})
            else:
                tokens.append({"t": form, "n":form, "lemma": lemma, "pos": pos, "morph":morph})
        witness_dict["tokens"] = tokens
        output_dict["witnesses"].append(witness_dict)
    return output_dict