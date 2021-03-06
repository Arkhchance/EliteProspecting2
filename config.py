import configparser
import os.path

class config():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.configFile = "EliteProspecting2.ini"
        if not os.path.exists(self.configFile):
            self.createConfig()

        self.loadConf()

    def loadConf(self):
        try:
            self.config.read(self.configFile)
        except Exception as e :
            print(e)

    def changeConf(self,section,var,val):
        self.config.set(section,var,str(val))

    def configSave(self):
        inifile = open(self.configFile,"w")
        self.config.write(inifile)
        print("settings saved !")

    def createConfig(self):
        inifile = open(self.configFile,"w")
        newConf = configparser.ConfigParser()
        #server section
        newConf.add_section("server")
        newConf.set("server","ip","51.254.124.98")
        newConf.set("server","port","44988")
        newConf.set("server","room","default")
        newConf.set("server","collect","1")

        #mining serction
        newConf.add_section("mining")
        newConf.set("mining","track_ltd","1")
        newConf.set("mining","track_painite","1")
        newConf.set("mining","ltd_t","18")
        newConf.set("mining","painite_t","25")
        newConf.set("mining","track_cargo","0")

        #ui serction
        newConf.add_section("ui")
        newConf.set("ui","text_color","Red")
        newConf.set("ui","text_other_color","#00ffff")
        newConf.set("ui","sound","1")
        newConf.set("ui","font_size","18")
        newConf.set("ui","pos_x","10")
        newConf.set("ui","pos_y","10")
        newConf.set("ui","total_message","6")
        newConf.set("ui","transparency","0")
        newConf.set("ui","online","0")
        newConf.set("ui","show_overlay","1")

        #ui colors
        newConf.add_section("ui_colors")
        newConf.set("ui_colors","backgroundColor","#2C3037")
        newConf.set("ui_colors","textColor","#47ACE1")
        newConf.set("ui_colors","boxColor","#40444B")
        newConf.set("ui_colors","boxTextColor","White")
        newConf.set("ui_colors","cbValid","#47ACE1")

        newConf.write(inifile)
        inifile.close()
