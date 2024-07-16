import wikipediaapi

def fetch_wikipedia_top_section(topic):
    wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')
    page = wiki_wiki.page(topic)

    if not page.exists():
        print(f"Topic '{topic}' does not exist on Wikipedia.")
        return None

    # Get the "Top" section, typically the summary before any sections
    top_section = page.summary
    return top_section

def append_to_file(file_path, content):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content + '\n\n')

def main():
    topic = input("Enter the Wikipedia topic: ")
    top_section = fetch_wikipedia_top_section(topic)
    
    if top_section:
        append_to_file('wikipedia_top_sections.txt', f"Topic: {topic}\n{top_section}")
        print(f"Added top section of '{topic}' to wikipedia_top_sections.txt")

if __name__ == '__main__':
    main()