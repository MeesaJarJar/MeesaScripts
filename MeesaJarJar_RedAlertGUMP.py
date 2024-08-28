# Made by MeesaJarJar - http://github.com/MeesaJarJar/  -------#
# BabyBro / MeesaJarJar on Discord - Peace & Love! -------------#
# -------------------------------------------------------------#
# Description: Red Alert - GUMP - Displays a flashing alert
# when reds are detected by someone running the script via
# Chat Guild commands. It also sends the location and who the 
# player saw to the guild. Resets to normal after a while. 
# -------------------------------------------------------------#
# START CONFIG ------------------------------------------------#


# END CONFIG --------------------------------------------------#
from System.Collections.Generic import List
from System import Int32 as int
from System import Byte

import os
import clr

from System.Collections.Generic import List
from System import Byte, String
from System import Int32 as int
from System.Threading import Thread, ThreadStart

clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System import DateTime
from System.Drawing import Bitmap, Graphics, Imaging, Color
from System.Windows.Forms import Screen

Timer.Create('REDALERTTIMER', 1)

redAlert = False
switchOn = False

RED = 32
GREEN = 68
WHITE = 1152
YELLOW = 2179
gumpNumber = 3423516
alertGumpNumber = 1351313

alertText = None
alertZone = None
alertArea = None
alertPlayer = None
alertX = None
alertY = None
alertSerial = None
alertHistory = []
showLog = True

