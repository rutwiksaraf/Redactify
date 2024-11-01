# README.md

## AUTHOR: RUTWIK SARAF

### INTRODUCTION

This project is a Python application designed to redact sensitive information (such as names, dates, addresses, phone numbers, and conceptual terms) from text files. Using various NLP techniques via the spaCy library, the application identifies specific entity types within text and obfuscates them accordingly.

### FUNCTION OVERVIEW

1. **READINGINPUT(FILE_TYPE)**: 
The readingInput function processes multiple files that match a specified pattern (like *.txt) from the directory, storing their content in a dictionary. It starts by calling glob.glob(file_type), which searches for files that match the given file_type pattern (e.g., all .txt files), returning a list of file names that match. The function then initializes an empty dictionary called content, which will hold each file's content under its file name as a key-value pair. For each file found, it opens the file in read mode ('r') with UTF-8 encoding, which ensures consistent handling of text across various languages and special characters. Using a context manager (with open(...) as f:), it reads the entire content of each file and stores this content in the content dictionary with the file name as the key. After processing all files, the function returns the content dictionary, which holds all file data organized by file name. This design makes it easy to collect, store, and access textual data from multiple sources at once, which is ideal for applications requiring batch processing of text files or organized preprocessing for larger textual datasets.

2. **REDACT_NAMES(TEXT, DOC, STATS)**: 
The redact_names function takes three inputs: a text string (text), a processed spaCy document (doc), and a statistics dictionary (stats). It uses a list representation of the original text (redacted_text) to easily manipulate specific character positions while redacting. The function loops through all named entities in the document, identified by the spaCy NLP model. When an entity with a label of "PERSON" (indicating a name) is detected, the function calculates its start and end character positions within the text using entity.start_char and entity.end_char. It then replaces characters between these positions with block characters (█), redacting the name while preserving the length of the original text for accuracy. As each name is redacted, the function increments the names count in the stats dictionary and appends a tuple with the original entity text, start position, end position, and entity label to track redacted data for later reference. Finally, the function returns the redacted text as a string by joining the modified list back into a single string.

3. **REDACT_DATES(TEXT, DOC, STATS)**: the redact_dates function takes in a text string (text), a spacy document object (doc), and a statistics dictionary (stats). it starts by creating a spacy matcher object to identify date patterns in the text. three patterns are specified in the date_patterns list: (1) dates with a day number followed by a month and year, (2) dates beginning with a month, followed by a day number and year, and (3) dates in mm/dd/yyyy format. each pattern uses regular expressions to match numeric day values or slash-delimited formats and includes month names to capture date structure. the matcher.add function associates these patterns with a unique date label, which then scans the text for all matches.

 - The matches are stored in matches, and redacted_text holds the original text as a list for easy character-by-character modification. For each match, the function identifies the start and end character positions, then replaces characters in that range with block characters (█), effectively redacting the date. Each redacted date updates the dates count in stats, and the entity text, start position, end position, and entity label are appended to stats["entities"]. Finally, the function returns the redacted text as a string, joining the modified list back into a single text output.

4. **REDACT_ADDRESSES(TEXT, DOC, STATS)**: The redact_addresses function is designed to find and redact address-related information in a given text. It takes three parameters: The text string (text), a spacy document object (doc), and a statistics dictionary (stats). The function begins by converting the input text into a list, stored in redacted_text, to allow character-level modifications. It then loops through each entity in doc.ents (extracted entities from the spacy document) to check if the entity's label is one of the geographical-related tags: "Gpe" (geo-political entities such as cities or countries), "loc" (generic locations), or "fac" (facilities). 

 - When an entity matches one of these labels, the function determines its start and end positions within the text, then replaces the characters in that range with block characters (█), effectively redacting the sensitive information. After each redaction, the function increments the count of redacted addresses in stats["addresses"] and records the redacted entity's text, start and end character positions, and entity label in stats["entities"] for further tracking or analysis. Once all applicable addresses have been redacted, the function returns the result as a single string by joining the modified redacted_text list back together.

