# Implementation of the FastAPI
# Notes:
#   * Could extend with upload capability: https://fastapi.tiangolo.com/tutorial/request-files/
#

from fastapi import FastAPI, Query
import subprocess

app = FastAPI()


@app.get("/fr_to_eng/")
async def endpoint_fr_to_eng(
        text: str = Query(
            ..., # requires input, no default
            title="French text to be translated",
            description="Query string to translate from French to English.",
            min_length=2, # min length string must be
            max_length=1000 # max length string must be
        ),
        T_sampling: float = Query(
            0.6, #default temperature
            title="Optional sampling randomness (temperature)",
            description="Fraction between 0 and 1 indicating the sampling temperature or randomness. The higher"
                        "the more random.",
            gt=0., # greater than 0
            le=1., # less than 1.
        ),
):

    translation = translate_fr_to_english(text, T_sampling)

    return translation

@app.get("/eng_to_fr/")
async def endpoint_eng_to_fr(
        text: str = Query(
            ..., # requires input, no default
            title="English text to be translated",
            description="Query string to translate from English to French.",
            min_length=2, # min length string must be
            max_length=1000 # max length string must be
        ),
        T_sampling: float = Query(
            0.6, #default temperature
            title="Optional sampling randomness (temperature)",
            description="Fraction between 0 and 1 indicating the sampling temperature or randomness. The higher"
                        "the more random.",
            gt=0., # greater than 0
            le=1., # less than 1.
        ),
):

    translation = translate_eng_to_french(text, T_sampling)

    return translation


def translate_fr_to_english(french_text,T_sampling):
    '''
    Translation function translating from French to English. Starts subprocess.
    :param french_text:
    :return:
    '''
    with open('fr_text.txt','w') as f:
        f.write(french_text)

    # execute the translation, log all outputs to .log file
    with open('run_translation_fr_eng.log', 'w') as f:
        process = subprocess.Popen(['./run_translation_fr_eng.sh',str(T_sampling)],
                                   stdout=f,
                                   stderr=f)
        print('wait')
        process.wait()
        print('finish')
    try:
        with open('back_trans_data/paraphrase/file_0_of_1.json') as f:
            print('translation from file:')
            lines = f.readlines()
            return_lines = ''.join(lines)
    except:
        print('translated file not available. Error!')
        return_lines = 'translated file not available. Error!'

    print('Resulting lines: ', return_lines)

    return return_lines


def translate_eng_to_french(english_text,T_sampling):
    '''
    Translation function translating from French to English. Starts subprocess.
    :param english_text:
    :return:
    '''
    with open('eng_text.txt','w') as f:
        f.write(english_text)

    # execute the translation, log all outputs to .log file
    with open('run_translation_eng_fr.log', 'w') as f:
        process = subprocess.Popen(['./run_translation_eng_fr.sh',str(T_sampling)],
                                   stdout=f,
                                   stderr=f)
        print('wait')
        process.wait()
        print('finish')
    try:
        with open('back_trans_data/paraphrase/file_0_of_1.json') as f:
            print('translation from file:')
            lines = f.readlines()
            return_lines = ''.join(lines)
    except:
        print('translated file not available. Error!')
        return_lines = 'translated file not available. Error!'

    print('Resulting lines: ', return_lines)

    return return_lines