uniqueNameDaemon =  ['Aamon', 'Agalierept', 'Agares', 'Aglasis', 'Aiwaz', 'Astaroth', 'Ayperos', 'Azatoth', 'Azmodaeus', 'Azrael', "Ba'al", 'Baal', 'Barbatos', 'Bathim', 'Bathsin', "Be'elzebub", "Be'elzebubba", 'Bechard', 'Beelzebuth', 'Botis', 'Brulefer', 'Bucon', 'Buer', 'Clauneck', 'Clitheret', 'Cthulhu', 'Druzil', 'El Chupacabra', 'Eleogap', 'Eliezer', 'Eligor', 'Eracove', 'Faraii', 'Fleurety', 'Frimost', 'Frucissiere', 'Fruitimiere', 'Glassyalabolas', 'Guland', 'Gusoyn', 'Hael', 'Haristum', 'Heramael', 'Hiepacth', 'Huictiigara', 'Humots', 'Khil', 'Maleki', 'Marbas', 'Mephistopheles', 'Mersilde', 'Minoson', 'Moloch', 'Molech', 'Morail', 'Musisin', 'Naberrs', 'Nebiros', 'Nebirots', 'Nyarlathotep', 'Pentagnony', 'Proculo', 'Pruslas', 'Pursan', 'Rofocale', 'Sargatans', 'Satanchia', 'Satanciae', 'Segal', 'Sergulath', 'Sergutthy', 'Sidragrosam', 'Sirchade', 'Surgat', 'Sustugriel', 'Tarchimache', 'Tarihimal', 'Trimasel', 'Vaelfar', 'Wormius', 'Yog-Sothoth', "Y'reif Eci", 'Zoray']
uniqueNameDarknightCreeper =  ['Pariah', 'Ydoc Llessue', 'Zhaan', 'Lorbna', 'Gragok', 'Thranger', 'Krygar', 'Grothelfiend', 'Centibis', 'Farthak', 'Laitesach', 'Crenabil', 'Krullus', 'Legron', 'Noirkrach', 'Blassarrabb', 'Gragragron', 'Vendodroth', 'Flaggroth', 'Vilithrar']
uniqueNameDemonKnight =  ['Hrallath the Dark Father', 'Heksen the Dark Father', 'Peinsluth the Dark Father', 'Keelus the Dark Father', "Kra'an the Dark Father", 'Ankou the Dark Father', "Turi'el the Dark Father", 'Azazel the Dark Father', 'Armarus the Dark Father', 'Grigorus the Dark Father', "Ga'ahp the Dark Father", 'Therion the Dark Father', 'Peirazo the Dark Father', 'Ponerus the Dark Father', 'Arhaios Ophis the Dark Father', 'Vairocan the Dark Father', 'Arsat the Dark Father', 'Karnax the Dark Father', "Taet Nu'uhn the Dark Father"]
uniqueNameLizardMan =  ['Aissssaiss', 'Aisyths', 'Alasthsiyss', 'Alessitsl', 'Alsiths', 'Alssi', 'Alsyth', 'Asahlysy', 'Asathsaisss', 'Asaysth', 'Asiashy', 'Asistsais', 'Asitssis', 'Asiyss', 'Astha', 'Asthcieth', 'Astysah', 'Athcesth', 'Athys', 'Athysthes', 'Atslah', 'Aysthyss', 'Cesthaysth', 'Cetys', 'Ciethlish', 'Citsy', 'Cythshi', 'Cytsi', 'Ekthsisthh', 'Essith', 'Estha', 'Etys', 'Halasth', 'Haless', 'Halsasah', 'Hasits', 'Hekths', 'Hiiths', 'Hiitsl', 'Hissis', 'Hlyiss', 'Hlylylyshi', 'Hlyshilyly', 'Hlysylyiss', 'Hlythilsyth', 'Hissalsthy', 'Hysslssi', 'Hsysylh', 'Hthessthil', 'Hthissy', 'Htisthh', 'Htsiathys', 'Hyisass', 'Hysil', 'Hysyiss', 'Iasia', 'Icythhlysy', 'Iithsissh', 'Iitsliss', 'Ilshy', 'Ilsyth', 'Isalraaat', 'Isassthys', 'Isathys', 'Isiss', 'Isissil', 'Isshi', 'Isshlshy', 'Isstha', 'Issthas', 'Issthyl', 'Issysh', 'Issyt', 'Isthhtis', 'Istis', 'Istththh', 'Isyts', 'Ithstsesh', 'Ithsy', 'Iththis', 'Itsesh', 'Itshas', 'Itsltlish', 'Itsthil', 'Itsylh', 'Iyssysil', 'Kthystshas', 'Kthythes', 'Lasath', 'Lastha', 'Lasthtsthih', 'Lesstslah', 'Lestha', 'Lilhals', 'Lilsyth', 'Lishaless', 'Lishath', 'Lissysh', 'Lissyt', 'Lithekths', 'Litsylh', 'Llithlish', 'Lshyshas', 'Lssissi', 'Lsthyssy', 'Lsyth', 'Lsythstha', 'Lyissisis', 'Lylsthy', 'Lylyisass', 'Lyshiisal', 'Lyssthih', 'Lyssthy', 'Lysyiitsl', 'Lythiiiths', 'Lytsthih', 'Saisalasths', 'Saishtsi', 'Saisssmyss', 'Salsesh', 'Salssi', 'Sasisthasth', 'Sasss', 'Sasth', 'Sath', 'Sathsthih', 'Sathys', 'Satslah', 'Saysth', 'Scesthhals', 'Seshsthyl', 'Sessith', 'Shasits', 'Shassthy', 'Shisis', 'Shitha', 'Shysil', 'Shythis', 'Siasia', 'Siaththh', 'Sicyth', 'Silshy', 'Silthyl', 'Sisal', 'Sisshi', 'Sisshlythi', 'Sistlilh', 'Sithtththh', 'Sitsesh', 'Sitshas', 'Sitstsi', 'Siyss', 'Slahyisass', 'Slasath', 'Slishless', 'Ssaisss', 'Ssasist', 'Sshiscesth', 'Ssisal', 'Ssithsiss', 'Ssiyth', 'Sssaisss', 'Ssssshi', 'Ssthasssthas', 'Ssthihssthy', 'Ssthssss', 'Ssthyl', 'Ssthyssths', 'Ssyraaath', 'Ssysah', 'Ssyshstha', 'Ssyssith', 'Ssytsth', 'Stasah', 'Sthasth', 'Sthasthas', 'Sthasthih', 'Sthihaisss', 'Sthihasits', 'Sthilsthy', 'Sthlyly', 'Sthlyshi', 'Sthlysy', 'Sthlythi', 'Sthmissa', 'Sthmyss', 'Sthsasist', 'Sthyss', 'Sthyasia', 'Sthycyth', 'Sthyltasah', 'Stissh', 'Stththh', 'Stysah', 'Sycieth', 'Sylhsths', 'Syllith', 'Syraaat', 'Syshsyts', 'Syslish', 'Syththil', 'Sythysth', 'Sytlilh', 'Sytlish', 'Sytsyth', 'Sytsyts', 'Syys', 'Tasahasath', 'Thalasths', 'Thaless', 'Thals', 'Thatsylh', 'Thays', 'Thekths', 'Theshthis', 'Thiiths', 'Thiitsl', 'Thilhlyshi', 'Thishthes', 'Thlyiss', 'Thlyly', 'Thlyshi', 'Thlysy', 'Thlythi', 'Thmissa', 'Thmyss', 'Thsais', 'Thslish', 'Ththes', 'Ththhllith', 'Ththis', 'Thtisthh', 'Thyisass', 'Thylmissa', 'Thys', 'Thysslah', 'Tisiss', 'Tissyth', 'Tisthhhsy', 'Tlilhlasth', 'Tlishkths', 'Tseshsath', 'Tshassasisth', 'Tsicyth', 'Tsitys', 'Tslahsits', 'Tsthihssthih', 'Tsthil', 'Tsycieth', 'Tsylhssyt', 'Tsytysah', 'Tththhsyt', 'Tysahyraaath', 'Tyscesth', 'Tysycieth', 'Yciethhlyly', 'Yisasshmyss', 'Yisstisthh', 'Yllith', 'Ylsthy', 'Yraaathlythi', 'Ysahlith', 'Ysasth', 'Ysath', 'Yscesth', 'Yshmissa', 'Yshtsi', 'Ysilsia', 'Yslish', 'Yssasisth', 'Ysssal', 'Yssthih', 'Yssths', 'Yssthy', 'Ystasah', 'Ysthsith', 'Ystsy', 'Ythals', 'Ythssysh', 'Ytlilh', 'Ytlish', 'Ytsais', 'Ytssysh', 'Ytsthih']
uniqueNameFireGargoyle =  ['a fiery gargoyle', 'a burning gargoyle', 'a smoldering gargoyle', 'a blistering gargoyle', 'a sweltering gargoyle', 'a flaming gargoyle', 'a scorching gargoyle', 'a blazing gargoyle', 'a searing gargoyle']
uniqueNameImpaler =  ['Po-Kor', 'Manglar', 'Verolyn', 'Gathfe', 'Skred', 'Flandrith', 'Stavinfeks', 'Steelbane', 'Crarigor', 'Empalk', 'Perfus', 'Cassiel', 'Magor', 'Xtul', 'Vladeer', 'Scrill', 'Slix', 'Ix', 'Selminus', 'Victux']
uniqueNameOrc =  ['Abghat', 'Adgulg', 'Aghed', 'Agugh', 'Aguk', 'Almthu', 'Alog', 'Ambilge', 'Apaugh', 'Argha', 'Argigoth', 'Argug', 'Arpigig', 'Auhgan', 'Azhug', 'Bagdud', 'Baghig', 'Bahgigoth', 'Bahgigoth', 'Bandagh', 'Barfu', 'Bargulg', 'Baugh', 'Bidgug', 'Bildud', 'Bilge', 'Bog', 'Boghat', 'Bogugh', 'Borgan', 'Borug', 'Braugh', 'Brougha', 'Brugagh', 'Bruigig', 'Buadagh', 'Buggug', 'Builge', 'Buimghig', 'Bulgan', 'Bumhug', 'Buomaugh', 'Buordud', 'Burghed', 'Buugug', 'Cabugbu', 'Cagan', 'Carguk', 'Carthurg', 'Clog', 'Corgak', 'Crothu', 'Cubub', 'Cukgilug', 'Curbag', 'Dabub', 'Dakgorim', 'Dakgu', 'Dalthu', 'Darfu', 'Deakgu', 'Dergu', 'Derthag', 'Digdug', 'Diggu', 'Dilug', 'Ditgurat', 'Dorgarag', 'Dregu', 'Dretkag', 'Drigka', 'Drikdarok', 'Drutha', 'Dudagog', 'Dugarod', 'Dugorim', 'Duiltag', 'Durbag', 'Eagungad', 'Eggha', 'Eggugat', 'Egharod', 'Eghuglat', 'Eichelberbog', 'Ekganit', 'Epkagut', 'Ergoth', 'Ertguth', 'Ewkbanok', 'Fagdud', 'Faghig', 'Fandagh', 'Farfu', 'Farghed', 'Fargigoth', 'Farod', 'Faugh', 'Feldgulg', 'Fidgug', 'Filge', 'Fodagog', 'Fogugh', 'Fozhug', 'Frikug', 'Frug', 'Frukag', 'Fubdagog', 'Fudhagh', 'Fupgugh', 'Furbog', 'Futgarek', 'Gaakt', 'Garekk', 'Gelub', 'Gholug', 'Gilaktug', 'Ginug', 'Gnabadug', 'Gnadug', 'Gnalurg', 'Gnarg', 'Gnarlug', 'Gnorl', 'Gnorth', 'Gnoth', 'Gnurl', 'Golag', 'Golag', 'Golub', 'Gomatug', 'Gomoku', 'Gorgu', 'Gorlag', 'Grikug', 'Grug', 'Grug', 'Grukag', 'Grukk', 'Grung', 'Gruul', 'Guag', 'Gubdagog', 'Gudhagh', 'Gug', 'Gug', 'Gujarek', 'Gujek', 'Gujjab', 'Gulm', 'Gulrn', 'Gunaakt', 'Gunag', 'Gunug', 'Gurukk', 'Guthakug', 'Guthug', 'Gutjja', 'Hagob', 'Hagu', 'Hagub', 'Haguk', 'Hebub', 'Hegug', 'Hibub', 'Hig', 'Hogug', 'Hoknath', 'Hoknuk', 'Hokulk', 'Holkurg', 'Horknuth', 'Hrolkug', 'Hugagug', 'Hugmug', 'Hugolm', 'Ig', 'Igmut', 'Ignatz', 'Ignorg', 'Igubat', 'Igug', 'Igurg', 'Ikgnath', 'Ikkath', 'Inkathu', 'Inkathurg', 'Isagubat', 'Jogug', 'Jokgagu', 'Jolagh', 'Jorgagu', 'Jregh', 'Jreghug', 'Jugag', 'Jughog', 'Jughragh', 'Jukha', 'Jukkhag', 'Julakgh', 'Kabugbu', 'Kagan', 'Kaghed', 'Kahigig', 'Karfu', 'Karguk', 'Karrghed', 'Karrhig', 'Karthurg', 'Kebub', 'Kegigoth', 'Kegth', 'Kerghug', 'Kertug', 'Kilug', 'Klapdud', 'Klapdud', 'Klog', 'Klughig', 'Knagh', 'Knaraugh', 'Knodagh', 'Knorgh', 'Knuguk', 'Knurigig', 'Kodagog', 'Kog', 'Kogan', 'Komarod', 'Korgak', 'Korgulg', 'Koughat', 'Kraugug', 'Krilge', 'Krothu', 'Krouthu', 'Krugbu', 'Krugorim', 'Kubub', 'Kugbu', 'Kukgilug', 'Kulgha', 'Kupgugh', 'Kurbag', 'Kurmbag', 'Laghed', 'Lamgugh', 'Mabub', 'Magdud', 'Malthu', 'Marfu', 'Margulg', 'Mazhug', 'Meakgu', 'Mergigoth', 'Milug', 'Mudagog', 'Mugarod', 'Mughragh', 'Mugorim', 'Murbag', 'Naghat', 'Naghig', 'Naguk', 'Nahgigoth', 'Nakgu', 'Narfu', 'Nargulg', 'Narhbub', 'Narod', 'Neghed', 'Nehrakgu', 'Nildud', 'Nodagog', 'Nofhug', 'Nogugh', 'Nomgulg', 'Noogugh', 'Nugbu', 'Nughilug', 'Nulgha', 'Numhug', 'Nurbag', 'Nurghed', 'Oagungad', 'Oakgu', 'Obghat', 'Oggha', 'Oggugat', 'Ogharod', 'Oghuglat', 'Oguk', 'Ohomdud', 'Ohulhug', 'Oilug', 'Okganit', 'Olaghig', 'Olaugh', 'Olmthu', 'Olodagh', 'Olog', 'Omaghed', 'Ombilge', 'Omegugh', 'Omogulg', 'Omugug', 'Onog', 'Onubub', 'Onugug', 'Oodagh', 'Oogorim', 'Oogugbu', 'Oomigig', 'Opathu', 'Opaugh', 'Opeghat', 'Opilge', 'Opkagut', 'Opoguk', 'Oquagan', 'Orgha', 'Orgoth', 'Orgug', 'Orpigig', 'Ortguth', 'Otugbu', 'Ougha', 'Ougigoth', 'Ouhgan', 'Owkbanok', 'Paghorim', 'Pahgigoth', 'Pahgorim', 'Pakgu', 'Parfu', 'Pargu', 'Parhbub', 'Parod', 'Peghed', 'Pehrakgu', 'Pergu', 'Perthag', 'Pigdug', 'Piggu', 'Pitgurat', 'Podagog', 'Pofhug', 'Pomgulg', 'Poogugh', 'Porgarag', 'Pregu', 'Pretkag', 'Prigka', 'Prikdarok', 'Prutha', 'Pughilug', 'Puiltag', 'Purbag', 'Qog', 'Quadagh', 'Quilge', 'Quimghig', 'Quomaugh', 'Quordud', 'Quugug', 'Raghat', 'Raguk', 'Rakgu', 'Rarfu', 'Rebub', 'Rilug', 'Rodagog', 'Rogan', 'Romarod', 'Routhu', 'Rugbu', 'Rugorim', 'Rurbag', 'Rurigig', 'Sabub', 'Saghig', 'Sahgigoth', 'Sahgorim', 'Sakgu', 'Salthu', 'Saraugug', 'Sarfu', 'Sargulg', 'Sarhbub', 'Sarod', 'Sbghat', 'Seakgu', 'Sguk', 'Shomdud', 'Shulhug', 'Sildud', 'Silge', 'Silug', 'Sinsbog', 'Slaghig', 'Slapdud', 'Slaugh', 'Slodagh', 'Slog', 'Slughig', 'Smaghed', 'Smegugh', 'Smogulg', 'Snog', 'Snubub', 'Snugug', 'Sodagh', 'Sog', 'Sogorim', 'Sogugbu', 'Sogugh', 'Sombilge', 'Somigig', 'Sonagh', 'Sorgulg', 'Sornaraugh', 'Soughat', 'Spathu', 'Speghat', 'Spilge', 'Spoguk', 'Squagan', 'Stugbu', 'Sudagog', 'Sugarod', 'Sugbu', 'Sugha', 'Sugigoth', 'Sugorim', 'Suhgan', 'Sulgha', 'Sulmthu', 'Sumhug', 'Sunodagh', 'Sunuguk', 'Supaugh', 'Supgugh', 'Surbag', 'Surgha', 'Surghed', 'Surgug', 'Surpigig', 'Tagdud', 'Taghig', 'Tandagh', 'Tandagh', 'Tarfu', 'Targhed', 'Targigoth', 'Tarod', 'Taugh', 'Taugh', 'Teldgulg', 'Tidgug', 'Tidgug', 'Tilge', 'Todagog', 'Tog', 'Toghat', 'Togugh', 'Torgan', 'Torug', 'Tozhug', 'Traugh', 'Trilug', 'Trougha', 'Trugagh', 'Truigig', 'Tuggug', 'Tulgan', 'Turbag', 'Turge', 'Ug', 'Ugghra', 'Uggug', 'Ughat', 'Ulgan', 'Ulmragha', 'Ulmrougha', 'Umhra', 'Umragig', 'Umruigig', 'Ungagh', 'Unrugagh', 'Urag', 'Uraugh', 'Urg', 'Urgan', 'Urghat', 'Urgran', 'Urlgan', 'Urmug', 'Urug', 'Urulg', 'Vabugbu', 'Vagan', 'Vagrungad', 'Vagungad', 'Vakgar', 'Vakgu', 'Vakmu', 'Valthurg', 'Vambag', 'Vamugbu', 'Varbu', 'Varbuk', 'Varfu', 'Vargan', 'Varguk', 'Varkgorim', 'Varthurg', 'Vegum', 'Vergu', 'Verlgu', 'Verthag', 'Verthurg', 'Vetorkag', 'Vidarok', 'Vigdolg', 'Vigdug', 'Viggu', 'Viggulm', 'Viguka', 'Vitgurat', 'Vitgut', 'Vlog', 'Vlorg', 'Vorgak', 'Vorgarag', 'Vothug', 'Vregu', 'Vretkag', 'Vrigka', 'Vrikdarok', 'Vrogak', 'Vrograg', 'Vrothu', 'Vruhag', 'Vrutha', 'Vubub', 'Vugub', 'Vuiltag', 'Vukgilug', 'Vultog', 'Vulug', 'Vurbag', 'Wakgut', 'Wanug', 'Wapkagut', 'Waruk', 'Wauktug', 'Wegub', 'Welub', 'Wholug', 'Wilaktug', 'Wingloug', 'Winug', 'Woabadug', 'Woggha', 'Woggugat', 'Woggugat', 'Wogharod', 'Wogharod', 'Woghuglat', 'Woglug', 'Wokganit', 'Womkug', 'Womrikug', 'Wonabadug', 'Worthag', 'Wraog', 'Wrug', 'Wrukag', 'Wrukaog', 'Wubdagog', 'Wudgh', 'Wudhagh', 'Wudugog', 'Wuglat', 'Wumanok', 'Wumkbanok', 'Wurgoth', 'Wurmha', 'Wurtguth', 'Wurthu', 'Wutgarek', 'Xaakt', 'Xago', 'Xagok', 'Xagu', 'Xaguk', 'Xarlug', 'Xarpug', 'Xegug', 'Xepug', 'Xig', 'Xnath', 'Xnaurl', 'Xnurl', 'Xoknath', 'Xokuk', 'Xolag', 'Xolkug', 'Xomath', 'Xomkug', 'Xomoku', 'Xonoth', 'Xorag', 'Xorakk', 'Xoroku', 'Xoruk', 'Xothkug', 'Xruul', 'Xuag', 'Xug', 'Xugaa', 'Xugag', 'Xugagug', 'Xugar', 'Xugarf', 'Xugha', 'Xugor', 'Xugug', 'Xujarek', 'Xuk', 'Xulgag', 'Xunaakt', 'Xunag', 'Xunug', 'Xurek', 'Xurl', 'Xurug', 'Xurukk', 'Xutag', 'Xuthakug', 'Xutjja', 'Yaghed', 'Yagnar', 'Yagnatz', 'Yahg', 'Yahigig', 'Yakgnath', 'Yakha', 'Yalakgh', 'Yargug', 'Yegigoth', 'Yegoth', 'Yerghug', 'Yerug', 'Ymafubag', 'Yokgagu', 'Yokgu', 'Yolmar', 'Yonkathu', 'Yregh', 'Yroh', 'Ysagubar', 'Yughragh', 'Yugug', 'Yugug', 'Yukgnath', 'Yukha', 'Yulakgh', 'Yunkathu', 'Zabghat', 'Zabub', 'Zaghig', 'Zahgigoth', 'Zahgorim', 'Zalthu', 'Zaraugug', 'Zarfu', 'Zargulg', 'Zarhbub', 'Zarod', 'Zeakgu', 'Zguk', 'Zildud', 'Zilge', 'Zilug', 'Zinsbog', 'Zlapdud', 'Zlog', 'Zlughig', 'Zodagh', 'Zog', 'Zogugbu', 'Zogugh', 'Zombilge', 'Zonagh', 'Zorfu', 'Zorgulg', 'Zorhgigoth', 'Zornaraugh', 'Zoughat', 'Zudagog', 'Zugarod', 'Zugbu', 'Zugorim', 'Zuhgan', 'Zulgha', 'Zulmthu', 'Zumhug', 'Zunodagh', 'Zunuguk', 'Zupaugh', 'Zupgugh', 'Zurbag', 'Zurgha', 'Zurghed', 'Zurgug', 'Zurpigig']
uniqueNameRatMan =  ['Ccketakiki', 'Chachak', 'Chachaktak', 'Chackuk', 'Chak', 'Chaki', 'Chaki', 'Chakreki', 'Chaktuki', 'Chakukki', 'Charitiki', 'Chatuki', 'Chectik', 'Chectik', 'Chek', 'Chekeckaki', 'Cheki', 'Chekkakii', 'Cherek', 'Chetak', 'Chetickuki', 'Chiackukk', 'Chichachak', 'Chichak', 'Chichak', 'Chichoki', 'Chichoki', 'Chickek', 'Chickek', 'Chickeki', 'Chickeki', 'Chickekiaki', 'Chikavi', 'Chikchickeki', 'Chikckak', 'Chikek', 'Chiketckuki', 'Chiki', 'Chikitchaki', 'Chiktaki', 'Chiritchek', 'Chitaviok', 'Chokchak', 'Chokirek', 'Chotechiki', 'Ckak', 'Ckek', 'Ckekckuki', 'Ckeki', 'Ckekickuk', 'Ckikhiki', 'Ckikicheki', 'Ckukchik', 'Ckukichek', 'Ctiktik', 'Dachek', 'Dackatuki', 'Dactuk', 'Dafactik', 'Deckarreki', 'Deektuk', 'Defetav', 'Dekckuk', 'Detckiki', 'Detckuki', 'Detik', 'Dicchok', 'Dickiki', 'Dikfachok', 'Ditecckek', 'Diwarek', 'Eachik', 'Eactiki', 'Ecckkekek', 'Eckaki', 'Eckechakiki', 'Ecketak', 'Ecterek', 'Ectuk', 'Eekckuk', 'Eektuk', 'Eicchiki', 'Eickuki', 'Ekiuki', 'Etakheki', 'Etavchiki', 'Etckuki', 'Etik', 'Fachchekiok', 'Fachok', 'Fackak', 'Fackek', 'Fackik', 'Factavi', 'Factik', 'Fecckik', 'Fechaki', 'Feractav', 'Fetav', 'Fetckiki', 'Firchik', 'Firecheki', 'Fireki', 'Fitactaki', 'Fitaki', 'Fitcheki', 'Frecckeki', 'Hekckeki', 'Hiki', 'Hikitchaki', 'Hokchek', 'Ikchaki', 'Iki', 'Kackak', 'Kactavi', 'Kadicchok', 'Kakhoki', 'Kaki', 'Kakiki', 'Karrekichoki', 'Katukickek', 'Kecckik', 'Kechaki', 'Kekachek', 'Kekachik', 'Kekkik', 'Kicchiki', 'Kichak', 'Kickak', 'Kidikiki', 'Kietik', 'Kik', 'Kikechokii', 'Kikiaki', 'Kiktaki', 'Kirchik', 'Kireki', 'Kireki', 'Kitak', 'Kitaki', 'Kitavi', 'Kitcheki', 'Ktukchok', 'Kukeckaki', 'Kuki', 'Kukiecckak', 'Rackek', 'Ractav', 'Ratitchaki', 'Recckeki', 'Recheki', 'Rekchectik', 'Reki', 'Rektav', 'Rektavi', 'Retchectik', 'Reteckaki', 'Retituki', 'Rikchickek', 'Rikecckak', 'Ritchek', 'Ritchekckiki', 'Ritiki', 'Ritikituk', 'Tackik', 'Tactaki', 'Tactikiv', 'Tadectuk', 'Tak', 'Tak', 'Taki', 'Taki', 'Taktav', 'Tavchichoki', 'Taviactak', 'Taviectuk', 'Tecckek', 'Techiki', 'Techikickik', 'Teckak', 'Tedetik', 'Tekactiki', 'Tekchichak', 'Tickukitaki', 'Tictak', 'Tidetckuki', 'Tikckek', 'Tikickeki', 'Titchaki', 'Tituki', 'Tukckaki', 'Tukitiki', 'Tukituki', 'Vachichak', 'Vackuk', 'Vactak', 'Vaveckaki', 'Vechoki', 'Vectaki', 'Vevactak', 'Vevitavi', 'Vitavi', 'Vitchak', 'Vitituki', 'Vivackuk', 'Vivitchak', 'Vovechoki', 'Warek', 'Warreki', 'Wecckak', 'Weckaki', 'Wedachek', 'Wikchichoki', 'Wochickeki']
uniqueNameShadowKnight =  ['Oghmus the Shadow Knight', 'Arametheus the Shadow Knight', 'Terxor the Shadow Knight', 'Erdok the Shadow Knight', 'Archatrix the Shadow Knight', 'Jonar the Shadow Knight', "Marth'Fador the Shadow Knight", 'Helzigar the Shadow Knight', 'Tyrnak the Shadow Knight', 'Krakus the Shadow Knight', 'Marcus Fel the Shadow Knight', 'Lord Kaos the Shadow Knight', 'Doomor the Shadow Knight', 'Uhn the Shadow Knight', 'Malashim the Shadow Knight', 'Samael the Shadow Knight', 'Nelokhiel the Shadow Knight', 'Montobulus the Shadow Knight', 'Usuhl the Shadow Knight', 'Zul the Shadow Knight']
uniqueNameCentaur =  ['Sophanon', 'Caryax', 'Daemeox', 'Phlegon', 'Aerophus', 'Euforus', 'Pallax', 'Nikaon', 'Licouax', 'Lindsaon', 'Bastax', 'Magdanon', 'Thayax', 'Aethon', 'Ceridus', 'Galenon', 'Rhysus', 'Auramax', 'Aldrax', 'Anaxus', 'Luceus', 'Quarax', 'Ariax', 'Balarax', 'Vincenus', 'Loxias', 'Birhamus', 'Lekax', 'Nyctinus', 'Myrsinus']
uniqueNameEtherealWarrior =  ['Galdrion', 'Briellis', 'Charpris', 'Jesurian', 'Agrast', 'Beldrion', 'Polis', 'Arafel', 'Melestoref', 'Lanculis', 'Judaselo', 'Pietrov']
uniqueNamePixie =  ['Klian', 'Klistra', 'Laeri', 'Ciline', 'Shiale', 'Ourie', 'Piepe', 'Liera', 'Sili', 'Sefi', 'Cynthe', 'Nedra', 'Hali', 'Jiki', 'Piku', 'Rael', 'Zanne', 'Zut', 'Sini', 'Os', 'Wienne', 'Xian', 'Ybri', 'Calee', 'Shendri', 'Shri']
uniqueNameEvilMage =  ['Ronlyn', 'Merkul', 'Zasfus', 'Zain', 'Doraghir', 'Danaghir', 'Staylin', 'Kraylin', 'Limnoch', 'Kranor', 'Kraenor', 'Kranostil', 'Kranostir', 'Lilithack', 'Terus', 'Thaelin', 'Thulack', 'Jiltharis', 'Garigor', 'Banothil', 'Bainothil', 'Quain', 'Ilzinias', 'Mardis the Avenger', 'Phalil the Unexpected', 'Lord Adnoc', 'Leje the Invincible', 'Master Akris', 'Sartan', 'Zejron the Wild', 'Pitt the Elder', 'Puzilan the Puzzler', 'Vantrom', 'Singhe-Dul', 'Tyrin Kuhl', 'Xarot the Black', 'Kwan Li', 'Lord of the Mists', 'Viktor Blackoak', 'Odilion', 'Raith', 'Lord of Rats', 'Bazerion the Wizard-Lord', 'Tybevriat Varn', 'Keldor the Modoc', 'Magelord Varsan', 'Izlay the Ebonheart', 'Slirith Iceblood', 'Alcor', 'Vitar', 'Feenark', 'Sang Qui', 'Lyticant', 'Aegnor', 'Aelfric', 'Ainvar', 'Arazion', 'Ardarion', 'Arkanis', 'Athrax', 'Barghest', 'Baros', 'Begarin', 'Beynlore', 'Burat', 'Cairne', 'Carthon', 'Chamdar', 'Ciric', 'Cruzado', 'Cyphrak', "D'Harun", 'Daelon', 'Daktar', 'Darvain', 'Dracus', 'Dradar', 'Draelin', 'Draenor', 'Durodund', 'Eklor', 'Elrak', 'Fangorn', 'Farynthane', 'Galtor', 'Gemma', 'Gragus', 'Irian', 'Israfel', 'Jaden', 'Jefahn', "K'shar", 'Kalimus', 'Kallomane', 'Kanax', 'Kelnos', 'Kharn', 'Khir', 'Kragon', 'Kylnath', 'Larac', 'Lathis', 'Lenroc', 'Lonthorynthoryl', 'Lorreck', 'Mattrick', 'Mazrim', 'Mazrim', 'Modrei', 'Morturus', 'Muktar', 'Murdon', 'Murron', 'Myndon', 'Mythran', 'Mytor', 'Nabius', 'Nalynkal', 'Nazgul', 'Paorin', 'Quillan', 'Rendar', 'Scythyn', 'Shilor', 'Sobran', 'Soltak', 'Sorz', 'Taban', 'Telzar', 'Teron', 'Trethovian', 'Tyrnar', 'Ulath', 'Vandor', 'Vermithrax', 'Vlade', 'Volan', 'Wydstrin', "X'calak", 'Xaelin', 'Xandor', 'Xarthos', 'Xaxtox', 'Xenix', 'Xiltanth', 'Xylor', 'Xystil', 'Yazad', 'Yllthane', 'Ylthallynon', 'Ythoryn', 'Zalifar', 'Zathrix', 'Zunrek']
uniqueNameEvilMageLord =  ['Xarot the Black Archmage', 'Kwan Li', 'Lord of the Mists', 'Bazerion', 'the Wizard-Lord', 'Ylthallynon', 'the Insane']
uniqueNameGolemController =  ['Zelik', 'Kronos', 'Zakron', 'Velis', 'Chujil', 'Hygraph', 'Dyntrall', 'Zarus', 'Phoseph', 'Malkavik', 'Zevras', 'Vakel', 'Daklon', 'Zamog', 'Tavurk', 'Drakov', 'Zazik', 'Yyntrix', 'Zazik', 'Fropoz', 'Noxtrag', 'Makzok', 'Galzan', 'Drakan', 'Drakzik', 'Vazmog']
uniqueNameSavage =  ['Kahl', 'Ghrom', 'Ogger', 'Vek', "Sai'ge", "Groov'h", 'Khaonem', 'Malen', 'Atar', 'Aicee', 'Vaype', 'Halex', 'Yar', 'Hanz', 'Evocah', 'Bishor', 'Jelak', 'Adrok', 'Praphut', 'Usile', 'Sann', 'Sabba', 'Prie', 'Atuk', 'Chaca', 'ShoJo', 'Baccu', 'Bonkie', 'Alli', 'Jexa', "La'Loh", 'Arda', 'Cordee', 'Lana', 'Lar', 'Araka', 'Rhunda', 'Squee', 'Bhora', 'Niha', 'Olaufee', 'Sinthe', 'Karawyn', 'Gruwulf', 'Masena', 'Nasha', 'Sargaza']
uniqueNameSavageRider =  ['Kahl', 'Ghrom', 'Ogger', 'Vek', "Sai'ge", "Groov'h", 'Khaonem', 'Malen', 'Atar', 'Aicee', 'Vaype', 'Halex', 'Yar', 'Hanz', 'Evocah', 'Bishor', 'Jelak', 'Adrok', 'Praphut', 'Usile', 'Sann', 'Sabba', 'Prie', 'Atuk', 'Chaca', 'ShoJo', 'Baccu', 'Bonkie', 'Alli']
uniqueNameSavageShaman =  ['Jexa', "La'Loh", 'Arda', 'Cordee', 'Lana', 'Lar', 'Araka', 'Rhunda', 'Squee', 'Bhora', 'Niha', 'Olaufee', 'Sinthe', 'Karawyn', 'Gruwulf', 'Masena', 'Nasha', 'Sargaza']
uniqueNameAncientLich =  ['Kaltivel', 'Anshu', 'Maliel', 'Baratoz', 'Almonjin']
uniqueNameBosses = ['Fafnir']

