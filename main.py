# main.py
# Import to run the app
from kivy.app import App
# Import to allow multiple screens in the app
from kivy.uix.screenmanager import ScreenManager, Screen
# Import to allow popups in error handling
from kivy.uix.popup import Popup
from kivy.uix.label import Label
# Import to parse a kv file for graphics
from kivy.lang import Builder
# Import datetime for expiration date tracking
import datetime
from datetime import datetime, timedelta
#import a database
from database import Database

#use a textfile as the database
db = Database("food.txt")

global added_item
added_item = 0
reminder = 0
global space
space = ""

class MainWindow(Screen):
    def update(self):
        global added_item
        global reminder
        global space
        # Format the date today
        today = datetime.now().date().strftime('%Y%m%d')
        # Check the expiration date for each item
        for item in db.items:
            # Format the expiration date of the item
            expiration_date = datetime.strptime(item['Expiration Date'], '%Y%m%d')
            # Calculate when the reminder for the expiration date should be sent
            expiration_reminder = expiration_date - timedelta(days=reminder)
            # Format the calculation
            expiration_reminder = expiration_reminder.date().strftime('%Y%m%d')
            # Notify the user
            if today >= expiration_reminder:
                notify(item['Name'])
        # Update the added item if an item has been added
        if added_item == 1:
            # Format the list
            self.ids.item_column.text = space
            self.ids.category_column.text = space
            self.ids.expiry_column.text = space
            # Add items
            for item in db.items:
                self.ids.item_column.text += item['Name'] + "\n"
            for item in db.items:
                self.ids.category_column.text += item['Category'] + "\n"
            # Format the expiration date in the format of Month, DD YYYY
            for item in db.items:
                expiration_date = datetime.strptime(item['Expiration Date'], '%Y%m%d')
                formatted_expiry = expiration_date.strftime('%B %d, %Y')
                self.ids.expiry_column.text += formatted_expiry + "\n"
            # Reset the added items
            added_item = 0
            space += "\n"

    def newBtn(self):
        manage_screen.current = "New Item"

    def sortBtn(self):
        manage_screen.current = "Sort List"

    def reminderBtn(self):
        manage_screen.current = "Reminders"

    def editBtn(self):
        manage_screen.current = "Edit List"

    def searchBtn(self):
        manage_screen.current = "Search List"


class NewItem(Screen):
    def submit(self):
        # Variable for checking if there is an item being added
        global added_item
        # Variable for checking for a preexisting error
        error = 0
        # Data validation: checks that the inputs are not blank
        if self.item_name.text != "" and self.category.text != "" and self.expiration_date.text != "":
            # Error handling: Ensures that the inputted information is valid
            try:
                # Turning the expiration date text into a YYYYMMDD format
                datetime.strptime(self.expiration_date.text, '%Y%m%d')
            except ValueError:
                # A popup notifying the user of an invalid entry
                invalidEntry()
                # Existing error
                error = 1
                # Stays in this screen to allow the user to re-input the expiration date
                manage_screen.current = "New Item"
            # Error handling: Only runs if no error exists
            if error == 0:
                # Accesses the database to add the item into the list
                db.add_item(self.item_name.text, self.category.text, self.expiration_date.text)
                # Existence of an added item
                added_item = 1
                # Returns to the main screen
                manage_screen.current = "Main Window"
                # Clears the added item in the screen of the added item
                self.item_name.text = ""
                self.category.text = ""
                self.expiration_date.text = ""
        # Notifies the user of an invalid entry if all fields are blank
        else:
            invalidEntry()


class SortList(Screen):
    # Sort items by name
    def nameSort(self):
        db.items.sort(key=lambda x: x.get('Name'))
    # Sort items by category
    def categorySort(self):
        db.items.sort(key=lambda x: x.get('Category'))
    # Sort items by expiration date
    def expirySort(self):
        db.items.sort(key=lambda x: x.get('Expiration Date'))
    # Return to main window and ensure every item is re-added
    def submit(self):
        global added_item
        added_item = 1
        manage_screen.current = "Main Window"


class Reminders(Screen):
    def submit(self):
        global reminder
        # Error handling: Ff the reminders can be set as text, then validate it.
        try:
            int(self.ids.set_reminder.text)
            # Set reminder
            reminder = int(self.ids.set_reminder.text)
            # Return to the main window
            manage_screen.current = "Main Window"
        # Notify the user of an invalid entry
        except ValueError:
            invalidEntry()


class EditList(Screen):
    def remove(self):
        global added_item
        # Data validation: Only run if all fields are filled in
        if self.item_name.text != "" and self.category.text != "" and self.expiration_date.text != "":
            # Remove the item
            db.remove_item(self.item_name.text, self.category.text, self.expiration_date.text)
            # Refresh the list
            added_item = 1
            # Return to the main window and clear the entries
            manage_screen.current = "Main Window"
            self.item_name.text = ""
            self.category.text = ""
            self.expiration_date.text = ""
        # Notify the user of an invalid entry
        else:
            invalidEntry()


class SearchList(Screen):
    def submit(self):
        manage_screen.current = "Main Window"
        # Clear all preexisting entries
        self.ids.item_search.text = ""
        self.ids.found_name.text = ""
        self.ids.found_category.text = ""
        self.ids.found_expiry.text = ""

    def search(self):
        global added_item
        sought_item = self.ids.item_search.text
        search_name = ""
        search_category = ""
        search_expiry = ""
        # Find the item sought after
        for item in db.items:
            # Match cases
            if item['Name'].lower() == sought_item.lower():
                added_item = 1
                # Add the found item to the list
                search_name += "\n" + item['Name']
                search_category += "\n" + item['Category']
                search_expiry += "\n" + item['Expiration Date']
                self.ids.found_name.text = search_name
                self.ids.found_category.text = search_category
                self.ids.found_expiry.text = search_expiry
        # Tell the user that the item has not been found
        if added_item == 0:
            self.ids.found_name.text = "The item does not exist."
            self.ids.found_category.text = ""
            self.ids.found_expiry.text = ""


class WindowManager(ScreenManager):
    pass


def invalidEntry():
    pop = Popup(title='Invalid Entry',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


def notify(item_name):
    pop = Popup(title='Expiration Notification',
                content=Label(text='The ' + item_name + ' has expired.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


#Parse the kv file through Builder
buildfile = Builder.load_file("Fridge.kv")


manage_screen = WindowManager()

#Declare all 6 windows
screens = [MainWindow(name="Main Window"), EditList(name="Edit List"), SortList(name="Sort List"),
           Reminders(name="Reminders"), SearchList(name="Search List"), NewItem(name="New Item")]
for screen in screens:
    # Add all widgets to the screen
    manage_screen.add_widget(screen)

#Initializes the current screen to be the main window
manage_screen.current = "Main Window"


class FridgeTracker(App):
    def build(self):
        return manage_screen


if __name__ == "__main__":
    FridgeTracker().run()
