##
## Store the corrected Text
##

from colorama import Fore, Style, init 
import re
from category import catTypes, CategoryItem, CategoryType

## init colorama
init(autoreset=True)

##
##
##----------------------------
class CorrectedText(object):
    
    # Constructor method: initializes the object
    def __init__(self, text):
        self.ctext  = text 
        self.cItems = []                # lista de categoryItems

        ## return a text with color marks
    def get_colored_text(self):
        
        text = self.ctext        
    
        # esto deberia ser via el categories dict
        
        # Replace text enclosed by [] with green color
        text = re.sub(r'\[(.*?)\]', lambda m: f"{Fore.GREEN}{m.group(1)}{Style.RESET_ALL}", text)
        
        # Replace text enclosed by {} with red color
        text = re.sub(r'\{(.*?)\}', lambda m: f"{Fore.RED}{m.group(1)}{Style.RESET_ALL}", text)
        
        # Replace text enclosed by () with Yellow color
        text = re.sub(r'\((.*?)\)', lambda m: f"{Fore.YELLOW}{m.group(1)}{Style.RESET_ALL}", text)
        
        # Replace text enclosed by <> with blue color
        text = re.sub(r'\<(.*?)\>', lambda m: f"{Fore.BLUE}{m.group(1)}{Style.RESET_ALL}", text)
                
        return text
        
    ## print colored text using colorama
    def show(self):
        print(self.get_colored_text())
        print("----------------")
        for result in self.cItems:
            print(f"Category: {result.cType}, Text: {result.text}")

        print("----------------")

        print(self.getTotalStr(True))


    def getTotalStr(self, withTitles=False):

        category_counts = {}

        # Iterate through the list and count items by category
        for item in self.cItems:
            if item.cType in category_counts:
                category_counts[item.cType] += 1
            else:
                category_counts[item.cType] = 1

        cout = ""
        for category, count in category_counts.items():
            if withTitles:
                cout += f"Category {category}: {count} items\t"
            else:    
                cout += f"{category}: {count} \t"

        return cout    


    ## actualiza la lista de categories
    def update(self):
        # Iterating over keys and values
        self.cItems = []

        # Iterate over the category types
        for sigla, category in catTypes.items():
            separator = category.sep
        
            # Escape the separators for regex if necessary
            open_sep = re.escape(separator[0])
            close_sep = re.escape(separator[1])
        
            # Regular expression to find text inside separators
            pattern = re.compile(f'{open_sep}(.*?){close_sep}')
        
            # Find all matches for the current category
            matches = pattern.findall(self.ctext)
        
            for match in matches:
                self.cItems.append( CategoryItem(sigla, match) )
                    
                #    {
                #    'category': category.name,
                #    'sigla': sigla,
                #    'extracted_text': match
                #})

        
        return self.cItems