5. **REDACT_PHONENUMBERS(TEXT, STATS)**: The redact_phonenumbers function is designed to detect and censor phone numbers in a given text to preserve privacy. It takes two arguments: A text string (text) and a statistics dictionary (stats). To identify phone numbers, it utilizes a regular expression pattern (phone_pattern) specifically designed to match common u.s. Phone number formats: Sequences of three digits followed by three more digits, and then four final digits, allowing for flexible separators like dashes, spaces, or periods.

 - The function converts text into a list stored in censored_text, facilitating in-place character modifications. It then uses python's re.finditer() to iterate over all phone number matches found in the text. For each match, the function determines the start and end character positions and replaces the characters in that range with block characters (█), ensuring that the phone number is fully obfuscated. In each case, it increments the count of redacted phone numbers in stats["phones"] and records the redacted information, including the matched text, its start and end positions, and its label ("phone"), in stats["entities"]. Finally, the function returns the modified text as a string by joining the censored_text list back together.

6. **REDACT_CONCEPTS(TEXT, DOC, CONCEPTS, STATS)**: The redact_concepts function redacts specific thematic concepts in a text, using spacy to identify and censor entire sentences containing these concepts. It takes four parameters: Text (the input text to be processed), doc (a spacy document object of the text), concepts (a list of targeted concepts for redaction), and stats (a dictionary for tracking redacted entities). 

 - The function first converts text into a list (redacted_text) to allow character-by-character redaction. Then, it creates a phrasematcher object named matcher, which is used to identify sentences containing any of the specified concepts. The concepts are converted to patterns using spacy, ensuring that the matching process will be semantically accurate. These patterns are added to the matcher under the label "concepts". 

 - The function then iterates over each sentence in doc, using the matcher to identify any matches for the targeted concepts within the sentence text. If a match is found, the entire sentence is redacted by replacing all characters between the sentence's start and end positions with block characters (█), preserving the length but fully obscuring content. For each redacted sentence, the function updates the stats dictionary by appending a tuple to stats["entities"], which includes the original sentence text, its start and end positions, and the label "concept". Finally, it returns the fully redacted text as a string.

7. **CONDITIONAL_REDACT(CONTENT, FLAGS, STATS, CONCEPTS)**: The conditional_redact function performs conditional redaction of sensitive information in a given text based on specified flags and concepts. It takes four parameters: Content (the text to be processed), flags (a dictionary indicating which types of information should be redacted), stats (a dictionary for tracking redacted entities), and concepts (a list of specific thematic concepts to redact). 

 - First, the function processes the input content through a spacy language model (nlp) to create a document object (doc). It initializes redacted_content as a copy of the original text to allow for conditional modifications. Then, it checks each flag in the flags dictionary: 

 - If the "names" flag is set to true, it calls the redact_names function, passing the current redacted_content, doc, and stats to censor names. 
 - Similarly, if the "dates," "addresses," or "phones" flags are enabled, it calls the respective functions (redact_dates, redact_addresses, redact_phone_numbers) to censor those types of information. 
If the concepts list is not empty, it calls the redact_concepts function to censor sentences containing the specified concepts. 
After executing these conditional redactions, the function returns the final redacted_content, which is the original text with all specified sensitive information obscured, allowing for secure handling of the content.

8. **SAVE_REDACTED(FILE_NAME, CONTENT, OUTPUT_DIR)**: The save_redacted function is designed to save redacted content to a new file in a specified output directory. It accepts three parameters: File_name, which is the name of the original file containing the content; Content, which is the redacted text to be saved; And output_dir, which is the directory where the new file will be stored. 

 - First, the function creates a new file name by combining the output_dir with the base name of file_name, appending the suffix .censored to indicate that this file contains redacted content. This is achieved using os.path.join, which properly forms the file path for the new file. 

 - Next, the function opens this new file in write mode with utf-8 encoding, ensuring that any special characters in the redacted content are handled correctly. Within the context of this opened file, the function writes the content to the file. Finally, once the writing is completed, the file is automatically closed, and the function executes successfully, creating a persistent copy of the redacted text in the designated output directory.

9. **WRITE_STATS(FILE_NAME, STATS, OUTPUT)**: The write_stats function is responsible for recording and outputting redaction statistics for a specified file. It accepts three parameters: File_name, which is the name of the file being processed; Stats, a dictionary containing redaction counts for names, dates, addresses, phone numbers, and concept sentences; And output, which specifies where to write the statistics—either to a file, standard error (stderr), or standard output (stdout). 

 - Within the function, a string stats_output is constructed that includes the file name and a summary of censor statistics, detailing the total number of each type of entity redacted. It also includes a detailed list of censored items, formatted as a tuple containing the text, start position, end position, and type for each entity in the stats['entities'] list. 

 - Depending on the value of the output parameter, the function either prints this string to stderr, prints it to stdout, or writes it to a specified file. When writing to a file, it opens the file in write mode with utf-8 encoding to ensure proper handling of characters. This function effectively provides a clear and organized report of redaction activity for each file processed.