unique_names = {
    'a Daemon': uniqueNameDaemon,
    'a Darknight Creeper': uniqueNameDarknightCreeper,
    'a Demon Knight': uniqueNameDemonKnight,
    'a Lizard Man': uniqueNameLizardMan,
    'a Fire Gargoyle': uniqueNameFireGargoyle,
    'an Impaler': uniqueNameImpaler,
    'an Orc': uniqueNameOrc,
    'a Rat Man': uniqueNameRatMan,
    'a Shadow Knight': uniqueNameShadowKnight,
    'a Centaur': uniqueNameCentaur,
    'an Ethereal Warrior': uniqueNameEtherealWarrior,
    'a Pixie': uniqueNamePixie,
    'an Evil Mage': uniqueNameEvilMage,
    'an Evil Mage Lord': uniqueNameEvilMageLord,
    'a Golem Controller': uniqueNameGolemController,
    'a Savage': uniqueNameSavage,
    'a Savage Rider': uniqueNameSavageRider,
    'a Savage Shaman': uniqueNameSavageShaman,
    'an Ancient Lich': uniqueNameAncientLich,
    'a boss': uniqueNameBosses
}

def checkUniqueName(name):
    for unique_name_type, name_list in unique_names.items():
        if name in name_list:
            return True
        if 'the dragon hunter' in str(name).lower() or 'an amazon' in str(name).lower():
            return True

