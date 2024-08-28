# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: RunebookAtlas Map - Clickable interface that
# displays all the rune locations from the Lincoln Mallmorial
# rune library on UOForever shard. Companion with the Runebook
# Atlas script as a requirement.
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Drawing import Bitmap, Graphics, Color, Pen, Size, Point
from System.Windows.Forms import ScrollBars, Label, Application, Form, PictureBox, MouseEventHandler, PictureBoxSizeMode, DockStyle, TextBox, AnchorStyles, Button, BorderStyle
import re
import csv
from math import sqrt

class ImageForm(Form):
    
    def __init__(self):
        super(ImageForm, self).__init__()
        self.Text = "Map Image"
        self.Width = 5120 // 4
        self.Height = 4096 // 4
        self.original_image = None
        self.SelectedX = 0
        self.SelectedY = 0
        self.labelx = ''
        self.detail_box = TextBox()
        self.detail_box.Multiline = True
        self.detail_box.ReadOnly = True
        self.detail_box.Anchor = AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top | AnchorStyles.Bottom
        self.detail_box.Visible = False
        self.detail_box.BorderStyle = BorderStyle.FixedSingle  # Add border for visibility
        self.Controls.Add(self.detail_box)
        
        # Load the image from the specified location
        try:
            self.original_image = Bitmap("C://Program Files (x86)//UOForever//UO//Forever//RazorEnhanced//Scripts//5120_4096_Map.png")
            self.scale = 0.25
            self.image = self.resize_image(self.original_image, self.scale)
            self.image_copy = self.image.Clone()  # Create a copy of the scaled image
        except Exception as e:
            print(f"Error loading image: {e}")
            return

        # Create PictureBox and add the image
        self.pictureBox = PictureBox()
        self.pictureBox.Image = self.image
        self.pictureBox.SizeMode = PictureBoxSizeMode.AutoSize
        self.pictureBox.Dock = DockStyle.Fill
        self.pictureBox.MouseClick += MouseEventHandler(self.OnMouseClick)
        self.locations = []  # List to store drawn circles coordinates
        
        self.Controls.Add(self.pictureBox)
        self.coordinates = self.load_coordinates("MasterRunebookCoordinates.csv")
        self.draw_gray_circles()  # Draw gray circles for all locations
        

    def resize_image(self, image, scale):
        width = int(image.Width * scale)
        height = int(image.Height * scale)
        resized_image = Bitmap(image, Size(width, height))
        return resized_image

    def on_button_click_cancel(self, sender, event):
        print("Button CANCEL clicked!")
        self.buttonGo.Visible = False
        self.buttonCancel.Visible = False  
        self.labelx = Label()
        self.labelx.Text = "Hello, World!"  # Set the text
        self.labelx.Location = Point(int(self.Width/2), int(self.Height/3))  # Set the location
        self.labelx.AutoSize = True  # Allow the label to adjust its size based on the text
        self.Controls.Add(self.labelx)  # Add the label to the form      
        self.locations = [] 
        self.draw_gray_circles()

        
    def on_button_click_go(self, sender, event):
        print("Button GO clicked!")

        myX = 0
        myY = 0
        mySerial = ''
        myName = ''
        
        mySerial,myX,myY,myName = self.find_runebook("MasterRunebookCoordinates.csv", self.SelectedX, self.SelectedY)