10. **MAIN()**: The main function serves as the entry point for a script designed to redact sensitive information from text files. It initially sets up argument parsing using the argparse library to handle command-line input. The function defines several required and optional arguments, including --input for specifying the file pattern to read, booleans for redacting names, dates, addresses, and phone numbers, and a repeated --concept argument to allow multiple concepts to be specified. It also includes --output to define the directory for saving censored files and --stats to determine where to write the statistics. 

 - After parsing the arguments, the function checks if the output directory exists; If not, it creates it. It then loads all input files matching the pattern by calling the readinginput function. A flags dictionary is constructed to track which types of sensitive information need to be redacted, and a concepts list is created based on user input. 

 - For each file, it initializes a statistics dictionary to count redactions. The conditional_redact function is then called to process the content, followed by saving the redacted file using save_redacted. Finally, it writes the redaction statistics to the specified output using the write_stats function, ensuring a complete and organized redaction process for each file processed.

### Approach

### Detailed explanation of the approach

#### 1. **Importing required libraries**
   - The code imports several libraries, including `argparse` for command-line argument parsing, `glob` for file pattern matching, `spacy` for natural language processing, `re` for regular expression matching, and `os` and `sys` for file and system operations. 

#### 2. **Initializing the spacy model**
   - The code loads a pretrained spacy language model (`en_core_web_lg`), which is used for named entity recognition (ner) and other text processing tasks. 

#### 3. **Reading input files**
   - The function `readinginput(file_type)` is defined to read all text files that match a given pattern. It uses `glob` to find files and reads their content into a dictionary (`content`) where the keys are file names and the values are the file contents. 

#### 4. **Redacting named entities**
   - The function `redact_names(text, doc, stats)` processes the text to redact named entities identified as "person" by spacy. It iterates over the named entities and replaces the text with a block character (█), updating the `stats` dictionary to count the redactions. 

#### 5. **Redacting dates**
   - The function `redact_dates(text, doc, stats)` uses spacy's `matcher` to find and redact dates based on regular expressions that define date formats. It replaces matched dates with block characters and updates the `stats` dictionary. 

#### 6. **Redacting addresses**
   - The function `redact_addresses(text, doc, stats)` identifies and redacts address-related entities (labels such as "gpe," "loc," and "fac") using spacy. Like the other redaction functions, it replaces the text with block characters and updates stats. 

#### 7. **Redacting phone numbers**
   - The function `redact_phonenumbers(text, stats)` uses a regular expression to identify and redact phone numbers in the text. It replaces matched phone numbers with block characters and updates the `stats`. 

#### 8. **Redacting concepts**
   - The function `redact_concepts(text, doc, concepts, stats)` uses spacy's `phrasematcher` to identify and redact sentences containing specified concepts. It converts concepts to spacy patterns and redacts whole sentences where a match is found. 

   ![Alt text](docs/concept_burrito.png)

#### 9. **Conditional redaction**
   - The function `conditional_redact(content, flags, stats, concepts)` calls the relevant redaction functions based on user flags. It takes the input text and flags to determine which types of sensitive information to redact and returns the redacted content. 

#### 10. **Saving redacted content**
   - The function `save_redacted(file_name, content, output_dir)` creates a new file in the specified output directory, appending `.censored` to the original file name and writing the redacted content into this file. 


#### 11. **Writing redaction statistics**
   - The function `write_stats(file_name, stats, output)` formats and writes redaction statistics to the specified output (either a file, `stderr`, or `stdout`). It displays total counts for each type of redaction and detailed entries of censored items. 

   ![Alt text](docs/stats.png)

   ![Alt text](docs/stderr.png)

   ![Alt text](docs/stdout.png)

#### 12. **Main function**
   - The `main()` function handles command-line arguments, sets up the output directory, and coordinates the overall redaction process. It calls the reading function to load input files, initializes statistics, calls `conditional_redact` for each file, saves redacted files, and writes statistics. 

#### 13. **Program entry point**
   - The code checks if the script is run directly and calls the `main()` function, starting the redaction process. 

This structured approach ensures a modular, clear, and effective method for redacting sensitive information from text files, allowing for flexibility and extensibility as needed. 


#### Whitespace redaction discussion

