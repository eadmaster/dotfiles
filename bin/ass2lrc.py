#!/usr/bin/env python
# -*- coding: utf-8 -*-

# derived from https://github.com/SamLangTen/ASS2LRC

import sys
import datetime
import re
import time


class ass_dialogue_word(object):
    """Represents a word with k-tag in ASS dialogue
    
    Attributes:
        word: A string of the word with k-tag.
        start_time: A datetime instance to represent start time of the word.
    """

    def __init__(self, word, start_time):
        """Init ass_dialogue_word"""
        self.word = word
        self.start_time = start_time


class ass_dialogue(object):
    """Represents an ASS dialogue

    Attributes:
        start_time: A datetime instance to represent start time of ASS dialogue.
        end_time: A datetime instance to represent end time of ASS dialogue.
        style: A string to represent style of ASS dialogue, usually to define different dialogues.
        text: A string if dialogue does not contain k-tag, or a list of ass_dialogue_word instances if dialogue contains k-tag.
    """

    def __init__(self, start_time, end_time, style, text):
        """Init ass_dialogue"""
        self.start_time = start_time
        self.end_time = end_time
        self.style = style
        self.text = text

    def __lt__(self, other):
        if self.start_time < other.start_time:
            return True
        return False

    @staticmethod
    def load_lrc(files):
        """Load and parse ASS file

        Load and parse ASS file. Not all the information and dialogue option will be parsed. This function only parse dialogue with its style, start time, end time and text. Any effect tag except K-tag will be removed.

        Args:
            filename: An opened ASS filename that will be loaded.

        Returns:
            A list of ass_dialogue instances.
        """
        dialogues = list()
        #files = open(filename, "r")
        for line in files:
            if line.startswith("Dialogue:"):
                phrased = line.split(",")
                start_time = datetime.datetime(1, 1, 1, int(phrased[1].split(":")[0]), int(phrased[1].split(":")[1]), int(
                    phrased[1].split(":")[2].split(".")[0]), int(phrased[1].split(":")[2].split(".")[1])*10000)
                end_time = datetime.datetime(1, 1, 1, int(phrased[2].split(":")[0]), int(phrased[2].split(":")[1]), int(
                    phrased[2].split(":")[2].split(".")[0]), int(phrased[2].split(":")[2].split(".")[1])*10000)
                style = phrased[3]
                words = list()
                # extract effect code: (\{[^{]*\}){0,1}[^{]*
                no_k_text = ""
                last_text = ""
                last_text = last_text.join(phrased[9:])
                last_time = start_time
                while True:
                    first_re = re.match(r"(\{[^{]*\}){0,1}[^{]*", last_text)
                    if first_re is None or first_re.group() == "":
                        break
                    re_start_index = last_text.find(first_re.group())
                    re_end_index = last_text.find(
                        first_re.group()) + len(first_re.group())
                    last_text = last_text[:re_start_index] + \
                        last_text[re_end_index:]
                    item = first_re.group()
                    # get K
                    ec_match = re.match(r"\{\\[K|k]\d*\}", item)
                    if (ec_match is not None):
                        word = ass_dialogue_word(item.replace(
                            re.match(r"\{\\[K|k]\d*\}", item).group(), ""), last_time)
                        last_time = last_time + datetime.timedelta(milliseconds=int(
                            ec_match.group().lower().replace("{\k", "").replace("}", "")) * 10)
                        if not word.word == "":
                            words.append(word)
                    else:
                        # clear effect code
                        ec2_match = re.match(r"\{[^\{|\}]*\}", item)
                        if ec2_match is not None:
                            no_k_text += item.replace(ec2_match.group(), "")
                        else:
                            no_k_text += item
                # if no effect code
                if len(words) == 0:
                    words = no_k_text.strip()
                dialogue = ass_dialogue(start_time, end_time, style, words)
                dialogues.append(dialogue)
        files.close()
        return dialogues


def __generate_lrc_timestamp(dt, format_str="[mm:ss.xx]"):
    m_digits = str(dt.minute).zfill(format_str.count("m"))
    s_digits = str(dt.second).zfill(format_str.count("s"))
    x_digits = str(int(dt.microsecond / 10000)).zfill(format_str.count("x"))
    # TODO(samlangten): check re return if nonetype
    m_group = re.search("m+", format_str)
    if m_group is not None:
        format_str = format_str.replace(m_group.group(), m_digits)
    s_group = re.search("s+", format_str)
    if s_group is not None:
        format_str = format_str.replace(s_group.group(), s_digits)
    x_group = re.search("x+", format_str)
    if x_group is not None:
        format_str = format_str.replace(x_group.group(), x_digits)
    return format_str