#        if myX != None and myY != None:
#            print('myx:', myX, 'myy:',myY)

        Misc.SetSharedValue("Atlas_Go",True)
        Misc.SetSharedValue("Atlas_Go_Serial",int(mySerial))
        Misc.SetSharedValue("Atlas_Go_Name",str(myName))
        Misc.SetSharedValue("Atlas_Go_RuneX",int(myX))
        Misc.SetSharedValue("Atlas_Go_RuneY",int(myY))
        Misc.Pause(100)
        self.Close() 
                
    def OnMouseClick(self, sender, event):
        print("clearing circles")
        self.clear_circles()  # Clear previously drawn circles

        # Restore the image from the copy
        self.image = self.image_copy.Clone()
        self.pictureBox.Image = self.image  # Update PictureBox with the restored image
        
        x = int(event.X / self.scale)
        y = int(event.Y / self.scale)
        print(f"Clicked at: ({x}, {y})")
        
        self.DrawCircle(int(x * self.scale), int(y * self.scale), 'red')  # Draw selected location circle

        nearest_location = self.find_nearest_location(int(x), int(y))
        print("Nearest location:", nearest_location)
        
        location_x, location_y = nearest_location
        print("Nearest coordinates:", location_x, location_y)
        self.SelectedX = location_x
        self.SelectedY = location_y
        
        dist = self.distance(x, y, location_x, location_y)
        print("Distance of:", dist)
        
        self.DrawCircle(int(location_x * self.scale), int(location_y * self.scale), 'green')  # Draw nearest location circle

        x = event.X
        y = event.Y
        
        
        self.detail_box.Location = Point(int((self.ClientSize.Width // 2) - 50), int(self.ClientSize.Height // 3))
        self.detail_box.Size = Size(100, 50)

        # Enable multiline and vertical scrollbars
        #self.detail_box.Multiline = True
        #self.detail_box.ScrollBars = ScrollBars.Vertical 

        # Try setting the text in the detail_box
        try:
            # Include multiple lines of text
            self.detail_box.Text = "Rune Location:    (" + str(location_x) + "," + str(location_y) +")"
        except Exception as e:
            print(f"FAILED TO SET TEXT BOX DETAILS: {e}")

        # Make the detail_box visible
        self.detail_box.Visible = True
        
        
        self.buttonGo = Button()
        self.buttonGo.Text = "Go!"
        self.buttonGo.Size = Size(100, 50)
        # Center the button on the form
        self.buttonGo.Location = Point((self.ClientSize.Width - self.buttonGo.Width) // 2,
                                     (self.ClientSize.Height - self.buttonGo.Height) // 3 + 75)
        # Add the button to the form
        self.Controls.Add(self.buttonGo)
        # Bring the button to the front
        self.buttonGo.BringToFront()
        # Optionally, add a click event handler for the button
        self.buttonGo.Click += self.on_button_click_go
        
        self.buttonCancel = Button()
        self.buttonCancel.Text = "Cancel"
        self.buttonCancel.Size = Size(100, 50)
        # Center the button on the form
        self.buttonCancel.Location = Point((self.ClientSize.Width - self.buttonGo.Width) // 2,
                                     ((self.ClientSize.Height - self.buttonGo.Height) // 3) + 75 + self.buttonGo.Height)
        # Add the button to the form
        self.Controls.Add(self.buttonCancel)
        # Bring the button to the front
        self.buttonCancel.BringToFront()
        # Optionally, add a click event handler for the button
        self.buttonCancel.Click += self.on_button_click_cancel
        

    def find_nearest_location(self, x, y):
        return min(self.coordinates, key=lambda coord: self.distance(x, y, coord[0], coord[1]))

    def distance(self, x1, y1, x2, y2):
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def DrawCircle(self, x, y, color):
        radius = 5  # Adjusted for the new image size
        
        if color == 'red':
            pen = Pen(Color.Red, 2)  # Adjusted for the new image size
        elif color =='green':
            pen = Pen(Color.Green, 2)  # Adjusted for the new image size
        else:
            pen = Pen(Color.Gray, 2)  # Adjusted for the new image size

        g = Graphics.FromImage(self.image)
        g.DrawEllipse(pen, x - radius, y - radius, radius * 2, radius * 2)
        g.Dispose()
        self.pictureBox.Image = self.image

    def draw_gray_circles(self):
        for location in self.coordinates:
            location_x, location_y = location
            self.DrawCircle(location_x * self.scale, location_y * self.scale, 'gray')  # Draw gray circle for each location
            self.locations.append((location_x, location_y))  # Store drawn circle coordinates

    def clear_circles(self):
        # Clear all previously drawn circles
        self.locations.clear()  # Clear the stored coordinates
        
    def show_all_locations(self, sender, event):
        self.clear_circles()  # Clear previously drawn circles
        self.draw_gray_circles()  # Draw gray circles for all locations
        
    def load_coordinates(self, filename):
        coordinates = []
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                row = str(row)
                start_index = row.find('(')
                end_index = row.find(')')
                coordinates_str = row[start_index+1:end_index]
                coordinates_str = coordinates_str.replace("'", "").replace(",", "") #'
                coordinates_str = coordinates_str.split()
                if len(coordinates_str) >= 2:
                    try:
                        location_x = int(coordinates_str[0])
                        location_y = int(coordinates_str[1])
                        coordinates.append((location_x, location_y))
                    except ValueError:
                        pass
        return coordinates
        
    def find_runebook(self, filename, X, Y):
        X  = int(X)
        Y = int(Y)
        pattern = r'\d+'
        print("Trying to find runebook with x y of ", X, Y)
        with open(filename, mode='r') as file:
            found = False
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                
                integers = re.findall(pattern, str(row))
                #print(integers)
                if int(integers[-2]) == X and int(integers[-1]) == Y:
                    print("FOUND EM IN THE FILE!")
                    found = True
                    print("integers:",integers)
                    print("Selected Name is:", row[4])
                    #      Serial, X, Y
                    return integers[0], integers[-2], integers[-1], row[4]
            print("End of find_runebook, did we find it?: ", found)
            
        if found == False:

            return [0,0]
            
form = ImageForm()
Application.Run(form)
