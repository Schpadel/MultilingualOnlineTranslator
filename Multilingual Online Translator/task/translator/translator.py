import sys

import requests
from bs4 import BeautifulSoup

languages = {
    '1': 'arabic',
    '2': 'german',
    '3': 'english',
    '4': 'spanish',
    '5': 'french',
    '6': 'hebrew',
    '7': 'japanese',
    '8': 'dutch',
    '9': 'polish',
    '10': 'portuguese',
    '11': 'romanian',
    '12': 'russian',
    '13': 'turkish',
    '0': 'all'
}

translation = set()
translation_list = list()
example_text = list()

print("Hello, you're welcome to the translator. Translator supports:")
print("""1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish""")


def get_user_input():
    global origin_language, target_language, word_to_translate
    print("Type the number of your language:")
    origin_language = input()
    print("Type the number of a language you want to translate to or '0' to translate to all languages:")
    target_language = input()
    print("Type the word you want to translate:")
    word_to_translate = input()


def get_command_line_arguments():
    global origin_language_string, target_language_string, word_to_translate, target_language
    arguments = sys.argv

    print(arguments)

    if arguments[1] not in languages.values():
        print("Sorry the program doesn't support {}".format(arguments[1]))
        sys.exit()
    if arguments[2] not in languages.values():
        print("Sorry the program doesn't support {}".format(arguments[2]))
        sys.exit()
    origin_language_string = arguments[1]
    target_language_string = arguments[2]

    if arguments[2] == "all":
        target_language = "0"
    else:
        target_language = arguments[2]

    word_to_translate = arguments[3]


def single_word_translation():
    url = "https://context.reverso.net/translation/{origin_lang}-{target_lang}/{word}".format(
        origin_lang=origin_language_string, target_lang=target_language_string, word=word_to_translate)
    print(url)
    header = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=header)
    with open(word_to_translate + ".txt", "w") as file:
        if page.ok:
            print(page.status_code, "OK")
            file.write(str(page.status_code) + " OK" + "\n")
            print(target_language_string.capitalize() + " Translations")
            file.write(target_language_string.capitalize() + " Translations" + "\n")
            soup = BeautifulSoup(page.content, "html.parser")
            target_text = soup.find_all("div", {"class": "trg ltr"})
            source_text = soup.find_all("div", {"class": "src ltr"})

            for target, source in zip(target_text, source_text):
                translation.add(target.find("em").text)  # translation words of text examples
                example_text.append(target.find("span", {"class": "text"}).text)
                example_text.append(source.find("span", {"class": "text"}).text)

            first_translation_word = soup.find_all('a', {"class": 'translation'})
            translation_list = [translation.get_text().strip().lower() for translation in first_translation_word]

            if len(translation_list):
                for word in translation_list:
                    print(word)
                    file.write(word + "\n")
            else:
                print("Sorry unable to find {}".format(word_to_translate))

            print(target_language_string.capitalize() + " Examples:")
            file.write(target_language_string.capitalize() + " Examples:" + "\n")
            counter = 1
            for sentence in example_text:
                print(sentence.strip())
                file.write(sentence.strip() + "\n")
                if counter % 2 == 0:
                    print()
                    file.write("\n")
                counter = counter + 1
        else:
            print("Something wrong with your internet connection")
            file.write("Something wrong with your internet connection" + "\n")


get_command_line_arguments()

if target_language != "0":
    single_word_translation()

if target_language == "0":

    with open(word_to_translate + ".txt", "w") as file:
        for value in languages.values():
            if value == origin_language_string:
                continue
            translation_list.clear()
            example_text.clear()
            target_language_string = value
            url = "https://context.reverso.net/translation/{origin_lang}-{target_lang}/{word}".format(
                origin_lang=origin_language_string, target_lang=target_language_string, word=word_to_translate)
            header = {"User-Agent": "Mozilla/5.0"}
            page = requests.get(url, headers=header)
            #  print(url)
            if page.ok:
                #  print(page.status_code, "OK")

                print(target_language_string.capitalize() + " Translation:")
                file.write(target_language_string.capitalize() + " Translation:" + "\n")
                soup = BeautifulSoup(page.content, "html.parser")
                if target_language_string == "arabic":
                    target_text = soup.find_all("div", {"class": "trg rtl arabic"})
                elif target_language_string == "hebrew":
                    target_text = soup.find_all("div", {"class": "trg rtl"})
                else:
                    target_text = soup.find_all("div", {"class": "trg ltr"})
                source_text = soup.find_all("div", {"class": "src ltr"})

                for target, source in zip(target_text, source_text):
                    translation_list.append(target.find("em").text)  # collects first translation of text element
                    example_text.append(target.find("span", {"class": "text"}).text)
                    example_text.append(source.find("span", {"class": "text"}).text)

                if len(translation_list):
                    first_translation_word = soup.find_all('a', {"class": 'translation'})
                    translation_list = [translation.get_text().strip().lower() for translation in
                                        first_translation_word]
                    first_translation = translation_list[0]
                    print(first_translation)
                    file.write(first_translation + "\n")
                    print()
                    file.write("\n")

                    print(target_language_string.capitalize() + " Example:")
                    file.write(target_language_string.capitalize() + " Example:" + "\n")
                    print(example_text[0].strip())
                    file.write(example_text[0].strip() + "\n")
                    print(example_text[1].strip())
                    file.write(example_text[1].strip() + "\n")
                    print()
                    file.write("\n")
                else:
                    print("Sorry, unable to find {}".format(word_to_translate))
                    file.write("Sorry, unable to find {}".format(word_to_translate) + "\n")

            else:
                print("Something wrong with your internet connection")
