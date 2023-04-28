import requests, signal, sys, optparse, re, os 
import threading
import pyfiglet
import mmap
from pyfiglet import Figlet
from termcolor import colored
from colorama import init
from colorama import Fore, Back, Style
init()
#Colors Variables
Green = Fore.GREEN
Red = Fore.RED
Normal = Fore.RESET
Yellow = Fore.YELLOW 
Blue = Fore.BLUE
Magenta = Fore.MAGENTA
BRed = Back.RED
BNormal = Back.RESET
Cyan = Fore.CYAN
White = Fore.WHITE

#Functions of the program
def exiting(sig, frame):
    print(f"\n\n {Yellow}Exiting of the program...{Normal}\n")
    sys.exit(1)

signal.signal(signal.SIGINT, exiting)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest= 'url_address', help= 'The url address of the target')
    parser.add_option('-w', '--wordlist', dest= 'wordlist_file', help= 'The wordlist with the data')
    parser.add_option('-e', '--extension', dest='extenfion_file', help='Add a file extension')
    parser.add_option('', '--fs', dest='size_filter', help='Filter size')
    parser.add_option('', '--fw', dest='words_filter', help='Filter words')
    parser.add_option("-t", "--threads", dest="num_threads", help="Enter the number of threads (Default 10)", default=10, type=int)
    (options, arguments) = parser.parse_args()
    if not options.url_address:
        parser.error("[-] Please indicate the target url, for more information... --help")
    if not options.wordlist_file:
        parser.error("[-] Please indicate the wordlist, for more information... --help")
    return options

def colorst(first_sc):
    if first_sc == '2':
        ColorST = Green
        return ColorST
    elif first_sc == '3':
        ColorST = Yellow
        return ColorST
    elif first_sc == '4':
        ColorST = Red
        return ColorST
    else:
        ColorST = White
        return ColorST


def information_sort(status_code, size, words_text, url_final):
     first_sc = str(status_code)[0]
     ColorST = colorst(first_sc)
     print(f"[" + f"{Magenta}Estatus Code:{Normal} {ColorST}{status_code}{Normal}           " + f"{Magenta}Size: {Normal}{Yellow}{size}{Normal}           " + f"{Magenta}Words:{Normal} {Yellow}{words_text}{Normal}]")
     print(f'\t{Blue}*{url_final}{Normal}\n')
    
def makeRequest(url, wordlist, thread_num, total_threads):
     archivo = open(wordlist)
     lines = archivo.readlines()
     for i in range(thread_num-1, len(lines), total_threads):
        if url[-1] != '/':
            url += '/'
        line = lines[i].strip()
        url_final = url + line
        url_final = url_final.strip()
        r = requests.get(url_final)
        words_text = len(re.findall(r'\w+', r.text))
        size = len(r.content)
        status_code = r.status_code
        if r.status_code != 404:
            information_sort(status_code, size, words_text, url_final)
     archivo.close()

def do_threads(url, wordlist, num_threads):
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=makeRequest, args=(url, wordlist, i+1, num_threads))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()
    print(Blue + "Author:FredBrave/FredBrav" + Normal)
#def main():
    
if __name__ == '__main__':
     options = get_arguments()
     banner = "BraveFuzz"
     f = Figlet(font='slant')
     print(colored(f.renderText('BraveFuzz'), 'green'))
     url = options.url_address
     wordlist = options.wordlist_file
     threads = options.num_threads
     do_threads(url, wordlist, threads)