The application censors both words and the whitespace between phrases to ensure sensitive terms are fully obfuscated. For concepts like names, redacting whitespace (e.g., between a first and last name) increases privacy by reducing the chance of reconstructing the original text through remaining structure. 

#### Parameters for flags

Each redaction type has a corresponding flag to specify which entity type(s) should be censored. Parameters include: 
- **--Names**: Redacts detected names. 
- **--Dates**: Redacts dates in standard formats. 
- **--Addresses**: Redacts locational information. 
- **--Phones**: Redacts phone numbers in typical u.s. Formats. 
- **--Concept [word/phrase]**: Redacts sentences containing the specified word or phrase, along with related terms. Custom terms can be added to the concept list to expand detection scope. 

#### Concept definition and justification

For this project, a **concept** is defined as any idea or theme represented by keywords or phrases related to it. For example, the concept "prison" includes related terms like "jail" or "incarcerated." when a sentence contains a specified concept, the entire sentence is redacted to maintain context and protect sensitive themes. 

- **Context creation**: The program uses spacy’s phrase matcher to identify key phrases linked to each concept, searching for semantic links to the main idea. This approach ensures consistency in redaction by addressing nuanced word usage that may imply sensitive content. 

- **Justification**: Redacting whole sentences with concept-related terms ensures that sensitive topics are fully obscured, reducing the risk of inadvertent information exposure. 



### Required installation commands

- Install spacy: `Pip Install Spacy`
- Install the spacy model: `Python -M Spacy Download EN_CORE_WEB_LG`

### How to run the code

To execute the program and redact sensitive information, run the following command: 

`Python Main.Py --Input "*.Txt" --Names --Dates --Addresses --Phones --Concept "Confidential" --Output "./Censored_Files" --Stats "Stdout"`

### Test case explanations

#### Address test case
The `test_redact_addresses()` function tests the functionality of `redact_addresses()` to verify it correctly identifies and redacts locational information. 
- **Input**: "I live in new york."
- **Expected output**: "I live in ████████."
- **Test checks**: The function checks that the address entity 'new york' is replaced with block characters and that the address count in `stats` is updated to 1. It also ensures that 'new york' is logged correctly as a "gpe" entity in `stats`. 

#### Concept test case
The `test_redact_concepts()` function examines the ability of `redact_concepts()` to identify and redact conceptual terms from text. 
- **Input**: "Artificial intelligence is evolving rapidly."
- **Expected output**: "████████████████████████████████████████████"
- **Test checks**: The function verifies that the term "artificial intelligence" is completely redacted and the entity count for concepts is updated accurately in `stats`. It also confirms that "artificial intelligence" is stored with the entity type "concept". 

#### Date test case
The `test_redact_dates()` function tests `redact_dates()` for accurate redaction of date formats. 
- **Input**: "The event is scheduled on 5th october 2023."
- **Expected output**: "The event is scheduled on ████████████████."
- **Test checks**: It checks that the date "5th october 2023" is successfully replaced with block characters. It also confirms that the date count in `stats` is updated to 1 and the entity log includes the term as "date". 

#### Name test case
The `test_redact_names()` function validates that `redact_names()` properly identifies and redacts person names in text. 
- **Input**: "John went to the store."
- **Expected output**: "████ Went to the store."
- **Test checks**: The function ensures that the name "john" is replaced with block characters. It checks that `stats['names']` is incremented by 1 and the name entity is recorded as "person" in `stats`. 

### Phone test case
The `test_redact_phones()` function tests the `redact_phonenumbers()` function to determine whether phone numbers are identified and redacted correctly. 
- **Input**: "My phone number is 123-456-7890."
- **Expected output**: "My phone number is ████████████."
- **Test checks**: The function confirms that the phone number "123-456-7890" is fully redacted. It also checks that `stats['phones']` is incremented to 1 and that the entity is logged as "phone" with its position and entity type in `stats`. 

![Alt text](docs/Testcase_passed.png)

### Assumptions

1. Input files follow consistent formatting to maintain structure after redaction. 
2. Redaction is based solely on entity detection from the spacy model (en_core_web_md). 
3. Phone numbers follow typical u.s. Formats (e.g., "123-456-7890"). 
4. Dates use common english-language date formats. 

### Known bugs and issues
1. If file formats vary widely or include unexpected entity types, redaction may not be fully accurate. 
2. Text formatting may be disrupted in the final output, especially when multiple entity types are redacted close together. 
3. Matching conceptual terms is case-sensitive and dependent on the accuracy of phrase matching. 


