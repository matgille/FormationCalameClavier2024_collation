import json

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
            form, lemma, pos, morph, *rest = token
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


def simplify_results(alignment_results):
    alignment_results_as_json = json.loads(alignment_results)
    zipped = list(zip(alignment_results_as_json['table'][0], alignment_results_as_json['table'][1], alignment_results_as_json['table'][2]))
    output_data = list()
    for locus in zipped:
        interm_list = []
        for index, witness in enumerate(locus):
            if witness is not None:
                interm_dict = dict()
                interm_dict['témoin'] = witness[0]['_sigil']
                interm_dict['forme'] = witness[0]['t']
                interm_dict['lemme'] = witness[0]['lemma']
                interm_dict['pos'] = witness[0]['pos']
                interm_dict['morph'] = witness[0]['morph']
                interm_list.append(interm_dict)
            else:
                interm_dict = dict()
                interm_dict['témoin'] = alignment_results_as_json["witnesses"][index]
                interm_dict['forme'] = None
                interm_dict['lemme'] = None
                interm_dict['pos'] = None
                interm_dict['morph'] = None
                interm_list.append(interm_dict)
        output_data.append(interm_list)
    return output_data