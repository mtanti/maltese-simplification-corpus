# Maltese Simplification Corpus

A document-level parallel corpus of simple and complex Maltese texts.

Version: 0.2

## What's this?

A number of websites of governmental and non-governmental Maltese organisations publish documents in a writing style called 'easy to read', which is meant to be accessible for children and people with particular special needs.
These are sometimes included as 'translations' of other official publications that are deemed important for said target audience.

This project is a collection of plain texts extracted from these documents with the aim of creating an opportunity to study the differences between easy-to-read text and non-simplified text.
It is useful for tasks such as automatic text simplification for the Maltese language, although the size and domain variability of the corpus is extremely limited at the moment.

## How was it made?

Easy-to-read versions of soft copy documents (primarily PDFs, but not only) in Maltese were manually searched for and downloaded together with their non-simple counterpart, if any.
We call the easy-to-read version the simple document and the non-simple version the complex document.
These documents were collected into the folder `raw_docs` and information about their source, date of download, and so on was logged into a JSON file (see Corpus format section for more information).

The pages from these documents were extracted as separate images into the folder `interm_pages` using the script `scripts/docs2pages.py`.
The application [labelImg](https://github.com/heartexlabs/labelImg) was used to manually draw bounding boxes around fragments of texts in the page images that should be extracted.
This was done to avoid undesirable text from being extracted such as page numbers and text that is not in Maltese, as well as to properly handle multi-column pages.
The following internal annotation rules were used to draw bounding boxes:

- Ignore magin notes such as foot notes, headers, footers, and page numbers.
- Ignore tables.
- Ignore tables of contents.
- Ignore words in pictures.
- Ignore repetitions of the title page (the second page is sometimes the first page in greyscale).
- Ignore paragraphs in the simple document that refer to the complex document by name (since the title of the complex document might not be in easy-to-read style).
- Ignore text that is not meant to be read by the target audience of the simple document such as the acknowledgements page.
- A paragraph on the same page cannot be split into multiple bounding boxes, but separate paragraphs can be.

Bounding boxes were saved in [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/) format XML files in the folder `interm_pages` together with the page images.
Some bounding boxes are used to replace an image region with a white box in order to remove something distracting from the page (named 'whiteout') whilst other bounding boxes are used to extract the text inside them (named 'text').

labelImg saves the full path to the image in the XML file, which is not necessary, so this is removed by using the script `scripts/remove_img_path_annos.py`.

Finally, the image regions described by the bounding boxes are OCRed using [Tesseract](https://tesseract-ocr.github.io/tessdoc/Home.html) using the script `scripts/pages2frags.py` with the Maltese pre-trained model ('mlt').
The reason for using an OCR instead of extracting text from the PDF directly is because some PDFs were written using special fonts to show unusual characters as Maltese diacritics (e.g. '˙' gets mapped to the Maltese letter 'ħ').
This, together with the method's inability to extract text from selected bounding boxes, makes direct text extraction less desirable than OCR.

The OCRed text is saved in the folder `interm_frags` which has a separate file for each 'text' bounding box with the file names being `<page#>_<box#>.txt`.
These allow for manual inspection and correction of the OCRed text (to be done in a future version).
These fragmented text files for each document are then concatenated together into a single document text file in the folder `corpus` using the script `scripts/frags2corpus.py`.

## Corpus format

The final corpus is available in the `corpus` folder.
The first set of folders in there is the domain of the website where the documents were downloaded from, for example `corpus/crpd.org.mt`.
In each of these domain folders is a document identifier folder which gives the name of the document from which text was extracted, for example `corpus/crpd.org.mt/Att dwar il-Koabitazzjoni`.
The identifier name is based on the title of the complex document but not exactly and should not be treated as such.
Finally, in this folder, there are one or two text files in UTF-8 character encoding, `simple.txt` for the simple (easy-to-read) version of the document and, if available, `complex.txt` for the complex (non-simple) version of the document.
The text files consist of just a concatenation of all the strings extracted by Tesseract from all the bounding boxes in the documents (with blank lines in between).

Information about the original documents can be found in a JSON file called `info.json`.
There is a different JSON file for each document identifier and these can be found in `raw_docs` by following the same folder path as in the `corpus` folder, for example, `raw_docs/crpd.org.mt/Att dwar il-Koabitazzjoni/info.json`.
The original documents are also in the same folder as the JSON file.
The format of the JSON file is as follows:

```
{
    "page_url": <URL of webpage from where the documents were downloaded>,
    "documents": [ <list of documents which can be simple or complex (complex might not be available)>
        {
            "type": <'complex' or 'simple'>,
            "fname": <file name of the document>,
            "url": <direct URL of the document>,
            "with_diacritics": <whether the document was written as proper Maltese text or text without Maltese diacritics (e.g. using 'h' instead of 'ħ')>,
            "retrieved": <date and time of when the documents were downloaded using ISO 8601 GMT>
        }
    ]
}
```

## Running the scripts

The scripts were written to be used on a Windows operating system.

To run the scripts, you will first need to create the Python Conda virtual environment with all the required Python modules.
The batch script `create_venv.bat` does this for you, provided that Python Conda is available through the command prompt.

Once you have the necessary modules installed, simply run the Python scripts in the `scripts` folder.
The scripts assume that the current directory is the `scripts` folder.