def __convert_ass_effect_word_to_text(text):
    if isinstance(text, list):
        text2 = ""
        for item2 in text:
            text2 += item2.word
        return text2
    else:
        return text


def ass_styles_filter(dialogues, styles):
    """Select specified styles in ASS dialogues
    
    Args:
        dialogues: A list of ass_dialogues instance.
        styles: A list of strings to indicate the dialogues with which styles will be kepts

    Returns:
        A list of ass_dialogues instances with style in styles
    """
    new_dialogues = list()
    for style_item in dialogues:
        if style_item.style in styles:
            new_dialogues.append(style_item)
    return new_dialogues


def convert_to_accurate_lrc(dialogues, space_end_timespan_ms, outter_char="[mm:ss.xx]"):
    """ Convert K-tag ASS dialogues to accurate LRC lyrics
    
    Convert Karaoke-tag of ASS file to accurate word-by-word timestamp.
    Notice that accurate timestamp is not supported by all players.

    Args:
        dialogues: A list of ass_dialogue instances.
        space_end_timespan_ms: A integer to indicate how long between two dialogues will blankline be added.
    
    Returns:
        A string contains converted LRC format text.
    """
    generated_text = ""
    dialogues.sort()
    for index, item in enumerate(dialogues):
        lryic = __generate_lrc_timestamp(item.start_time)
        if isinstance(item.text, list):
            text = ""
            for item2 in item.text:
                text += __generate_lrc_timestamp(item2.start_time,
                                                 outter_char) + item2.word
            lryic += text
        else:
            lryic += item.text
        generated_text += lryic + "\n"
        # append ending
        if not index == len(dialogues) - 1:
            td = dialogues[index + 1].start_time - item.end_time
            if td.total_seconds() * 1000 > space_end_timespan_ms:
                lryic = __generate_lrc_timestamp(item.end_time)
                generated_text += lryic + "\n"
        else:
            lryic = __generate_lrc_timestamp(item.end_time)
            generated_text += lryic + "\n"
    return generated_text


def convert_to_compact_lrc(dialogues, space_end_timespan_ms):
    """ Convert ASS dialogues to LRC lyrics with compact mode.

    Convert ASS dialogues to compacted LRC lyrics. Every two dialogues with text will share the same timestamp.
    Notice that compacted timestamp is not supported by all players.

    Args:
        dialogues: A list of ass_dialogue instances.
        space_end_timespan_ms: A integer to indicate how long between two dialogues will blankline be added.

    Returns:
        A string contains converted LRC format text.
    """
    generated_text = ""
    dialogues.sort()
    blanks_dialogues = list()
    # Add blank line
    for index, item in enumerate(dialogues):
        if not index == len(dialogues) - 1:
            td = dialogues[index + 1].start_time - item.end_time
            if td.total_seconds() * 1000 > space_end_timespan_ms:
                lryic = __generate_lrc_timestamp(item.end_time)
                blanks_dialogues.append(lryic)
        else:
            lryic = __generate_lrc_timestamp(item.end_time)
            blanks_dialogues.append(lryic)
    # Generate
    i = 0
    while len(dialogues) > 0:
        this_line_generated_text = __generate_lrc_timestamp(
            dialogues[i].start_time)
        j = i + 1
        this_line_text = __convert_ass_effect_word_to_text(dialogues[i].text)
        while j < len(dialogues):
            if __convert_ass_effect_word_to_text(dialogues[j].text) == this_line_text:
                this_line_generated_text += __generate_lrc_timestamp(
                    dialogues[j].start_time)
                dialogues.pop(j)
            else:
                j += 1
        this_line_generated_text += this_line_text + "\n"
        generated_text += this_line_generated_text
        dialogues.pop(i)
    generated_text += "".join(blanks_dialogues) + " \n"
    return generated_text