def updateAlertGump():
    global redAlert, switchOn, WHITE, alertGumpNumber
    
    gd = Gumps.CreateGump(True,True,False,False)
    if gd:
        Gumps.AddPage(gd, 0) 

        if showLog:
            Gumps.AddButton(gd,288,185,2706,2707,9999,1,1)
        else:    
            Gumps.AddButton(gd,288,185,2704,2705,9999,1,1)
            
        if showLog:
            count = 0
            invertedAlertHistory = alertHistory[::-1]
            
            for logLine in invertedAlertHistory[0:11]:
                Gumps.AddImage(gd,300,248 + (20*count),3507)
                Gumps.AddImage(gd,180,248 + (20*count),3507)

                Gumps.AddImage(gd,180,225 + (20*count),1463)
                Gumps.AddImage(gd,220,225 + (20*count),1465)
            
                count +=1
                if count ==1:
                    Gumps.AddBackground(gd,175,240,370,10,410)
            
                
            count = 0    
            for logLine in invertedAlertHistory[0:11]:
               
                Gumps.AddLabel(gd,200,250 + (20*count),WHITE,str(logLine[6]) +":   " + str(logLine[1]) + " , " + str(logLine[3]) + " , " + str(logLine[4]) + " , " + str(logLine[5]))
                count +=1
                
            if count >=1:
                Gumps.AddBackground(gd,175,250 + (20*count),370,10,410)
            
            
        if redAlert:
            msg = str(alertPlayer) + ' ' + str(alertArea) + ' ' + str(alertX) + ',' + str(alertY)
            Gumps.AddBackground(gd,174,210,(9 * len(str(msg))),40,302)
            if not showLog:
                Gumps.AddAlphaRegion(gd,174,210,(9 * len(str(msg))),40)

            Gumps.AddLabelCropped(gd,200,220,(7 * len(str(msg))),50, 33, str(msg))

            if switchOn:
                Gumps.AddImage(gd,180,180,10840) 
                Gumps.AddImage(gd,200,170,9804)
                switchOn = False
            else:
                
                Gumps.AddImage(gd,180,180,10840)
                Gumps.AddLabel(gd,185,185,WHITE,"*RED SIGHTED*")
                switchOn = True
        else:
            
            Gumps.AddImage(gd,180,180,10820) 
            Gumps.AddLabel(gd,220,185,WHITE,"Clear")
                          
        Gumps.SendGump(alertGumpNumber, Player.Serial, 400, 400, gd.gumpDefinition, gd.gumpStrings)

