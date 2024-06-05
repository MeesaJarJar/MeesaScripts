# Made by Meesa Jar Jar(BabyBro on Discord) & DinoDNA - Peace and Love!
# Meesa Rune Atlas - Easy, automated traveling by recalling or gating used exclusively 
# with the Lincoln Mallmorial Rune Library on the UOForever Server.
# To be used with the Rune Atlas script and the Sextant script
#Special Thanks to Wisps/Nebu & Juggz for Code Contributions, and the PWN Guild for testing for me!

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from System.Drawing import Bitmap, Graphics, Color, Pen, Font, Brush, SolidBrush, Size, Point
from System.Windows.Forms import ScrollBars, Label, Application, Form, PictureBox, MouseEventHandler, PictureBoxSizeMode, DockStyle, TextBox, AnchorStyles, Button, BorderStyle
import re
import csv
from math import sqrt

class ImageForm(Form):
    
    def __init__(self):
        super(ImageForm, self).__init__()
        self.Text = "Meesa Jar Jar`s Rune Atlas Map"
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
        self.detail_box.BorderStyle = BorderStyle.FixedSingle  
        self.Controls.Add(self.detail_box)
        
        self.MIBX = 0
        self.MIBY = 0

        try:
            self.original_image = Bitmap("./RazorEnhanced/Scripts/MeesaJarJar_RuneAtlas/5120_4096_Map.png")
            self.scale = 0.25
            self.image = self.resize_image(self.original_image, self.scale)
            self.image_copy = self.image.Clone()  
        except Exception as e:
            print(f"Error loading image: {e}")
            return

        self.pictureBox = PictureBox()
        self.pictureBox.Image = self.image
        self.pictureBox.SizeMode = PictureBoxSizeMode.AutoSize
        self.pictureBox.Dock = DockStyle.Fill
        self.pictureBox.MouseClick += MouseEventHandler(self.OnMouseClick)
        self.locations = []  
        
        self.Controls.Add(self.pictureBox)
        self.coordinates = self.load_coordinates('./RazorEnhanced/Scripts/MeesaJarJar_RuneAtlas/MeesaJarJar_RunebookAtlas_Coordinates.csv')
        self.draw_gray_circles() 
        self.drawMIBCircle()  
        self.drawPlayerCircle()
        
    def resize_image(self, image, scale):
        width = int(image.Width * scale)
        height = int(image.Height * scale)
        resized_image = Bitmap(image, Size(width, height))
        return resized_image

    def on_button_click_cancel(self, sender, event):
        self.buttonGo.Visible = False
        self.buttonCancel.Visible = False  
        self.buttonClose.Visible = True   
        self.locations = [] 
        self.detail_box.Text = ''
        self.detail_box.Visible = False
        
        self.draw_gray_circles()
        self.drawMIBCircle()  
        self.drawPlayerCircle()

    def on_button_click_close(self, sender, event):
        self.Close() 
        
    def on_button_click_go(self, sender, event):
        myX = 0
        myY = 0
        mySerial = ''
        myName = ''
        
        mySerial,myX,myY,myName = self.find_runebook('./RazorEnhanced/Scripts/MeesaJarJar_RuneAtlas/MeesaJarJar_RunebookAtlas_Coordinates.csv', self.SelectedX, self.SelectedY)

        Misc.SetSharedValue("Atlas_Go",True)
        Misc.SetSharedValue("Atlas_Go_Serial",int(mySerial))
        Misc.SetSharedValue("Atlas_Go_Name",str(myName))
        Misc.SetSharedValue("Atlas_Go_RuneX",int(myX))
        Misc.SetSharedValue("Atlas_Go_RuneY",int(myY))
        Misc.Pause(100)
        self.Close() 
                
    def OnMouseClick(self, sender, event):
        self.clear_circles() 


        self.image = self.image_copy.Clone()
        self.pictureBox.Image = self.image  
        
        x = int(event.X / self.scale)
        y = int(event.Y / self.scale)

        self.DrawCircle(int(x * self.scale), int(y * self.scale), 'red')  

        nearest_location = self.find_nearest_location(int(x), int(y))

        location_x, location_y = nearest_location

        self.SelectedX = location_x
        self.SelectedY = location_y
        
        dist = self.distance(x, y, location_x, location_y)
        
        self.DrawCircle(int(location_x * self.scale), int(location_y * self.scale), 'green')  

        x = event.X
        y = event.Y
        
        
        self.detail_box.Location = Point(int((self.ClientSize.Width // 2) - 50), int(self.ClientSize.Height // 3))
        self.detail_box.Size = Size(100, 50)

        try:
            self.detail_box.Text = "Rune Location:    (" + str(location_x) + "," + str(location_y) +")"
        except Exception as e:
            print(f"FAILED TO SET TEXT BOX DETAILS: {e}")

        self.detail_box.Visible = True

        self.buttonGo = Button()
        self.buttonGo.Text = "Go!"
        self.buttonGo.Size = Size(100, 50)

        self.buttonGo.Location = Point((self.ClientSize.Width - self.buttonGo.Width) // 2,
                                     (self.ClientSize.Height - self.buttonGo.Height) // 3 + 75)

        self.Controls.Add(self.buttonGo)
        self.buttonGo.BringToFront()
        self.buttonGo.Click += self.on_button_click_go
        #self.buttonGo.Visible = False
        
        self.buttonCancel = Button()
        self.buttonCancel.Text = "Show Locations"
        self.buttonCancel.Size = Size(100, 25)
        self.buttonCancel.Location = Point((self.ClientSize.Width - self.buttonGo.Width) // 2,
                                     ((self.ClientSize.Height - self.buttonGo.Height) // 3) + 75 + self.buttonGo.Height)
        self.Controls.Add(self.buttonCancel)
        self.buttonCancel.BringToFront()
        self.buttonCancel.Click += self.on_button_click_cancel
        
        self.buttonClose = Button()
        self.buttonClose.Text = "Close"
        self.buttonClose.Size = Size(100, 50)
        self.buttonClose.Location = Point((self.ClientSize.Width - self.buttonGo.Width) // 2,
                                     ((self.ClientSize.Height - self.buttonGo.Height) // 3) + 100 + self.buttonGo.Height)
        self.Controls.Add(self.buttonClose)
        self.buttonClose.BringToFront()
        self.buttonClose.Click += self.on_button_click_close  
    
        self.drawMIBCircle()  
        self.drawPlayerCircle()    

    def find_nearest_location(self, x, y):
        return min(self.coordinates, key=lambda coord: self.distance(x, y, coord[0], coord[1]))

    def distance(self, x1, y1, x2, y2):
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def DrawCircle(self, x, y, color, radius=5):
        x = int(x)
        y = int(y)
        if color == 'red':
            pen = Pen(Color.Red, 2)  
        elif color =='green':
            pen = Pen(Color.Green, 2)  
        elif color == 'yellow':
            pen = Pen(Color.Yellow, 2)
        elif color == 'orange':
            pen = Pen(Color.Orange, 2)

        elif color == 'green':
            pen = Pen(Color.Green, 2)
        
        elif color == 'white':
            pen = Pen(Color.White, 2)            
        else:
            pen = Pen(Color.Gray, 2)  

        g = Graphics.FromImage(self.image)
        g.DrawEllipse(pen, x - radius, y - radius, radius * 2, radius * 2)
        g.Dispose()
        self.pictureBox.Image = self.image

    def draw_gray_circles(self):
        for location in self.coordinates:
            location_x, location_y = location
            self.DrawCircle(location_x * self.scale, location_y * self.scale, 'gray')  
            self.locations.append((location_x, location_y))  

    def clear_circles(self):
       
        self.locations.clear()  
        
    def show_all_locations(self, sender, event):
        self.clear_circles()  
        self.draw_gray_circles() 
        
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
        with open(filename, mode='r') as file:
            found = False
            reader = csv.reader(file)
            next(reader) 
            for row in reader:
                integers = re.findall(pattern, str(row))
                if int(integers[-2]) == X and int(integers[-1]) == Y:
                    found = True
                    return integers[0], integers[-2], integers[-1], row[4]
            print("End of find_runebook, did we find it?: ", found)
            
        if found == False:

            return [0,0]

    def drawMIBCircle(self):

        try:
            mib_x = int(Misc.ReadSharedValue("Atlas_Go_MIBX"))
            mib_y = int(Misc.ReadSharedValue("Atlas_Go_MIBY"))
            self.DrawCircle(round(mib_x * self.scale), round(mib_y * self.scale), 'yellow')
            self.DrawCircle(round(mib_x * self.scale), round(mib_y * self.scale), 'orange', radius=10)  # Double the radius for the orange circle
        
            
        except Exception as e:
            print(f"Error drawing MIB circle: {e}")    
        
        
        g = Graphics.FromImage(self.image)
        font = Font("Arial", 28)
        brush = SolidBrush(Color.Orange)
        text = "MIB"
        text_position = Point(int(mib_x * self.scale - 50), int(mib_y * self.scale - 100))
        g.DrawString(text, font, brush, text_position)
        pen = Pen(Color.Orange, 2)
        g.DrawLine(pen, text_position.X + 50, text_position.Y + 32, mib_x * self.scale, mib_y * self.scale)
        g.Dispose()
        self.pictureBox.Image = self.image
            
    def drawPlayerCircle(self):

        try:
            mib_x = Player.Position.X
            mib_y = Player.Position.Y
            self.DrawCircle(round(mib_x * self.scale), round(mib_y * self.scale), 'white')
            self.DrawCircle(round(mib_x * self.scale), round(mib_y * self.scale), 'green', radius=10)  # Double the radius for the orange circle
        
            
        except Exception as e:
            print(f"Error drawing MIB circle: {e}")    
        
        
        g = Graphics.FromImage(self.image)
        font = Font("Arial", 28)
        brush = SolidBrush(Color.Green)
        text = "Player"
        text_position = Point(int(mib_x * self.scale - 50), int(mib_y * self.scale - 100))
        g.DrawString(text, font, brush, text_position)
        
        
        font = Font("Arial", 29)
        brush = SolidBrush(Color.White)
        text = "Player"
        text_position = Point(int(mib_x * self.scale - 52), int(mib_y * self.scale - 102))
        g.DrawString(text, font, brush, text_position)
        
        pen = Pen(Color.Green, 2)
        g.DrawLine(pen, text_position.X + 50, text_position.Y + 32, mib_x * self.scale, mib_y * self.scale)
        g.Dispose()
        self.pictureBox.Image = self.image    

form = ImageForm()
Application.Run(form)