def convert_to_normal_lrc(dialogues, space_end_timespan_ms):
    """ Convert ASS dialogues to LRC lyrics.

    Args:
        dialogues: A list of ass_dialogue instances.
        space_end_timespan_ms: A integer to indicate how long between two dialogues will blankline be added.

    Returns:
        A string contains converted LRC format text.
    """
    generated_text = ""
    dialogues.sort()
    for index, item in enumerate(dialogues):
        lryic = __generate_lrc_timestamp(item.start_time)
        if isinstance(item.text, list):
            text = ""
            for item2 in item.text:
                text += item2.word
            lryic += text
        else:
            lryic += item.text
        if lryic:  # TODO: avoid multiple lines https://github.com/SamLangTen/ASS2LRC/issues/2
            generated_text += lryic + "\n"
        # append ending
        if not index == len(dialogues) - 1:
            td = dialogues[index + 1].start_time - item.end_time
            if td.total_seconds() * 1000 > space_end_timespan_ms:
                lryic = __generate_lrc_timestamp(item.end_time)
                generated_text += lryic + "\n"
        else:
            lryic = __generate_lrc_timestamp(item.end_time)
            generated_text += lryic + "\n"
    return generated_text



import getopt


def display_usage(name):
    print("usage: python " + name +
          " [--help] -i <inputfile> -o <outputfile> [-t mileseconds] [-s stylename] [-c|-a] [-f [mm:ss.xx]]")
    print("")
    print("-i --input\tAn ASS filename which will be converted to lrc")
    print("-o --output\tA LRC filename where the convered text will be stored")
    print("-t --split_timespan\tA new blank line will be added if the start time of two between dialogues greater than this argument, default is 1000ms")
    print("-s --convert_styles\tA filter to decide which style of dialogue in ASS should be converted into LRC file")
    print("-c --compact\tCombine timestamp of dialogues with same text, not supported by all players. Not compatible with accurate option")
    print("-a --accurate\tConvert Karaoke-tag of ASS file to accurate word-by-word timestamp, not supported by all players. Not compatible with compact option")
    print("-f --accurate_format\tUsed with accurate option, to set format of accurate word-by-word timestamp since every player may have its own accurate timestamp")

if __name__ == "old__main__":
    inputfilename = ""
    outputfilename = ""
    split_timespan = 1000
    convert_styles = list()
    is_compact = False
    accurate_format = None
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "hi:o:t:s:caf:", [
                                   "help", "input=", "output=", "split_timespan=", "convert_styles=","compact","accurate","accurate_format="])
    except getopt.GetoptError:
        display_usage(sys.argv[0])
        sys.exit(2)
    for opt, arg in opts:
        if (opt in ("-i", "--input")):
            inputfilename = arg
        elif (opt in ("-o", "--output")):
            outputfilename = arg
        elif (opt in ("-t", "--split_timespan")):
            split_timespan = int(arg)
        elif (opt in ("-s", "--convert_styles")):
            convert_styles.extend(arg.split(" "))
        elif (opt in ("-c", "--compact")):
            is_compact = True
        elif (opt in ("-a", "--accurate")):
            if accurate_format is None:
                accurate_format = "[mm:ss.xx]"
        elif (opt in ("-f", "--accurate_format")):
            accurate_format = arg
        elif (opt in ("-h", "--help")):
            display_usage(sys.argv[0])
            sys.exit(2)

    if inputfilename == "":
        display_usage(sys.argv[0])
        sys.exit(2)
    



if __name__ == "__main__":
	import argparse, sys
	parser = argparse.ArgumentParser()
	parser.add_argument('infile', nargs='?', default="-", help="input file, default to stdin if unspecified. Supports passing urls.")
	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file, default to stdout if unspecified")
	args = parser.parse_args()

	if args.infile == "-":
		infile = sys.stdin
		sys.stderr.write("reading from stdin...\n")
	elif args.infile.startswith(("http://", "ftp://", "https://")):  # TODO: proper URL validation
		from urllib.request import urlopen
		infile = urlopen(args.infile)
		# switch to text file mode
		import codecs
		infile = codecs.getreader("utf-8")(infile)
	else:
		infile = open(args.infile)
	
	# convert
	dialogues = ass_dialogue.load_lrc(infile)
	# if convert styles set
	#if len(convert_styles) != 0:
	#    dialogues = ass_styles_filter(dialogues, convert_styles)
	#convert: normal, compact, accurate
	#if is_compact:
	#    output_text = convert_to_compact_lrc(dialogues, split_timespan)
	#elif accurate_format is not None:
	#    output_text = convert_to_accurate_lrc(dialogues, split_timespan, accurate_format)
	#else:
	split_timespan = 1000
	output_text = convert_to_normal_lrc(dialogues, split_timespan)

	args.outfile.write("[by:ASS2LRC]\n\n")  # banner header
	output_text = output_text.replace("\n\n", "\n")
	args.outfile.write(output_text)


    