Player.ChatSay("Meesa love the Lincoln Mallmorial!")        
Journal.Clear()    
while True:
    Misc.Pause(1000)
    gd = Gumps.GetGumpData(alertGumpNumber)

    if gd:
        if gd.buttonid == 9999:
            
            if showLog == True:
                showLog = False
            else:
                showLog = True

            
        gd.buttonid = -1   
     
    if Timer.Check("REDALERTTIMER") == False:
                
                redAlert = False
                
    if Journal.Search("REDALERT|"):
        line = Journal.GetLineText('REDALERT|',True)
        if line:

            alertText = line.split('|')
            alertZone = alertText[5]
            alertArea = alertText[6]
            alertPlayer = alertText[2]
            alertX = alertText[3]
            alertY = alertText[4]
            alertSerial = alertText[1]

            current_time = DateTime.Now
            formatted_time = current_time.ToString("h:mm tt")
            alertHistory.append([alertSerial,alertPlayer,alertZone,alertArea,alertX,alertY,formatted_time])
            if Timer.Check("REDALERTTIMER") == False:
                Timer.Create('REDALERTTIMER', 60000)
                redAlert = True
                

    mobileFilter = Mobiles.Filter()
    mobileFilter.Enabled = True
    mobileFilter.RangeMin = -1
    mobileFilter.RangeMax = 50
    mobileFilter.CheckLineOfSight = False
    mobileFilter.IsGhost = False  
    
    mobileFilter.Notorieties = List[Byte](bytes([6])) 

    foundMobiles = Mobiles.ApplyFilter(mobileFilter)
    
    if foundMobiles:
        for mobile in foundMobiles:

            mobileSerial = mobile.Serial
            mobileName = mobile.Name
            mobileUniqueNameType = checkUniqueName(mobileName)
            if mobileUniqueNameType:
                Misc.Pause(10)
            else:
                if mobile.MobileID == 400 or mobile.MobileID == 401:
                    if 'hue:' not in str(mobile.Properties).lower():
                        if Timer.Check("RED_" + str(mobile.Serial)) == False and Friend.IsFriend(mobile.Serial) == False:
                            Timer.Create("RED_" + str(mobile.Serial),60000)
                            Player.ChatGuild("REDALERT|" +str(mobile.Serial) + "|" + str(mobile.Name) + "|" + str(mobile.Position.X) + "|"  + str(mobile.Position.Y) + "|" + str(Player.Zone()) + '|'  + str( Player.Area()))
                            
                
    updateAlertGump()
       
    Journal.Clear()